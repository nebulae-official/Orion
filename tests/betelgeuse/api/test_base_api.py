# tests/betelgeuse/api/test_base_api.py
from __future__ import annotations

import json
import logging
from unittest.mock import MagicMock

import pytest
import requests
from pytest_mock import MockerFixture

from nebula_orion.betelgeuse import config, constants

# Use absolute imports for target code
from nebula_orion.betelgeuse.api.base import BaseAPIClient
from nebula_orion.betelgeuse.auth.token import APITokenAuth
from nebula_orion.betelgeuse.errors import (
    BetelgeuseError,
    NotionAPIError,
    NotionRequestError,
)

# --- Fixtures ---


@pytest.fixture
def mock_auth(mocker: MockerFixture) -> MagicMock:
    """Provide a mock APITokenAuth object."""
    auth = MagicMock(spec=APITokenAuth)
    auth.get_auth_headers.return_value = {"Authorization": "Bearer test_token"}
    return auth


@pytest.fixture
def mock_requests_session(mocker: MockerFixture) -> MagicMock:
    """Mock the requests.Session instance used by BaseAPIClient."""
    mock_session = MagicMock(spec=requests.Session)
    # This allows the .update() call in BaseAPIClient.__init__ to actually modify it,
    # and the spread operator (**self._session.headers) in .request() to work correctly.
    mock_session.headers = {}

    # Mock the request method on the session instance
    mock_session.request = MagicMock(spec=requests.Session.request)

    # Patch the Session constructor to return our mock instance
    mocker.patch("requests.Session", return_value=mock_session)
    return mock_session


@pytest.fixture
def base_client(mock_auth: MagicMock, mock_requests_session: MagicMock) -> BaseAPIClient:
    """Provide a BaseAPIClient instance with mocked Session and Auth."""
    # The mock_requests_session fixture already patches the constructor
    client = BaseAPIClient(auth=mock_auth)
    # Ensure the client is actually using the mocked session
    assert client._session is mock_requests_session
    return client


@pytest.fixture
def mock_response(mocker: MockerFixture) -> MagicMock:
    """Factory fixture to create mock requests.Response objects."""

    def _create(
        status_code: int = 200,
        json_data: dict | None = None,
        text_data: str | None = None,
        ok: bool = True,
        content: bytes | None = None,
        reason: str | None = None,
        raise_for_status: Exception | None = None,
    ) -> MagicMock:
        response = MagicMock(spec=requests.Response)
        response.status_code = status_code
        response.ok = ok
        response.reason = reason or ("OK" if ok else "Error")
        response.text = text_data or ""

        # Determine content based on inputs
        effective_content = content
        if effective_content is None:
            if json_data is not None:
                try:
                    # Try to serialize properly for more realistic content
                    effective_content = bytes(json.dumps(json_data), "utf-8")
                except TypeError:
                    effective_content = bytes(str(json_data), "utf-8")  # Fallback
            elif text_data is not None:
                effective_content = bytes(text_data, "utf-8")
            else:
                effective_content = b""
        response.content = effective_content

        # Configure .json() method
        if json_data is not None:
            response.json.return_value = json_data
        else:
            # --- FIX: Provide all args to JSONDecodeError ---
            # Use the real json.JSONDecodeError for the side effect
            response.json.side_effect = json.JSONDecodeError(
                "Mock JSON decode error",
                doc=response.text,  # Pass the text that failed to decode
                pos=0,  # Position of the error
            )

        # Mock raise_for_status if needed
        if raise_for_status:
            response.raise_for_status.side_effect = raise_for_status

        return response

    return _create


# --- Tests ---


def test_base_client_initialization(
    base_client: BaseAPIClient,
    mock_auth: MagicMock,
    mock_requests_session: MagicMock,
) -> None:
    """Test client stores auth and config, sets up session headers."""
    assert base_client.auth == mock_auth
    assert base_client.base_url == config.API_BASE_URL.rstrip("/")
    assert base_client.notion_version == config.NOTION_VERSION
    assert base_client.timeout == config.REQUEST_TIMEOUT
    assert base_client._session is mock_requests_session

    # Verify that the session's headers dictionary contains the common headers
    # after BaseAPIClient.__init__ has run (which happens in the base_client fixture).
    actual_session_headers = base_client._session.headers
    assert isinstance(actual_session_headers, dict)  # Verify it's the dict we expect

    # Check for expected keys and values
    assert actual_session_headers.get("Notion-Version") == config.NOTION_VERSION
    assert actual_session_headers.get("Content-Type") == "application/json"
    assert actual_session_headers.get("Accept") == "application/json"
    assert actual_session_headers.get("User-Agent") == "Nebula-Orion (Betelgeuse Module)"

    # We don't check for Authorization here, as it's added per-request, not to session headers.
    assert "Authorization" not in actual_session_headers


