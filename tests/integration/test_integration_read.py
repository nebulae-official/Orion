# tests/betelgeuse/test_client.py
from __future__ import annotations

import logging
from typing import Any
from unittest.mock import MagicMock, call

import pytest
from pydantic import ValidationError  # Import Pydantic error
from pytest_mock import MockerFixture

# Use absolute imports
from nebula_orion.betelgeuse import constants
from nebula_orion.betelgeuse.api.base import BaseAPIClient
from nebula_orion.betelgeuse.auth.token import APITokenAuth
from nebula_orion.betelgeuse.client import NotionClient
from nebula_orion.betelgeuse.errors import (
    AuthenticationError,
    BetelgeuseError,
    NotionAPIError,
)
from nebula_orion.betelgeuse.models import Database, Page  # Import models

# --- Test Data Fixtures (Copied/Adapted from Model Tests for Client Use) ---

# Sample data for testing Page model
SAMPLE_PAGE_DATA: dict[str, Any] = {
    "object": "page",
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
        "title": {
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
            "id": "%3A%3A%3A",
            "type": "select",
            "select": {"id": "select-id-1", "name": "In Progress", "color": "blue"},
        },
    },
}

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
    "icon": None,
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
    "description": [],
    "properties": {
        "Name": {"id": "title", "name": "Name", "type": "title", "title": {}},
        "Status": {
            "id": "prop_status_id",
            "name": "Status",
            "type": "select",
            "select": {"options": [{"id": "opt1", "name": "Todo", "color": "gray"}]},
        },
    },
    "is_inline": False,
}

# Sample data for database query results (list object)
SAMPLE_QUERY_RESPONSE_PAGE_1: dict[str, Any] = {
    "object": "list",
    "results": [
        SAMPLE_PAGE_DATA,
        {
            **SAMPLE_PAGE_DATA,
            "id": "page-uuid-other",
            "properties": {
                "title": {
                    "id": "title",
                    "type": "title",
                    "title": [{"plain_text": "Another Page"}],
                },
            },
        },
    ],
    "next_cursor": "cursor-for-page-2",
    "has_more": True,
    "type": "page_or_database",
    "page_or_database": {},
}

SAMPLE_QUERY_RESPONSE_PAGE_2: dict[str, Any] = {
    "object": "list",
    "results": [
        {
            **SAMPLE_PAGE_DATA,
            "id": "page-uuid-final",
            "properties": {
                "title": {
                    "id": "title",
                    "type": "title",
                    "title": [{"plain_text": "Final Page"}],
                },
            },
        },
        {
            "id": "invalid-item-123",
            "object": "block",
            "type": "paragraph",
            "paragraph": {},
        },  # Invalid item (not a page)
    ],
    "next_cursor": None,
    "has_more": False,
    "type": "page_or_database",
    "page_or_database": {},
}

SAMPLE_QUERY_RESPONSE_EMPTY: dict[str, Any] = {
    "object": "list",
    "results": [],
    "next_cursor": None,
    "has_more": False,
    "type": "page_or_database",
    "page_or_database": {},
}


# --- Fixtures ---


@pytest.fixture
def mock_api_client(mocker: MockerFixture) -> MagicMock:
    """Provides a mock BaseAPIClient instance with a mocked request method."""
    mock = MagicMock(spec=BaseAPIClient)
    # Mock the request method directly on the instance
    mock.request = MagicMock()
    return mock


@pytest.fixture
def client_with_mocks(mocker: MockerFixture, mock_api_client: MagicMock) -> NotionClient:
    """Provides a NotionClient instance with mocked BaseAPIClient."""
    # Mock auth part (assuming it works from Iteration 1 tests)
    mocker.patch(
        "nebula_orion.betelgeuse.client.auth_token_module.APITokenAuth",
        autospec=True,
    )
    # Patch BaseAPIClient constructor to return our mock instance
    mocker.patch(
        "nebula_orion.betelgeuse.client.BaseAPIClient",
        return_value=mock_api_client,
    )

    client = NotionClient(auth_token="fake_token_for_test")
    # Ensure the mock is injected
    assert client._api_client is mock_api_client  # type: ignore[attr-defined]
    return client


# --- Tests for Iteration 1 (Keep for Regression) ---
# (Include the passing tests from Iteration 1:
#  test_client_init_success, test_client_init_uses_env_var_token_if_none_passed,
#  test_client_init_raises_auth_error_on_token_auth_failure,
#  test_client_init_raises_auth_error_on_base_client_failure, test_client_repr)
# --- Tests for Iteration 1 (Keep for Regression) ---


