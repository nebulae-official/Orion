from __future__ import annotations

import logging
import sys

# --- Import the library ---
# Ensure your environment (e.g., activated .venv) can find the package
# Requires 'pip install -e .' to have been run in the project root
try:
    import nebula_orion
    from nebula_orion import log_config  # Access log_config constants if needed
except ImportError as e:
    print("Error: Failed to import the 'nebula_orion' library.")
    print("Please ensure:")
    print("  1. You are in the project's root directory.")
    print("  2. The virtual environment (.venv) is activated.")
    print("  3. You have installed the package in editable mode: pip install -e .[dev]")
    print(f"Original error: {e}")
    sys.exit(1)

# --- Basic Info ---
print("*" * 60)
print(" Welcome to the Nebula Orion Library Setup Check!")
print("*" * 60)
print(f"-> Library Version: {nebula_orion.__version__}")
print(f"-> Base Logger Name: {nebula_orion.log_config.LOGGER_NAME}")

# --- Setup Logging ---
print("\n-> Attempting to set up logging...")
log_file_path = nebula_orion.log_config.DEFAULT_LOG_FILE
try:
    # Use DEBUG level to see more output for this check
    nebula_orion.setup_logging(level=logging.DEBUG, log_to_file=True, log_to_console=True)
    print("   Logging setup called successfully.")
    print("   Console logging level: DEBUG (or higher)")
    print(f"   File logging enabled: Yes (Outputting to: {log_file_path})")
except Exception as e:
    print(f"   ERROR during logging setup: {type(e).__name__}: {e}")
    print("   Please check file permissions or dependencies (e.g., coloredlogs).")
    # Continue script if possible, but logging might not work fully

# --- Test Logging Output ---
print("\n-> Testing logger output...")

# Get the main library logger
main_logger = nebula_orion.logger
# Get a logger for a hypothetical module
module_logger = nebula_orion.get_logger("welcome_script")

# Log messages at different levels
main_logger.debug("This is a DEBUG message from the main logger.")
main_logger.info("This is an INFO message from the main logger.")
main_logger.warning("This is a WARNING message from the main logger.")
module_logger.info("This is an INFO message from the 'welcome_script' child logger.")
try:
    # Simulate an error
    _ = 1 / 0
except ZeroDivisionError:
    main_logger.exception(
        "This is an ERROR message (simulated).",
    )  # Log with traceback

print("\n-> Verification Steps:")
print(
    " 1. Check the CONSOLE output above for log messages (DEBUG, INFO, WARNING, ERROR).",
)
print("    You should see colored output if 'coloredlogs' is working.")
print(f" 2. Check the LOG FILE: {log_file_path}")
print(
    "    It should contain the same messages (without color) and the traceback for the error.",
)
print(" 3. Ensure the 'logs' directory was created if it didn't exist.")

print("\n" + "*" * 60)
print(" Setup check complete.")
print(" If you see SUCCESS messages and the log outputs, you're ready!")
print("*" * 60)
