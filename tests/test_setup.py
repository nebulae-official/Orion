# tests/test_setup.py
from __future__ import annotations

import importlib.metadata
import logging

import pytest

# Import items from the top-level package
import nebula_orion

# --- Version Test ---


def test_version_consistency() -> None:
    """Check that __version__ matches the installed package version."""
    try:
        # Get the installed package version using importlib.metadata
        installed_version = importlib.metadata.version("nebula-orion")
    except importlib.metadata.PackageNotFoundError:
        pytest.skip("Package nebula-orion not installed (requires 'pip install -e .')")

    # Compare with the version defined in __init__.py
    assert nebula_orion.__version__ is not None
    assert nebula_orion.__version__ == installed_version
    assert len(nebula_orion.__version__) > 0  # Basic sanity check


def test_package_exposes_correctly() -> None:
    """Test that key items are exposed in the top-level __all__."""
    assert hasattr(nebula_orion, "__version__")
    assert hasattr(nebula_orion, "setup_logging")
    assert hasattr(nebula_orion, "logger")
    assert hasattr(nebula_orion, "get_logger")
    # Check they are also in __all__ if defined (good practice)
    if hasattr(nebula_orion, "__all__"):
        assert "setup_logging" in nebula_orion.__all__
        assert "__version__" in nebula_orion.__all__
        assert "logger" in nebula_orion.__all__
        assert "get_logger" in nebula_orion.__all__


def test_logger_instance_type() -> None:
    """Check that the exposed logger is a logging.Logger instance."""
    assert isinstance(nebula_orion.logger, logging.Logger)
    assert nebula_orion.logger.name == nebula_orion.log_config.LOGGER_NAME
