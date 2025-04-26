from __future__ import annotations

from datetime import datetime
from typing import Any

import pytest
from pydantic import ValidationError

# Assuming models are in src/nebula_orion/betelgeuse/models
from nebula_orion.betelgeuse.models.base import BaseObjectModel

# Sample data closely matching Notion API structure
SAMPLE_BASE_DATA: dict[str, Any] = {
    "object": "list",  # Example, could be any object type
    "id": "some-random-uuid-1234",
    "created_time": "2022-06-28T08:10:00.000Z",
    "last_edited_time": "2022-06-29T10:20:00.000Z",
    "created_by": {"object": "user", "id": "user-uuid-1"},
    "last_edited_by": {"object": "user", "id": "user-uuid-2"},
    "parent": {"type": "workspace", "workspace": True},
    "archived": False,
    "url": "https://www.notion.so/some-url",  # Included as it exists in BaseObjectModel
    "extra_field_not_in_model": "should_be_ignored",
}


def test_base_model_successful_parsing() -> None:
    """Test successful parsing of valid data using Pydantic v2."""
    model = BaseObjectModel.model_validate(SAMPLE_BASE_DATA)

    assert model.id == SAMPLE_BASE_DATA["id"]
    assert model.object == SAMPLE_BASE_DATA["object"]
    assert isinstance(model.created_time, datetime)
    assert isinstance(model.last_edited_time, datetime)
    # Pydantic automatically converts ISO strings to datetime
    assert (
        model.created_time.isoformat(timespec="milliseconds").replace("+00:00", "Z")
        == "2022-06-28T08:10:00.000Z"
    )
    assert (
        model.last_edited_time.isoformat(timespec="milliseconds").replace("+00:00", "Z")
        == "2022-06-29T10:20:00.000Z"
    )
    assert model.created_by == SAMPLE_BASE_DATA["created_by"]
    assert model.last_edited_by == SAMPLE_BASE_DATA["last_edited_by"]
    assert model.parent == SAMPLE_BASE_DATA["parent"]
    assert model.archived is False
    assert model.url == SAMPLE_BASE_DATA["url"]


def test_base_model_defaults() -> None:
    """Test default values are applied when optional fields are missing."""
    data = SAMPLE_BASE_DATA.copy()
    # Remove fields with defaults or Optionals
    del data["archived"]
    del data["url"]
    del data["created_by"]
    del data["last_edited_by"]

    model = BaseObjectModel.model_validate(data)
    assert model.archived is False  # Default value
    assert model.url == ""  # Default value
    assert model.created_by is None  # Optional field defaults to None
    assert model.last_edited_by is None


def test_base_model_missing_required_field_raises_error() -> None:
    """Test Pydantic ValidationError is raised if required fields are missing."""
    data = SAMPLE_BASE_DATA.copy()
    del data["id"]  # 'id' is required

    with pytest.raises(ValidationError) as excinfo:
        BaseObjectModel.model_validate(data)
    # Check that the error message mentions the missing field
    errors = excinfo.value.errors()
    assert len(errors) == 1
    assert errors[0]["type"] == "missing"
    assert "id" in errors[0]["loc"]


def test_base_model_incorrect_type_raises_error() -> None:
    """Test ValidationError is raised for incorrect field types."""
    data_bad_time = SAMPLE_BASE_DATA.copy()
    data_bad_time["created_time"] = "not-a-datetime"  # Invalid datetime string

    with pytest.raises(ValidationError) as excinfo_time:
        BaseObjectModel.model_validate(data_bad_time)
    errors_time = excinfo_time.value.errors()
    assert len(errors_time) == 1
    assert errors_time[0]["type"] == "datetime_from_date_parsing"  # Pydantic v2 type
    assert "created_time" in errors_time[0]["loc"]

    data_bad_bool = SAMPLE_BASE_DATA.copy()
    data_bad_bool["archived"] = "maybe"  # Not a boolean
    with pytest.raises(ValidationError) as excinfo_bool:
        BaseObjectModel.model_validate(data_bad_bool)
    errors_bool = excinfo_bool.value.errors()
    assert len(errors_bool) == 1
    assert errors_bool[0]["type"] == "bool_parsing"  # Pydantic v2 type
    assert "archived" in errors_bool[0]["loc"]


def test_base_model_ignores_extra_fields() -> None:
    """Test that extra fields are ignored due to Config.extra = 'ignore'."""
    data = SAMPLE_BASE_DATA.copy()
    # Add an extra field not defined in the model
    data["some_random_extra_field"] = "this should not cause an error"

    try:
        model = BaseObjectModel.model_validate(data)
        # Check that the extra field is not present on the model instance
        assert not hasattr(model, "some_random_extra_field")
        # Check via __dict__ as well
        assert "some_random_extra_field" not in model.__dict__
    except ValidationError as e:
        pytest.fail(f"ValidationError was raised unexpectedly for extra field: {e}")


def test_base_model_repr() -> None:
    """Test the __repr__ method."""
    model = BaseObjectModel.model_validate(SAMPLE_BASE_DATA)
    expected_repr = f"<BaseObjectModel(id='{SAMPLE_BASE_DATA['id']}', object='{SAMPLE_BASE_DATA['object']}')>"
    assert repr(model) == expected_repr
