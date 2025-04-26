# src/nebula_orion/betelgeuse/models/database.py
from __future__ import annotations

from typing import Any, Literal  # Import Literal

from pydantic import Field

from .base import BaseObjectModel

# Basic types (can be Pydantic models later)
PropertySchema = dict[str, Any]  # Represents the definition of a DB property
RichTextData = dict[str, Any]
IconData = dict[str, Any]
CoverData = dict[str, Any]


class Database(BaseObjectModel):
    """Represent a Notion Database object using Pydantic.

    Inherits common fields from BaseObjectModel.
    Ref: https://developers.notion.com/reference/database-object
    """

    # --- Fields ---
    object: Literal["database"] = "database"

    # Inherited: id, created_time, last_edited_time, archived, parent, url,
    #            created_by, last_edited_by

    title: list[RichTextData] = Field(default_factory=list)
    description: list[RichTextData] = Field(default_factory=list)
    properties: dict[str, PropertySchema] = Field(
        default_factory=dict,
    )  # Schema definition
    is_inline: bool = False
    icon: IconData | None = None
    cover: CoverData | None = None

    # --- Helper Methods ---
    def get_title(self) -> str:
        """Retrieve the title of the database as a plain string.

        Returns:
            The plain text title string.

        """
        return "".join(rt.get("plain_text", "") for rt in self.title).strip()

    def get_property_schema(self, property_name_or_id: str) -> PropertySchema | None:
        """Retrieve the schema definition for a specific property by its name or ID.

        Args:
            property_name_or_id: The name or ID of the property.

        Returns:
            The dictionary describing the property schema, or None if not found.

        """
        return self.properties.get(property_name_or_id)

    def __repr__(self) -> str:
        """Provide a concise representation of the Database object.

        Returns:
            A string representation of the Database object.

        """
        title = self.get_title()
        title_repr = f", title='{title[:30]}...' " if title else ""
        return f"<Database(id='{self.id}'{title_repr})>"
