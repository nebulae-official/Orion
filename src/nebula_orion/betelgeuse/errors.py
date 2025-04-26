"""Custom exceptions for the Betelgeuse Notion client library."""

from __future__ import annotations


class BetelgeuseError(Exception):
    """Base exception for all errors raised by the Betelgeuse library."""


class NotionAPIError(BetelgeuseError):
    """Raised when the Notion API returns an error response (e.g., 4xx, 5xx)."""

    def __init__(self, status_code: int, error_code: str, message: str) -> None:
        """Initialize the Notion API Error.

        Args:
            status_code: The HTTP status code returned by the API.
            error_code: The error code string provided by the Notion API.
            message: The error message provided by the Notion API.

        """
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        super().__init__(f"Notion API Error ({status_code} - {error_code}): {message}")


class NotionRequestError(BetelgeuseError):
    """Raised for issues during the HTTP request itself.

    Examples include network connection errors, timeouts, or DNS issues.
    Wraps the underlying exception (e.g., from the `requests` library).
    """


class AuthenticationError(BetelgeuseError):
    """Raised when authentication fails or required credentials are missing."""
