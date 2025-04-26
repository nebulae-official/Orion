from __future__ import annotations

from datetime import datetime
from typing import Any

import pytest
from pydantic import ValidationError

# Assuming models are in src/nebula_orion/betelgeuse/models
from nebula_orion.betelgeuse.models.page import Page

# Sample data for testing Page model (extends base data)
SAMPLE_PAGE_DATA: dict[str, Any] = {
    "object": "page",  # Correct object type
    "id": "page-uuid-4567",
    "created_time": "2023-01-10T11:00:00.000Z",
    "last_edited_time": "2023-01-11T12:30:00.000Z",
    "created_by": {"object": "user", "id": "user-uuid-3"},
    "last_edited_by": {"object": "user", "id": "user-uuid-4"},
    "parent": {"type": "database_id", "database_id": "db-uuid-123"},
    "archived": False,
    "url": "https://www.notion.so/page-url-4567",
    "icon": {"type": "emoji", "emoji": "📄"},
    "cover": {"type": "external", "external": {"url": "https://example.com/cover.jpg"}},
    "properties": {
        "title": {  # Correct title property structure
            "id": "title",
            "type": "title",
            "title": [
                {
                    "type": "text",
                    "text": {"content": "Test Page Title ", "link": None},
                    "annotations": {},
                    "plain_text": "Test Page Title ",
                    "href": None,
                },
            ],
        },
        "Status": {
            "id": "%3A%3A%3A",  # Example ID
            "type": "select",
            "select": {"id": "select-id-1", "name": "In Progress", "color": "blue"},
        },
        "EmptyProp": {  # Example of a property that might be empty
            "id": "empty1",
            "type": "rich_text",
            "rich_text": [],
        },
    },
    "extra_page_field": "should_be_ignored",  # Test extra field ignoring
}


def test_page_model_successful_parsing() -> None:
    """Test successful parsing of valid page data."""
    model = Page.model_validate(SAMPLE_PAGE_DATA)

    # Test inherited fields
    assert model.id == SAMPLE_PAGE_DATA["id"]
    assert model.object == "page"  # Validated by Literal type hint
    assert model.parent == SAMPLE_PAGE_DATA["parent"]
    assert model.archived is False
    assert model.url == SAMPLE_PAGE_DATA["url"]
    assert isinstance(model.created_time, datetime)
    assert isinstance(model.last_edited_time, datetime)

    # Test page-specific fields
    assert model.icon == SAMPLE_PAGE_DATA["icon"]
    assert model.cover == SAMPLE_PAGE_DATA["cover"]
    assert model.properties == SAMPLE_PAGE_DATA["properties"]


def test_page_model_missing_optional_fields() -> None:
    """Test parsing when optional fields (icon, cover) are missing."""
    data = SAMPLE_PAGE_DATA.copy()
    del data["icon"]
    del data["cover"]

    model = Page.model_validate(data)
    assert model.icon is None
    assert model.cover is None


def test_page_model_get_title() -> None:
    """Test the get_title() helper method."""
    model = Page.model_validate(SAMPLE_PAGE_DATA)
    # Note: Added strip() in get_title implementation
    assert model.get_title() == "Test Page Title"

    # Test with missing title property
    data_no_title_prop = SAMPLE_PAGE_DATA.copy()
    # Need a deep copy if modifying nested dicts
    data_no_title_prop["properties"] = data_no_title_prop["properties"].copy()
    del data_no_title_prop["properties"]["title"]
    model_no_title = Page.model_validate(data_no_title_prop)
    assert model_no_title.get_title() == ""

    # Test with empty title property value
    data_empty_title = SAMPLE_PAGE_DATA.copy()
    data_empty_title["properties"] = data_empty_title["properties"].copy()
    data_empty_title["properties"]["title"] = {
        "id": "title",
        "type": "title",
        "title": [],  # Empty list
    }
    model_empty_title = Page.model_validate(data_empty_title)
    assert model_empty_title.get_title() == ""

    # Test with incorrect title property type
    data_wrong_type = SAMPLE_PAGE_DATA.copy()
    data_wrong_type["properties"] = data_wrong_type["properties"].copy()
    data_wrong_type["properties"]["title"] = {
        "id": "title",
        "type": "rich_text",
        "rich_text": [{"plain_text": "Wrong Type"}],
    }
    model_wrong_type = Page.model_validate(data_wrong_type)
    assert model_wrong_type.get_title() == ""


def test_page_model_get_property_value() -> None:
    """Test the get_property_value() helper method."""
    model = Page.model_validate(SAMPLE_PAGE_DATA)

    status_prop = model.get_property_value("Status")
    assert status_prop == SAMPLE_PAGE_DATA["properties"]["Status"]

    title_prop = model.get_property_value("title")
    assert title_prop == SAMPLE_PAGE_DATA["properties"]["title"]

    missing_prop = model.get_property_value("NonExistentProperty")
    assert missing_prop is None


def test_page_model_repr() -> None:
    """Test the __repr__ method."""
    model = Page.model_validate(SAMPLE_PAGE_DATA)
    # Title is less than 30 chars, so no truncation expected here
    expected_repr = f"<Page(id='{SAMPLE_PAGE_DATA['id']}', title='Test Page Title...' )>"
    assert repr(model) == expected_repr

    # Test repr without a title
    data_no_title_prop = SAMPLE_PAGE_DATA.copy()
    data_no_title_prop["properties"] = data_no_title_prop["properties"].copy()
    del data_no_title_prop["properties"]["title"]
    model_no_title = Page.model_validate(data_no_title_prop)
    expected_repr_no_title = f"<Page(id='{SAMPLE_PAGE_DATA['id']}')>"
    assert repr(model_no_title) == expected_repr_no_title


def test_page_model_validation_error_wrong_object() -> None:
    """Test validation fails if 'object' is not 'page' due to Literal hint."""
    data = SAMPLE_PAGE_DATA.copy()
    data["object"] = "database"  # Incorrect object type

    with pytest.raises(ValidationError) as excinfo:
        Page.model_validate(data)
    # Check Pydantic v2 error details
    errors = excinfo.value.errors()
    assert len(errors) == 1
    assert errors[0]["type"] == "literal_error"
    assert "object" in errors[0]["loc"]
