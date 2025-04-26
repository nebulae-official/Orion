from __future__ import annotations

import os
import sys

# --- Setup sys.path if running script directly ---
from pathlib import Path
from pprint import pformat  # For pretty printing dicts/objects

project_root = Path(__file__).resolve().parent.parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
# -------------------------------------------------

try:
    from nebula_orion import __version__, get_logger, log_config, setup_logging
    from nebula_orion.betelgeuse import (
        BetelgeuseError,
        Database,
        NotionAPIError,
        NotionClient,
        NotionRequestError,
        Page,
    )
    from nebula_orion.betelgeuse.auth import API_TOKEN_ENV_VAR
except ImportError as e:
    print("ERROR: Failed to import library components.")
    print("Ensure you have run 'pip install -e .' in the project root.")
    print(f"Import Error: {e}")
    sys.exit(1)

# --- Configuration ---
LOG_LEVEL = "DEBUG"  # Use INFO or DEBUG
# --- !!! IMPORTANT !!! ---
# Set these environment variables OR fill them in directly below
# You need IDs of a page and a database your integration token can access.
NOTION_TOKEN = os.getenv(API_TOKEN_ENV_VAR)
TEST_PAGE_ID = os.getenv(
    "TEST_NOTION_PAGE_ID",
    "YOUR_PAGE_ID_HERE",
)  # Replace placeholder
TEST_DB_ID = os.getenv(
    "TEST_NOTION_DATABASE_ID",
    "YOUR_DATABASE_ID_HERE",
)  # Replace placeholder
# -------------------------

# --- Setup Logging ---
setup_logging(level=LOG_LEVEL, log_to_console=True, log_to_file=True)
log = get_logger("manual_test_iter2")

# --- Test Execution ---
log.info("=" * 20 + f" Starting Iteration 2 Manual Test (v{__version__}) " + "=" * 20)

# --- Token Check ---
if not NOTION_TOKEN:
    log.error(f"FATAL: {API_TOKEN_ENV_VAR} environment variable not set.")
    sys.exit(1)
if "YOUR_" in TEST_PAGE_ID or "YOUR_" in TEST_DB_ID:
    log.warning(
        "Placeholders detected for TEST_NOTION_PAGE_ID or TEST_NOTION_DATABASE_ID. "
        "Please set environment variables or edit script.",
    )
    # Optionally exit if placeholders are required for tests below
    # sys.exit(1)

# --- Initialize Client ---
log.info("1. Initializing NotionClient...")
client: NotionClient | None = None
try:
    client = NotionClient(auth_token=NOTION_TOKEN)
    log.info(f"   SUCCESS: Client Initialized: {client!r}")
except Exception:
    log.exception("   FAILED: Error during client initialization.")
    sys.exit(1)

# --- Test Retrieve Page ---
log.info("-" * 60)
log.info(f"2. Attempting to retrieve Page ID: {TEST_PAGE_ID}")
if client and "YOUR_" not in TEST_PAGE_ID:
    try:
        page: Page = client.retrieve_page(TEST_PAGE_ID)
        log.info("   SUCCESS: Retrieved Page!")
        log.info(f"     ID: {page.id}")
        log.info(f"     Object Type: {page.object}")
        log.info(f"     Title: '{page.get_title()}'")
        log.info(f"     Parent: {page.parent}")
        log.info(f"     Archived: {page.archived}")
        log.debug(f"    Page Properties (raw): \n{pformat(page.properties, indent=4)}")
    except (NotionAPIError, NotionRequestError, BetelgeuseError) as e:
        log.exception(f"   FAILED: Error retrieving page: {type(e).__name__}: {e}")
    except Exception:
        log.exception("   FAILED: Unexpected error retrieving page.")
else:
    log.warning("   SKIPPED: Client not initialized or TEST_NOTION_PAGE_ID not set.")

# --- Test Retrieve Database ---
log.info("-" * 60)
log.info(f"3. Attempting to retrieve Database ID: {TEST_DB_ID}")
if client and "YOUR_" not in TEST_DB_ID:
    try:
        database: Database = client.retrieve_database(TEST_DB_ID)
        log.info("   SUCCESS: Retrieved Database!")
        log.info(f"     ID: {database.id}")
        log.info(f"     Object Type: {database.object}")
        log.info(f"     Title: '{database.get_title()}'")
        log.info(f"     Parent: {database.parent}")
        log.info(f"     Is Inline: {database.is_inline}")
        log.debug(
            f"    Database Properties Schema (raw): \n{pformat(database.properties, indent=4)}",
        )
    except (NotionAPIError, NotionRequestError, BetelgeuseError) as e:
        log.exception(f"   FAILED: Error retrieving database: {type(e).__name__}: {e}")
    except Exception:
        log.exception("   FAILED: Unexpected error retrieving database.")
else:
    log.warning("   SKIPPED: Client not initialized or TEST_NOTION_DATABASE_ID not set.")

# --- Test Query Database ---
log.info("-" * 60)
log.info(f"4. Attempting to query Database ID: {TEST_DB_ID} (fetching max 5 pages)")
if client and "YOUR_" not in TEST_DB_ID:
    try:
        page_iterator = client.query_database(TEST_DB_ID, page_size=5)
        count = 0
        max_to_log = 5
        log.info("   Iterating through query results...")
        for page in page_iterator:
            count += 1
            log.info(
                f"     Result {count}: Page ID={page.id}, Title='{page.get_title()}'",
            )
            if count >= max_to_log:
                log.info(f"     (Stopping log after {max_to_log} results)")
                # Consume rest of iterator silently if needed, or just break
                break
        log.info(f"   SUCCESS: Query finished. Found at least {count} pages.")
        if count == 0:
            log.warning(
                "   Note: Query returned 0 results. Ensure the database has pages.",
            )

    except (NotionAPIError, NotionRequestError, BetelgeuseError) as e:
        log.exception(f"   FAILED: Error querying database: {type(e).__name__}: {e}")
    except Exception:
        log.exception("   FAILED: Unexpected error querying database.")
else:
    log.warning("   SKIPPED: Client not initialized or TEST_NOTION_DATABASE_ID not set.")


log.info("=" * 20 + " Iteration 2 Manual Test Finished " + "=" * 20)
log.info(f"Check console output and log file at: {log_config.DEFAULT_LOG_FILE}")
