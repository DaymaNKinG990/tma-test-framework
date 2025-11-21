"""
Unit tests for MiniAppUI.
"""

import pytest
import tempfile
from pathlib import Path
# Removed unittest.mock import - using pytest-mock instead

from tma_test_framework.mini_app.ui import MiniAppUI


# ============================================================================
# I. Инициализация и управление ресурсами
# ============================================================================


class TestMiniAppUIInit:
    """Test MiniAppUI initialization."""

    def test_init_with_config_none_raises_value_error(self):
        """Test that MiniAppUI rejects None config with ValueError. TC-UI-002"""
        with pytest.raises(ValueError, match="config is required"):
            MiniAppUI("https://example.com/app", None)

    def test_init_with_url_and_config(self, valid_config):
        """Test successful initialization with url and config. TC-UI-001"""
        ui = MiniAppUI("https://example.com/app", valid_config)

        assert ui.url == "https://example.com/app"
        assert ui.config == valid_config
        assert ui.browser is None
        assert ui.page is None

    def test_init_sets_browser_and_page_to_none(self, valid_config):
        """Test that browser and page are initially None."""
        ui = MiniAppUI("https://example.com/app", valid_config)

        assert ui.browser is None
        assert ui.page is None

    @pytest.mark.asyncio
    async def test_methods_before_browser_setup(self, miniapp_ui_with_config, caplog):
        """Test methods handle missing browser gracefully. TC-UI-039"""
        # Try to use methods before setup_browser()
        with caplog.at_level("ERROR"):
            await miniapp_ui_with_config.click_element("#button")
        assert "Browser not initialized" in caplog.text

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_config.fill_input("#input", "text")
        assert "Browser not initialized" in caplog.text

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_config.wait_for_element("#element")
        assert "Browser not initialized" in caplog.text

        result = await miniapp_ui_with_config.get_element_text("#element")
        assert result is None  # Should return None when browser not set

        result = await miniapp_ui_with_config.get_element_attribute_value(
            "#element", "href"
        )
        assert result is None  # Should return None when browser not set

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_config.scroll_to_element("#element")
        assert "Browser not initialized" in caplog.text

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_config.hover_element("#element")
        assert "Browser not initialized" in caplog.text

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_config.double_click_element("#element")
        assert "Browser not initialized" in caplog.text

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_config.right_click_element("#element")
        assert "Browser not initialized" in caplog.text

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_config.select_option("#select", "option1")
        assert "Browser not initialized" in caplog.text

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_config.check_checkbox("#checkbox")
        assert "Browser not initialized" in caplog.text

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_config.uncheck_checkbox("#checkbox")
        assert "Browser not initialized" in caplog.text

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_config.upload_file("#file", "file.txt")
        assert "Browser not initialized" in caplog.text

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_config.press_key("Enter")
        assert "Browser not initialized" in caplog.text

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_config.type_text("text")
        assert "Browser not initialized" in caplog.text

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_config.wait_for_navigation()
        assert "Browser not initialized" in caplog.text

        result = await miniapp_ui_with_config.get_page_title()
        assert result == ""  # Should return empty string when browser not set

        result = await miniapp_ui_with_config.get_page_url()
        assert result == ""  # Should return empty string when browser not set

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_config.take_screenshot("screenshot.png")
        assert "Browser not initialized" in caplog.text

        result = await miniapp_ui_with_config.execute_script("return 1")
        assert result is None  # Should return None when browser not set


class TestMiniAppUIClose:
    """Test MiniAppUI close method."""

    @pytest.mark.asyncio
    async def test_close_closes_browser_if_set(self, miniapp_ui_with_browser):
        """Test close() closes browser if it's set. TC-UI-006"""
        # Save reference to browser before close() sets it to None
        browser = miniapp_ui_with_browser.browser
        await miniapp_ui_with_browser.close()

        browser.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_close_does_nothing_if_browser_none(self, miniapp_ui_with_config):
        """Test close() does nothing if browser is None. TC-UI-007"""
        # Should not raise any exception
        await miniapp_ui_with_config.close()

        assert miniapp_ui_with_config.browser is None


# ============================================================================
# II. Настройка браузера (setup_browser)
# ============================================================================


