#!/usr/bin/env python
# scripts/test_iter3_manual.py
from __future__ import annotations

import os
import sys

# --- Setup sys.path if running script directly ---
from pathlib import Path
from pprint import pformat

project_root = Path(__file__).resolve().parent.parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
# -------------------------------------------------

try:
    from nebula_orion import __version__, get_logger, setup_logging
    from nebula_orion.betelgeuse import (
        BetelgeuseError,
        NotionAPIError,
        NotionClient,
        NotionRequestError,
    )
    from nebula_orion.betelgeuse.auth import API_TOKEN_ENV_VAR

    # Import specific blocks if you want to check instanceof
    from nebula_orion.betelgeuse.blocks import Heading1Block, ParagraphBlock
except ImportError as e:
    print("ERROR: Failed to import library components.")
    print("Ensure you have run 'pip install -e .' in the project root.")
    print(f"Import Error: {e}")
    sys.exit(1)

# --- Configuration ---
LOG_LEVEL = "INFO"  # Use INFO or DEBUG
# --- !!! IMPORTANT !!! ---
# Set these environment variables OR fill them in directly below
NOTION_TOKEN = os.getenv(API_TOKEN_ENV_VAR)
# ID of a Block (can be a Page ID) that HAS children blocks
# Ensure your integration token has access to this parent AND its children
PARENT_BLOCK_ID = os.getenv("TEST_NOTION_PARENT_BLOCK_ID", "YOUR_PARENT_BLOCK_ID_HERE")
# -------------------------

# --- Setup Logging ---
setup_logging(level=LOG_LEVEL, log_to_console=True, log_to_file=True)
log = get_logger("manual_test_iter3")

# --- Test Execution ---
log.info("=" * 20 + f" Starting Iteration 3 Manual Test (v{__version__}) " + "=" * 20)

# --- Prerequisite Checks ---
if not NOTION_TOKEN:
    log.error(f"FATAL: {API_TOKEN_ENV_VAR} environment variable not set.")
    sys.exit(1)
if "YOUR_" in PARENT_BLOCK_ID:
    log.error(
        "FATAL: Placeholder detected for TEST_NOTION_PARENT_BLOCK_ID. "
        "Please set environment variable or edit script.",
    )
    sys.exit(1)

# --- Initialize Client ---
log.info("1. Initializing NotionClient...")
client: NotionClient | None = None
try:
    client = NotionClient(auth_token=NOTION_TOKEN)
    log.info(f"   SUCCESS: Client Initialized: {client!r}")
except Exception:
    log.exception("   FAILED: Error during client initialization.")
    sys.exit(1)

# --- Test Retrieve Block Children ---
log.info("-" * 60)
log.info(f"2. Attempting to retrieve children for Parent Block ID: {PARENT_BLOCK_ID}")
if client:
    try:
        block_iterator = client.retrieve_block_children(PARENT_BLOCK_ID, page_size=10)
        count = 0
        max_to_log = 10  # Log details for first 10 found blocks
        log.info("   Iterating through block children results...")

        for block in block_iterator:
            count += 1
            log.info(f"   --- Child Block {count} ---")
            log.info(f"     ID: {block.id}")
            log.info(f"     Type: {block.type}")
            log.info(f"     Has Children: {block.has_children}")
            log.info(
                f"     Parsed Model Type: {type(block).__name__}",
            )  # See if it parsed to specific type

            # Log specific content based on parsed type
            if isinstance(block, ParagraphBlock):
                text = "".join([rt.plain_text for rt in block.paragraph.rich_text])
                log.info(f"     Paragraph Text: '{text[:100]}...'")
            elif isinstance(block, Heading1Block):
                text = "".join([rt.plain_text for rt in block.heading_1.rich_text])
                log.info(f"     Heading 1 Text: '{text[:100]}...'")
            # Add more elif blocks for other types you want to inspect

            # Log raw data at DEBUG level if needed
            log.debug(f"    Raw Block Data:\n{pformat(block.model_dump(), indent=2)}")

            if count >= max_to_log:
                log.info(f"     (Stopping detailed log after {max_to_log} blocks)")
                # Consume rest silently to check for errors during iteration
                for _ in block_iterator:
                    pass
                break

        log.info(
            f"   SUCCESS: Finished iterating. Found {count} child blocks (logged details for up to {max_to_log}).",
        )
        if count == 0:
            log.warning(
                "   Note: Found 0 child blocks. Ensure the parent block has children and the integration has access.",
            )

    except (NotionAPIError, NotionRequestError, BetelgeuseError) as e:
        log.exception(
            f"   FAILED: Error retrieving block children: {type(e).__name__}: {e}",
        )
    except Exception:
        log.exception("   FAILED: Unexpected error retrieving block children.")
else:
    log.error("   SKIPPED: Client not initialized.")


log.info("=" * 20 + " Iteration 3 Manual Test Finished " + "=" * 20)
log.info("Check console output and log file.")
