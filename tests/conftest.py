"""
Global test configuration and fixtures for TMA Framework tests.
"""

import asyncio
import tempfile
import logging

import pytest
from loguru import logger
from telethon.sessions import StringSession
from tma_test_framework.mtproto_client import UserInfo, ChatInfo, MessageInfo

# Import fixtures from tests.fixtures modules
# Pytest requires explicit imports for fixtures to be discovered
# Import order matters: more specific fixtures should be imported first
# to avoid conflicts with generic ones

# Config data fixtures (no conflicts)
from tests.fixtures.config import *  # noqa: F401, F403

# General data fixtures (includes valid_config - this is the main one)
from tests.fixtures.data_fixtures import (  # noqa: F401
    valid_config_data as valid_config_data_from_data,
    valid_config,  # Main valid_config fixture
)

# MiniAppApi fixtures
from tests.fixtures.miniapp_api import *  # noqa: F401, F403

# MTProto client fixtures
from tests.fixtures.mtproto_client import *  # noqa: F401, F403

# Other component fixtures (they use valid_config from data_fixtures)
# Import only non-conflicting fixtures
from tests.fixtures.miniapp_ui import *  # noqa: F401, F403
from tests.fixtures.base_miniapp import (  # noqa: F401
    base_miniapp_with_config,
    base_miniapp_urls,
    invalid_urls,
)


# Configure loguru to work with pytest caplog
# Use a sink that sends loguru logs to standard logging
def loguru_sink(message):
    """Sink that redirects loguru logs to standard logging for caplog."""
    # Map loguru levels to logging levels
    level_map = {
        "TRACE": logging.DEBUG,
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "SUCCESS": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    # Get the record from the message
    record = message.record

    # Get standard logging level
    log_level = level_map.get(record["level"].name, logging.INFO)

    # Get logger name
    logger_name = record.get("name", "loguru")

    # Create LogRecord for standard logging
    log_record = logging.LogRecord(
        name=logger_name,
        level=log_level,
        pathname=str(record.get("file", {}).path)
        if hasattr(record.get("file", None), "path")
        else "",
        lineno=record.get("line", 0),
        msg=str(record["message"]),
        args=(),
        exc_info=record.get("exception"),
    )

    # Send to standard logging
    std_logger = logging.getLogger(logger_name)
    std_logger.handle(log_record)


# Remove default loguru handler and add our sink
logger.remove()
logger.add(loguru_sink, format="{message}", serialize=False)


@pytest.fixture(scope="function")
def event_loop():
    """
    Create an instance of the default event loop for the test.

    Changed scope from "session" to "function" for better compatibility
    with pytest-xdist parallel execution. Each worker needs its own event loop.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture
def mock_telegram_client(mocker):
    """Create a mock Telegram client."""
    client = mocker.AsyncMock()
    client.is_user_authorized.return_value = True
    client.connect = mocker.AsyncMock()
    client.disconnect = mocker.AsyncMock()
    client.get_me = mocker.AsyncMock()
    client.get_entity = mocker.AsyncMock()
    client.send_message = mocker.AsyncMock()
    client.get_messages = mocker.AsyncMock()
    client.get_messages.return_value = []
    return client


# mock_telegram_user, mock_telegram_chat, and mock_telegram_message
# are already imported from tests.fixtures.mtproto_client
# No need to redefine them here


@pytest.fixture
def mock_http_client(mocker):
    """Create a mock HTTP client."""
    client = mocker.AsyncMock()
    client.get = mocker.AsyncMock()
    client.post = mocker.AsyncMock()
    client.put = mocker.AsyncMock()
    client.delete = mocker.AsyncMock()
    return client


@pytest.fixture
def mock_playwright_browser(mocker):
    """Create a mock Playwright browser."""
    browser = mocker.AsyncMock()
    browser.close = mocker.AsyncMock()
    browser.new_page = mocker.AsyncMock()
    return browser


@pytest.fixture
def mock_playwright_page(mocker):
    """Create a mock Playwright page."""
    page = mocker.AsyncMock()
    page.goto = mocker.AsyncMock()
    page.close = mocker.AsyncMock()
    page.screenshot = mocker.AsyncMock()
    page.evaluate = mocker.AsyncMock()
    page.locator = mocker.AsyncMock()
    page.wait_for_selector = mocker.AsyncMock()
    page.click = mocker.AsyncMock()
    page.fill = mocker.AsyncMock()
    return page


@pytest.fixture
def mock_playwright_element(mocker):
    """Create a mock Playwright element."""
    element = mocker.AsyncMock()
    element.click = mocker.AsyncMock()
    element.fill = mocker.AsyncMock()
    element.text_content = mocker.AsyncMock()
    element.get_attribute = mocker.AsyncMock()
    element.is_visible = mocker.AsyncMock()
    element.is_enabled = mocker.AsyncMock()
    return element


@pytest.fixture
def mock_string_session():
    """Create a mock StringSession."""
    session = StringSession("test_session_string")
    return session


@pytest.fixture
def mock_sqlite_session(mocker):
    """Create a mock SQLiteSession."""
    session = mocker.MagicMock()
    session.save = mocker.MagicMock()
    return session


# Test data factories
class TestDataFactory:
    """Factory for creating test data."""

    @staticmethod
    def create_user_info(**kwargs) -> UserInfo:
        """Create UserInfo with default values."""
        defaults = {
            "id": 123456789,
            "first_name": "Test User",
            "username": "test_user",
            "last_name": "Test",
            "phone": "+1234567890",
            "is_verified": True,
            "is_premium": False,
        }
        defaults.update(kwargs)
        return UserInfo(**defaults)  # type: ignore[arg-type]

    @staticmethod
    def create_chat_info(**kwargs) -> ChatInfo:
        """Create ChatInfo with default values."""
        defaults = {
            "id": 987654321,
            "title": "Test Chat",
            "username": "test_chat",
            "type": "group",
            "is_verified": False,
        }
        defaults.update(kwargs)
        return ChatInfo(**defaults)  # type: ignore[arg-type]

    @staticmethod
    def create_message_info(**kwargs) -> MessageInfo:
        """Create MessageInfo with default values."""
        defaults = {
            "id": 111222333,
            "chat": TestDataFactory.create_chat_info(),
            "date": "2023-10-20T10:00:00Z",
            "text": "Test message",
            "from_user": TestDataFactory.create_user_info(),
            "reply_to": None,
            "media": None,
        }
        defaults.update(kwargs)
        return MessageInfo(**defaults)  # type: ignore[arg-type]


@pytest.fixture
def test_data_factory():
    """Provide test data factory."""
    return TestDataFactory


# Async test helpers
@pytest.fixture
async def async_mock(mocker):
    """Create an async mock."""
    return mocker.AsyncMock()


# Error simulation fixtures
@pytest.fixture
def mock_connection_error():
    """Mock connection error."""
    return ConnectionError("Connection failed")


@pytest.fixture
def mock_timeout_error():
    """Mock timeout error."""
    return asyncio.TimeoutError("Operation timed out")


@pytest.fixture
def mock_telegram_error():
    """Mock Telegram API error."""
    from telethon.errors import FloodWaitError

    return FloodWaitError(60)


# Performance testing fixtures
@pytest.fixture
def performance_timer():
    """Timer for performance testing."""
    import time

    start_time = time.perf_counter()
    yield lambda: time.perf_counter() - start_time
