# tests/betelgeuse/auth/test_token.py
import pytest
from pytest_mock import MockerFixture

from nebula_orion.betelgeuse.auth.token import API_TOKEN_ENV_VAR, APITokenAuth
from nebula_orion.betelgeuse.errors import AuthenticationError


def test_api_token_auth_with_explicit_token() -> None:
    """Test initializing with an explicit token."""
    token: str = "explicit_token_123"
    auth = APITokenAuth(token=token)
    assert auth.token == token  # Accessing protected member for test validation
    assert auth.get_auth_headers() == {"Authorization": f"Bearer {token}"}


def test_api_token_auth_from_env_var(mocker: MockerFixture) -> None:
    """Test initializing by reading from environment variable."""
    token: str = "env_token_456"
    # Mock specifically for the API_TOKEN_ENV_VAR key
    # Lambda type hint: Callable[[str, Optional[str]], Optional[str]]
    mocker.patch("os.getenv", lambda k, d=None: token if k == API_TOKEN_ENV_VAR else d)

    auth = APITokenAuth()  # No token passed explicitly
    assert auth.token == token
    assert auth.get_auth_headers() == {"Authorization": f"Bearer {token}"}


def test_api_token_auth_explicit_token_overrides_env(mocker: MockerFixture) -> None:
    """Test that explicit token takes precedence over environment variable."""
    explicit_token: str = "explicit_token_789"
    env_token: str = "env_token_should_be_ignored"

    # Mock os.getenv to return the env_token
    # Lambda type hint: Callable[[str, Optional[str]], Optional[str]]
    mocker.patch(
        "os.getenv", lambda k, d=None: env_token if k == API_TOKEN_ENV_VAR else d
    )

    auth = APITokenAuth(token=explicit_token)  # Explicit token passed
    assert auth.token == explicit_token
    assert auth.get_auth_headers() == {"Authorization": f"Bearer {explicit_token}"}


def test_api_token_auth_missing_token_raises_error(mocker: MockerFixture) -> None:
    """Test that AuthenticationError is raised if no token is found."""
    # Ensure os.getenv returns None for the token variable
    # Lambda type hint: Callable[[str, Optional[str]], Optional[str]]
    mocker.patch("os.getenv", lambda k, d=None: None if k == API_TOKEN_ENV_VAR else d)

    with pytest.raises(AuthenticationError, match="No API token provided"):
        APITokenAuth()  # No explicit token, env var mocked to None
