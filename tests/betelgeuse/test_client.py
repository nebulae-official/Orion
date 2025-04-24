from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import MagicMock  # Import patch if needed, MagicMock is key

import pytest

from nebula_orion.betelgeuse import config
from nebula_orion.betelgeuse.auth.token import APITokenAuth

# Use absolute imports in tests as well
from nebula_orion.betelgeuse.client import NotionClient
from nebula_orion.betelgeuse.errors import AuthenticationError

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

# Type hint for the fixture return value
MockDeps = tuple[MagicMock, MagicMock]


# Use mocker fixture provided by pytest-mock
@pytest.fixture(autouse=True)
def mock_dependencies(mocker: MockerFixture) -> MockDeps:
    """Auto-mock dependencies (APITokenAuth, BaseAPIClient constructors) for client tests."""
    # Mock the classes themselves to check instantiation arguments
    mock_api_token_auth_cls: MagicMock = mocker.patch(
        "nebula_orion.betelgeuse.client.APITokenAuth", spec=True
    )
    mock_base_api_client_cls: MagicMock = mocker.patch(
        "nebula_orion.betelgeuse.client.BaseAPIClient", spec=True
    )

    # Return the mocked classes (constructors)
    return mock_api_token_auth_cls, mock_base_api_client_cls


def test_client_init_with_explicit_token(mock_dependencies: MockDeps) -> None:
    """Test client initialization with an explicit token."""
    mock_api_token_auth_cls, mock_base_api_client_cls = mock_dependencies
    token: str = "client_token_123"

    # Create a mock instance returned by the mocked APITokenAuth constructor
    mock_auth_instance = MagicMock(spec=APITokenAuth)
    mock_api_token_auth_cls.return_value = mock_auth_instance

    client = NotionClient(auth_token=token)

    # Check APITokenAuth constructor was called correctly
    mock_api_token_auth_cls.assert_called_once_with(token=token)

    # Check BaseAPIClient constructor was called correctly, passing the auth instance
    mock_base_api_client_cls.assert_called_once_with(
        auth=mock_auth_instance,  # Check the instance was passed
        base_url=config.API_BASE_URL,
        notion_version=config.NOTION_VERSION,
        timeout=config.REQUEST_TIMEOUT,
    )
    assert client.auth == mock_auth_instance
    # The client._api_client holds the *instance* returned by the mocked BaseAPIClient constructor
    assert client._api_client == mock_base_api_client_cls.return_value


def test_client_init_with_env_var(mock_dependencies: MockDeps) -> None:
    """Test client initialization reading token from environment variable (indirectly)."""
    mock_api_token_auth_cls, mock_base_api_client_cls = mock_dependencies

    # We assume APITokenAuth handles env var lookup correctly (tested elsewhere)
    # We just need to ensure it's called with token=None when NotionClient gets None
    mock_auth_instance = MagicMock(spec=APITokenAuth)
    mock_api_token_auth_cls.return_value = mock_auth_instance

    # We don't need to mock os.getenv here because we mock APITokenAuth directly.
    client = NotionClient(auth_token=None)  # Or just NotionClient()

    # Check APITokenAuth constructor was called with None
    mock_api_token_auth_cls.assert_called_once_with(token=None)

    # Check BaseAPIClient constructor was called correctly
    mock_base_api_client_cls.assert_called_once_with(
        auth=mock_auth_instance,
        base_url=config.API_BASE_URL,
        notion_version=config.NOTION_VERSION,
        timeout=config.REQUEST_TIMEOUT,
    )
    assert client.auth == mock_auth_instance
    assert client._api_client == mock_base_api_client_cls.return_value


def test_client_init_missing_token_raises_error(mock_dependencies: MockDeps) -> None:
    """Test AuthenticationError is raised if APITokenAuth constructor fails."""
    mock_api_token_auth_cls, mock_base_api_client_cls = mock_dependencies

    # Configure the mocked APITokenAuth constructor to raise the error
    msg = "No API token provided. Please set the NOTION_API_TOKEN environment variable."
    mock_api_token_auth_cls.side_effect = AuthenticationError(msg)
    with pytest.raises(AuthenticationError, match=msg):
        NotionClient()  # No token provided, mock constructor raises error

    # Ensure BaseAPIClient constructor was NOT called if auth failed
    mock_base_api_client_cls.assert_not_called()


def test_client_repr(mock_dependencies: MockDeps) -> None:
    """Test the __repr__ method of the client."""
    mock_api_token_auth_cls, _ = mock_dependencies
    # Need APITokenAuth() to succeed, so set a return value for its mock constructor
    mock_api_token_auth_cls.return_value = MagicMock(spec=APITokenAuth)

    client = NotionClient(auth_token="repr_token")  # noqa: S106
    expected_repr = f"<NotionClient(api_version='{config.NOTION_VERSION}')>"
    assert repr(client) == expected_repr
