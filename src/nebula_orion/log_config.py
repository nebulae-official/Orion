"""Log configuration for the Nebula Orion application.

This module provides centralized logging configuration for the entire application.
It sets up console and file handlers, custom formatters, and configures log levels.
Other modules should import and use this configuration.
"""

from __future__ import annotations

import logging
import logging.config
import sys
from pathlib import Path

# Default log format
DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Default log levels
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_CONSOLE_LEVEL = "INFO"
DEFAULT_FILE_LEVEL = "DEBUG"

# Log file settings
DEFAULT_LOG_DIR = "logs"
DEFAULT_LOG_FILENAME = "nebula_orion.log"


def get_log_file_path() -> str:
    """Get the path to the log file, creating directory if needed.

    Returns:
        The full path to the log file.

    """
    log_dir = Path(DEFAULT_LOG_DIR)
    if not log_dir.exists():
        log_dir.mkdir(parents=True)

    return str(log_dir / DEFAULT_LOG_FILENAME)


def configure_logging(
    log_level: str | None = None,
    console_level: str | None = None,
    file_level: str | None = None,
    log_format: str | None = None,
    date_format: str | None = None,
) -> None:
    """Configure logging for the application.

    Args:
        log_level: Overall log level (default: from env or INFO)
        console_level: Console handler log level (default: from env or INFO)
        file_level: File handler log level (default: from env or DEBUG)
        log_format: Log format string (default: from env or predefined format)
        date_format: Date format string (default: from env or predefined format)

    """
    # Get configuration defaults
    log_level = log_level or DEFAULT_LOG_LEVEL
    console_level = console_level or DEFAULT_CONSOLE_LEVEL
    file_level = file_level or DEFAULT_FILE_LEVEL
    log_format = log_format or DEFAULT_LOG_FORMAT
    date_format = date_format or DEFAULT_DATE_FORMAT

    # Create a dict config
    config_dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": log_format,
                "datefmt": date_format,
            },
        },
        "handlers": {
            "console": {
                "level": console_level,
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
            },
            "file": {
                "level": file_level,
                "formatter": "standard",
                "class": "logging.FileHandler",
                "filename": get_log_file_path(),
                "mode": "a",
            },
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": True,
            },
            "nebula_orion": {
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": False,
            },
        },
    }

    # Apply the configuration
    logging.config.dictConfig(config_dict)


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the given name.

    Args:
        name: The name of the logger

    Returns:
        A configured logger instance

    """
    return logging.getLogger(name)
