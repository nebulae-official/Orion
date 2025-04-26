"""Betelgeuse: A Pythonic Layer for the Notion API within the Nebula Orion library."""

from __future__ import annotations

# Expose the main client class for easy import
# Expose constants or config vars if useful
from .auth.token import API_TOKEN_ENV_VAR
from .client import NotionClient

# Expose core exceptions if needed directly by users
from .errors import (
    AuthenticationError,
    BetelgeuseError,
    NotionAPIError,
    NotionRequestError,
)

# Expose Pydantic models
from .models import BaseObjectModel, Database, Page

__all__ = [
    "API_TOKEN_ENV_VAR",
    "AuthenticationError",
    "BaseObjectModel",
    "BetelgeuseError",
    "Database",
    "NotionAPIError",
    "NotionClient",
    "NotionRequestError",
    "Page",
]
