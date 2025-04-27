# src/nebula_orion/betelgeuse/client.py
from __future__ import annotations

from collections.abc import Iterator  # Added Type

# Standard library imports first
from typing import Any

# Then dependencies
from pydantic import ValidationError

# Then local package imports (absolute)
from nebula_orion import get_logger
from nebula_orion.betelgeuse import config, constants
from nebula_orion.betelgeuse.api.base import BaseAPIClient
from nebula_orion.betelgeuse.auth import token as auth_token_module

# Import specific block types for the factory mapping
from nebula_orion.betelgeuse.blocks import (  # Import other block types as they are created
    BulletedListItemBlock,
    CalloutBlock,
    Heading1Block,
    Heading2Block,
    Heading3Block,
    NumberedListItemBlock,
    ParagraphBlock,
    QuoteBlock,
    ToDoBlock,
    ToggleBlock,
)
from nebula_orion.betelgeuse.errors import (
    AuthenticationError,
    BetelgeuseError,
    NotionAPIError,
    NotionRequestError,
)

# Import the Pydantic models
from nebula_orion.betelgeuse.models import Block, Database, Page  # Added Block

log = get_logger(__name__)

# --- Block Type Mapping (Factory Pattern) ---
# Maps the 'type' string from the API to our Pydantic Block subclasses
# Add more entries here as you implement more block types
BLOCK_TYPE_MAP: dict[str, type[Block]] = {
    "paragraph": ParagraphBlock,
    "heading_1": Heading1Block,
    "heading_2": Heading2Block,
    "heading_3": Heading3Block,
    "callout": CalloutBlock,
    "quote": QuoteBlock,
    "bulleted_list_item": BulletedListItemBlock,
    "numbered_list_item": NumberedListItemBlock,
    "to_do": ToDoBlock,
    "toggle": ToggleBlock,
    # "image": ImageBlock, # Example for future
    # ... add mappings for all block types you model ...
}


def _parse_block_data(block_data: dict[str, Any]) -> Block:
    """Parse raw block data dictionary into the appropriate Block model instance.

    Uses the BLOCK_TYPE_MAP to find the correct Pydantic model based on the
    'type' field in the input data. Falls back to the base Block model if the
    specific type is not found or validation fails for the specific type.

    Args:
        block_data: A dictionary representing a single block from the Notion API.

    Returns:
        An instance of a Block subclass (e.g., ParagraphBlock) or the base Block
        if the specific type is unknown/unsupported or validation fails.

    Raises:
        BetelgeuseError: If basic block validation (e.g., base Block model) fails.

    """
    block_type = block_data.get("type")
    block_id = block_data.get("id", "unknown_id")

    if not block_type:
        log.exception("Block data missing 'type' field for ID: %s", block_id)
        # Or raise an error? For now, try base parsing.
        block_type = "unknown"  # Treat as unknown

    model_class = BLOCK_TYPE_MAP.get(block_type)

    if model_class:
        try:
            # Attempt to parse using the specific model
            return model_class.model_validate(block_data)
        except ValidationError as e:
            log.warning(
                "Validation failed for specific block type '%s' (ID: %s). "
                "Falling back to base Block model. Error: %s",
                block_type,
                block_id,
                e,
                exc_info=False,
            )
            # Fall through to base Block parsing on specific model validation failure

    # Fallback for unknown types or specific validation failures
    log.debug(
        "Parsing block type '%s' (ID: %s) with base Block model.",
        block_type,
        block_id,
    )
    try:
        # Base Block model might still capture common fields
        # It will ignore the type-specific field (e.g., 'paragraph') if not defined
        return Block.model_validate(block_data)
    except ValidationError as e:
        # If even base validation fails, something is fundamentally wrong
        log.exception("Failed to parse base block data for ID %s: %s", block_id, e)
        msg = f"Failed to parse base block data for ID {block_id}"
        raise BetelgeuseError(msg) from e