@pytest.fixture
def mock_api_token_auth_cls(mocker: MockerFixture) -> MagicMock:
    """Mocks the APITokenAuth class constructor."""
    return mocker.patch(
        "nebula_orion.betelgeuse.client.auth_token_module.APITokenAuth",
        autospec=True,
    )


@pytest.fixture
def mock_base_api_client_cls(mocker: MockerFixture) -> MagicMock:
    """Mocks the BaseAPIClient class constructor."""
    return mocker.patch("nebula_orion.betelgeuse.client.BaseAPIClient", autospec=True)


@pytest.fixture
def mock_auth_instance(mock_api_token_auth_cls: MagicMock) -> MagicMock:
    """Provides a mock instance returned by APITokenAuth constructor."""
    instance = MagicMock(spec=APITokenAuth)
    mock_api_token_auth_cls.return_value = instance
    return instance


@pytest.fixture
def mock_api_client_instance(mock_base_api_client_cls: MagicMock) -> MagicMock:
    """Provides a mock instance returned by BaseAPIClient constructor."""
    instance = MagicMock(spec=BaseAPIClient)
    mock_base_api_client_cls.return_value = instance
    return instance


def test_client_init_uses_env_var_token_if_none_passed(
    mock_api_token_auth_cls: MagicMock,
    mock_base_api_client_cls: MagicMock,
) -> None:
    """Test APITokenAuth is called with None when no token is passed to client."""
    NotionClient(auth_token=None)  # Or NotionClient()
    mock_api_token_auth_cls.assert_called_once_with(token=None)
    mock_base_api_client_cls.assert_called_once()  # Ensure API client init still called


