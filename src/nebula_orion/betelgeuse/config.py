# src/nebula_orion/betelgeuse/config.py
from __future__ import annotations

import os

# Use absolute imports from within the same package level
from . import constants
from .auth import token as auth_token_module  # Avoid circular import with auth.token

# --- API Configuration ---

# Base URL for the Notion API. Can be overridden by environment variable.
API_BASE_URL: str = os.getenv("NOTION_API_URL", constants.DEFAULT_NOTION_API_URL)

# Notion API Version (passed in headers). Can be overridden by environment variable.
# See: https://developers.notion.com/reference/versioning
NOTION_VERSION: str = os.getenv("NOTION_VERSION", constants.DEFAULT_NOTION_VERSION)

# Default timeout for API requests in seconds. Can be overridden by environment variable.
# Ensure conversion to int, provide default if env var is invalid.
try:
    REQUEST_TIMEOUT: int = int(
        os.getenv(
            "NOTION_REQUEST_TIMEOUT",
            str(constants.DEFAULT_REQUEST_TIMEOUT_SECONDS),  # Default needs conversion
        ),
    )
except ValueError:
    REQUEST_TIMEOUT = constants.DEFAULT_REQUEST_TIMEOUT_SECONDS


# --- Authentication Configuration ---

# Default authentication token read from environment variable.
# The client will primarily use the token passed during instantiation,
# but this allows fallback or environment-based configuration.
DEFAULT_AUTH_TOKEN: str | None = os.getenv(auth_token_module.API_TOKEN_ENV_VAR)
