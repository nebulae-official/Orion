# nebula_orion/betelgeuse/__init__.py
"""Betelgeuse: A Pythonic Layer for the Notion API."""

__version__ = "0.1.0"  # Initial version

# Expose the main client class for easy import
from nebula_orion.betelgeuse.auth.token import (
    API_TOKEN_ENV_VAR,
)  # Expose the env var name
from nebula_orion.betelgeuse.client import NotionClient

# Optionally expose common errors or constants
from nebula_orion.betelgeuse.errors import NotionAPIError, NotionRequestError

__all__ = [
    "API_TOKEN_ENV_VAR",
    "NotionAPIError",
    "NotionClient",
    "NotionRequestError",
    "__version__",
]
