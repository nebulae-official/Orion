# ✨ Nebula Orion: A Powerful Python Toolkit

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]() [![Tests Passing](https://img.shields.io/badge/tests-passing-brightgreen.svg)]() [![Documentation Status](https://img.shields.io/badge/docs-in_progress-blue.svg)]() [![PyPI version](https://img.shields.io/badge/pypi-coming_soon-orange.svg)]() [![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

> 🌌 Nebula Orion is a constellation of powerful Python modules for advanced productivity and workspace management, with Betelgeuse serving as its first and brightest star for comprehensive Notion integration.

## 📚 Table of Contents

- [✨ Features](#-features)
- [🛠️ Installation](#️-installation)
- [🚀 Quick Start (Iteration 3)](#-quick-start-iteration-3)
- [🌠 Modules](#-modules)
- [📖 Documentation](#-documentation)
- [🤝 Contributing](#-contributing)
- [🗺️ Roadmap](#️-roadmap)
- [📝 License](#-license)

## ✨ Features

Nebula Orion is built as a modular ecosystem. The first available module is **Betelgeuse**:

- 🔴 **Betelgeuse** - Notion API Integration (Reading Blocks)
  - Core client (`NotionClient`) for initializing connection.
  - API Token authentication (direct or `NOTION_API_TOKEN` env var).
  - Base API request layer (`BaseAPIClient`) using `requests`.
  - Custom exception classes (`NotionAPIError`, `BetelgeuseError`, etc.).
  - Configurable via environment variables.
  - Centralized logging setup (`nebula_orion.setup_logging`).
  - Pydantic models for core objects (`Page`, `Database`, `Block`, `User`, `RichText`, `FileObject`, etc.).
  - High-level methods for reading data:
      - `retrieve_page(page_id)`
      - `retrieve_database(database_id)`
      - `query_database(...)` with pagination.
  - **New:** `retrieve_block_children(block_id)` method with pagination.
  - **New:** Parsing of common block types (Paragraph, Headings, ToDo, Lists, Quote, Callout, Toggle) into specific Pydantic models. Falls back gracefully to base `Block` model for unsupported types.

*(Features like reading *all* block types, creating/updating content, builders, sync, OAuth etc., are planned for future iterations).*

## 🛠️ Installation

### Prerequisites

- Python 3.12 or higher
- `pip` or `uv` package manager

### Standard Installation (When Published)

```bash
pip install nebula-orion
```

### Development Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/nebulae-official/orion.git](https://github.com/nebulae-official/orion.git)
    cd orion
    ```
2.  Set up a virtual environment (recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate # Linux/macOS
    # or .\\.venv\\Scripts\\activate # Windows
    ```
3.  Install in editable mode with development dependencies:
    ```bash
    pip install -e .[dev]
    ```

## 🚀 Quick Start (Iteration 3)

This demonstrates initializing the client and using methods to read pages, databases, and block children.

```python
from __future__ import annotations

import os
import logging
from nebula_orion import setup_logging, get_logger
from nebula_orion.betelgeuse import (
    NotionClient, AuthenticationError, NotionAPIError, Page, Database, Block
)
# Import specific block types if you want to check for them
from nebula_orion.betelgeuse.blocks import ParagraphBlock, Heading1Block

# --- Setup Logging ---
setup_logging(level=logging.INFO, log_to_file=False)
log = get_logger("quickstart_iter3")

# --- Get Notion Token & IDs ---
# Ensure these are set in your environment or replace placeholders
NOTION_TOKEN = os.getenv("NOTION_API_TOKEN")
DATABASE_ID = os.getenv("TEST_NOTION_DATABASE_ID", "YOUR_DATABASE_ID_HERE")
# Use a Page ID known to have child blocks for the block test
PARENT_BLOCK_ID = os.getenv("TEST_NOTION_PARENT_BLOCK_ID", "YOUR_PAGE_OR_BLOCK_ID_WITH_CHILDREN")

if not NOTION_TOKEN or "YOUR_" in DATABASE_ID or "YOUR_" in PARENT_BLOCK_ID:
    log.error("Error: Required environment variables (NOTION_API_TOKEN, "
              "TEST_NOTION_DATABASE_ID, TEST_NOTION_PARENT_BLOCK_ID) not set.")
    exit()

# --- Initialize the Client ---
log.info("Initializing NotionClient...")
try:
    client = NotionClient(auth_token=NOTION_TOKEN)
    log.info(f"Client Initialized: {client!r}")
except Exception as e:
    log.error(f"Initialization failed: {e}", exc_info=True)
    exit()

# --- Example: Retrieve a Database ---
try:
    db: Database = client.retrieve_database(DATABASE_ID)
    log.info(f"Retrieved database: '{db.get_title()}'")
except Exception as e:
    log.error(f"Failed to retrieve database: {e}")

# --- Example: Query Database Pages ---
log.info(f"Querying database {DATABASE_ID}...")
try:
    page_count = 0
    for page in client.query_database(DATABASE_ID, page_size=3):
        page_count += 1
        log.info(f"  Found page {page_count}: '{page.get_title()}' (ID: {page.id})")
        if page_count >= 3: # Limit results for demo
            break
    log.info(f"Query finished. Showed first {page_count} pages.")
except Exception as e:
    log.error(f"Database query failed: {e}")

# --- Example: Retrieve Block Children ---
log.info(f"Retrieving children for block/page: {PARENT_BLOCK_ID}")
try:
    block_count = 0
    for block in client.retrieve_block_children(PARENT_BLOCK_ID, page_size=5):
        block_count += 1
        log.info(f"  Found child block {block_count}: Type='{block.type}', ID='{block.id}'")
        # Example of checking specific block type content
        if isinstance(block, ParagraphBlock):
            text_content = "".join(rt.plain_text for rt in block.paragraph.rich_text)
            log.info(f"    -> Paragraph Text: '{text_content[:50]}...'")
        elif isinstance(block, Heading1Block):
            text_content = "".join(rt.plain_text for rt in block.heading_1.rich_text)
            log.info(f"    -> Heading 1 Text: '{text_content[:50]}...'")

        if block_count >= 5: # Limit results for demo
            break
    log.info(f"Block retrieval finished. Showed first {block_count} child blocks.")
except Exception as e:
    log.error(f"Retrieving block children failed: {e}")

```

## 🌠 Modules

Nebula Orion is designed as a constellation of specialized modules:

### Current Modules

- **🔴 Betelgeuse** - Notion API Integration (Core Read API)
  - Provides client setup, authentication, Pydantic models, and methods for reading Notion Pages, Databases, and Block Children.

### Upcoming Modules

- **🔵 Rigel** - Task Scheduling & Workflow Management
- **🟡 Bellatrix** - Data Visualization & Reporting
- **🟠 Saiph** - Advanced Content Generation
- **🟣 Mintaka** - Team Collaboration Tools

## 📖 Documentation

*(Links are placeholders until documentation is built and hosted)*

- [Official Documentation](https://orion.readthedocs.io/)
- [Betelgeuse Module Guide]()
- [API Reference]()
- [Tutorials]()

## 🤝 Contributing

We love your input! Check out our [Contributing Guide](CONTRIBUTING.md) to get started.

### Development Commands

*(Assumes a Makefile exists in the project root)*

- `make install` - Set up development environment and install dependencies
- `make test` - Run the unit and integration test suite (requires env vars for integration tests)
- `make lint` - Run Ruff linter
- `make format` - Run Ruff formatter
- `make docs` - Build documentation (if configured)
- `make clean` - Clean build artifacts
- `make build` - Build the package distribution files

### Agile Development

Our project uses an agile methodology with:
- 2-week sprint cycles
- Regular sprint planning and retrospectives
- [Project board](https://github.com/nebulae-official/orion/projects)
- [Issue tracker](https://github.com/nebulae-official/orion/issues)

## 🗺️ Roadmap

### Near-term Objectives (Iteration 4 & Beyond)

- ✨ **Betelgeuse:** Implement creating and updating Pages.
- ✨ **Betelgeuse:** Implement `PageBuilder` helper class for easier page creation.
- ✨ **Betelgeuse:** Implement creating and updating Blocks.
- ✨ **Betelgeuse:** Add Pydantic models for more Block types (media, embeds, lists, etc.).
- 🧪 Enhance test coverage for write operations and builders.
- 📚 Expand official documentation with write API guides.

### Long-term Vision

The Nebula Orion ecosystem will expand to include:
- Complete Betelgeuse module (CRUD operations for all Notion objects, sync, OAuth).
- New modules (Rigel, Bellatrix, etc.).
- Cross-module integrations.
- Advanced AI-powered features.
- Enterprise capabilities.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ by Gishant Singh**

[Website](https://github.com/nebulae-official) • [Documentation](https://docs.nebulae.dev) • [GitHub](https://github.com/nebulae-official/orion)

</div>
