"""Main entry point for the Nebula Orion application.

This module serves as the primary entry point for the Nebula Orion application.
It handles initialization and orchestration of the Notion management components.
"""

from nebula_orion import hello
from nebula_orion.log_config import get_logger

# Create a logger for this module
logger = get_logger("Orion")


def main() -> None:
    """Execute the main application logic."""
    result = hello()
    logger.info(result)


if __name__ == "__main__":
    main()
