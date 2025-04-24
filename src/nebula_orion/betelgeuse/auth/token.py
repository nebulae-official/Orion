# nebula_orion/betelgeuse/auth/token.py
"""Handles API Token authentication for the Notion API."""

from __future__ import annotations

import os

from dotenv import load_dotenv

# Use absolute import
from nebula_orion.betelgeuse.errors import AuthenticationError
from nebula_orion.log_config import get_logger

# Standard environment variable name for the token
API_TOKEN_ENV_VAR = "NOTION_API_TOKEN"  # noqa: S105

load_dotenv()
logger = get_logger("Betelgeuse")


class APITokenAuth:
    """Authentication strategy using a Notion integration token (API token)."""

    def __init__(self, token: str | None = None) -> None:
        """Initialize API Token authentication.

        Args:
            token: The Notion API integration token. If None, attempts
                   to read from the NOTION_API_TOKEN environment variable.

        Raises:
            AuthenticationError: If no token is provided or found.

        """
        logger.debug("Initializing APITokenAuth...")
        resolved_token: str | None = None
        if token:
            logger.debug("Using provided API token.")
            resolved_token = token
        else:
            logger.debug(
                "No token provided, attempting to load from environment variable '%s'.",
                API_TOKEN_ENV_VAR,
            )
            resolved_token = os.getenv(API_TOKEN_ENV_VAR)
            if resolved_token:
                logger.debug("Found API token in environment variable.")
            else:
                logger.warning(
                    "API token not found in environment variable '%s'.",
                    API_TOKEN_ENV_VAR,
                )

        if not resolved_token:
            msg = (
                f"No API token provided. Please pass it directly or set the "
                f"'{API_TOKEN_ENV_VAR}' environment variable."
            )
            logger.error(f"AuthenticationError: {msg}")
            raise AuthenticationError(
                msg,
            )
        self._token = resolved_token
        logger.info("APITokenAuth initialized successfully.")

    @property
    def token(self) -> str:
        """Return the API token."""
        return self._token

    @token.setter
    def token(self, value: str) -> None:
        """Set the API token."""
        self._token = value

    def get_auth_headers(self) -> dict[str, str]:
        """Return the necessary headers for API token authentication."""
        logger.debug("Generating authentication headers.")
        # Avoid logging the token itself for security
        return {"Authorization": f"Bearer {self._token}"}