class NotionClient:
    """The main client for interacting with the Notion API via Betelgeuse.

    (Docstring remains the same)
    """

    def __init__(self, auth_token: str | None = None) -> None:
        """Initialize the Notion Client.

        (Code remains the same as Iteration 2)
        """
        log.info("Initializing NotionClient...")
        try:
            self.auth = auth_token_module.APITokenAuth(token=auth_token)
            log.debug("Authentication handler initialized.")
        except AuthenticationError:
            raise
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

    # --- Page Methods (from Iteration 2) ---
    def retrieve_page(self, page_id: str) -> Page:
        """Retrieve a Page object using its ID."""
        # (Code remains the same as Iteration 2)
        log.info("Retrieving page with ID: %s", page_id)
        path = f"/v1/pages/{page_id}"
        try:
            response_data = self._api_client.request(method=constants.GET, path=path)
            page = Page.model_validate(response_data)
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
            raise
        except Exception as e:
            log.exception("Unexpected error retrieving page: %s", page_id)
            msg = f"Unexpected error retrieving page {page_id}"
            raise BetelgeuseError(msg) from e

    # --- Database Methods (from Iteration 2) ---
    def retrieve_database(self, database_id: str) -> Database:
        """Retrieves a Database object using its ID."""
        # (Code remains the same as Iteration 2)
        log.info("Retrieving database with ID: %s", database_id)
        path = f"/v1/databases/{database_id}"
        try:
            response_data = self._api_client.request(method=constants.GET, path=path)
            database = Database.model_validate(response_data)
            log.debug("Successfully retrieved and parsed database: %s", database.id)
            return database
        except ValidationError as e:
            log.exception(
                "Failed to validate Database response (ID: %s). Errors: %s",
                database_id,
                e,
            )
            raise BetelgeuseError(
                f"Failed to parse Database response (ID: {database_id})",
            ) from e
        except (NotionAPIError, NotionRequestError) as e:
            log.warning("API or Request Error retrieving database %s: %s", database_id, e)
            raise
        except Exception as e:
            log.exception("Unexpected error retrieving database: %s", database_id)
            msg = f"Unexpected error retrieving database {database_id}"
            raise BetelgeuseError(
                msg,
            ) from e

    def query_database(
        self,
        database_id: str,
        filter_data: dict[str, Any] | None = None,
        sorts_data: list[dict[str, Any]] | None = None,
        page_size: int = 100,
    ) -> Iterator[Page]:
        """Queries a database and yields Pydantic Page objects for results."""
        # (Code remains the same as Iteration 2)
        log.info("Querying database ID: %s", database_id)
        if not 1 <= page_size <= 100:
            log.warning("page_size %d out of range (1-100), adjusting to 100.", page_size)
            page_size = 100

        path = f"/v1/databases/{database_id}/query"
        start_cursor: str | None = None
        has_more: bool = True
        page_count = 0
        total_results = 0

        request_body: dict[str, Any] = {}
        if filter_data:
            request_body["filter"] = filter_data
        if sorts_data:
            request_body["sorts"] = sorts_data

        while has_more:
            page_count += 1
            log.debug("Querying database page %d (cursor: %s)", page_count, start_cursor)
            paginated_body = request_body.copy()
            paginated_body["page_size"] = page_size
            if start_cursor:
                paginated_body["start_cursor"] = start_cursor

            try:
                response_data = self._api_client.request(
                    method=constants.POST,
                    path=path,
                    json_data=paginated_body,
                )
            except (NotionAPIError, NotionRequestError) as e:
                log.exception(
                    "API/Request error during database query (page %d, DB ID: %s): %s",
                    page_count,
                    database_id,
                    e,
                )
                raise

            if (
                not isinstance(response_data, dict)
                or response_data.get("object") != "list"
            ):
                log.exception(
                    "Unexpected response format for database query: %s",
                    type(response_data),
                )
                raise BetelgeuseError(
                    "Unexpected response format received for database query.",
                )

            results: list[dict[str, Any]] = response_data.get("results", [])
            log.debug("Received %d results on page %d.", len(results), page_count)
            for item_data in results:
                try:
                    page = Page.model_validate(item_data)
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
                        exc_info=False,
                    )
                    continue

            has_more = response_data.get("has_more", False)
            start_cursor = response_data.get("next_cursor")

        log.info(
            "Finished querying database %s. Total results yielded: %d across %d pages.",
            database_id,
            total_results,
            page_count,
        )

    # --- Block Methods (NEW for Iteration 3) ---
    def retrieve_block_children(
        self,
        block_id: str,
        page_size: int = 100,
    ) -> Iterator[Block]:
        """Retrieves Block objects that are children of the given block ID.

        Handles pagination automatically. Parses results into specific Block
        subclasses where possible (e.g., ParagraphBlock, Heading1Block) based
        on the `type` field, falling back to the base Block model for unknown types.

        Ref: https://developers.notion.com/reference/get-block-children

        Args:
            block_id: Identifier (UUID) for the block whose children are to be retrieved.
                      This can be a page ID or a block ID that supports children.
            page_size: Number of results per API request (1-100).

        Yields:
            Block: A Pydantic Block object (or subclass) for each child block.

        Raises:
            NotionAPIError: If the Notion API returns an error during any request phase.
            NotionRequestError: If any network request fails during pagination.
            BetelgeuseError: If the response format is unexpected or parsing fails severely.

        """
        log.info("Retrieving block children for block ID: %s", block_id)
        if not 1 <= page_size <= 100:
            log.warning("page_size %d out of range (1-100), adjusting to 100.", page_size)
            page_size = 100

        path = f"/v1/blocks/{block_id}/children"
        start_cursor: str | None = None
        has_more: bool = True
        page_count = 0
        total_results = 0

        while has_more:
            page_count += 1
            log.debug(
                "Retrieving block children page %d (cursor: %s)",
                page_count,
                start_cursor,
            )
            # Prepare query parameters for this specific page request
            query_params: dict[str, Any] = {"page_size": page_size}
            if start_cursor:
                query_params["start_cursor"] = start_cursor

            try:
                # Make the API request (GET for block children)
                response_data = self._api_client.request(
                    method=constants.GET,
                    path=path,
                    query_params=query_params,  # Use query_params for GET
                )
            except (NotionAPIError, NotionRequestError) as e:
                log.exception(
                    "API/Request error retrieving block children (page %d, Parent ID: %s): %s",
                    page_count,
                    block_id,
                    e,
                )
                raise  # Stop iteration and propagate the error

            if (
                not isinstance(response_data, dict)
                or response_data.get("object") != "list"
            ):
                log.exception(
                    "Unexpected response format for block children: %s",
                    type(response_data),
                )
                raise BetelgeuseError(
                    "Unexpected response format received for block children.",
                )

            results: list[dict[str, Any]] = response_data.get("results", [])
            log.debug("Received %d block results on page %d.", len(results), page_count)
            for item_data in results:
                try:
                    # Use the factory function to parse into specific block type
                    block_model = _parse_block_data(item_data)
                    yield block_model
                    total_results += 1
                except BetelgeuseError as e:
                    # Log severe parsing errors from the factory but continue if possible
                    log.exception("Failed to parse block item, skipping: %s", e)
                    continue
                except Exception:
                    # Catch unexpected errors during parsing/yielding
                    log.exception(
                        "Unexpected error processing block item %s",
                        item_data.get("id"),
                    )
                    continue  # Skip this block

            # Update pagination state for the next loop
            has_more = response_data.get("has_more", False)
            start_cursor = response_data.get("next_cursor")  # None if no more pages

        log.info(
            "Finished retrieving block children for %s. Total results yielded: %d across %d pages.",
            block_id,
            total_results,
            page_count,
        )

    def __repr__(self) -> str:
        """Provide a helpful representation of the client."""
        # (Code remains the same as Iteration 2)
        return f"<NotionClient(api_version='{config.NOTION_VERSION}')>"
