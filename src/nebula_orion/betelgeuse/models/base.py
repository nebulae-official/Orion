# src/nebula_orion/betelgeuse/models/base.py
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

# Type alias for Parent object structure (can be refined later with specific models)
# It typically contains a 'type' key and another key based on the type.
ParentData = dict[str, Any]


class BaseObjectModel(BaseModel):
    """Base Pydantic model for Notion objects providing common attributes.

    Parses and validates data using Pydantic based on Notion API responses.
    """

    # --- Fields directly mapped from Notion API ---
    id: str
    object: str  # The type of Notion object (e.g., 'page', 'database', 'user')
    created_time: datetime
    last_edited_time: datetime
    archived: bool = False
    parent: ParentData  # Structure varies (db_id, page_id, workspace, block_id)
    url: str = ""  # URL is present on pages and databases, maybe others

    # User objects who created/edited - often partial representations
    created_by: dict[str, Any] | None = Field(None)
    last_edited_by: dict[str, Any] | None = Field(None)

    # --- Pydantic Configuration ---
    model_config = ConfigDict(
        extra="ignore",  # Ignore extra fields from API
        populate_by_name=True,  # Allow using field name or alias
        # frozen=True, # Optional: Make models immutable
    )

    def __repr__(self) -> str:
        """Concise representation for debugging."""
        return f"<{self.__class__.__name__}(id='{self.id}', object='{self.object}')>"
