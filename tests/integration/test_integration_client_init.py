# tests/integration/test_integration_client_init.py
from __future__ import annotations

import os

import pytest

# Use absolute imports
from nebula_orion.betelgeuse import NotionClient, constants
from nebula_orion.betelgeuse.errors import AuthenticationError, NotionAPIError

# Environment variable name
NOTION_API_TOKEN_VAR = "NOTION_API_TOKEN"

# --- Test Marker ---
# Mark all tests in this file as 'integration'
pytestmark = pytest.mark.integration

# --- Skip Condition ---
# Skip all tests in this file if the token environment variable is not set
requires_token = pytest.mark.skipif(
    not os.getenv(NOTION_API_TOKEN_VAR),
    reason=f"Requires {NOTION_API_TOKEN_VAR} environment variable to be set.",
)


@requires_token
def test_client_init_integration() -> None:
    """Verify client initialization works with a real token (from env var)."""
    try:
        # Initialize without mocks, relies on env var set by APITokenAuth
        client = NotionClient()
        assert client is not None
        assert isinstance(client, NotionClient)
        # Check internal client setup happened
        assert client.auth is not None
        assert client._api_client is not None  # type: ignore[attr-defined]
    except AuthenticationError as e:
        pytest.fail(f"AuthenticationError raised unexpectedly: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected exception during client init: {type(e).__name__}: {e}")


@requires_token
def test_client_auth_works_get_users_me_integration() -> None:
    """Verify the client's token works by fetching the bot user info."""
    client = NotionClient()  # Assumes token is in env var

    try:
        # Use the internal _api_client directly to make a simple GET request
        # GET /v1/users/me is a good endpoint to test authentication
        bot_user_info = client._api_client.request(  # type: ignore[attr-defined]
            method=constants.GET,
            path="/v1/users/me",
        )

        # Basic validation of the response structure
        assert isinstance(bot_user_info, dict)
        assert bot_user_info.get("object") == "user"
        assert bot_user_info.get("type") == "bot"
        assert "id" in bot_user_info
        assert "name" in bot_user_info
        assert "bot" in bot_user_info  # Should contain owner info etc.

    except NotionAPIError as e:
        pytest.fail(f"NotionAPIError raised during /v1/users/me call: {e}")
    except Exception as e:
        pytest.fail(
            f"Unexpected exception during /v1/users/me call: {type(e).__name__}: {e}",
        )
