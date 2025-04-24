"""Test cases for the core Nebula Orion functionality."""

import logging
import shutil
import subprocess
import sys
from pathlib import Path

from nebula_orion import __version__, hello
from nebula_orion.log_config import (
    DEFAULT_LOG_DIR,
    configure_logging,
    get_log_file_path,
    get_logger,
)
from nebula_orion.main import main


def test_hello() -> None:
    """Test that hello() returns the expected greeting message."""
    expected = "Hello from nebula-orion! Welcome to the Nebula Orion project."
    assert hello() == expected


def test_version_consistency() -> None:
    """Test that version is consistent across project files."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent

    # Read version from Makefile
    makefile_version = None
    makefile_content = (project_root / "Makefile").open().read()
    for line in makefile_content.split("\n"):
        if line.startswith("version :="):
            makefile_version = line.split(":=")[1].strip()
            break

    # Read version from pyproject.toml
    pyproject_version = None
    pyproject_content = (project_root / "pyproject.toml").open().read()
    for line in pyproject_content.split("\n"):
        if line.strip().startswith("version = "):
            pyproject_version = line.split("=")[1].strip().strip('"')
            break

    # Compare versions
    assert __version__ == makefile_version, (
        f"Version mismatch between __init__.py ({__version__}) "
        f"and Makefile ({makefile_version})"
    )
    assert __version__ == pyproject_version, (
        f"Version mismatch between __init__.py ({__version__}) "
        f"and pyproject.toml ({pyproject_version})"
    )


def test_logging_configuration() -> None:
    """Test that logging is configured correctly."""
    # Configure logging with default settings
    configure_logging()

    # Check root logger configuration
    root_logger = logging.getLogger()
    assert root_logger.level == logging.INFO

    # Verify handlers are configured on root logger
    root_handlers = root_logger.handlers
    assert any(isinstance(h, logging.StreamHandler) for h in root_handlers), (
        "Console handler not found"
    )
    assert any(isinstance(h, logging.FileHandler) for h in root_handlers), (
        "File handler not found"
    )

    # Verify log file exists
    log_file = Path(get_log_file_path())
    assert log_file.exists(), "Log file was not created"
    assert log_file.is_file(), "Log file path is not a file"


def test_logger_output() -> None:
    """Test that logger properly writes messages."""
    # Configure logging
    configure_logging()
    logger = get_logger("test_output_logger")

    # Test messages
    test_msg = "Test log message"
    logger.info(test_msg)

    # Read the log file and verify the message was written
    log_file = Path(get_log_file_path())
    log_content = log_file.read_text()
    assert test_msg in log_content, "Test message not found in log file"


def test_log_directory_creation() -> None:
    """Test that the log directory is created if it doesn't exist."""
    # Remove the logs directory if it exists
    log_dir = Path(DEFAULT_LOG_DIR)
    if log_dir.exists():
        shutil.rmtree(log_dir)

    # Get log file path (should create directory)
    log_path = get_log_file_path()

    # Verify directory was created
    assert log_dir.exists(), "Log directory was not created"
    assert log_dir.is_dir(), "Log directory is not a directory"

    # Clean up
    shutil.rmtree(log_dir)


def test_main_function() -> None:
    """Test the main function with logging configuration."""
    # Remove existing log file if it exists
    log_dir = Path(DEFAULT_LOG_DIR)
    if log_dir.exists():
        shutil.rmtree(log_dir)

    # Configure logging first
    configure_logging()

    # Run main function
    main()

    # Verify log file contains expected message
    log_file = Path(get_log_file_path())
    assert log_file.exists(), "Log file was not created"
    log_content = log_file.read_text()
    assert "Hello from nebula-orion!" in log_content, "Expected log message not found"

    # Clean up
    shutil.rmtree(log_dir)


def test_main_script_execution() -> None:
    """Test the main script execution through command line."""
    # Configure logging first
    configure_logging()

    # Run main through command line
    result = subprocess.run(
        [sys.executable, "-m", "nebula_orion.main"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "Main script execution failed"
