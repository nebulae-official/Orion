# src/nebula_orion/log_config.py
from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# coloredlogs is now a required dependency
import coloredlogs

# Define a specific logger name for the library
LOGGER_NAME = "nebula_orion"

# Define default log formats
CONSOLE_LOG_FORMAT = "%(message)s"
FILE_LOG_FORMAT = (
    "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s"
)

# Define default log file path (e.g., logs/orion.log in project root)
DEFAULT_LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
DEFAULT_LOG_FILE = DEFAULT_LOG_DIR / "orion.log"

# --- Add this flag back ---
# Keep track if logging has been set up to prevent duplicate handlers
_logging_configured = False
# --------------------------


def setup_logging(
    level: int | str = logging.INFO,
    log_file: str | Path = DEFAULT_LOG_FILE,
    log_to_file: bool = True,
    log_to_console: bool = True,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
) -> None:
    """Configure logging for the nebula-orion library.

    Sets up console logging (colored) and optional rotating file logging.

    Args:
        level: The minimum logging level (e.g., logging.DEBUG, "INFO").
        log_file: The path to the log file.
        log_to_file: Whether to enable file logging.
        log_to_console: Whether to enable console logging.
        max_bytes: Maximum size of the log file before rotation.
        backup_count: Number of backup log files to keep.

    """
    # --- Add this check back ---
    global _logging_configured
    if _logging_configured:
        # Optionally log a debug message if called again
        # logging.getLogger(LOGGER_NAME).debug("Logging already configured.")
        return
    # ---------------------------

    logger = logging.getLogger(LOGGER_NAME)
    # Ensure level is set *before* adding handlers that might filter
    logger.setLevel(level)
    # Prevent handler duplication from upstream loggers if they exist
    logger.propagate = False

    # --- Console Handler ---
    if log_to_console:
        field_styles = coloredlogs.DEFAULT_FIELD_STYLES.copy()
        level_styles = coloredlogs.DEFAULT_LEVEL_STYLES.copy()
        # Note: coloredlogs.install potentially modifies the logger level
        # and adds handlers directly.
        coloredlogs.install(
            level=level,
            logger=logger,
            fmt=CONSOLE_LOG_FORMAT,
            stream=sys.stdout,
            field_styles=field_styles,
            level_styles=level_styles,
        )

    # --- File Handler ---
    if log_to_file:
        log_path = Path(log_file)
        try:
            log_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )
            file_formatter = logging.Formatter(FILE_LOG_FORMAT)
            file_handler = RotatingFileHandler(
                log_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
            )
            file_handler.setFormatter(file_formatter)
            # Explicitly set handler level to capture everything from logger level down
            file_handler.setLevel(level)
            logger.addHandler(file_handler)  # Add the file handler
        except OSError as e:
            # Use logger.exception to include stack trace
            msg = f"Failed to create log directory or file handler for {log_path}: {e}"
            # Log to console if possible, even if file logging failed
            logger.exception(msg)

    # --- Set flag after configuration ---
    _logging_configured = True
    # ------------------------------------


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance within the library's namespace."""
    # Ensure child loggers inherit config from the main library logger
    return logging.getLogger(f"{LOGGER_NAME}.{name}")
