"""
Fixtures for integration tests.
"""

from pytest import fixture


@fixture
def integration_config(valid_config):
    """Config for integration tests."""
    return valid_config


@fixture
def mock_mini_app_url():
    """Mock Mini App URL for testing."""
    return "https://example.com/mini-app"


@fixture
def mock_mini_app_url_with_start_param():
    """Mock Mini App URL with start parameter."""
    return "https://example.com/mini-app?start=test123"


@fixture
def mock_bot_username():
    """Mock bot username for testing."""
    return "test_bot"


@fixture
def mock_api_response_data():
    """Mock API response data."""
    return {"status": "ok", "data": {"key": "value"}}


@fixture
def mock_init_data():
    """Mock initData string."""
    return "user=%7B%22id%22%3A123%7D&auth_date=1698000000&hash=abc123"


@fixture
def mock_bot_token():
    """Mock bot token for initData validation."""
    return "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
