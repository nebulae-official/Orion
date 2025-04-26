from __future__ import annotations

import os
import sys

# --- Setup sys.path if running script directly ---
# This allows importing nebula_orion from the project root
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
# -------------------------------------------------

try:
    from nebula_orion import get_logger, log_config, setup_logging
    from nebula_orion.betelgeuse import (
        AuthenticationError,
        NotionAPIError,
        NotionClient,
        constants,
    )
    from nebula_orion.betelgeuse.auth import API_TOKEN_ENV_VAR
except ImportError as e:
    print("ERROR: Failed to import library components.")
    print("Ensure you have run 'pip install -e .' in the project root.")
    print(f"Import Error: {e}")
    sys.exit(1)

# --- Configuration ---
# Set desired log level for manual test (e.g., DEBUG)
LOG_LEVEL = "INFO"
# Option 1: Set token directly here (replace None) - KEEP SECRET
EXPLICIT_TOKEN: str | None = None
# Option 2: Rely on environment variable (recommended)
ENV_TOKEN = os.getenv(API_TOKEN_ENV_VAR)

# --- Setup Logging ---
# Configure logging to see output during the test
# (This assumes setup_logging itself works based on welcome script)
setup_logging(level=LOG_LEVEL, log_to_console=True, log_to_file=True)
log = get_logger("manual_test_iter1")  # Use a specific logger

# --- Test Execution ---
log.info("--- Starting Iteration 1 Manual Test ---")

# Determine token to use
test_token = EXPLICIT_TOKEN or ENV_TOKEN
if not test_token:
    msg = f"""
    TEST FAILED: No Notion API token found.
    Set the {API_TOKEN_ENV_VAR} environment variable or
    the EXPLICIT_TOKEN variable in this script.
    """
    log.exception(msg)
    sys.exit(1)

# --- Test 1: Client Initialization ---
log.info("Attempting to initialize NotionClient...")
client: NotionClient | None = None
try:
    client = NotionClient(auth_token=test_token)

    log.info(f"SUCCESS: NotionClient initialized: {client!r}")
except AuthenticationError as e:
    log.exception(
        f"TEST FAILED: AuthenticationError during initialization: {e}",
    )
    sys.exit(1)
except Exception as e:
    log.exception(
        f"TEST FAILED: Unexpected error during initialization: {e}",
    )
    sys.exit(1)

# --- Test 2: Basic API Call (Requires Client Init Success) ---
log.info("Attempting basic API call (GET /v1/users/me) to verify auth...")
if client and hasattr(client, "_api_client"):
    try:
        bot_info = client._api_client.request(method=constants.GET, path="/v1/users/me")  # type: ignore[attr-defined]
        log.info("SUCCESS: API call successful!")
        # Log relevant parts of the response at DEBUG level
        log.debug("Bot User Info Received:")
        log.debug(f"  ID: {bot_info.get('id')}")
        log.debug(f"  Name: {bot_info.get('name')}")
        log.debug(f"  Type: {bot_info.get('type')}")
        log.debug(f"  Owner Type: {bot_info.get('bot', {}).get('owner', {}).get('type')}")

        # Basic check
        if not (bot_info.get("object") == "user" and bot_info.get("type") == "bot"):
            log.warning(
                "Response structure might not be as expected, but call succeeded.",
            )

    except NotionAPIError as e:
        log.exception(
            f"TEST FAILED: NotionAPIError during API call: {e}",
        )  # No need for traceback here
        log.exception("Check if your token is valid and has access to the workspace.")
    except Exception as e:
        log.exception(f"TEST FAILED: Unexpected error during API call: {e}")
else:
    log.exception("Skipping API call test because client initialization failed.")


log.info("--- Iteration 1 Manual Test Finished ---")
log.info(f"Check console output and log file at: {log_config.DEFAULT_LOG_FILE}")
