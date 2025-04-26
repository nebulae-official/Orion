from __future__ import annotations

"""
Pydantic models representing Notion API objects like Pages, Databases, etc.
"""
from .base import BaseObjectModel
from .database import Database
from .page import Page

# Add other core object models here as they are created (Block, User, etc.)

__all__ = [
    "BaseObjectModel",
    "Database",
    "Page",
]
