from __future__ import annotations

import logging

# --- Single source of truth for version ---
__version__ = "0.1.0"

# --- Central Logger ---
# Get the root logger for the library package.
# Child modules can access it via logging.getLogger(__name__)
# or by importing this instance.
# We don't call setup_logging here by default, let the application do it.
# But provide easy access to the setup function.
from .log_config import (  # Expose setup function and logger getter
    LOGGER_NAME,
    get_logger,
    setup_logging,
)

# Get the main library logger instance
logger = logging.getLogger(LOGGER_NAME)

# --- Optional: Basic fallback configuration ---
# If no configuration is done by the application, add a NullHandler
# to prevent "No handler found" warnings. Application should configure properly.
if not logger.hasHandlers():
    logger.addHandler(logging.NullHandler())

# --- Make key components accessible ---
from nebula_orion.betelgeuse.client import NotionClient

__all__ = [
    "NotionClient",
    "__version__",
    "get_logger",  # Expose the function to get child loggers
    "logger",  # Expose the main logger instance
    "setup_logging",  # Expose the setup function
]
