"""Test cases for the core Nebula Orion functionality."""

from pathlib import Path

from nebula_orion import __version__, hello


def test_hello() -> None:
    """Test that hello() returns the expected greeting message."""
    expected = "Hello from nebula-orion! Welcome to the Nebula Orion project."
    assert hello() == expected


def test_version_consistency() -> None:
    """Test that version is consistent across project files."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent

    # Read version from Makefile
    makefile_content = (project_root / "Makefile").open().read()
    for line in makefile_content.split("\n"):
        if line.startswith("version :="):
            makefile_version = line.split(":=")[1].strip()
            break

    # Read version from pyproject.toml
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
