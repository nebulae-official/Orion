from __future__ import annotations

from datetime import datetime
from typing import Any

import pytest
from pydantic import ValidationError

# Assuming models are in src/nebula_orion/betelgeuse/models
from nebula_orion.betelgeuse.models.database import Database

# Sample data for testing Database model
SAMPLE_DB_DATA: dict[str, Any] = {
    "object": "database",
    "id": "db-uuid-9876",
    "created_time": "2021-05-15T10:00:00.000Z",
    "last_edited_time": "2021-05-16T15:45:00.000Z",
    "created_by": {"object": "user", "id": "user-uuid-5"},
    "last_edited_by": {"object": "user", "id": "user-uuid-6"},
    "parent": {"type": "page_id", "page_id": "page-uuid-abc"},
    "archived": False,
    "url": "https://www.notion.so/db-url-9876",
    "icon": None,  # Optional field missing
    "cover": {
        "type": "external",
        "external": {"url": "https://example.com/db_cover.png"},
    },
    "title": [
        {
            "type": "text",
            "text": {"content": " Projects DB ", "link": None},
            "annotations": {},
            "plain_text": " Projects DB ",
            "href": None,
        },
    ],
    "description": [],  # Optional field empty
    "properties": {
        "Name": {  # Example Title property schema
            "id": "title",
            "name": "Name",
            "type": "title",
            "title": {},
        },
        "Status": {  # Example Select property schema
            "id": "prop_status_id",
            "name": "Status",
            "type": "select",
            "select": {
                "options": [
                    {"id": "opt1", "name": "Todo", "color": "gray"},
                    {"id": "opt2", "name": "Doing", "color": "blue"},
                    {"id": "opt3", "name": "Done", "color": "green"},
                ],
            },
        },
    },
    "is_inline": False,
    "extra_db_field": "should_be_ignored",
}


def test_database_model_successful_parsing() -> None:
    """Test successful parsing of valid database data."""
    model = Database.model_validate(SAMPLE_DB_DATA)

    # Test inherited fields
    assert model.id == SAMPLE_DB_DATA["id"]
    assert model.object == "database"  # Validated by Literal
    assert model.parent == SAMPLE_DB_DATA["parent"]
    assert model.archived is False
    assert model.url == SAMPLE_DB_DATA["url"]
    assert isinstance(model.created_time, datetime)
    assert isinstance(model.last_edited_time, datetime)
    assert model.last_edited_by == SAMPLE_DB_DATA["last_edited_by"]

    # Test database-specific fields
    assert model.title == SAMPLE_DB_DATA["title"]
    assert model.description == SAMPLE_DB_DATA["description"]  # Empty list
    assert model.properties == SAMPLE_DB_DATA["properties"]
    assert model.is_inline is False
    assert model.icon is None  # Optional field was None
    assert model.cover == SAMPLE_DB_DATA["cover"]


def test_database_model_missing_optional_fields() -> None:
    """Test parsing when optional fields (icon, cover, description) are missing."""
    data = SAMPLE_DB_DATA.copy()
    # Ensure keys are fully removed, not just None
    if "icon" in data:
        del data["icon"]
    if "cover" in data:
        del data["cover"]
    if "description" in data:
        del data["description"]

    model = Database.model_validate(data)
    assert model.icon is None
    assert model.cover is None
    # Check default_factory was used for lists
    assert model.description == []


def test_database_model_get_title() -> None:
    """Test the get_title() helper method."""
    model = Database.model_validate(SAMPLE_DB_DATA)
    assert model.get_title() == "Projects DB"  # Note: strip() applied

    # Test with empty title list
    data_empty_title = SAMPLE_DB_DATA.copy()
    data_empty_title["title"] = []
    model_empty_title = Database.model_validate(data_empty_title)
    assert model_empty_title.get_title() == ""


def test_database_model_get_property_schema() -> None:
    """Test the get_property_schema() helper method."""
    model = Database.model_validate(SAMPLE_DB_DATA)

    status_schema = model.get_property_schema("Status")
    assert status_schema == SAMPLE_DB_DATA["properties"]["Status"]

    name_schema = model.get_property_schema("Name")
    assert name_schema == SAMPLE_DB_DATA["properties"]["Name"]

    missing_schema = model.get_property_schema("NonExistentProperty")
    assert missing_schema is None


def test_database_model_repr() -> None:
    """Test the __repr__ method."""
    model = Database.model_validate(SAMPLE_DB_DATA)
    expected_repr = f"<Database(id='{SAMPLE_DB_DATA['id']}', title='Projects DB...' )>"
    assert repr(model) == expected_repr

    # Test repr with empty title
    data_empty_title = SAMPLE_DB_DATA.copy()
    data_empty_title["title"] = []
    model_empty_title = Database.model_validate(data_empty_title)
    expected_repr_no_title = f"<Database(id='{SAMPLE_DB_DATA['id']}')>"
    assert repr(model_empty_title) == expected_repr_no_title


def test_database_model_validation_error_wrong_object() -> None:
    """Test validation fails if 'object' is not 'database' due to Literal hint."""
    data = SAMPLE_DB_DATA.copy()
    data["object"] = "page"  # Incorrect object type

    with pytest.raises(ValidationError) as excinfo:
        Database.model_validate(data)
    errors = excinfo.value.errors()
    assert len(errors) == 1
    assert errors[0]["type"] == "literal_error"
    assert "object" in errors[0]["loc"]
