from importlib import reload

import pytest
from pytest_mock import MockerFixture  # Import type for mocker

# Import the modules to be reloaded
from nebula_orion.betelgeuse import config, constants
from nebula_orion.betelgeuse.auth import token as auth_token_module


@pytest.fixture(autouse=True)
def clear_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure a clean environment for config tests."""
    vars_to_clear = [
        "NOTION_API_URL",
        "NOTION_VERSION",
        "NOTION_REQUEST_TIMEOUT",
        "NOTION_API_TOKEN",
    ]
    for var in vars_to_clear:
        monkeypatch.delenv(var, raising=False)
    # Ensure modules using env vars at import time are reloaded after clearing
    reload(config)
    reload(auth_token_module)


def test_config_defaults(mocker: MockerFixture) -> None:
    """Test that config uses default values when env vars are not set."""
    # Ensure os.getenv returns None for our config vars
    mocker.patch("os.getenv", lambda k, d=None: d)

    # Reload the config module to pick up the mocked getenv
    reload(config)
    reload(auth_token_module)  # Reload module using the env var name

    assert config.API_BASE_URL == constants.DEFAULT_NOTION_API_URL
    assert config.NOTION_VERSION == constants.DEFAULT_NOTION_VERSION
    assert config.REQUEST_TIMEOUT == constants.DEFAULT_TIMEOUT
    assert config.DEFAULT_AUTH_TOKEN is None  # Checks env var lookup


def test_config_from_env_vars(mocker: MockerFixture) -> None:
    """Test that config values are loaded from environment variables."""
    test_url: str = "http://localhost:1234"
    test_version: str = "2023-01-01"
    test_timeout: str = "60"
    test_token: str = "env_token_123"

    env_vars: dict[str, str] = {
        "NOTION_API_URL": test_url,
        "NOTION_VERSION": test_version,
        "NOTION_REQUEST_TIMEOUT": test_timeout,
        "NOTION_API_TOKEN": test_token,
    }

    # Patch os.getenv to return specific values for specific keys
    # Lambda type hint: Callable[[str, Optional[str]], Optional[str]]
    mocker.patch("os.getenv", lambda k, d=None: env_vars.get(k, d))

    # Reload the config module to pick up the mocked getenv
    reload(config)
    reload(auth_token_module)  # Reload module using the env var name

    assert test_url == config.API_BASE_URL
    assert test_version == config.NOTION_VERSION
    assert int(test_timeout) == config.REQUEST_TIMEOUT
    assert test_token == config.DEFAULT_AUTH_TOKEN
