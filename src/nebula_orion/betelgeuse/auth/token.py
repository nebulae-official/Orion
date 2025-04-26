from __future__ import annotations

import os

# Use absolute imports for sibling modules/packages
from nebula_orion import get_logger  # Use central logger getter
from nebula_orion.betelgeuse import errors  # Import sibling errors module

# Get a logger specific to this module
log = get_logger(__name__)

# Standard environment variable name for the token
API_TOKEN_ENV_VAR: str = "NOTION_API_TOKEN"


class APITokenAuth:
    """Authentication strategy using a Notion integration token (API token).

    Reads the token from the provided argument or the environment variable.
    """

    def __init__(self, token: str | None = None) -> None:
        """Initialize API Token authentication.

        Args:
            token: The Notion API integration token. If None, attempts
                   to read from the NOTION_API_TOKEN environment variable.

        Raises:
            AuthenticationError: If no token is provided and cannot be found
                                 in the environment variable.

        """
        resolved_token: str | None = token or os.getenv(API_TOKEN_ENV_VAR)

        if not resolved_token:
            log.error(
                "Authentication failed: No API token provided directly or found "
                "in environment variable '%s'.",
                API_TOKEN_ENV_VAR,
            )
            msg = (
                f"No API token provided. Pass it directly or set the "
                f"'{API_TOKEN_ENV_VAR}' environment variable."
            )
            raise errors.AuthenticationError(
                msg,
            )

        # Basic check for token format (internal integrations start with 'secret_')
        if not resolved_token.startswith("secret_"):
            log.warning(
                "Provided token does not start with 'secret_'. Ensure it is a "
                "valid Notion Internal Integration Token.",
            )

        self._token: str = resolved_token
        log.debug("APITokenAuth initialized successfully.")

    def get_auth_headers(self) -> dict[str, str]:
        """Return the necessary headers for API token authentication."""
        return {"Authorization": f"Bearer {self._token}"}

    def get_token(self) -> str:
        """Return the API token used for authentication."""
        return self._token
