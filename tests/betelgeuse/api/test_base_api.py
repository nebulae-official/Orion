from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Optional  # Import necessary types
from unittest.mock import MagicMock

import pytest
import requests

from nebula_orion.betelgeuse import constants
from nebula_orion.betelgeuse.api.base import BaseAPIClient
from nebula_orion.betelgeuse.auth.token import APITokenAuth
from nebula_orion.betelgeuse.errors import NotionAPIError, NotionRequestError

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

# Type alias for the mock response factory
MockResponseFactory = Callable[
    [int, Optional[dict[str, Any]], Optional[str], bool, Optional[bytes]],
    MagicMock,  # The factory returns a MagicMock representing a Response
]


# Fixture for a reusable mock auth object
@pytest.fixture
def mock_auth() -> MagicMock:
    """Provide a mock APITokenAuth object."""
    auth = MagicMock(spec=APITokenAuth)
    auth.get_auth_headers.return_value = {"Authorization": "Bearer test_token"}
    return auth


# Fixture for creating mock response objects
@pytest.fixture
def mock_requests_response() -> MockResponseFactory:
    """Provide a factory for creating mock requests.Response objects."""

    def _create_response(
        status_code: int,
        json_data: dict[str, Any] | None = None,
        text_data: str | None = None,
        ok: bool = True,
        content: bytes | None = None,
    ) -> MagicMock:
        response = MagicMock(spec=requests.Response)
        response.status_code = status_code
        response.ok = ok
        response.text = text_data or ""

        if json_data is not None:
            response.json.return_value = json_data
            response.content = (
                bytes(str(json_data), "utf-8") if content is None else content
            )
        else:
            response.json.side_effect = requests.exceptions.JSONDecodeError(
                "Mock decode error", "", 0
            )
            response.content = (
                bytes(text_data or "", "utf-8") if content is None else content
            )

        if content == b"":
            response.content = b""  # Explicitly set empty bytes

        return response

    return _create_response


# Fixture for the BaseAPIClient instance
@pytest.fixture
def base_client(mock_auth: MagicMock) -> BaseAPIClient:
    """Provide a BaseAPIClient instance with mock authentication."""
    return BaseAPIClient(auth=mock_auth)


def test_base_client_initialization(
    base_client: BaseAPIClient, mock_auth: MagicMock
) -> None:
    """Test client stores auth and configuration correctly."""
    assert base_client.auth == mock_auth
    assert base_client.base_url == constants.DEFAULT_NOTION_API_URL
    assert base_client.notion_version == constants.DEFAULT_NOTION_VERSION
    assert base_client.timeout == constants.DEFAULT_TIMEOUT
    assert isinstance(base_client._session, requests.Session)


def test_get_common_headers(base_client: BaseAPIClient, mock_auth: MagicMock) -> None:
    """Test that common headers include auth and Notion-Version."""
    headers: dict[str, str] = base_client._get_common_headers()
    assert headers["Notion-Version"] == constants.DEFAULT_NOTION_VERSION
    assert headers["Authorization"] == "Bearer test_token"
    assert headers["Content-Type"] == "application/json"
    assert headers["Accept"] == "application/json"


def test_request_successful_get(
    base_client: BaseAPIClient,
    mocker: MockerFixture,
    mock_requests_response: MockResponseFactory,
) -> None:
    """Test a successful GET request."""
    path: str = "/v1/users/me"
    expected_response_data: dict[str, Any] = {"object": "user", "id": "123"}
    mock_response: MagicMock = mock_requests_response(
        status_code=200,
        json_data=expected_response_data,
        ok=True,
    )
    mock_session_request: MagicMock = mocker.patch.object(
        base_client._session,
        "request",
        return_value=mock_response,
    )

    response_data: dict[str, Any] = base_client.request(method="GET", path=path)

    mock_session_request.assert_called_once_with(
        method="GET",
        url=f"{constants.DEFAULT_NOTION_API_URL}{path}",
        headers=base_client._get_common_headers(),
        params=None,
        json=None,
        timeout=constants.DEFAULT_TIMEOUT,
    )
    assert response_data == expected_response_data


