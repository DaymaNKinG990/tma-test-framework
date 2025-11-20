"""
Fixtures for MiniAppUI testing.
"""

from pytest import fixture
from playwright.async_api import Browser, Page

from src.mini_app.ui import MiniAppUI
from src.config import Config
from tests.fixtures.base_miniapp import _get_base_config_data


@fixture
def valid_config() -> Config:
    """Create a valid Config instance."""
    return Config(**_get_base_config_data())


@fixture
def mock_playwright(mocker):
    """Create a mock Playwright instance."""
    playwright = mocker.MagicMock()
    playwright.chromium = mocker.MagicMock()
    playwright.chromium.launch = mocker.AsyncMock()
    return playwright


@fixture
def mock_browser(mocker):
    """Create a mock Browser instance."""
    browser = mocker.AsyncMock(spec=Browser)
    browser.close = mocker.AsyncMock()
    browser.new_page = mocker.AsyncMock()
    return browser


@fixture
def mock_page(mocker):
    """Create a mock Page instance."""
    page = mocker.AsyncMock(spec=Page)
    page.click = mocker.AsyncMock()
    page.fill = mocker.AsyncMock()
    page.hover = mocker.AsyncMock()
    page.dblclick = mocker.AsyncMock()
    page.check = mocker.AsyncMock()
    page.uncheck = mocker.AsyncMock()
    page.select_option = mocker.AsyncMock()
    page.wait_for_selector = mocker.AsyncMock()
    page.wait_for_load_state = mocker.AsyncMock()
    page.screenshot = mocker.AsyncMock()
    page.query_selector = mocker.AsyncMock()
    page.locator = mocker.MagicMock()
    page.set_extra_http_headers = mocker.AsyncMock()
    page.set_input_files = mocker.AsyncMock()
    page.keyboard = mocker.MagicMock()
    page.keyboard.press = mocker.AsyncMock()
    page.keyboard.type = mocker.AsyncMock()
    page.evaluate = mocker.AsyncMock()
    page.title = mocker.AsyncMock(return_value="Test Page")
    page.url = "https://example.com/app"

    # Mock locator methods
    mock_locator = mocker.MagicMock()
    mock_locator.scroll_into_view_if_needed = mocker.AsyncMock()
    page.locator.return_value = mock_locator

    # Mock element for query_selector
    mock_element = mocker.MagicMock()
    mock_element.text_content = mocker.AsyncMock(return_value="Test text")
    mock_element.get_attribute = mocker.AsyncMock(return_value="test-value")
    page.query_selector.return_value = mock_element

    return page


@fixture
def miniapp_ui_with_config(valid_config):
    """Create MiniAppUI with valid config."""
    return MiniAppUI("https://example.com/app", valid_config)


@fixture
def miniapp_ui_with_browser(miniapp_ui_with_config, mock_browser, mock_page):
    """Create MiniAppUI with browser and page set up."""
    miniapp_ui_with_config.browser = mock_browser
    miniapp_ui_with_config.page = mock_page
    return miniapp_ui_with_config


@fixture
def mock_async_playwright(mock_playwright, mock_browser, mock_page):
    """Create a mock async_playwright context manager."""

    async def async_playwright_mock():
        playwright_instance = mock_playwright
        playwright_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_page.return_value = mock_page
        return playwright_instance

    return async_playwright_mock


# Test data
@fixture
def selectors():
    """Various CSS selectors for testing."""
    return [
        "#submit",
        ".btn-primary",
        '[data-testid="input"]',
        "invalid",  # For error testing
    ]


@fixture
def keys():
    """Various keyboard keys for testing."""
    return [
        "Enter",
        "Tab",
        "Escape",
        "ArrowDown",
    ]


@fixture
def attributes():
    """Various HTML attributes for testing."""
    return [
        "value",
        "href",
        "disabled",
        "class",
    ]
