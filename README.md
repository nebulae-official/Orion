# ✨ Nebula Orion: A Powerful Python Toolkit

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]() [![Documentation Status](https://img.shields.io/badge/docs-in_progress-blue.svg)]() [![PyPI version](https://img.shields.io/badge/pypi-coming_soon-orange.svg)]() [![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

> 🌌 Nebula Orion is a constellation of powerful Python modules for advanced productivity and workspace management, with Betelgeuse serving as its first and brightest star for comprehensive Notion integration.

## 📚 Table of Contents

- [✨ Features](#-features)
- [🛠️ Installation](#️-installation)
- [🚀 Quick Start (Iteration 2)](#-quick-start-iteration-2)
- [🌠 Modules](#-modules)
- [📖 Documentation](#-documentation)
- [🤝 Contributing](#-contributing)
- [🗺️ Roadmap](#️-roadmap)
- [📝 License](#-license)

## ✨ Features

Nebula Orion is built as a modular ecosystem. The first available module is **Betelgeuse**:

- 🔴 **Betelgeuse** - Notion API Integration (Reading Pages/Databases)
  - Core client (`NotionClient`) for initializing connection to the Notion API.
  - Handles API Token authentication (direct or via `NOTION_API_TOKEN` env var).
  - Provides a base API request layer (`BaseAPIClient`) using `requests`.
  - Includes custom exception classes (`NotionAPIError`, `NotionRequestError`, `AuthenticationError`, `BetelgeuseError`).
  - Configurable via environment variables.
  - Centralized logging setup (`nebula_orion.setup_logging`).
  - **New:** Pydantic models (`Page`, `Database`, `BaseObjectModel`) for parsing and validating API responses.
  - **New:** High-level methods for reading data:
      - `NotionClient.retrieve_page(page_id)`
      - `NotionClient.retrieve_database(database_id)`
      - `NotionClient.query_database(...)` with automatic pagination handling.

*(Features like reading blocks, creating/updating content, builders, sync, OAuth etc., are planned for future iterations).*

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

## 🚀 Quick Start (Iteration 2)

This demonstrates initializing the client and using the new high-level methods to read data.

```python
from __future__ import annotations

import os
import logging
from nebula_orion import setup_logging, get_logger
from nebula_orion.betelgeuse import (
    NotionClient, AuthenticationError, NotionAPIError, Page, Database
)

# --- Setup Logging ---
setup_logging(level=logging.INFO, log_to_file=False)
log = get_logger("quickstart_iter2")

# --- Get Notion Token & IDs ---
# Ensure these are set in your environment or replace placeholders
NOTION_TOKEN = os.getenv("NOTION_API_TOKEN")
DATABASE_ID = os.getenv("TEST_NOTION_DATABASE_ID", "YOUR_DATABASE_ID_HERE")
PAGE_ID = os.getenv("TEST_NOTION_PAGE_ID", "YOUR_PAGE_ID_HERE")

if not NOTION_TOKEN or "YOUR_" in DATABASE_ID or "YOUR_" in PAGE_ID:
    log.error("Error: Required environment variables (NOTION_API_TOKEN, "
              "TEST_NOTION_DATABASE_ID, TEST_NOTION_PAGE_ID) not set.")
    exit()

# --- Initialize the Client ---
log.info("Initializing NotionClient...")
try:
    client = NotionClient(auth_token=NOTION_TOKEN)
    log.info(f"Client Initialized: {client!r}")
except AuthenticationError as e:
    log.error(f"Authentication failed: {e}")
    exit()

# --- Retrieve a Specific Database ---
log.info(f"Retrieving database: {DATABASE_ID}")
try:
    db: Database = client.retrieve_database(DATABASE_ID)
    log.info(f"Successfully retrieved database: '{db.get_title()}' (ID: {db.id})")
    log.info(f"  Number of properties defined: {len(db.properties)}")
except Exception as e:
    log.error(f"Failed to retrieve database: {e}", exc_info=True)

# --- Retrieve a Specific Page ---
log.info(f"Retrieving page: {PAGE_ID}")
try:
    page: Page = client.retrieve_page(PAGE_ID)
    log.info(f"Successfully retrieved page: '{page.get_title()}' (ID: {page.id})")
    log.info(f"  Parent: {page.parent}")
except Exception as e:
    log.error(f"Failed to retrieve page: {e}", exc_info=True)

# --- Query a Database (Get first few pages) ---
log.info(f"Querying database {DATABASE_ID} for pages...")
try:
    count = 0
    max_results_to_show = 5
    # Example: Query with a simple sort (adjust property name if needed)
    sort_criteria = [{"property": "Name", "direction": "ascending"}] # Optional sort
    page_iterator = client.query_database(
        DATABASE_ID,
        sorts_data=sort_criteria,
        page_size=5 # Fetch small pages for demo
    )

    log.info("Iterating through query results:")
    for result_page in page_iterator:
        count += 1
        log.info(f"  - Result {count}: '{result_page.get_title()}' (ID: {result_page.id})")
        if count >= max_results_to_show:
            log.info(f"  (Stopping after showing {max_results_to_show} results)")
            break

    if count == 0:
        log.warning("  Query returned 0 results. Is the database populated?")
    log.info("Database query finished.")

except Exception as e:
    log.error(f"Failed during database query: {e}", exc_info=True)

```

## 🌠 Modules

Nebula Orion is designed as a constellation of specialized modules:

### Current Modules

- **🔴 Betelgeuse** - Notion API Integration (Reading API)
  - Provides core client setup, authentication, Pydantic models, and methods for reading Notion Pages and Databases.

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

### Near-term Objectives (Iteration 3 & Beyond)

- ✨ **Betelgeuse:** Implement reading Block children and parsing common block types.
- ✨ **Betelgeuse:** Introduce Pydantic models for Blocks and Rich Text components.
- ✨ **Betelgeuse:** Implement creating and updating Pages.
- ✨ **Betelgeuse:** Add helper classes/builders for constructing page/block data.
- 🧪 Enhance test coverage for new features.
- 📚 Continue building official documentation.

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
