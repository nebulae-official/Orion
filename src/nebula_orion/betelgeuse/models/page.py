# src/nebula_orion/betelgeuse/models/page.py
from __future__ import annotations

from typing import Any, Literal  # Import Literal for object type

from pydantic import Field

from .base import BaseObjectModel  # Use absolute import from sibling

# Basic types for complex nested structures (can be Pydantic models later)
PropertyValue = dict[str, Any]
RichTextData = dict[str, Any]
IconData = dict[str, Any]  # Can be emoji or file object
CoverData = dict[str, Any]  # Can be file or external object


class Page(BaseObjectModel):
    """Represent a Notion Page object using Pydantic.

    Inherits common fields from BaseObjectModel.
    Ref: https://developers.notion.com/reference/page-object
    """

    # --- Fields ---
    # Use Literal to ensure the object type is correct upon parsing
    object: Literal["page"] = "page"

    # Inherited: id, created_time, last_edited_time, archived, parent, url,
    #            created_by, last_edited_by

    properties: dict[str, PropertyValue] = Field(default_factory=dict)
    icon: IconData | None = None
    cover: CoverData | None = None

    # --- Helper Methods ---

    def get_title(self) -> str:
        """Retrieve the title of the page as a plain string (if available).

        Assumes the title property is named 'title' and is of type 'title'.
        Returns an empty string if the property isn't found or is empty.

        Returns:
            The plain text title string.

        """
        title_property_value = self.properties.get("title")
        # Check if title_property exists and has the expected structure
        if title_property_value and title_property_value.get("type") == "title":
            title_list: list[RichTextData] = title_property_value.get("title", [])
            return "".join(rt.get("plain_text", "") for rt in title_list).strip()
        return ""

    def get_property_value(self, property_name_or_id: str) -> PropertyValue | None:
        """Retrieve the raw value dictionary for a given property name or ID.

        Note: This returns the raw Notion property value structure. More specific
              parsing methods might be added later or handled by dedicated
              Property models.

        Args:
            property_name_or_id: The name (or ID) of the property.

        Returns:
            The raw property value dictionary from the API, or None if not found.

        """
        return self.properties.get(property_name_or_id)

    def __repr__(self) -> str:
        """Provide a concise representation for debugging.

        Returns:
            A string representation of the Page object.

        """
        title = self.get_title()
        # Truncate long titles for readability
        title_repr = f", title='{title[:30]}...' " if title else ""
        return f"<Page(id='{self.id}'{title_repr})>"
