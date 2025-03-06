"""Main entry point for the Nebula Orion application.

This module serves as the primary entry point for the Nebula Orion application.
It handles the initialization and orchestration of the application components.
"""

from nebula_orion import hello


def main() -> None:
    """Execute the main application logic."""
    print(hello())


if __name__ == "__main__":
    main()
