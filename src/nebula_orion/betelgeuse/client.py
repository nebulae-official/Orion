# src/nebula_orion/betelgeuse/client.py
from __future__ import annotations

from collections.abc import Iterator

# Standard library imports first
from typing import Any

# Then dependencies
from pydantic import ValidationError

# Then local package imports (absolute)
from nebula_orion import get_logger
from nebula_orion.betelgeuse import config, constants
from nebula_orion.betelgeuse.api.base import BaseAPIClient
from nebula_orion.betelgeuse.auth import token as auth_token_module
from nebula_orion.betelgeuse.errors import (
    AuthenticationError,
    BetelgeuseError,
    NotionAPIError,
    NotionRequestError,
)

# Import the Pydantic models
from nebula_orion.betelgeuse.models import Database, Page

log = get_logger(__name__)


class NotionClient:
    """The main client for interacting with the Notion API via Betelgeuse.

    Provides high-level methods corresponding to major Notion API functionalities.
    Handles authentication and initializes the underlying API request client.
    """

    def __init__(self, auth_token: str | None = None) -> None:
        """Initialize the Notion Client.

        Args:
            auth_token: Your Notion integration token (starting with 'ntn_').
                        If None, it will attempt to use the value from the
                        NOTION_API_TOKEN environment variable.

        Raises:
            AuthenticationError: If no valid authentication token is provided or found.
            TypeError: If an unsupported authentication object type is used internally.

        """
        log.info("Initializing NotionClient...")
        try:
            self.auth = auth_token_module.APITokenAuth(token=auth_token)
            log.debug("Authentication handler initialized.")
        except AuthenticationError:
            raise  # Logged within APITokenAuth
        except Exception as e:
            log.exception("Unexpected error during authentication setup.")
            msg = "Failed to set up authentication."
            raise AuthenticationError(msg) from e

        try:
            self._api_client = BaseAPIClient(
                auth=self.auth,
                base_url=config.API_BASE_URL,
                notion_version=config.NOTION_VERSION,
                timeout=config.REQUEST_TIMEOUT,
            )
            log.debug("Base API client initialized.")
        except Exception as e:
            log.exception("Unexpected error during BaseAPIClient initialization.")
            msg = "Failed to initialize API client."
            raise AuthenticationError(msg) from e

        log.info("NotionClient initialized successfully.")

    # --- Page Methods ---
    def retrieve_page(self, page_id: str) -> Page:
        """Retrieve a Page object using its ID.

        Ref: https://developers.notion.com/reference/retrieve-a-page

        Args:
            page_id: Identifier (UUID) for the page.

        Returns:
            A Pydantic Page object representing the retrieved page.

        Raises:
            NotionAPIError: If the Notion API returns an error (e.g., 404 Not Found).
            NotionRequestError: If the network request fails.
            BetelgeuseError: If the API response cannot be parsed into a Page model.

        """
        log.info("Retrieving page with ID: %s", page_id)
        path = f"/v1/pages/{page_id}"
        try:
            response_data = self._api_client.request(method=constants.GET, path=path)
            page = Page.model_validate(response_data)  # Use Pydantic v2 method
            log.debug("Successfully retrieved and parsed page: %s", page.id)
            return page
        except ValidationError as e:
            log.exception(
                "Failed to validate Page response (ID: %s). Errors: %s",
                page_id,
                e,
            )
            msg = f"Failed to parse Page response (ID: {page_id})"
            raise BetelgeuseError(msg) from e
        except (NotionAPIError, NotionRequestError) as e:
            log.warning("API or Request Error retrieving page %s: %s", page_id, e)
            raise  # Re-raise known API/Request errors
        except Exception as e:
            log.exception("Unexpected error retrieving page: %s", page_id)
            msg = f"Unexpected error retrieving page {page_id}"
            raise BetelgeuseError(msg) from e

    # --- Database Methods ---
    def retrieve_database(self, database_id: str) -> Database:
        """Retrieve a Database object using its ID.

        Ref: https://developers.notion.com/reference/retrieve-a-database

        Args:
            database_id: Identifier (UUID) for the database.

        Returns:
            A Pydantic Database object representing the retrieved database.

        Raises:
            NotionAPIError: If the Notion API returns an error.
            NotionRequestError: If the network request fails.
            BetelgeuseError: If the API response cannot be parsed into a Database model.

        """
        log.info("Retrieving database with ID: %s", database_id)
        path = f"/v1/databases/{database_id}"
        try:
            response_data = self._api_client.request(method=constants.GET, path=path)
            database = Database.model_validate(response_data)  # Use Pydantic v2 method
            log.debug("Successfully retrieved and parsed database: %s", database.id)
            return database
        except ValidationError as e:
            log.error(
                "Failed to validate Database response (ID: %s). Errors: %s",
                database_id,
                e,
                exc_info=False,
            )
            raise BetelgeuseError(
                f"Failed to parse Database response (ID: {database_id})",
            ) from e
        except (NotionAPIError, NotionRequestError) as e:
            log.warning("API or Request Error retrieving database %s: %s", database_id, e)
            raise
        except Exception as e:
            log.exception("Unexpected error retrieving database: %s", database_id)
            raise BetelgeuseError(
                f"Unexpected error retrieving database {database_id}",
            ) from e

    def query_database(
        self,
        database_id: str,
        filter_data: dict[str, Any] | None = None,
        sorts_data: list[dict[str, Any]] | None = None,
        page_size: int = 100,  # Notion default/max is 100
    ) -> Iterator[Page]:
        """Queries a database and yields Pydantic Page objects for results, handling pagination.

        Ref: https://developers.notion.com/reference/post-database-query

        Args:
            database_id: Identifier (UUID) for the database.
            filter_data: Notion filter object structure (passed directly as JSON).
                         Ref: https://developers.notion.com/reference/post-database-query-filter
            sorts_data: Notion sorts object structure (list of sort objects).
                        Ref: https://developers.notion.com/reference/post-database-query-sort
            page_size: Number of results per API request (1-100).

        Yields:
            Page: A Pydantic Page object for each result found in the query.

        Raises:
            NotionAPIError: If the Notion API returns an error during any request phase.
            NotionRequestError: If any network request fails during pagination.
            BetelgeuseError: If the response format is unexpected or parsing fails severely.
                           Individual page parsing errors are logged as warnings by default.

        """
        log.info("Querying database ID: %s", database_id)
        if not 1 <= page_size <= 100:
            log.warning("page_size %d out of range (1-100), adjusting to 100.", page_size)
            page_size = 100

        path = f"/v1/databases/{database_id}/query"
        start_cursor: str | None = None
        has_more: bool = True
        page_count = 0
        total_results = 0

        # Construct the constant part of the request body (filter/sorts)
        request_body: dict[str, Any] = {}
        if filter_data:
            request_body["filter"] = filter_data
        if sorts_data:
            request_body["sorts"] = sorts_data

        while has_more:
            page_count += 1
            log.debug("Querying database page %d (cursor: %s)", page_count, start_cursor)
            # Prepare body for this specific page request
            paginated_body = request_body.copy()
            paginated_body["page_size"] = page_size
            if start_cursor:
                paginated_body["start_cursor"] = start_cursor

            try:
                # Make the API request (POST for queries)
                response_data = self._api_client.request(
                    method=constants.POST,
                    path=path,
                    json_data=paginated_body,
                )
            except (NotionAPIError, NotionRequestError) as e:
                log.error(
                    "API/Request error during database query (page %d, DB ID: %s): %s",
                    page_count,
                    database_id,
                    e,
                )
                raise  # Stop iteration and propagate the error

            if (
                not isinstance(response_data, dict)
                or response_data.get("object") != "list"
            ):
                log.error(
                    "Unexpected response format for database query: %s",
                    type(response_data),
                )
                msg = "Unexpected response format received for database query."
                raise BetelgeuseError(msg)

            results: list[dict[str, Any]] = response_data.get("results", [])
            log.debug("Received %d results on page %d.", len(results), page_count)
            for item_data in results:
                try:
                    # Attempt to parse each result as a Page
                    page = Page.model_validate(item_data)  # Use Pydantic v2 method
                    yield page
                    total_results += 1
                except ValidationError as e:
                    item_id = item_data.get("id", "unknown_id")
                    log.warning(
                        "Skipping item ID '%s' in DB query results (DB ID: %s) "
                        "due to validation error: %s",
                        item_id,
                        database_id,
                        e,
                        exc_info=False,  # Usually don't need full traceback for skipped items
                    )
                    continue  # Skip this invalid item

            # Update pagination state for the next loop
            has_more = response_data.get("has_more", False)
            start_cursor = response_data.get("next_cursor")  # None if no more pages

        log.info(
            "Finished querying database %s. Total results yielded: %d across %d pages.",
            database_id,
            total_results,
            page_count,
        )

    def __repr__(self) -> str:
        """Concise representation of the NotionClient instance.

        Returns:
            A string representation of the NotionClient instance.

        """
        return f"<NotionClient(api_version='{config.NOTION_VERSION}')>"
