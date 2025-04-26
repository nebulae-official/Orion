from __future__ import annotations

import logging
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from nebula_orion.betelgeuse import config
from nebula_orion.betelgeuse.api.base import BaseAPIClient
from nebula_orion.betelgeuse.auth.token import APITokenAuth

# Use absolute imports
from nebula_orion.betelgeuse.client import NotionClient
from nebula_orion.betelgeuse.errors import AuthenticationError

# --- Fixtures ---


@pytest.fixture
def mock_api_token_auth_cls(mocker: MockerFixture) -> MagicMock:
    """Mock the APITokenAuth class constructor."""
    return mocker.patch(
        "nebula_orion.betelgeuse.client.auth_token_module.APITokenAuth",
        autospec=True,
    )


@pytest.fixture
def mock_base_api_client_cls(mocker: MockerFixture) -> MagicMock:
    """Mock the BaseAPIClient class constructor."""
    return mocker.patch("nebula_orion.betelgeuse.client.BaseAPIClient", autospec=True)


@pytest.fixture
def mock_auth_instance(mock_api_token_auth_cls: MagicMock) -> MagicMock:
    """Provide a mock instance returned by APITokenAuth constructor."""
    instance = MagicMock(spec=APITokenAuth)
    mock_api_token_auth_cls.return_value = instance
    return instance


@pytest.fixture
def mock_api_client_instance(mock_base_api_client_cls: MagicMock) -> MagicMock:
    """Provide a mock instance returned by BaseAPIClient constructor."""
    instance = MagicMock(spec=BaseAPIClient)
    mock_base_api_client_cls.return_value = instance
    return instance


# --- Tests ---


def test_client_init_success(
    mock_api_token_auth_cls: MagicMock,
    mock_base_api_client_cls: MagicMock,
    mock_auth_instance: MagicMock,
    mock_api_client_instance: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test successful client initialization with explicit token."""
    token = "secret_client_token_123"
    caplog.set_level(logging.DEBUG)

    client = NotionClient(auth_token=token)

    # Check APITokenAuth constructor was called correctly
    mock_api_token_auth_cls.assert_called_once_with(token=token)
    # Check BaseAPIClient constructor was called correctly
    mock_base_api_client_cls.assert_called_once_with(
        auth=mock_auth_instance,  # Check the instance was passed
        base_url=config.API_BASE_URL,
        notion_version=config.NOTION_VERSION,
        timeout=config.REQUEST_TIMEOUT,
    )
    # Check instances are stored
    assert client.auth is mock_auth_instance
    assert client._api_client is mock_api_client_instance  # type: ignore[attr-defined]
    # Check logs
    assert "Initializing NotionClient..." in caplog.text
    assert "Authentication handler initialized." in caplog.text
    assert "Base API client initialized." in caplog.text
    assert "NotionClient initialized successfully." in caplog.text


def test_client_init_uses_env_var_token_if_none_passed(
    mock_api_token_auth_cls: MagicMock,
    mock_base_api_client_cls: MagicMock,
) -> None:
    """Test APITokenAuth is called with None when no token is passed to client."""
    # APITokenAuth handles env var lookup internally (tested elsewhere)
    NotionClient(auth_token=None)  # Or NotionClient()
    mock_api_token_auth_cls.assert_called_once_with(token=None)
    mock_base_api_client_cls.assert_called_once()  # Ensure API client init still called


def test_client_init_raises_auth_error_on_token_auth_failure(
    mock_api_token_auth_cls: MagicMock,
    mock_base_api_client_cls: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test AuthenticationError propagation if APITokenAuth init fails."""
    auth_fail_error = AuthenticationError("Token setup failed")
    mock_api_token_auth_cls.side_effect = auth_fail_error
    caplog.set_level(logging.ERROR)  # Auth logs error

    with pytest.raises(AuthenticationError) as excinfo:
        NotionClient()

    assert excinfo.value is auth_fail_error  # Check exact error propagated
    mock_base_api_client_cls.assert_not_called()  # API client init shouldn't happen


def test_client_init_raises_auth_error_on_base_client_failure(
    mock_api_token_auth_cls: MagicMock,
    mock_base_api_client_cls: MagicMock,
    mock_auth_instance: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test error propagation if BaseAPIClient init fails."""
    # Simulate BaseAPIClient raising an unexpected error during init
    base_client_fail_error = TypeError("Bad config for BaseAPIClient")
    mock_base_api_client_cls.side_effect = base_client_fail_error
    caplog.set_level(logging.ERROR)

    with pytest.raises(AuthenticationError) as excinfo:
        NotionClient()

    assert "Failed to initialize API client" in str(excinfo.value)
    # Check underlying exception is chained
    assert excinfo.value.__cause__ is base_client_fail_error
    assert "Unexpected error during BaseAPIClient initialization" in caplog.text


def test_client_repr(
    mock_api_token_auth_cls: MagicMock,
    mock_base_api_client_cls: MagicMock,
) -> None:
    """Test the __repr__ method of the client."""
    # Need successful init for repr
    mock_api_token_auth_cls.return_value = MagicMock(spec=APITokenAuth)
    mock_base_api_client_cls.return_value = MagicMock(spec=BaseAPIClient)

    client = NotionClient(auth_token="secret_repr_token")
    expected_repr = f"<NotionClient(api_version='{config.NOTION_VERSION}')>"
    assert repr(client) == expected_repr