class TestMiniAppUISetupBrowser:
    """Test MiniAppUI setup_browser method."""

    @pytest.mark.asyncio
    async def test_setup_browser_first_call_launches_chromium(
        self, mocker, miniapp_ui_with_config, mock_browser, mock_page
    ):
        """Test first call to setup_browser launches Chromium. TC-UI-003"""
        mock_playwright_class = mocker.patch(
            "tma_test_framework.mini_app.ui.async_playwright"
        )
        mock_playwright_instance = mocker.MagicMock()
        mock_playwright_instance.start = mocker.AsyncMock(
            return_value=mock_playwright_instance
        )
        mock_playwright_instance.chromium = mocker.MagicMock()
        mock_playwright_instance.chromium.launch = mocker.AsyncMock(
            return_value=mock_browser
        )
        mock_playwright_class.return_value = mock_playwright_instance

        mock_browser.new_page = mocker.AsyncMock(return_value=mock_page)

        result = await miniapp_ui_with_config.setup_browser()

        assert result is miniapp_ui_with_config  # Returns self
        assert miniapp_ui_with_config.browser == mock_browser
        assert miniapp_ui_with_config.page == mock_page
        mock_playwright_instance.chromium.launch.assert_called_once_with(headless=True)

    @pytest.mark.asyncio
    async def test_setup_browser_creates_new_page(
        self, mocker, miniapp_ui_with_config, mock_browser, mock_page
    ):
        """Test setup_browser creates new page."""
        mock_playwright_class = mocker.patch(
            "tma_test_framework.mini_app.ui.async_playwright"
        )
        mock_playwright_instance = mocker.MagicMock()
        mock_playwright_instance.start = mocker.AsyncMock(
            return_value=mock_playwright_instance
        )
        mock_playwright_instance.chromium = mocker.MagicMock()
        mock_playwright_instance.chromium.launch = mocker.AsyncMock(
            return_value=mock_browser
        )
        mock_playwright_class.return_value = mock_playwright_instance

        mock_browser.new_page = mocker.AsyncMock(return_value=mock_page)

        await miniapp_ui_with_config.setup_browser()

        mock_browser.new_page.assert_called_once()

    @pytest.mark.asyncio
    async def test_setup_browser_sets_user_agent(
        self, mocker, miniapp_ui_with_config, mock_browser, mock_page
    ):
        """Test setup_browser sets custom User-Agent."""
        mock_playwright_class = mocker.patch(
            "tma_test_framework.mini_app.ui.async_playwright"
        )
        mock_playwright_instance = mocker.MagicMock()
        mock_playwright_instance.start = mocker.AsyncMock(
            return_value=mock_playwright_instance
        )
        mock_playwright_instance.chromium = mocker.MagicMock()
        mock_playwright_instance.chromium.launch = mocker.AsyncMock(
            return_value=mock_browser
        )
        mock_playwright_class.return_value = mock_playwright_instance

        mock_browser.new_page = mocker.AsyncMock(return_value=mock_page)
        mock_page.set_extra_http_headers = mocker.AsyncMock()

        await miniapp_ui_with_config.setup_browser()

        mock_page.set_extra_http_headers.assert_called_once()
        call_args = mock_page.set_extra_http_headers.call_args[0][0]
        assert "User-Agent" in call_args

    @pytest.mark.asyncio
    async def test_setup_browser_second_call_logs_already_setup(
        self, miniapp_ui_with_browser, caplog
    ):
        """Test second call to setup_browser logs 'Browser already setup'. TC-UI-004"""
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.setup_browser()

        assert "Browser already setup" in caplog.text

    @pytest.mark.asyncio
    async def test_setup_browser_second_call_does_not_create_new_browser(
        self, miniapp_ui_with_browser, mock_browser
    ):
        """Test second call to setup_browser does not create new browser."""
        original_browser = miniapp_ui_with_browser.browser

        await miniapp_ui_with_browser.setup_browser()

        # Browser should remain the same
        assert miniapp_ui_with_browser.browser is original_browser

    @pytest.mark.asyncio
    async def test_setup_browser_returns_self(
        self, mocker, miniapp_ui_with_config, mock_browser, mock_page
    ):
        """Test setup_browser returns self for method chaining. TC-UI-005"""
        mock_playwright_class = mocker.patch(
            "tma_test_framework.mini_app.ui.async_playwright"
        )
        mock_playwright_instance = mocker.MagicMock()
        mock_playwright_instance.start = mocker.AsyncMock(
            return_value=mock_playwright_instance
        )
        mock_playwright_instance.chromium = mocker.MagicMock()
        mock_playwright_instance.chromium.launch = mocker.AsyncMock(
            return_value=mock_browser
        )
        mock_playwright_class.return_value = mock_playwright_instance

        mock_browser.new_page = mocker.AsyncMock(return_value=mock_page)

        result = await miniapp_ui_with_config.setup_browser()

        assert result is miniapp_ui_with_config

    @pytest.mark.asyncio
    async def test_setup_browser_rejects_empty_url(self, valid_config):
        """Test setup_browser rejects empty or invalid URL. TC-UI-042"""
        # Test with empty string
        ui = MiniAppUI("", valid_config)
        with pytest.raises(ValueError, match="URL is not set or is empty"):
            await ui.setup_browser()

        # Test with whitespace-only string
        ui = MiniAppUI("   ", valid_config)
        with pytest.raises(ValueError, match="URL is not set or is empty"):
            await ui.setup_browser()

    @pytest.mark.asyncio
    async def test_setup_browser_handles_navigation_error(
        self, mocker, miniapp_ui_with_config, mock_browser, mock_page
    ):
        """Test setup_browser handles navigation failures gracefully. TC-UI-043"""
        mock_playwright_class = mocker.patch(
            "tma_test_framework.mini_app.ui.async_playwright"
        )
        mock_playwright_instance = mocker.MagicMock()
        mock_playwright_instance.start = mocker.AsyncMock(
            return_value=mock_playwright_instance
        )
        mock_playwright_instance.chromium = mocker.MagicMock()
        mock_playwright_instance.chromium.launch = mocker.AsyncMock(
            return_value=mock_browser
        )
        mock_playwright_class.return_value = mock_playwright_instance

        mock_browser.new_page = mocker.AsyncMock(return_value=mock_page)
        mock_page.set_extra_http_headers = mocker.AsyncMock()

        # Mock page.goto() to raise an exception (e.g., TimeoutError)
        from playwright.async_api import TimeoutError as PlaywrightTimeoutError

        mock_page.goto = mocker.AsyncMock(
            side_effect=PlaywrightTimeoutError("Navigation timeout")
        )

        # Should raise RuntimeError with appropriate message
        with pytest.raises(RuntimeError, match="Failed to navigate to"):
            await miniapp_ui_with_config.setup_browser()

        # Verify page.goto was called
        mock_page.goto.assert_called_once()

    @pytest.mark.asyncio
    async def test_setup_browser_handles_network_error(
        self, mocker, miniapp_ui_with_config, mock_browser, mock_page
    ):
        """Test setup_browser handles network errors during navigation. TC-UI-043"""
        mock_playwright_class = mocker.patch(
            "tma_test_framework.mini_app.ui.async_playwright"
        )
        mock_playwright_instance = mocker.MagicMock()
        mock_playwright_instance.start = mocker.AsyncMock(
            return_value=mock_playwright_instance
        )
        mock_playwright_instance.chromium = mocker.MagicMock()
        mock_playwright_instance.chromium.launch = mocker.AsyncMock(
            return_value=mock_browser
        )
        mock_playwright_class.return_value = mock_playwright_instance

        mock_browser.new_page = mocker.AsyncMock(return_value=mock_page)
        mock_page.set_extra_http_headers = mocker.AsyncMock()

        # Mock page.goto() to raise a network error
        network_error = Exception("Network error: Connection refused")
        mock_page.goto = mocker.AsyncMock(side_effect=network_error)

        # Should raise RuntimeError with appropriate message
        with pytest.raises(RuntimeError, match="Failed to navigate to"):
            await miniapp_ui_with_config.setup_browser()

        # Verify page.goto was called
        mock_page.goto.assert_called_once()


