from __future__ import annotations

import logging

import pytest
from pytest_mock import MockerFixture

# Use absolute imports for testing target code
from nebula_orion.betelgeuse.auth.token import API_TOKEN_ENV_VAR, APITokenAuth
from nebula_orion.betelgeuse.errors import AuthenticationError

VALID_TOKEN = "ntn_ValidTokenString123"
NON_STANDARD_TOKEN = "nonstandard_token_format"


def test_api_token_auth_with_explicit_token() -> None:
    """Test initializing with an explicit, valid token."""
    auth = APITokenAuth(token=VALID_TOKEN)
    assert auth._token == VALID_TOKEN  # type: ignore [attr-defined] # Access protected for test
    assert auth.get_auth_headers() == {"Authorization": f"Bearer {VALID_TOKEN}"}


def test_api_token_auth_from_env_var(mocker: MockerFixture) -> None:
    """Test initializing by reading a valid token from environment variable."""
    mocker.patch("os.getenv", return_value=VALID_TOKEN)
    # Mock specifically for the API_TOKEN_ENV_VAR key
    mocker.patch(
        "os.getenv",
        lambda k, d=None: VALID_TOKEN if k == API_TOKEN_ENV_VAR else d,
    )

    auth = APITokenAuth()  # No token passed explicitly
    assert auth._token == VALID_TOKEN  # type: ignore [attr-defined]
    assert auth.get_auth_headers() == {"Authorization": f"Bearer {VALID_TOKEN}"}


def test_api_token_auth_explicit_token_overrides_env(mocker: MockerFixture) -> None:
    """Test that explicit token takes precedence over environment variable."""
    env_token = "env_token_should_be_ignored"
    mocker.patch(
        "os.getenv",
        lambda k, d=None: env_token if k == API_TOKEN_ENV_VAR else d,
    )

    auth = APITokenAuth(token=VALID_TOKEN)  # Explicit token passed
    assert auth._token == VALID_TOKEN  # type: ignore [attr-defined]
    assert auth.get_auth_headers() == {"Authorization": f"Bearer {VALID_TOKEN}"}


def test_api_token_auth_missing_token_raises_error(mocker: MockerFixture) -> None:
    """Test that AuthenticationError is raised if no token is found."""
    mocker.patch("os.getenv", lambda k, d=None: None if k == API_TOKEN_ENV_VAR else d)

    with pytest.raises(AuthenticationError, match="No API token provided"):
        APITokenAuth()  # No explicit token, env var mocked to None


def test_api_token_auth_logs_warning_for_non_standard_token(
    mocker: MockerFixture,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that a warning is logged for tokens not starting with 'ntn_'."""
    # Mock getenv to avoid raising error if env var also missing
    mocker.patch("os.getenv", return_value=None)
    # Set specific log level capture for this test
    caplog.set_level(logging.WARNING, logger="nebula_orion.betelgeuse.auth.token")

    APITokenAuth(token=NON_STANDARD_TOKEN)

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelname == "WARNING"
    # Check the actual message logged, not just 'in text'
    expected_msg_part = "Provided token does not start with 'ntn_'"
    assert expected_msg_part in record.message, (
        f"Log message mismatch. Got: {record.message}"
    )


def test_api_token_auth_no_warning_for_standard_token(
    mocker: MockerFixture,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that no warning is logged for tokens starting with 'ntn_'."""
    mocker.patch("os.getenv", return_value=None)
    caplog.set_level(logging.WARNING, logger="nebula_orion.betelgeuse.auth.token")

    APITokenAuth(token=VALID_TOKEN)

    warning_message_part = "Provided token does not start with 'ntn_'"
    found_warning = any(
        warning_message_part in rec.message
        for rec in caplog.records
        if rec.levelno == logging.WARNING
    )
    assert not found_warning, "Warning log was unexpectedly generated for a valid token."
