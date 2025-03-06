"""Nebula Orion Project.

A Python library designed to provide robust Notion workspace management capabilities
through its Betelgeuse module. It offers comprehensive tools for database management,
page operations, and workspace automation.

For additional details, configuration options, and usage examples, please refer to the
official project documentation.
#TODO: Add documentation link
"""

from nebula_orion.log_config import configure_logging, get_logger

# Initialize logging with default configuration
configure_logging()

# Create a logger for the package
logger = get_logger("Orion")

__version__ = "0.1.0"
__author__ = "Gishant Singh"
__email__ = "khiladisngh@hotmail.com"
__license__ = "MIT"


def hello() -> str:
    """Return a greeting message."""
    return "Hello from nebula-orion! Welcome to the Nebula Orion project."