def test_base_client_init_raises_on_bad_auth_type(mocker: MockerFixture) -> None:
    """Test TypeError is raised if auth object is not APITokenAuth."""
    bad_auth = object()  # Not an APITokenAuth instance
    with pytest.raises(TypeError, match="Unsupported authentication type"):
        BaseAPIClient(auth=bad_auth)  # type: ignore


def test_request_successful_get(
    base_client: BaseAPIClient,
    mock_requests_session: MagicMock,
    mock_response: MagicMock,
    mock_auth: MagicMock,
) -> None:
    """Test a successful GET request."""
    path = "/v1/users/me"
    expected_response_data = {"object": "user", "id": "bot-id"}
    mock_resp = mock_response(status_code=200, json_data=expected_response_data, ok=True)
    mock_requests_session.request.return_value = mock_resp

    response_data = base_client.request(method=constants.GET, path=path)

    # --- Verification Change ---
    # 1. Verify the mock was called once
    mock_requests_session.request.assert_called_once()
    # 2. Get the actual call arguments
    call_args, call_kwargs = mock_requests_session.request.call_args
    # 3. Assert individual arguments
    assert call_kwargs.get("method") == constants.GET
    assert call_kwargs.get("url") == f"{base_client.base_url}{path}"
    assert call_kwargs.get("params") is None
    assert call_kwargs.get("json") is None
    assert call_kwargs.get("timeout") == base_client.timeout
    # 4. Check essential headers within the passed headers dictionary
    actual_headers = call_kwargs.get("headers", {})
    auth_headers = mock_auth.get_auth_headers.return_value
    assert actual_headers.get("Authorization") == auth_headers["Authorization"]
    assert actual_headers.get("Notion-Version") == base_client.notion_version
    assert actual_headers.get("Accept") == "application/json"
    assert actual_headers.get("User-Agent") is not None  # Check presence

    # 5. Assert the response data is correct
    assert response_data == expected_response_data


# tests/betelgeuse/api/test_base_api.py

# ... (imports and fixtures) ...


def test_request_successful_post_with_data(
    base_client: BaseAPIClient,
    mock_requests_session: MagicMock,
    mock_response: MagicMock,
    mock_auth: MagicMock,
) -> None:
    """Test a successful POST request with a JSON body."""
    path = "/v1/databases/db-id/query"
    request_data = {"filter": {"property": "Status", "select": {"equals": "Done"}}}
    expected_response_data = {"object": "list", "results": []}
    mock_resp = mock_response(status_code=200, json_data=expected_response_data, ok=True)
    mock_requests_session.request.return_value = mock_resp

    response_data = base_client.request(
        method=constants.POST,
        path=path,
        json_data=request_data,
    )

    # --- Verification Change ---
    # 1. Verify the mock was called once
    mock_requests_session.request.assert_called_once()
    # 2. Get the actual call arguments
    call_args, call_kwargs = mock_requests_session.request.call_args
    # 3. Assert individual arguments
    assert call_kwargs.get("method") == constants.POST
    assert call_kwargs.get("url") == f"{base_client.base_url}{path}"
    assert call_kwargs.get("params") is None
    assert call_kwargs.get("json") == request_data  # Check body
    assert call_kwargs.get("timeout") == base_client.timeout
    # 4. Check essential headers
    actual_headers = call_kwargs.get("headers", {})
    auth_headers = mock_auth.get_auth_headers.return_value
    assert actual_headers.get("Authorization") == auth_headers["Authorization"]
    assert actual_headers.get("Notion-Version") == base_client.notion_version
    assert actual_headers.get("Content-Type") == "application/json"  # Important for POST

    # 5. Assert the response data is correct
    assert response_data == expected_response_data


def test_request_successful_no_content_204(
    base_client: BaseAPIClient,
    mock_requests_session: MagicMock,
    mock_response: MagicMock,
) -> None:
    """Test handling of successful 204 No Content response."""
    path = "/v1/blocks/block-id"
    mock_resp = mock_response(status_code=204, ok=True, content=b"")  # No body
    mock_requests_session.request.return_value = mock_resp

    response_data = base_client.request(method=constants.DELETE, path=path)

    mock_requests_session.request.assert_called_once()  # Verify request made
    assert response_data == {}  # Expect empty dict for no content