def test_client_init_raises_auth_error_on_token_auth_failure(
    mock_api_token_auth_cls: MagicMock,
    mock_base_api_client_cls: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test AuthenticationError propagation if APITokenAuth init fails."""
    auth_fail_error = AuthenticationError("Token setup failed")
    mock_api_token_auth_cls.side_effect = auth_fail_error
    caplog.set_level(logging.ERROR)  # Auth logs error

    with pytest.raises(AuthenticationError) as excinfo:
        NotionClient()

    assert excinfo.value is auth_fail_error  # Check exact error propagated
    mock_base_api_client_cls.assert_not_called()  # API client init shouldn't happen


def test_client_init_raises_auth_error_on_base_client_failure(
    mock_api_token_auth_cls: MagicMock,
    mock_base_api_client_cls: MagicMock,
    mock_auth_instance: MagicMock,  # Fixture needed even if unused in calls
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test error propagation if BaseAPIClient init fails."""
    base_client_fail_error = TypeError("Bad config for BaseAPIClient")
    mock_base_api_client_cls.side_effect = base_client_fail_error
    caplog.set_level(logging.ERROR)

    with pytest.raises(AuthenticationError) as excinfo:
        NotionClient()

    assert "Failed to initialize API client" in str(excinfo.value)
    assert excinfo.value.__cause__ is base_client_fail_error
    assert "Unexpected error during BaseAPIClient initialization" in caplog.text


# --- Tests for Iteration 2 Methods ---


def test_retrieve_page_success(
    client_with_mocks: NotionClient,
    mock_api_client: MagicMock,
) -> None:
    """Test successful page retrieval and parsing into Page model."""
    page_id = SAMPLE_PAGE_DATA["id"]
    mock_api_client.request.return_value = SAMPLE_PAGE_DATA

    page = client_with_mocks.retrieve_page(page_id)

    mock_api_client.request.assert_called_once_with(
        method=constants.GET,
        path=f"/v1/pages/{page_id}",
    )
    assert isinstance(page, Page)
    assert page.id == page_id
    assert page.object == "page"
    assert page.get_title() == "Test Page Title"


def test_retrieve_page_parsing_error(
    client_with_mocks: NotionClient,
    mock_api_client: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test BetelgeuseError wrapping Pydantic ValidationError on invalid page data."""
    page_id = "page-invalid-data"
    invalid_data = {"object": "page", "id": page_id}  # Missing required fields
    mock_api_client.request.return_value = invalid_data
    caplog.set_level(logging.ERROR)

    with pytest.raises(
        BetelgeuseError,
        match=f"Failed to parse Page response \\(ID: {page_id}\\)",
    ) as excinfo:
        client_with_mocks.retrieve_page(page_id)

    assert isinstance(excinfo.value.__cause__, ValidationError)
    assert f"Failed to validate Page response (ID: {page_id})" in caplog.text


def test_retrieve_page_api_error(
    client_with_mocks: NotionClient,
    mock_api_client: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test propagation of NotionAPIError from API client."""
    page_id = "page-not-found"
    api_error = NotionAPIError(404, "object_not_found", "Could not find page")
    mock_api_client.request.side_effect = api_error
    caplog.set_level(logging.WARNING)

    with pytest.raises(NotionAPIError) as excinfo:
        client_with_mocks.retrieve_page(page_id)

    assert excinfo.value is api_error
    assert f"API or Request Error retrieving page {page_id}" in caplog.text


def test_retrieve_database_success(
    client_with_mocks: NotionClient,
    mock_api_client: MagicMock,
) -> None:
    """Test successful database retrieval and parsing into Database model."""
    db_id = SAMPLE_DB_DATA["id"]
    mock_api_client.request.return_value = SAMPLE_DB_DATA

    database = client_with_mocks.retrieve_database(db_id)

    mock_api_client.request.assert_called_once_with(
        method=constants.GET,
        path=f"/v1/databases/{db_id}",
    )
    assert isinstance(database, Database)
    assert database.id == db_id
    assert database.object == "database"
    assert database.get_title() == "Projects DB"


def test_retrieve_database_parsing_error(
    client_with_mocks: NotionClient,
    mock_api_client: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test BetelgeuseError wrapping Pydantic ValidationError on invalid db data."""
    db_id = "db-invalid-data"
    invalid_data = {"object": "database", "id": db_id}  # Missing required fields
    mock_api_client.request.return_value = invalid_data
    caplog.set_level(logging.ERROR)

    with pytest.raises(
        BetelgeuseError,
        match=f"Failed to parse Database response \\(ID: {db_id}\\)",
    ) as excinfo:
        client_with_mocks.retrieve_database(db_id)

    assert isinstance(excinfo.value.__cause__, ValidationError)
    assert f"Failed to validate Database response (ID: {db_id})" in caplog.text


def test_retrieve_database_api_error(
    client_with_mocks: NotionClient,
    mock_api_client: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test propagation of NotionAPIError from API client."""
    db_id = "db-forbidden"
    api_error = NotionAPIError(403, "restricted_resource", "Cannot access database")
    mock_api_client.request.side_effect = api_error
    caplog.set_level(logging.WARNING)

    with pytest.raises(NotionAPIError) as excinfo:
        client_with_mocks.retrieve_database(db_id)

    assert excinfo.value is api_error
    assert f"API or Request Error retrieving database {db_id}" in caplog.text


def test_query_database_no_results(
    client_with_mocks: NotionClient,
    mock_api_client: MagicMock,
) -> None:
    """Test querying a database that returns an empty list."""
    db_id = "db-empty"
    mock_api_client.request.return_value = SAMPLE_QUERY_RESPONSE_EMPTY

    results = list(client_with_mocks.query_database(db_id))

    expected_body = {"page_size": 100}  # Default page size
    mock_api_client.request.assert_called_once_with(
        method=constants.POST,
        path=f"/v1/databases/{db_id}/query",
        json_data=expected_body,
    )
    assert results == []


def test_query_database_single_page_no_pagination(
    client_with_mocks: NotionClient,
    mock_api_client: MagicMock,
) -> None:
    """Test query with results fitting on one page (has_more=False)."""
    db_id = "db-single"
    response_data = SAMPLE_QUERY_RESPONSE_PAGE_1.copy()
    response_data["has_more"] = False  # Modify response
    response_data["next_cursor"] = None
    mock_api_client.request.return_value = response_data

    results = list(client_with_mocks.query_database(db_id, page_size=50))

    expected_body = {"page_size": 50}
    mock_api_client.request.assert_called_once_with(
        method=constants.POST,
        path=f"/v1/databases/{db_id}/query",
        json_data=expected_body,
    )
    assert len(results) == len(response_data["results"])
    assert all(isinstance(p, Page) for p in results)
    assert results[0].id == SAMPLE_PAGE_DATA["id"]
    assert results[1].id == "page-uuid-other"


def test_query_database_multiple_pages(
    client_with_mocks: NotionClient,
    mock_api_client: MagicMock,
) -> None:
    """Test query requiring multiple paginated requests."""
    db_id = "db-multi"
    # Configure mock to return page 1 then page 2
    mock_api_client.request.side_effect = [
        SAMPLE_QUERY_RESPONSE_PAGE_1,
        SAMPLE_QUERY_RESPONSE_PAGE_2,
    ]

    results = list(
        client_with_mocks.query_database(db_id, page_size=2),
    )  # Use smaller page size for test

    # Check API calls
    expected_calls = [
        call(  # First call
            method=constants.POST,
            path=f"/v1/databases/{db_id}/query",
            json_data={"page_size": 2},  # Uses specified page_size
        ),
        call(  # Second call
            method=constants.POST,
            path=f"/v1/databases/{db_id}/query",
            json_data={"page_size": 2, "start_cursor": "cursor-for-page-2"},
        ),
    ]
    mock_api_client.request.assert_has_calls(expected_calls)
    assert mock_api_client.request.call_count == 2

    # Check combined results (excluding the invalid item from page 2)
    assert len(results) == 3
    assert results[0].id == SAMPLE_PAGE_DATA["id"]
    assert results[1].id == "page-uuid-other"
    assert results[2].id == "page-uuid-final"
    assert all(isinstance(p, Page) for p in results)


def test_query_database_with_filter_sorts(
    client_with_mocks: NotionClient,
    mock_api_client: MagicMock,
) -> None:
    """Test passing filter and sorts data to the API call."""
    db_id = "db-filter-sort"
    my_filter = {"property": "Status", "select": {"equals": "Done"}}
    my_sorts = [{"property": "Name", "direction": "ascending"}]
    mock_api_client.request.return_value = SAMPLE_QUERY_RESPONSE_EMPTY  # Empty results ok

    list(
        client_with_mocks.query_database(
            db_id,
            filter_data=my_filter,
            sorts_data=my_sorts,
        ),
    )

    expected_body = {
        "filter": my_filter,
        "sorts": my_sorts,
        "page_size": 100,  # Default page size
    }
    mock_api_client.request.assert_called_once_with(
        method=constants.POST,
        path=f"/v1/databases/{db_id}/query",
        json_data=expected_body,
    )


def test_query_database_skips_invalid_page_data(
    client_with_mocks: NotionClient,
    mock_api_client: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that pages failing Pydantic validation within results are skipped."""
    db_id = "db-bad-page"
    # Response contains one valid page and one invalid page (missing required fields)
    bad_page_data = {"object": "page", "id": "bad-page-id"}
    response_with_bad_page = {
        "object": "list",
        "results": [SAMPLE_PAGE_DATA, bad_page_data],
        "next_cursor": None,
        "has_more": False,
        "type": "page_or_database",
        "page_or_database": {},
    }
    mock_api_client.request.return_value = response_with_bad_page
    caplog.set_level(logging.WARNING)

    results = list(client_with_mocks.query_database(db_id))

    # Check only the valid page was yielded
    assert len(results) == 1
    assert results[0].id == SAMPLE_PAGE_DATA["id"]
    assert isinstance(results[0], Page)

    # Check warning log for the skipped item
    assert (
        f"Skipping item ID 'bad-page-id' in DB query results (DB ID: {db_id})"
        in caplog.text
    )
    assert "due to validation error" in caplog.text


def test_query_database_raises_on_api_error_mid_pagination(
    client_with_mocks: NotionClient,
    mock_api_client: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that iteration stops and error is raised if API fails during pagination."""
    db_id = "db-fails-mid"
    api_error = NotionAPIError(500, "internal_server_error", "Server error")
    mock_api_client.request.side_effect = [
        SAMPLE_QUERY_RESPONSE_PAGE_1,  # First page succeeds
        api_error,  # Second page fails
    ]
    caplog.set_level(logging.ERROR)

    results = []
    with pytest.raises(NotionAPIError) as excinfo:
        # Consume the iterator
        for page in client_with_mocks.query_database(db_id):
            results.append(page)

    assert excinfo.value is api_error  # Check the correct error is raised
    # Check only results from the first page were yielded
    assert len(results) == len(SAMPLE_QUERY_RESPONSE_PAGE_1["results"])
    assert mock_api_client.request.call_count == 2  # Both calls attempted
    assert (
        f"API/Request error during database query (page 2, DB ID: {db_id})" in caplog.text
    )
