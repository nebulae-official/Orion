# nebula_orion/betelgeuse/api/base.py
"""Base client for making raw HTTP requests to the Notion API.

Handles authentication headers, request execution, and basic error parsing.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import requests

# Use absolute imports
from nebula_orion.betelgeuse import config
from nebula_orion.betelgeuse.errors import NotionAPIError, NotionRequestError
from nebula_orion.log_config import get_logger

if TYPE_CHECKING:
    from nebula_orion.betelgeuse.auth.token import (
        APITokenAuth,
    )

logger = get_logger("Betelgeuse")


class BaseAPIClient:
    """Handles low-level HTTP communication with the Notion API."""

    def __init__(
        self,
        auth: APITokenAuth,  # Start with specific auth, could be more generic later
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
        logger.info(
            "Initializing BaseAPIClient for URL: %s, Version: %s",
            base_url,
            notion_version,
        )
        self.auth = auth
        self.base_url = base_url.rstrip("/")  # Ensure no trailing slash
        self.notion_version = notion_version
        self.timeout = timeout
        self._session = (
            requests.Session()
        )  # Use a session for potential connection pooling
        logger.debug("Requests session created.")

    def _get_common_headers(self) -> dict[str, str]:
        """Return headers common to all requests."""
        logger.debug("Generating common request headers.")
        headers = {
            "Notion-Version": self.notion_version,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        auth_headers = self.auth.get_auth_headers()
        headers.update(auth_headers)
        # Avoid logging sensitive headers like Authorization directly
        logger.debug(
            "Common headers generated (Authorization header present but not logged)."
        )
        return headers

    def request(
        self,
        method: str,
        path: str,
        query_params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an authenticated request to the Notion API.

        Args:
            method: HTTP method (e.g., "GET", "POST", "PATCH").
            path: API endpoint path (e.g., "/v1/pages" or "/v1/databases/{id}").
            query_params: Dictionary of URL query parameters.
            json_data: Dictionary of data to send as JSON body (for POST/PATCH).

        Returns:
            The JSON response from the Notion API as a dictionary.

        Raises:
            NotionRequestError: If the request fails due to network issues, timeouts.
            NotionAPIError: If the Notion API returns an error response (e.g., 4xx).

        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = self._get_common_headers()

        # Log request details (be careful with sensitive data in json_data if applicable)
        log_params = query_params if query_params else {}
        log_data = json_data if json_data else {}
        logger.info("Sending API request: %s %s", method, url)
        logger.debug(
            "Request details - Headers: %s, Params: %s, JSON Body: %s",
            {
                k: v for k, v in headers.items() if k != "Authorization"
            },  # Don't log auth
            log_params,
            log_data,  # Consider masking sensitive parts if necessary
        )

        try:
            response = self._session.request(
                method=method,
                url=url,
                headers=headers,
                params=query_params,
                json=json_data,
                timeout=self.timeout,
            )
            logger.debug("Received response: Status Code %s", response.status_code)

            # Check for Notion API specific errors (usually JSON format)
            if not response.ok:
                try:
                    error_data = response.json()
                    error_code = error_data.get("code", "unknown")
                    error_message = error_data.get(
                        "message", "No error message provided."
                    )
                    logger.error(
                        "Notion API Error: Status=%s, Code=%s, Message=%s",
                        response.status_code,
                        error_code,
                        error_message,
                    )
                    raise NotionAPIError(
                        status_code=response.status_code,
                        error_code=error_code,
                        message=error_message,
                    ) from None
                except (requests.exceptions.JSONDecodeError, KeyError) as e:
                    # If error response isn't JSON or lacks expected keys
                    error_text = response.text or "Unknown error structure."
                    logger.error(
                        "Notion API Error: Status=%s, Could not parse error response: %s",
                        response.status_code,
                        error_text,
                        exc_info=True,
                    )
                    raise NotionAPIError(
                        status_code=response.status_code,
                        error_code="unknown_error_format",
                        message=error_text,
                    ) from e

            # For successful requests, attempt to return JSON, handle potential empty body
            # Return empty dict for success responses with no body (e.g., 204 No Content)
            logger.info(
                "API request successful: %s %s - Status %s",
                method,
                url,
                response.status_code,
            )
            response_json = response.json() if response.content else {}
            logger.debug(
                "Response JSON: %s", response_json
            )  # Log successful data at debug
            return response_json

        except requests.exceptions.RequestException as e:
            # Catch potential network errors, timeouts, etc. from the requests library
            msg = f"HTTP Request failed: {e}"
            logger.error(
                "Notion Request Error during %s %s: %s",
                method,
                url,
                msg,
                exc_info=True,
            )
            raise NotionRequestError(msg) from e
