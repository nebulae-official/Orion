"""Betelgeuse: A Pythonic Layer for the Notion API within the Nebula Orion library."""

# Expose the main client class for easy import
# Expose constants or config vars if useful
from .auth.token import API_TOKEN_ENV_VAR
from .client import NotionClient

# Expose core exceptions if needed directly by users
from .errors import AuthenticationError, BetelgeuseError, NotionAPIError

__all__ = [
    "API_TOKEN_ENV_VAR",
    "AuthenticationError",
    "BetelgeuseError",
    "NotionAPIError",
    "NotionClient",
]
