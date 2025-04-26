from __future__ import annotations

# Use absolute imports
from nebula_orion import get_logger
from nebula_orion.betelgeuse import config
from nebula_orion.betelgeuse.api.base import BaseAPIClient
from nebula_orion.betelgeuse.auth import token as auth_token_module
from nebula_orion.betelgeuse.errors import AuthenticationError

log = get_logger(__name__)


class NotionClient:
    """The main client for interacting with the Notion API via Betelgeuse.

    Provides high-level methods corresponding to major Notion API functionalities.
    Handles authentication and initializes the underlying API request client.
    """

    def __init__(self, auth_token: str | None = None) -> None:
        """Initialize the Notion Client.

        Args:
            auth_token: Your Notion integration token (starting with 'secret_').
                        If None, it will attempt to use the value from the
                        NOTION_API_TOKEN environment variable.

        Raises:
            AuthenticationError: If no valid authentication token is provided or found.
            TypeError: If an unsupported authentication object type is used internally.

        """
        log.info("Initializing NotionClient...")
        try:
            # Initialize the authentication handler (currently only API Token)
            # The APITokenAuth constructor handles env var lookup if auth_token is None
            self.auth = auth_token_module.APITokenAuth(token=auth_token)
            log.debug("Authentication handler initialized.")
        except AuthenticationError:
            # Log implicitly done within APITokenAuth, re-raise
            raise
        except Exception as e:
            # Catch unexpected errors during auth setup
            log.exception("Unexpected error during authentication setup.")
            raise AuthenticationError("Failed to set up authentication.") from e

        try:
            # Initialize the low-level API client, passing the auth handler
            self._api_client = BaseAPIClient(
                auth=self.auth,
                base_url=config.API_BASE_URL,
                notion_version=config.NOTION_VERSION,
                timeout=config.REQUEST_TIMEOUT,
            )
            log.debug("Base API client initialized.")
        except Exception as e:
            # Catch unexpected errors during base client setup
            log.exception("Unexpected error during BaseAPIClient initialization.")
            # Wrap in a library error, though AuthenticationError might also fit
            raise AuthenticationError("Failed to initialize API client.") from e

        # In future iterations, specific API endpoint groups (pages, databases)
        # might be initialized here, e.g.:
        # self.pages = PagesAPI(self._api_client)
        # self.databases = DatabasesAPI(self._api_client)
        log.info("NotionClient initialized successfully.")

    def __repr__(self) -> str:
        """Provides a helpful representation of the client."""
        # Avoid leaking sensitive info like the token
        return f"<NotionClient(api_version='{config.NOTION_VERSION}')>"

    # --- Placeholder for Iteration 2 Methods ---
    # def retrieve_page(self, page_id: str) -> Page: ...
    # def retrieve_database(self, database_id: str) -> Database: ...
    # def query_database(self, database_id: str, ...) -> Iterator[Page]: ...
