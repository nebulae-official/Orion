# nebula_orion/betelgeuse/config.py
"""Configuration settings for the Betelgeuse client.

Can be modified by the user before client instantiation if needed.
"""

from __future__ import annotations

import os

from nebula_orion.betelgeuse.auth.token import API_TOKEN_ENV_VAR

# Use absolute imports
from nebula_orion.betelgeuse.constants import (
    DEFAULT_NOTION_API_URL,
    DEFAULT_NOTION_VERSION,
    DEFAULT_TIMEOUT,
)
from nebula_orion.log_config import get_logger

logger = get_logger("Betelgeuse.Config")

# --- API Configuration ---
# Base URL for the Notion API
_api_base_url_env = os.getenv("NOTION_API_URL")
API_BASE_URL: str = _api_base_url_env or DEFAULT_NOTION_API_URL
if _api_base_url_env:
    logger.info("Using API Base URL from environment: %s", API_BASE_URL)
else:
    logger.info("Using default API Base URL: %s", API_BASE_URL)


# Notion API Version (passed in headers)
# See: https://developers.notion.com/reference/versioning
_notion_version_env = os.getenv("NOTION_VERSION")
NOTION_VERSION: str = _notion_version_env or DEFAULT_NOTION_VERSION
if _notion_version_env:
    logger.info("Using Notion Version from environment: %s", NOTION_VERSION)
else:
    logger.info("Using default Notion Version: %s", NOTION_VERSION)


# Default timeout for API requests in seconds
_request_timeout_env = os.getenv("NOTION_REQUEST_TIMEOUT")
REQUEST_TIMEOUT: int = DEFAULT_TIMEOUT
if _request_timeout_env:
    try:
        REQUEST_TIMEOUT = int(_request_timeout_env)
        logger.info("Using Request Timeout from environment: %s", REQUEST_TIMEOUT)
    except ValueError:
        logger.warning(
            "Invalid NOTION_REQUEST_TIMEOUT value '%s' in environment. Using default: %s",
            _request_timeout_env,
            DEFAULT_TIMEOUT,
        )
else:
    logger.info("Using default Request Timeout: %s", REQUEST_TIMEOUT)


# --- Authentication Configuration ---
# Default method is API Token, potentially extended later
DEFAULT_AUTH_TOKEN: str | None = os.getenv(API_TOKEN_ENV_VAR, None)
if DEFAULT_AUTH_TOKEN:
    logger.debug(
        "Default auth token found in environment variable %s.", API_TOKEN_ENV_VAR
    )
else:
    logger.debug(
        "Default auth token not found in environment variable %s. Client will require explicit token.",
        API_TOKEN_ENV_VAR,
    )
