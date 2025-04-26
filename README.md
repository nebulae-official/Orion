# ✨ Nebula Orion: A Powerful Python Toolkit

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Documentation Status](https://img.shields.io/badge/docs-latest-blue.svg)]()
[![PyPI version](https://badge.fury.io/py/nebula-orion.svg)](https://badge.fury.io/py/nebula-orion)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

> 🌌 Nebula Orion is a constellation of powerful Python modules for advanced productivity and workspace management, with Betelgeuse serving as its first and brightest star for comprehensive Notion integration.

## 📚 Table of Contents

- [✨ Features](#-features)
- [🛠️ Installation](#️-installation)
- [🚀 Quick Start](#-quick-start)
- [🌠 Modules](#-modules)
- [📖 Documentation](#-documentation)
- [🤝 Contributing](#-contributing)
- [🗺️ Roadmap](#️-roadmap)
- [📝 License](#-license)

## ✨ Features

Nebula Orion is built as a modular ecosystem, with each module named after a star in the Orion constellation, focusing on specific productivity needs:

- 🔴 **Betelgeuse** - Comprehensive Notion API Integration
  - Complete Notion REST API coverage with clean Pythonic interfaces
  - Intuitive object models for pages, databases, blocks, and users
  - Powerful builder patterns for complex content creation
  - Automated synchronization between local and remote content
  - OAuth implementation for secure integration in third-party apps
  - Rich content manipulation with support for all Notion block types

## 🛠️ Installation

### Prerequisites

- Python 3.12 or higher
- UV package manager (recommended)

### Standard Installation

```bash
pip install nebula-orion
```

### Development Installation

1. Clone the repository
```bash
git clone https://github.com/nebulae-official/orion.git
cd orion
```

2. Set up the development environment
```bash
make install
```

## 🚀 Quick Start

### Using the Betelgeuse Module

```python
from __future__ import annotations

import os
import logging # Import standard logging
from nebula_orion import setup_logging, get_logger, constants
from nebula_orion.betelgeuse import NotionClient, AuthenticationError, NotionAPIError

# --- Setup Logging (Optional but Recommended) ---
# Configure logging to see output (e.g., INFO level to console)
setup_logging(level=logging.INFO, log_to_file=False) # Disable file for quick start
log = get_logger("quickstart")

# --- Get Notion Token ---
# Best practice: Use environment variables
# Ensure NOTION_API_TOKEN is set in your environment
# export NOTION_API_TOKEN="secret_YOUR_TOKEN_HERE"
# Or, less securely, define it directly:
# NOTION_TOKEN = "secret_YOUR_TOKEN_HERE"
NOTION_TOKEN = os.getenv("NOTION_API_TOKEN")

if not NOTION_TOKEN:
    log.error("Error: NOTION_API_TOKEN environment variable not set.")
    exit()

# --- Initialize the Client ---
log.info("Initializing NotionClient...")
try:
    # Pass the token directly (or omit if only using env var)
    notion_client = NotionClient(auth_token=NOTION_TOKEN)
    log.info(f"Client Initialized: {notion_client!r}")
except AuthenticationError as e:
    log.error(f"Authentication failed: {e}")
    exit()
except Exception as e:
    log.error(f"Unexpected error during initialization: {e}", exc_info=True)
    exit()

# --- Make a Basic API Call (Iteration 1 - Low Level) ---
# High-level methods like retrieve_page are not yet implemented.
# We access the internal _api_client to make a raw request for demonstration.
log.info("Making a test API call (GET /v1/users/me)...")
try:
    # Access internal client - Note: This might change in future versions!
    api_client = notion_client._api_client # type: ignore[attr-defined]

    # GET /v1/users/me endpoint retrieves info about the integration's bot user
    bot_info = api_client.request(method=constants.GET, path="/v1/users/me")

    log.info("API call successful!")
    # Process the raw dictionary response
    bot_name = bot_info.get("name", "Unknown Bot")
    bot_id = bot_info.get("id")
    log.info(f"Authenticated as bot: '{bot_name}' (ID: {bot_id})")

except NotionAPIError as e:
    log.error(f"Notion API Error: {e.status_code} - {e.error_code} - {e.message}")
except Exception as e:
    log.error(f"An unexpected error occurred during API call: {e}", exc_info=True)
```

## 🌠 Modules

Nebula Orion is designed as a constellation of specialized modules, each named after a star in the Orion constellation:

### Current Modules

- **🔴 Betelgeuse** - Notion API Integration
  - Like the red supergiant star it's named after, Betelgeuse is the first and brightest module in the Orion ecosystem, providing comprehensive Notion workspace management capabilities.

### Upcoming Modules

- **🔵 Rigel** - Task Scheduling & Workflow Management
- **🟡 Bellatrix** - Data Visualization & Reporting
- **🟠 Saiph** - Advanced Content Generation
- **🟣 Mintaka** - Team Collaboration Tools

## 📖 Documentation

- [Official Documentation](https://nebula-orion.readthedocs.io/)
- [Betelgeuse Module Guide](https://nebula-orion.readthedocs.io/modules/betelgeuse/)
- [API Reference](https://nebula-orion.readthedocs.io/api/)
- [Tutorials](https://nebula-orion.readthedocs.io/tutorials/)

## 🤝 Contributing

We love your input! Check out our [Contributing Guide](CONTRIBUTING.md) to get started.

### Development Commands

- `make test` - Run the test suite
- `make docs` - Build documentation
- `make clean` - Clean build artifacts
- `make run` - Run the application
- `make build` - Build the package

### Agile Development

Our project uses an agile methodology with:
- 2-week sprint cycles
- Regular sprint planning and retrospectives
- [Project board](https://github.com/nebulae-official/orion/projects)
- [Issue tracker](https://github.com/nebulae-official/orion/issues)

## 🗺️ Roadmap

### Near-term Objectives

- 🔴 **Betelgeuse v1.0** - Complete Notion API wrapper with all core functionality
- 📚 Comprehensive documentation and tutorials
- 🧪 Extensive test coverage and CI/CD pipeline
- 🔐 OAuth integration for third-party applications

### Long-term Vision

The Nebula Orion ecosystem will expand to include:
- New modules to handle additional productivity needs
- Cross-module integrations for seamless workflows
- Advanced AI-powered features for content generation and analysis
- Enterprise capabilities for team and organization management
- Mobile SDK for cross-platform support

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ by Gishant Singh**

[Website](https://github.com/nebulae-official) • [Documentation](https://docs.nebulae.dev) • [GitHub](https://github.com/nebulae-official/orion)

</div>
