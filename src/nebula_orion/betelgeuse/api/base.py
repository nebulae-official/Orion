from __future__ import annotations

from typing import Any

import requests  # Import the HTTP library

# Use absolute imports
from nebula_orion import get_logger
from nebula_orion.betelgeuse import config, errors
from nebula_orion.betelgeuse.auth import (
    token as auth_token_module,
)  # Import specific module

log = get_logger(__name__)


class BaseAPIClient:
    """Handles low-level HTTP communication with the Notion API."""

    def __init__(
        self,
        auth: auth_token_module.APITokenAuth,  # Use specific auth type for now
        base_url: str = config.API_BASE_URL,
        notion_version: str = config.NOTION_VERSION,
        timeout: int = config.REQUEST_TIMEOUT,
    ) -> None:
        """Initialize the base API client.

        Args:
            auth: An authentication handler object (e.g., APITokenAuth).
            base_url: The base URL for the Notion API.
            notion_version: The Notion API version string.
            timeout: Default request timeout in seconds.

        """
        if not isinstance(auth, auth_token_module.APITokenAuth):
            # Simple type check, could be more robust if supporting multiple auth types
            msg = "Unsupported authentication type provided."
            raise TypeError(msg)

        self.auth = auth
        self.base_url: str = base_url.rstrip("/")  # Ensure no trailing slash
        self.notion_version: str = notion_version
        self.timeout: int = timeout
        # Use a session for connection pooling and potential header persistence
        self._session = requests.Session()
        # Set common headers on the session
        self._session.headers.update(self._get_common_headers())

        log.debug(
            "BaseAPIClient initialized. Base URL: %s, Version: %s, Timeout: %ds",
            self.base_url,
            self.notion_version,
            self.timeout,
        )

    def _get_common_headers(self) -> dict[str, str]:
        """Return headers common to all requests (excluding auth)."""
        # Auth headers will be retrieved per request if needed, or set on session
        return {
            "Notion-Version": self.notion_version,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Nebula-Orion (Betelgeuse Module)",  # Identify client
        }

    def request(
        self,
        method: str,
        path: str,
        query_params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an authenticated request to the Notion API.

        Args:
            method: HTTP method (e.g., constants.GET, constants.POST).
            path: API endpoint path (e.g., "/v1/pages/{id}"). Should start with '/'.
            query_params: Dictionary of URL query parameters.
            json_data: Dictionary of data to send as JSON body (for POST/PATCH).

        Returns:
            The JSON response from the Notion API as a dictionary.
            Returns an empty dictionary for successful responses with no body (e.g., 204).

        Raises:
            NotionRequestError: If the request fails due to network issues, timeouts etc.
            NotionAPIError: If the Notion API returns an error response (e.g., 4xx, 5xx).
            BetelgeuseError: For other library-specific issues during request setup.

        """
        if not path.startswith("/"):
            log.exception("API path should start with '/', got: %s", path)
            # Or adjust path: path = f"/{path}"
            msg = f"Invalid API path format: {path}"
            raise errors.BetelgeuseError(msg)

        request_url: str = f"{self.base_url}{path}"
        # Get fresh auth headers for each request in case token can be refreshed
        auth_headers: dict[str, str] = self.auth.get_auth_headers()
        # Combine session headers (common) with per-request auth headers
        headers: dict[str, str] = {**self._session.headers, **auth_headers}

        log.debug("Making API request: %s %s", method.upper(), request_url)
        if query_params:
            log.debug("Query Params: %s", query_params)
        if json_data:
            # Avoid logging sensitive data in request body unless DEBUG level is very verbose
            log.debug("Request Body Keys: %s", list(json_data.keys()))
        try:
            response: requests.Response = self._session.request(
                method=method,
                url=request_url,
                headers=headers,  # Pass combined headers
                params=query_params,
                json=json_data,
                timeout=self.timeout,
            )

            log.debug(
                "API Response: Status Code: %d, Reason: %s",
                response.status_code,
                response.reason,
            )

            # Check for HTTP errors (4xx, 5xx)
            if not response.ok:
                # Attempt to parse Notion's specific error format
                try:
                    error_data: dict[str, Any] = response.json()
                    api_error_code = error_data.get("code", "unknown_api_code")
                    api_error_message = error_data.get("message", "No message provided.")
                    log.warning(
                        "Notion API Error received: Status=%d Code=%s Message=%s",
                        response.status_code,
                        api_error_code,
                        api_error_message,
                    )
                    raise errors.NotionAPIError(
                        status_code=response.status_code,
                        error_code=api_error_code,
                        message=api_error_message,
                    )
                except (
                    requests.exceptions.JSONDecodeError,
                    KeyError,
                    TypeError,
                ) as json_e:
                    # Handle cases where error response is not the expected JSON format
                    error_text = response.text or "No response body"
                    log.warning(
                        "Failed to parse Notion API error response (Status: %d). Body: %s",
                        response.status_code,
                        error_text[:200],  # Log truncated body
                        exc_info=False,  # Don't need json parsing stack trace usually
                    )
                    raise errors.NotionAPIError(
                        status_code=response.status_code,
                        error_code="unknown_error_format",
                        message=f"Unknown error format. Response body: {error_text[:200]}...",
                    ) from json_e  # Chain the exception

            # Handle successful responses
            # Return empty dict for 204 No Content or other success codes with no body
            if response.status_code == 204 or not response.content:
                log.debug("Received success response with no content body.")
                return {}

            # Attempt to parse successful JSON response
            try:
                response_json: dict[str, Any] = response.json()
                # Optionally log parts of success response at DEBUG level
                # log.debug("Success response keys: %s", list(response_json.keys()))
                return response_json
            except requests.exceptions.JSONDecodeError as json_e:
                log.exception(
                    "Failed to decode successful API response JSON. Status: %d, Body: %s",
                    response.status_code,
                    response.text[:200],  # Include decoding error details
                )
                # This indicates an issue with the API or our expectation
                raise errors.BetelgeuseError(
                    f"Failed to decode successful API response JSON: {response.text[:200]}...",
                ) from json_e

        except requests.exceptions.RequestException as req_e:
            # Handle network errors, timeouts, etc. from the requests library
            log.exception("HTTP Request failed: %s", req_e)
            raise errors.NotionRequestError(f"HTTP Request failed: {req_e}") from req_e