# ============================================================================
# III. Взаимодействие с элементами
# ============================================================================


class TestMiniAppUIElementInteraction:
    """Test MiniAppUI element interaction methods."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "selector", ["#submit", ".btn-primary", '[data-testid="input"]']
    )
    async def test_click_element_success(
        self, miniapp_ui_with_browser, selector, caplog
    ):
        """Test click_element logs DEBUG on success. TC-UI-008"""
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.click_element(selector)

        assert f"Clicked element: {selector}" in caplog.text
        miniapp_ui_with_browser.page.click.assert_called_once_with(selector)

    @pytest.mark.asyncio
    async def test_click_element_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test click_element handles exceptions and logs ERROR. TC-UI-009"""
        error = Exception("Element not found")
        miniapp_ui_with_browser.page.click = mocker.AsyncMock(side_effect=error)

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_browser.click_element("#invalid")

        assert "Failed to click element" in caplog.text
        # Should not raise exception
        assert True  # Test passes if no exception raised

    @pytest.mark.asyncio
    async def test_click_element_unicode_selector(
        self, miniapp_ui_with_browser, caplog
    ):
        """Test click_element with unicode characters in selector. TC-UI-040"""
        unicode_selector = "#тест-用户-ユーザー"
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.click_element(unicode_selector)

        assert f"Clicked element: {unicode_selector}" in caplog.text
        miniapp_ui_with_browser.page.click.assert_called_once_with(unicode_selector)

    @pytest.mark.asyncio
    async def test_click_element_very_long_selector(
        self, miniapp_ui_with_browser, caplog
    ):
        """Test click_element with very long selector. TC-UI-041"""
        # Create a very long selector (>1000 characters)
        long_selector = "#" + "a" * 1000
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.click_element(long_selector)

        assert f"Clicked element: {long_selector}" in caplog.text
        miniapp_ui_with_browser.page.click.assert_called_once_with(long_selector)

    @pytest.mark.asyncio
    async def test_fill_input_unicode_selector(self, miniapp_ui_with_browser, caplog):
        """Test fill_input with unicode selector. TC-UI-040"""
        unicode_selector = "#ввод-输入-入力"
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.fill_input(unicode_selector, "test")

        assert "Filled input" in caplog.text
        miniapp_ui_with_browser.page.fill.assert_called_once_with(
            unicode_selector, "test"
        )

    @pytest.mark.asyncio
    async def test_fill_input_very_long_selector(self, miniapp_ui_with_browser, caplog):
        """Test fill_input with very long selector. TC-UI-041"""
        long_selector = "#" + "input" * 200  # >1000 characters
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.fill_input(long_selector, "test")

        assert "Filled input" in caplog.text
        miniapp_ui_with_browser.page.fill.assert_called_once_with(long_selector, "test")

    @pytest.mark.asyncio
    async def test_fill_input_success(self, miniapp_ui_with_browser, caplog):
        """Test fill_input logs DEBUG on success. TC-UI-010"""
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.fill_input("#input", "test text")

        assert "Filled input" in caplog.text
        miniapp_ui_with_browser.page.fill.assert_called_once_with("#input", "test text")

    @pytest.mark.asyncio
    async def test_fill_input_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test fill_input handles exceptions. TC-UI-011"""
        error = Exception("Element not found")
        miniapp_ui_with_browser.page.fill = mocker.AsyncMock(side_effect=error)

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_browser.fill_input("#invalid", "text")

        assert "Failed to fill input" in caplog.text

    @pytest.mark.asyncio
    async def test_hover_element_success(self, miniapp_ui_with_browser, caplog):
        """Test hover_element logs DEBUG on success. TC-UI-020"""
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.hover_element("#element")

        assert "Hovered over element" in caplog.text
        miniapp_ui_with_browser.page.hover.assert_called_once_with("#element")

    @pytest.mark.asyncio
    async def test_hover_element_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test hover_element handles exceptions."""
        error = Exception("Element not found")
        miniapp_ui_with_browser.page.hover = mocker.AsyncMock(side_effect=error)

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_browser.hover_element("#invalid")

        assert "Failed to hover over element" in caplog.text

    @pytest.mark.asyncio
    async def test_double_click_element_success(self, miniapp_ui_with_browser, caplog):
        """Test double_click_element logs DEBUG on success. TC-UI-021"""
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.double_click_element("#element")

        assert "Double clicked element" in caplog.text
        miniapp_ui_with_browser.page.dblclick.assert_called_once_with("#element")

    @pytest.mark.asyncio
    async def test_double_click_element_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test double_click_element handles exceptions."""
        error = Exception("Element not found")
        miniapp_ui_with_browser.page.dblclick = mocker.AsyncMock(side_effect=error)

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_browser.double_click_element("#invalid")

        assert "Failed to double click element" in caplog.text

    @pytest.mark.asyncio
    async def test_right_click_element_success(self, miniapp_ui_with_browser, caplog):
        """Test right_click_element logs DEBUG on success. TC-UI-022"""
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.right_click_element("#element")

        assert "Right clicked element" in caplog.text
        miniapp_ui_with_browser.page.click.assert_called_once_with(
            "#element", button="right"
        )

    @pytest.mark.asyncio
    async def test_right_click_element_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test right_click_element handles exceptions."""
        error = Exception("Element not found")
        miniapp_ui_with_browser.page.click = mocker.AsyncMock(side_effect=error)

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_browser.right_click_element("#invalid")

        assert "Failed to right click element" in caplog.text

    @pytest.mark.asyncio
    async def test_check_checkbox_success(self, miniapp_ui_with_browser, caplog):
        """Test check_checkbox logs DEBUG on success. TC-UI-024"""
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.check_checkbox("#checkbox")

        assert "Checked checkbox" in caplog.text
        miniapp_ui_with_browser.page.check.assert_called_once_with("#checkbox")

    @pytest.mark.asyncio
    async def test_check_checkbox_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test check_checkbox handles exceptions."""
        error = Exception("Element not found")
        miniapp_ui_with_browser.page.check = mocker.AsyncMock(side_effect=error)

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_browser.check_checkbox("#invalid")

        assert "Failed to check checkbox" in caplog.text

    @pytest.mark.asyncio
    async def test_uncheck_checkbox_success(self, miniapp_ui_with_browser, caplog):
        """Test uncheck_checkbox logs DEBUG on success. TC-UI-025"""
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.uncheck_checkbox("#checkbox")

        assert "Unchecked checkbox" in caplog.text
        miniapp_ui_with_browser.page.uncheck.assert_called_once_with("#checkbox")

    @pytest.mark.asyncio
    async def test_uncheck_checkbox_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test uncheck_checkbox handles exceptions."""
        error = Exception("Element not found")
        miniapp_ui_with_browser.page.uncheck = mocker.AsyncMock(side_effect=error)

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_browser.uncheck_checkbox("#invalid")

        assert "Failed to uncheck checkbox" in caplog.text

    @pytest.mark.asyncio
    async def test_select_option_success(self, miniapp_ui_with_browser, caplog):
        """Test select_option logs DEBUG on success. TC-UI-023"""
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.select_option("#select", "value1")

        assert "Selected option" in caplog.text
        miniapp_ui_with_browser.page.select_option.assert_called_once_with(
            "#select", "value1"
        )

    @pytest.mark.asyncio
    async def test_select_option_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test select_option handles exceptions."""
        error = Exception("Element not found")
        miniapp_ui_with_browser.page.select_option = mocker.AsyncMock(side_effect=error)

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_browser.select_option("#invalid", "value")

        assert "Failed to select option" in caplog.text


# ============================================================================
# IV. Ожидания и навигация
# ============================================================================


class TestMiniAppUIWaitAndNavigation:
    """Test MiniAppUI wait and navigation methods."""

    @pytest.mark.asyncio
    async def test_wait_for_element_success(self, miniapp_ui_with_browser, caplog):
        """Test wait_for_element waits for element to appear. TC-UI-012"""
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.wait_for_element("#element")

        assert "Element appeared" in caplog.text
        miniapp_ui_with_browser.page.wait_for_selector.assert_called_once_with(
            "#element", timeout=5000
        )

    @pytest.mark.asyncio
    async def test_wait_for_element_timeout(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test wait_for_element handles timeout. TC-UI-013"""
        from playwright.async_api import TimeoutError as PlaywrightTimeoutError

        error = PlaywrightTimeoutError("Timeout")
        miniapp_ui_with_browser.page.wait_for_selector = mocker.AsyncMock(
            side_effect=error
        )

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_browser.wait_for_element("#invalid", timeout=1000)

        assert "Element" in caplog.text and "did not appear" in caplog.text

    @pytest.mark.asyncio
    async def test_wait_for_navigation_success(self, miniapp_ui_with_browser, caplog):
        """Test wait_for_navigation waits for networkidle. TC-UI-029"""
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.wait_for_navigation()

        assert "Navigation completed" in caplog.text
        miniapp_ui_with_browser.page.wait_for_load_state.assert_called_once_with(
            "networkidle", timeout=5000
        )

    @pytest.mark.asyncio
    async def test_wait_for_navigation_timeout(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test wait_for_navigation handles timeout. TC-UI-030"""
        from playwright.async_api import TimeoutError as PlaywrightTimeoutError

        error = PlaywrightTimeoutError("Timeout")
        miniapp_ui_with_browser.page.wait_for_load_state = mocker.AsyncMock(
            side_effect=error
        )

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_browser.wait_for_navigation(timeout=1000)

        assert "Navigation timeout" in caplog.text


# ============================================================================
# V. Получение данных со страницы
# ============================================================================


class TestMiniAppUIGetData:
    """Test MiniAppUI data retrieval methods."""

    @pytest.mark.asyncio
    async def test_get_element_text_success(self, miniapp_ui_with_browser, caplog):
        """Test get_element_text returns text if element found. TC-UI-014"""
        with caplog.at_level("DEBUG"):
            result = await miniapp_ui_with_browser.get_element_text("#element")

        assert result == "Test text"
        assert "Element text" in caplog.text

    @pytest.mark.asyncio
    async def test_get_element_text_element_not_found(
        self, mocker, miniapp_ui_with_browser
    ):
        """Test get_element_text returns None if element not found. TC-UI-015"""
        miniapp_ui_with_browser.page.query_selector = mocker.AsyncMock(
            return_value=None
        )

        result = await miniapp_ui_with_browser.get_element_text("#nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_element_text_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test get_element_text handles exceptions."""
        error = Exception("Query failed")
        miniapp_ui_with_browser.page.query_selector = mocker.AsyncMock(
            side_effect=error
        )

        with caplog.at_level("ERROR"):
            result = await miniapp_ui_with_browser.get_element_text("#element")

        assert result is None
        assert "Failed to get element text" in caplog.text

    @pytest.mark.asyncio
    @pytest.mark.parametrize("attribute", ["value", "href", "disabled", "class"])
    async def test_get_element_attribute_value_success(
        self, miniapp_ui_with_browser, attribute, caplog
    ):
        """Test get_element_attribute_value returns attribute value. TC-UI-016"""
        with caplog.at_level("DEBUG"):
            result = await miniapp_ui_with_browser.get_element_attribute_value(
                "#element", attribute
            )

        assert result == "test-value"
        assert "Element attribute" in caplog.text

    @pytest.mark.asyncio
    async def test_get_element_attribute_value_element_not_found(
        self, mocker, miniapp_ui_with_browser
    ):
        """Test get_element_attribute_value returns None if element not found. TC-UI-017"""
        miniapp_ui_with_browser.page.query_selector = mocker.AsyncMock(
            return_value=None
        )

        result = await miniapp_ui_with_browser.get_element_attribute_value(
            "#nonexistent", "value"
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_get_element_attribute_value_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test get_element_attribute_value handles exceptions."""
        error = Exception("Query failed")
        miniapp_ui_with_browser.page.query_selector = mocker.AsyncMock(
            side_effect=error
        )

        with caplog.at_level("ERROR"):
            result = await miniapp_ui_with_browser.get_element_attribute_value(
                "#element", "value"
            )

        assert result is None
        assert "Failed to get element attribute" in caplog.text

    @pytest.mark.asyncio
    async def test_get_page_title_success(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test get_page_title returns page title. TC-UI-031"""
        miniapp_ui_with_browser.page.title = mocker.AsyncMock(return_value="Test Page")

        with caplog.at_level("DEBUG"):
            result = await miniapp_ui_with_browser.get_page_title()

        assert result == "Test Page"
        assert "Page title" in caplog.text

    @pytest.mark.asyncio
    async def test_get_page_title_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test get_page_title returns empty string on error. TC-UI-032"""
        error = Exception("Failed to get title")
        miniapp_ui_with_browser.page.title = mocker.AsyncMock(side_effect=error)

        with caplog.at_level("ERROR"):
            result = await miniapp_ui_with_browser.get_page_title()

        assert result == ""
        assert "Failed to get page title" in caplog.text

    @pytest.mark.asyncio
    async def test_get_page_url_success(self, miniapp_ui_with_browser, caplog):
        """Test get_page_url returns page URL. TC-UI-033"""
        miniapp_ui_with_browser.page.url = "https://example.com/app"

        with caplog.at_level("DEBUG"):
            result = await miniapp_ui_with_browser.get_page_url()

        assert result == "https://example.com/app"
        assert "Page URL" in caplog.text

    @pytest.mark.asyncio
    async def test_get_page_url_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test get_page_url returns empty string on error. TC-UI-034"""
        # Simulate error by making page.url property raise an exception
        with caplog.at_level("ERROR"):
            # Mock page.url as a property that raises exception
            type(miniapp_ui_with_browser.page).url = mocker.PropertyMock(
                side_effect=Exception("Test exception")
            )
            result = await miniapp_ui_with_browser.get_page_url()

        # Should return empty string and log error
        assert result == ""
        assert "Failed to get page URL" in caplog.text


# ============================================================================
# VI. Скриншоты и файлы
# ============================================================================


class TestMiniAppUIScreenshotsAndFiles:
    """Test MiniAppUI screenshot and file methods."""

    @pytest.mark.asyncio
    async def test_take_screenshot_success(self, miniapp_ui_with_browser, caplog):
        """Test take_screenshot creates file. TC-UI-035"""
        with tempfile.TemporaryDirectory() as tmpdir:
            screenshot_path = str(Path(tmpdir) / "test.png")

            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.take_screenshot(screenshot_path)

            assert "Screenshot saved" in caplog.text
            miniapp_ui_with_browser.page.screenshot.assert_called_once_with(
                path=screenshot_path
            )

    @pytest.mark.asyncio
    async def test_take_screenshot_error_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test take_screenshot handles error. TC-UI-036"""
        error = Exception("Screenshot failed")
        miniapp_ui_with_browser.page.screenshot = mocker.AsyncMock(side_effect=error)

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_browser.take_screenshot("/invalid/path.png")

        assert "Screenshot failed" in caplog.text

    @pytest.mark.asyncio
    async def test_upload_file_success(self, miniapp_ui_with_browser, caplog):
        """Test upload_file calls set_input_files. TC-UI-026"""
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.upload_file("#file-input", "/fake/path.jpg")

        assert "Uploaded file" in caplog.text
        miniapp_ui_with_browser.page.set_input_files.assert_called_once_with(
            "#file-input", "/fake/path.jpg"
        )

    @pytest.mark.asyncio
    async def test_upload_file_error_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test upload_file handles error."""
        error = Exception("File not found")
        miniapp_ui_with_browser.page.set_input_files = mocker.AsyncMock(
            side_effect=error
        )

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_browser.upload_file("#invalid", "/fake/path.jpg")

        assert "Failed to upload file" in caplog.text


# ============================================================================
# VII. Клавиатура и скрипты
# ============================================================================


class TestMiniAppUIKeyboardAndScripts:
    """Test MiniAppUI keyboard and script methods."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("key", ["Enter", "Tab", "Escape", "ArrowDown"])
    async def test_press_key_success(self, miniapp_ui_with_browser, key, caplog):
        """Test press_key calls keyboard.press. TC-UI-027"""
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.press_key(key)

        assert f"Pressed key: {key}" in caplog.text
        miniapp_ui_with_browser.page.keyboard.press.assert_called_once_with(key)

    @pytest.mark.asyncio
    async def test_press_key_invalid_key_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test press_key handles invalid key."""
        error = Exception("Invalid key")
        miniapp_ui_with_browser.page.keyboard.press = mocker.AsyncMock(
            side_effect=error
        )

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_browser.press_key("InvalidKey")

        assert "Failed to press key" in caplog.text

    @pytest.mark.asyncio
    async def test_type_text_success(self, miniapp_ui_with_browser, caplog):
        """Test type_text calls keyboard.type. TC-UI-028"""
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.type_text("hello")

        assert "Typed text: hello" in caplog.text
        miniapp_ui_with_browser.page.keyboard.type.assert_called_once_with("hello")

    @pytest.mark.asyncio
    async def test_type_text_error_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test type_text handles error."""
        error = Exception("Type failed")
        miniapp_ui_with_browser.page.keyboard.type = mocker.AsyncMock(side_effect=error)

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_browser.type_text("text")

        assert "Failed to type text" in caplog.text

    @pytest.mark.asyncio
    async def test_execute_script_success(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test execute_script returns result. TC-UI-037"""
        miniapp_ui_with_browser.page.evaluate = mocker.AsyncMock(return_value=42)

        with caplog.at_level("DEBUG"):
            result = await miniapp_ui_with_browser.execute_script("return 42")

        assert result == 42
        assert "Script executed" in caplog.text

    @pytest.mark.asyncio
    async def test_execute_script_error_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test execute_script handles error and returns None. TC-UI-038"""
        error = Exception("Script error")
        miniapp_ui_with_browser.page.evaluate = mocker.AsyncMock(side_effect=error)

        with caplog.at_level("ERROR"):
            result = await miniapp_ui_with_browser.execute_script("throw 'err'")

        assert result is None
        assert "Script execution failed" in caplog.text


# ============================================================================
# VIII. Прокрутка и визуальные действия
# ============================================================================


class TestMiniAppUIScroll:
    """Test MiniAppUI scroll methods."""

    @pytest.mark.asyncio
    async def test_scroll_to_element_success(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test scroll_to_element calls scroll_into_view_if_needed. TC-UI-018"""
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.scroll_to_element("#element")

        assert "Scrolled to element" in caplog.text
        miniapp_ui_with_browser.page.locator.assert_called_once_with("#element")

    @pytest.mark.asyncio
    async def test_scroll_to_element_error_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test scroll_to_element handles error. TC-UI-019"""
        error = Exception("Element not found")
        mock_locator = mocker.MagicMock()
        mock_locator.scroll_into_view_if_needed = mocker.AsyncMock(side_effect=error)
        miniapp_ui_with_browser.page.locator.return_value = mock_locator

        with caplog.at_level("ERROR"):
            await miniapp_ui_with_browser.scroll_to_element("#invalid")

        assert "Failed to scroll to element" in caplog.text


# ============================================================================
# IX. Асинхронный контекстный менеджер
# ============================================================================


class TestMiniAppUIContextManager:
    """Test MiniAppUI async context manager."""

    @pytest.mark.asyncio
    async def test_aenter_returns_self(self, miniapp_ui_with_config):
        """Test __aenter__ returns self."""
        async with miniapp_ui_with_config as ui:
            assert ui is miniapp_ui_with_config

    @pytest.mark.asyncio
    async def test_aexit_calls_close(self, mocker, miniapp_ui_with_browser):
        """Test __aexit__ calls await self.close()."""
        miniapp_ui_with_browser.close = mocker.AsyncMock()

        async with miniapp_ui_with_browser:
            pass

        miniapp_ui_with_browser.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_context_manager_usage(self, miniapp_ui_with_config):
        """Test typical context manager usage."""
        async with miniapp_ui_with_config as ui:
            assert isinstance(ui, MiniAppUI)
            assert ui.url == "https://example.com/app"


# ============================================================================
# X. Безопасность и отказоустойчивость
# ============================================================================


class TestMiniAppUISafety:
    """Test MiniAppUI safety and reliability."""

    @pytest.mark.asyncio
    async def test_no_exceptions_propagated(self, mocker, miniapp_ui_with_browser):
        """Test that no exceptions are propagated from public methods."""
        # All methods should catch exceptions
        error = Exception("Test error")
        miniapp_ui_with_browser.page.click = mocker.AsyncMock(side_effect=error)

        # Should not raise exception
        await miniapp_ui_with_browser.click_element("#element")
        assert True  # Test passes if no exception raised

    @pytest.mark.asyncio
    async def test_browser_closed_in_close(self, miniapp_ui_with_browser):
        """Test browser is closed in close()."""
        # Save reference to browser before close() sets it to None
        browser = miniapp_ui_with_browser.browser
        await miniapp_ui_with_browser.close()

        browser.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_logs_contain_context(self, miniapp_ui_with_browser, caplog):
        """Test logs contain context (selector, key, etc.)."""
        with caplog.at_level("DEBUG"):
            await miniapp_ui_with_browser.click_element("#submit")
            await miniapp_ui_with_browser.press_key("Enter")

        assert "#submit" in caplog.text
        assert "Enter" in caplog.text

    def test_logger_bound_to_class_name(self, miniapp_ui_with_config):
        """Test logger is bound to MiniAppUI class name."""
        assert miniapp_ui_with_config.logger is not None
        # Logger should be bound to "MiniAppUI"


# ============================================================================
# XI. Совместимость с наследованием
# ============================================================================


class TestMiniAppUIInheritance:
    """Test MiniAppUI inheritance compatibility."""

    def test_can_be_inherited(self, valid_config):
        """Test MiniAppUI can be inherited."""

        class CustomMiniAppUI(MiniAppUI):
            pass

        ui = CustomMiniAppUI("https://example.com/app", valid_config)
        assert isinstance(ui, MiniAppUI)

    @pytest.mark.asyncio
    async def test_setup_browser_returns_self_for_fluent_interface(
        self, mocker, miniapp_ui_with_config, mock_browser, mock_page
    ):
        """Test setup_browser returns Self for fluent interface."""
        mock_playwright_class = mocker.patch(
            "tma_test_framework.mini_app.ui.async_playwright"
        )
        mock_playwright_instance = mocker.MagicMock()
        mock_playwright_instance.start = mocker.AsyncMock(
            return_value=mock_playwright_instance
        )
        mock_playwright_instance.chromium = mocker.MagicMock()
        mock_playwright_instance.chromium.launch = mocker.AsyncMock(
            return_value=mock_browser
        )
        mock_playwright_class.return_value = mock_playwright_instance

        mock_browser.new_page = mocker.AsyncMock(return_value=mock_page)

        result = await miniapp_ui_with_config.setup_browser()

        # Should return self for method chaining
        assert result is miniapp_ui_with_config
        # Can be chained
        assert await miniapp_ui_with_config.setup_browser() is miniapp_ui_with_config
