# src/nebula_orion/betelgeuse/models/__init__.py
from __future__ import annotations

"""
Pydantic models representing Notion API objects like Pages, Databases, Blocks, etc.
"""
# Import base and common models first
from .base import BaseObjectModel
from .block import Block  # Import the base Block model
from .common import (  # Import common types that might be used across models; Add others as needed
    Annotations,
    AnyRichText,
    FileObject,
    PartialUser,
    RichTextEquation,
    RichTextMention,
    RichTextText,
    SelectOption,
    User,
)

# Import core object models
from .database import Database
from .page import Page

__all__ = [
    "Annotations",
    "AnyRichText",
    # Base / Common
    "BaseObjectModel",
    "Block",
    # Core Objects
    "Database",
    "FileObject",
    "Page",
    "PartialUser",
    "RichTextEquation",
    "RichTextMention",
    "RichTextText",
    "SelectOption",
    "User",
    # Specific block types are NOT exposed via models.__all__
]
