# nebula_orion/betelgeuse/client.py
"""The main entry point for interacting with the Notion API via Betelgeuse."""

from __future__ import annotations

from nebula_orion.betelgeuse import config
from nebula_orion.betelgeuse.api.base import BaseAPIClient

# Use absolute imports
from nebula_orion.betelgeuse.auth.token import APITokenAuth
from nebula_orion.betelgeuse.errors import AuthenticationError
from nebula_orion.log_config import get_logger

logger = get_logger("Betelgeuse")


class NotionClient:
    """A client for interacting with the Notion API.

    Provides methods corresponding to major Notion API functionalities.
    """

    def __init__(self, auth_token: str | None = None) -> None:
        """Initialize the Notion Client.

        Args:
            auth_token: Your Notion integration token. If None, it will attempt
                        to use the value from the NOTION_API_TOKEN environment
                        variable (via config/auth modules).

        Raises:
            AuthenticationError: If no authentication token is provided or found.

        """
        logger.info("Initializing NotionClient...")
        # Set up authentication - currently only supports API Token
        try:
            # Pass the token explicitly if provided,otherwise APITokenAuth
            # handles env var lookup
            self.auth = APITokenAuth(token=auth_token)
            logger.info("Authentication handler created successfully.")
        except AuthenticationError as e:
            msg = "No API token provided. Please set the NOTION_API_TOKEN environment variable."
            logger.exception(f"Authentication failed: {msg}")
            raise AuthenticationError(msg) from e

        # Initialize the low-level API client, passing the auth handler
        logger.debug("Initializing BaseAPIClient...")
        self._api_client = BaseAPIClient(
            auth=self.auth,
            base_url=config.API_BASE_URL,
            notion_version=config.NOTION_VERSION,
            timeout=config.REQUEST_TIMEOUT,
        )
        logger.info(
            "NotionClient initialized successfully with API version %s.",
            config.NOTION_VERSION,
        )

        # In future iterations, specific API modules (pages, databases, etc.)
        # would be initialized here, likely passing self._api_client to them.
        # e.g., self.pages = PagesAPI(self._api_client)
        # e.g., self.databases = DatabasesAPI(self._api_client)

    # --- Placeholder for future methods ---
    # Example of how future methods will use the _api_client
    # def retrieve_page(self, page_id: str) -> Dict[str, Any]:
    #     """Retrieves a Page object using its ID. (Placeholder)"""
    #     path = f"v1/pages/{page_id}"
    #     # In Iteration 2, this would call the low-level request method
    #     # and potentially parse the result into a Page model object.
    #     # return self._api_client.request(method="GET", path=path)
    #     print(f"Placeholder: Would request GET {path}") # Placeholder action
    #     return {"id": page_id, "object": "page", "message": "Placeholder Data"}

    def __repr__(self) -> str:
        """Return a string representation of the NotionClient.

        Returns:
            str: A string representation showing the API version.

        """
        # Provide a helpful representation, avoid leaking token
        return f"<NotionClient(api_version='{config.NOTION_VERSION}')>"