def test_request_raises_notion_api_error_known_format(
    base_client: BaseAPIClient,
    mock_requests_session: MagicMock,
    mock_response: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test raising NotionAPIError for error responses with valid Notion JSON."""
    path = "/v1/pages/not-found"
    error_data = {
        "object": "error",
        "status": 404,
        "code": "object_not_found",
        "message": "Could not find page.",
    }
    mock_resp = mock_response(status_code=404, json_data=error_data, ok=False)
    mock_requests_session.request.return_value = mock_resp
    caplog.set_level(logging.WARNING)

    with pytest.raises(NotionAPIError) as excinfo:
        base_client.request(method=constants.GET, path=path)

    mock_requests_session.request.assert_called_once()
    assert excinfo.value.status_code == 404
    assert excinfo.value.error_code == "object_not_found"
    assert excinfo.value.message == "Could not find page."
    # Check log message
    assert "Notion API Error received" in caplog.text
    assert "Status=404" in caplog.text
    assert "Code=object_not_found" in caplog.text


def test_request_raises_notion_api_error_unknown_format(
    base_client: BaseAPIClient,
    mock_requests_session: MagicMock,
    mock_response: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test raising NotionAPIError for error responses with non-JSON body."""
    path = "/v1/gateway_timeout"
    error_text = "<html><body>Gateway Timeout</body></html>"
    mock_resp = mock_response(status_code=504, text_data=error_text, ok=False)
    # Ensure .json() call inside the handler raises an error
    mock_resp.json.side_effect = requests.exceptions.JSONDecodeError("mock", "", 0)
    mock_requests_session.request.return_value = mock_resp
    caplog.set_level(logging.WARNING)

    with pytest.raises(NotionAPIError) as excinfo:
        base_client.request(method=constants.GET, path=path)

    mock_requests_session.request.assert_called_once()
    assert excinfo.value.status_code == 504
    assert excinfo.value.error_code == "unknown_error_format"
    assert error_text in excinfo.value.message  # Check original text included
    # Check log message
    assert "Failed to parse Notion API error response" in caplog.text
    assert "Status: 504" in caplog.text
    assert error_text in caplog.text


def test_request_raises_notion_request_error_on_network_issue(
    base_client: BaseAPIClient,
    mock_requests_session: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test raising NotionRequestError on requests.RequestException."""
    path = "/v1/network/error"
    network_error = requests.exceptions.Timeout("Connection timed out")
    mock_requests_session.request.side_effect = network_error
    caplog.set_level(logging.ERROR)

    with pytest.raises(NotionRequestError) as excinfo:
        base_client.request(method=constants.GET, path=path)

    mock_requests_session.request.assert_called_once()
    assert f"HTTP Request failed: {network_error}" in str(excinfo.value)
    # Check underlying exception is chained
    assert excinfo.value.__cause__ is network_error
    # Check log message
    assert "HTTP Request failed" in caplog.text
    assert str(network_error) in caplog.text


def test_request_raises_betelgeuse_error_on_invalid_path(
    base_client: BaseAPIClient,
    mock_requests_session: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test raising BetelgeuseError if path doesn't start with '/'."""
    invalid_path = "v1/missing/slash"
    caplog.set_level(logging.ERROR)

    with pytest.raises(BetelgeuseError, match="Invalid API path format"):
        base_client.request(method=constants.GET, path=invalid_path)

    mock_requests_session.request.assert_not_called()  # Should fail before request
    assert f"API path should start with '/', got: {invalid_path}" in caplog.text


def test_request_raises_betelgeuse_error_on_success_decode_error(
    base_client: BaseAPIClient,
    mock_requests_session: MagicMock,
    mock_response: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test BetelgeuseError on JSONDecodeError for a 2xx response."""
    path = "/v1/success/bad/json"
    mock_resp = mock_response(
        status_code=200,
        ok=True,
        text_data="<invalid json>",
        content=b"<invalid json>",
    )
    # Ensure .json() raises the error
    decode_error = requests.exceptions.JSONDecodeError("mock decode", "", 0)
    mock_resp.json.side_effect = decode_error
    mock_requests_session.request.return_value = mock_resp
    caplog.set_level(logging.ERROR)

    with pytest.raises(
        BetelgeuseError,
        match="Failed to decode successful API response JSON",
    ):
        base_client.request(method=constants.GET, path=path)

    mock_requests_session.request.assert_called_once()
    assert "Failed to decode successful API response JSON" in caplog.text
    assert "<invalid json>" in caplog.text
