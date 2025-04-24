"""Custom exceptions for the Betelgeuse Notion client library."""

from nebula_orion.log_config import get_logger

logger = get_logger("Betelgeuse.Error")


class BetelgeuseError(Exception):
    """Base exception for all errors raised by this library."""


class NotionAPIError(BetelgeuseError):
    """Raised when the Notion API returns an error response."""

    def __init__(self, status_code: int, error_code: str, message: str) -> None:
        """Initialize the NotionAPIError with status code, error code, and message.

        Args:
            status_code (int): The HTTP status code returned by the Notion API.
            error_code (str): The specific error code returned by the Notion API.
            message (str): A descriptive error message.

        """
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        log_message = (
            f"Notion API Error created: Status={status_code}, "
            f"Code={error_code}, Message={message}"
        )
        # Log as warning since it represents an API-level failure condition
        logger.warning(log_message)
        super().__init__(f"Notion API Error ({status_code} - {error_code}): {message}")


class NotionRequestError(BetelgeuseError):
    """Raised for issues during the HTTP request itself (e.g., network issues)."""

    def __init__(self, message: str) -> None:
        """Initialize the NotionRequestError.

        Args:
            message (str): A descriptive error message.
        """
        # Log as error as it often indicates a more severe network/connectivity problem
        logger.error("Notion Request Error created: %s", message)
        super().__init__(message)


class AuthenticationError(BetelgeuseError):
    """Raised when authentication fails or is missing."""

    def __init__(self, message: str) -> None:
        """Initialize the AuthenticationError.

        Args:
            message (str): A descriptive error message.
        """
        # Log as error because it prevents any API interaction
        logger.error("Authentication Error created: %s", message)
        super().__init__(message)
