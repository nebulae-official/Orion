# src/nebula_orion/betelgeuse/blocks/text.py
from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, ConfigDict, Field

# Use absolute imports for sibling modules
from nebula_orion.betelgeuse.models.block import Block  # Import base Block

if TYPE_CHECKING:
    from nebula_orion.betelgeuse.models.common import (  # Import common types
        AnyRichText,
        IconData,
    )

# --- Block Content Models (Specific to Block Types) ---


class TextBlockContent(BaseModel):
    """Content common to text-based blocks like paragraph, headings, etc."""

    rich_text: list[AnyRichText] = Field(default_factory=list)
    color: str = "default"
    # Note: children for text blocks are usually handled via retrieve_block_children
    # children: Optional[List['Block']] = None # Requires forward ref or TypeAlias

    model_config = ConfigDict(extra="ignore")


class ParagraphBlockContent(TextBlockContent):
    """Content specific to 'paragraph' blocks."""

    # Currently same as TextBlockContent


class HeadingBlockContent(TextBlockContent):
    """Content specific to 'heading_1/2/3' blocks."""

    is_toggleable: bool = False


class CalloutBlockContent(TextBlockContent):
    """Content specific to 'callout' blocks."""

    icon: IconData | None = None


class QuoteBlockContent(TextBlockContent):
    """Content specific to 'quote' blocks."""

    # Currently same as TextBlockContent


class BulletedListItemBlockContent(TextBlockContent):
    """Content specific to 'bulleted_list_item' blocks."""


class NumberedListItemBlockContent(TextBlockContent):
    """Content specific to 'numbered_list_item' blocks."""


class ToDoBlockContent(TextBlockContent):
    """Content specific to 'to_do' blocks."""

    checked: bool = False


class ToggleBlockContent(TextBlockContent):
    """Content specific to 'toggle' blocks."""


# --- Specific Block Models ---


class ParagraphBlock(Block):
    """Model for 'paragraph' blocks."""

    type: Literal["paragraph"] = "paragraph"
    paragraph: ParagraphBlockContent


class Heading1Block(Block):
    """Model for 'heading_1' blocks."""

    type: Literal["heading_1"] = "heading_1"
    heading_1: HeadingBlockContent


class Heading2Block(Block):
    """Model for 'heading_2' blocks."""

    type: Literal["heading_2"] = "heading_2"
    heading_2: HeadingBlockContent


class Heading3Block(Block):
    """Model for 'heading_3' blocks."""

    type: Literal["heading_3"] = "heading_3"
    heading_3: HeadingBlockContent


class CalloutBlock(Block):
    """Model for 'callout' blocks."""

    type: Literal["callout"] = "callout"
    callout: CalloutBlockContent


class QuoteBlock(Block):
    """Model for 'quote' blocks."""

    type: Literal["quote"] = "quote"
    quote: QuoteBlockContent


class BulletedListItemBlock(Block):
    """Model for 'bulleted_list_item' blocks."""

    type: Literal["bulleted_list_item"] = "bulleted_list_item"
    bulleted_list_item: BulletedListItemBlockContent


class NumberedListItemBlock(Block):
    """Model for 'numbered_list_item' blocks."""

    type: Literal["numbered_list_item"] = "numbered_list_item"
    numbered_list_item: NumberedListItemBlockContent


class ToDoBlock(Block):
    """Model for 'to_do' blocks."""

    type: Literal["to_do"] = "to_do"
    to_do: ToDoBlockContent


class ToggleBlock(Block):
    """Model for 'toggle' blocks."""

    type: Literal["toggle"] = "toggle"
    toggle: ToggleBlockContent


# --- Update Block Type Map (if using factory) ---
# Add these specific block types to the map in models/block.py or a central registry
# Example (if map defined in models.block):
# from .text import ParagraphBlock, Heading1Block, ... # Import the classes
# BLOCK_TYPE_MAP.update({
#     "paragraph": ParagraphBlock,
#     "heading_1": Heading1Block,
#     "heading_2": Heading2Block,
#     "heading_3": Heading3Block,
#     "callout": CalloutBlock,
#     "quote": QuoteBlock,
#     "bulleted_list_item": BulletedListItemBlock,
#     "numbered_list_item": NumberedListItemBlock,
#     "to_do": ToDoBlock,
#     "toggle": ToggleBlock,
# })