def test_request_successful_post(
    base_client: BaseAPIClient,
    mocker: MockerFixture,
    mock_requests_response: MockResponseFactory,
) -> None:
    """Test a successful POST request with JSON data."""
    path: str = "/v1/pages"
    request_data: dict[str, Any] = {"parent": {"database_id": "db1"}, "properties": {}}
    expected_response_data: dict[str, Any] = {"object": "page", "id": "page1"}
    mock_response: MagicMock = mock_requests_response(
        status_code=200,
        json_data=expected_response_data,
        ok=True,
    )
    mock_session_request: MagicMock = mocker.patch.object(
        base_client._session,
        "request",
        return_value=mock_response,
    )

    response_data: dict[str, Any] = base_client.request(
        method="POST",
        path=path,
        json_data=request_data,
    )

    mock_session_request.assert_called_once_with(
        method="POST",
        url=f"{constants.DEFAULT_NOTION_API_URL}{path}",
        headers=base_client._get_common_headers(),
        params=None,
        json=request_data,  # Ensure json data is passed
        timeout=constants.DEFAULT_TIMEOUT,
    )
    assert response_data == expected_response_data


def test_request_successful_no_content(
    base_client: BaseAPIClient,
    mocker: MockerFixture,
    mock_requests_response: MockResponseFactory,
) -> None:
    """Test a successful request that returns no content (e.g., 204)."""
    path: str = "/v1/blocks/some_id"
    mock_response: MagicMock = mock_requests_response(
        status_code=204,
        ok=True,
        content=b"",
    )
    mock_session_request: MagicMock = mocker.patch.object(
        base_client._session,
        "request",
        return_value=mock_response,
    )

    response_data: dict[str, Any] = base_client.request(method="DELETE", path=path)

    mock_session_request.assert_called_once()
    assert response_data == {}  # Expect empty dict for no content success


def test_request_notion_api_error_known_format(
    base_client: BaseAPIClient,
    mocker: MockerFixture,
    mock_requests_response: MockResponseFactory,
) -> None:
    """Test handling of Notion API error with standard JSON format."""
    path: str = "/v1/databases/invalid_id"
    error_data: dict[str, Any] = {
        "object": "error",
        "status": 404,
        "code": "object_not_found",
        "message": "Could not find database.",
    }
    mock_response: MagicMock = mock_requests_response(
        status_code=404,
        json_data=error_data,
        ok=False,
    )
    mock_session_request: MagicMock = mocker.patch.object(
        base_client._session,
        "request",
        return_value=mock_response,
    )

    with pytest.raises(NotionAPIError) as excinfo:
        base_client.request(method="GET", path=path)

    mock_session_request.assert_called_once()
    assert excinfo.value.status_code == 404
    assert excinfo.value.error_code == "object_not_found"
    assert "Could not find database" in str(excinfo.value)


def test_request_notion_api_error_unknown_format(
    base_client: BaseAPIClient,
    mocker: MockerFixture,
    mock_requests_response: MockResponseFactory,
) -> None:
    """Test handling of API error with non-standard/non-JSON body."""
    path: str = "/v1/some_error_endpoint"
    error_text: str = "<html><body>Gateway Timeout</body></html>"
    mock_response: MagicMock = mock_requests_response(
        status_code=504,
        text_data=error_text,
        ok=False,
    )
    # Ensure .json() call inside the handler raises an error
    mock_response.json.side_effect = requests.exceptions.JSONDecodeError(
        "Mock decode error", "", 0
    )
    mock_session_request: MagicMock = mocker.patch.object(
        base_client._session,
        "request",
        return_value=mock_response,
    )

    with pytest.raises(NotionAPIError) as excinfo:
        base_client.request(method="GET", path=path)

    mock_session_request.assert_called_once()
    assert excinfo.value.status_code == 504
    assert excinfo.value.error_code == "unknown_error_format"
    assert error_text in str(excinfo.value)


def test_request_network_error(
    base_client: BaseAPIClient,
    mocker: MockerFixture,
) -> None:
    """Test handling of underlying requests library errors."""
    path: str = "/v1/timeout_endpoint"
    # Mock the request method to raise a requests exception
    mock_session_request: MagicMock = mocker.patch.object(
        base_client._session,
        "request",
        side_effect=requests.exceptions.Timeout("Connection timed out"),
    )

    with pytest.raises(
        NotionRequestError,
        match="HTTP Request failed: Connection timed out",
    ):
        base_client.request(method="GET", path=path)

    mock_session_request.assert_called_once()
