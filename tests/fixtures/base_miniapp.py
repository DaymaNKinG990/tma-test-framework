"""
Fixtures for BaseMiniApp testing.
"""

from pytest import fixture

from tma_test_framework.config import Config
from tma_test_framework.mini_app.base import BaseMiniApp


def _get_base_config_data() -> dict:
    """Get base config data for creating Config instances."""
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session_string_123456789",
        "timeout": 30,
        "retry_count": 3,
        "retry_delay": 1.0,
        "log_level": "DEBUG",
    }


@fixture
def valid_config() -> Config:
    """Create a valid Config instance."""
    return Config(**_get_base_config_data())


@fixture
def base_miniapp_urls():
    """Valid URLs for BaseMiniApp testing."""
    return [
        "https://example.com/app",
        "https://t.me/mybot/app?start=123",
        "http://localhost:8080",
        "https://mybot.telegram.app/start",
    ]


@fixture
def invalid_urls():
    """Invalid URLs for BaseMiniApp testing."""
    return [
        None,  # TypeError expected
        123,  # TypeError expected
        [],  # TypeError expected
    ]


@fixture
def base_miniapp_with_config(valid_config):
    """Create BaseMiniApp with valid config."""
    return BaseMiniApp("https://example.com/app", valid_config)


@fixture
def base_miniapp_without_config():
    """Create BaseMiniApp without config (will try to create default Config)."""
    # Note: This will fail because Config() requires api_id and api_hash
    # We'll test this in the test itself
    pass
