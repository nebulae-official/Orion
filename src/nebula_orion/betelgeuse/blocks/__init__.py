# src/nebula_orion/betelgeuse/blocks/__init__.py
from __future__ import annotations

"""
This package contains Pydantic models for specific Notion Block types.
Each module typically focuses on a category of blocks (text, media, etc.).
"""

# Import specific block types to make them available
from .text import (
    BulletedListItemBlock,
    CalloutBlock,
    Heading1Block,
    Heading2Block,
    Heading3Block,
    NumberedListItemBlock,
    ParagraphBlock,
    QuoteBlock,
    ToDoBlock,
    ToggleBlock,
)

# You can create a Union of all known block types for type hinting if needed
# Example: AnyTextBlock = Union[ParagraphBlock, Heading1Block, ...]

__all__ = [
    "BulletedListItemBlock",
    "CalloutBlock",
    "Heading1Block",
    "Heading2Block",
    "Heading3Block",
    "NumberedListItemBlock",
    "ParagraphBlock",
    "QuoteBlock",
    "ToDoBlock",
    "ToggleBlock",
    # Add other imported block types here
]
