# src/nebula_orion/betelgeuse/models/block.py
from __future__ import annotations

from typing import Any, Literal

from pydantic import ConfigDict

# Use absolute imports for sibling modules
from .base import BaseObjectModel

# --- Base Block Model ---
# Ref: https://developers.notion.com/reference/block


class Block(BaseObjectModel):
    """Base Pydantic model for all Notion Block objects.

    Inherits common fields like id, parent, timestamps, etc.
    """

    object: Literal["block"] = "block"
    type: str  # Specific block type (e.g., 'paragraph', 'heading_1')
    has_children: bool = False

    # The actual block content is stored in a key matching the 'type' field
    # We use Optional[Dict] here; subclasses will define the specific structure.
    paragraph: dict[str, Any] | None = None
    heading_1: dict[str, Any] | None = None
    heading_2: dict[str, Any] | None = None
    heading_3: dict[str, Any] | None = None
    bulleted_list_item: dict[str, Any] | None = None
    numbered_list_item: dict[str, Any] | None = None
    to_do: dict[str, Any] | None = None
    toggle: dict[str, Any] | None = None
    child_page: dict[str, Any] | None = None
    child_database: dict[str, Any] | None = None
    embed: dict[str, Any] | None = None
    image: dict[str, Any] | None = None
    video: dict[str, Any] | None = None
    file: dict[str, Any] | None = None
    pdf: dict[str, Any] | None = None
    bookmark: dict[str, Any] | None = None
    callout: dict[str, Any] | None = None
    quote: dict[str, Any] | None = None
    equation: dict[str, Any] | None = None
    divider: dict[str, Any] | None = None
    table_of_contents: dict[str, Any] | None = None
    breadcrumb: dict[str, Any] | None = None
    column_list: dict[str, Any] | None = None
    column: dict[str, Any] | None = None
    link_preview: dict[str, Any] | None = None
    link_to_page: dict[str, Any] | None = None
    synced_block: dict[str, Any] | None = None
    template: dict[str, Any] | None = None
    table: dict[str, Any] | None = None
    table_row: dict[str, Any] | None = None
    # Add other block types as needed...
    unsupported: dict[str, Any] | None = None  # For blocks not yet modeled

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    # Pydantic v2: Use root_validator to ensure only one block type field is present
    # (or handle this during parsing/factory creation)
    # @root_validator(pre=True) # pre=True runs before field validation
    # def check_block_type_data(cls, values):
    #     block_type = values.get('type')
    #     # Check if the corresponding key exists, handle potential errors
    #     return values

    def __repr__(self) -> str:
        """Concise representation including block type."""
        return f"<Block(id='{self.id}', type='{self.type}')>"


# --- Block Parsing Factory (Example) ---
# This function will be used later to parse a list of block dicts
# into specific Block subclass instances.

# Forward references are needed if subclasses are defined later in other files
# from . import blocks # Assuming block subclasses are in a 'blocks' module

# Define a mapping from type string to Block subclass
# This will be populated as we define more block types
# BLOCK_TYPE_MAP: Dict[str, Type[Block]] = {}

# def parse_block_data(block_data: Dict[str, Any]) -> Block:
#     """Parses raw block data into the appropriate Block model instance."""
#     block_type = block_data.get("type")
#     if not block_type:
#         raise ValueError("Block data missing 'type' field.")

#     model_class = BLOCK_TYPE_MAP.get(block_type)
#     if model_class:
#         try:
#             return model_class.model_validate(block_data)
#         except ValidationError as e:
#             # Handle validation error for specific type, maybe fallback?
#             log.warning("Validation failed for block type '%s', ID '%s': %s",
#                         block_type, block_data.get('id'), e, exc_info=False)
#             # Fallback to base Block model or raise error?
#             # For now, let's try base Block which might capture basic fields
#             pass # Fall through to base Block parsing

#     # Fallback for unknown or failed specific types
#     log.debug("Parsing block type '%s' with base Block model.", block_type)
#     try:
#         # Add the unknown type data under the 'unsupported' key if needed
#         # block_data['unsupported'] = block_data.get(block_type, {})
#         return Block.model_validate(block_data)
#     except ValidationError as e:
#         # If even base validation fails, raise a specific error
#         raise BetelgeuseError(f"Failed to parse base block data for ID {block_data.get('id')}") from e
