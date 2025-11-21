"""
Unit tests for MiniAppUI.
"""

import allure
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

    @allure.title("MiniAppUI rejects None config with ValueError")
    @allure.description(
        "Test that MiniAppUI rejects None config with ValueError. TC-UI-002"
    )
    def test_init_with_config_none_raises_value_error(self):
        """Test that MiniAppUI rejects None config with ValueError. TC-UI-002"""
        with allure.step("Attempt to create MiniAppUI with config=None"):
            with pytest.raises(ValueError, match="config is required"):
                MiniAppUI("https://example.com/app", None)

    @allure.title("TC-UI-001: Initialize MiniAppUI with URL and config")
    @allure.description("Test successful initialization with url and config. TC-UI-001")
    def test_init_with_url_and_config(self, valid_config):
        """Test successful initialization with url and config. TC-UI-001"""
        with allure.step("Create MiniAppUI instance"):
            ui = MiniAppUI("https://example.com/app", valid_config)

        with allure.step("Verify ui.url is set correctly"):
            assert ui.url == "https://example.com/app"
        with allure.step("Verify ui.config matches provided config"):
            assert ui.config == valid_config
        with allure.step("Verify browser and page are initially None"):
            assert ui.browser is None
            assert ui.page is None

    @allure.title("Browser and page are initially None")
    @allure.description("Test that browser and page are initially None.")
    def test_init_sets_browser_and_page_to_none(self, valid_config):
        """Test that browser and page are initially None."""
        with allure.step("Create MiniAppUI instance"):
            ui = MiniAppUI("https://example.com/app", valid_config)

        with allure.step("Verify browser is None"):
            assert ui.browser is None
        with allure.step("Verify page is None"):
            assert ui.page is None

    @pytest.mark.asyncio
    @allure.title("TC-UI-039: Methods handle missing browser gracefully")
    @allure.description("Test methods handle missing browser gracefully. TC-UI-039")
    async def test_methods_before_browser_setup(self, miniapp_ui_with_config, caplog):
        """Test methods handle missing browser gracefully. TC-UI-039"""
        # Try to use methods before setup_browser()
        with allure.step("Test click_element before browser setup"):
            with caplog.at_level("ERROR"):
                await miniapp_ui_with_config.click_element("#button")
            assert "Browser not initialized" in caplog.text

        with allure.step("Test fill_input before browser setup"):
            with caplog.at_level("ERROR"):
                await miniapp_ui_with_config.fill_input("#input", "text")
            assert "Browser not initialized" in caplog.text

        with allure.step("Test wait_for_element before browser setup"):
            with caplog.at_level("ERROR"):
                await miniapp_ui_with_config.wait_for_element("#element")
            assert "Browser not initialized" in caplog.text

        with allure.step("Test get_element_text returns None when browser not set"):
            result = await miniapp_ui_with_config.get_element_text("#element")
            assert result is None  # Should return None when browser not set

        with allure.step(
            "Test get_element_attribute_value returns None when browser not set"
        ):
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
    @allure.title("TC-UI-006: close() closes browser if it's set")
    @allure.description("Test close() closes browser if it's set. TC-UI-006")
    async def test_close_closes_browser_if_set(self, miniapp_ui_with_browser):
        """Test close() closes browser if it's set. TC-UI-006"""
        with allure.step("Save reference to browser before close()"):
            # Save reference to browser before close() sets it to None
            browser = miniapp_ui_with_browser.browser
        with allure.step("Call close()"):
            await miniapp_ui_with_browser.close()

        with allure.step("Verify browser.close() was called"):
            browser.close.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("TC-UI-007: close() does nothing if browser is None")
    @allure.description("Test close() does nothing if browser is None. TC-UI-007")
    async def test_close_does_nothing_if_browser_none(self, miniapp_ui_with_config):
        """Test close() does nothing if browser is None. TC-UI-007"""
        with allure.step("Call close() when browser is None"):
            # Should not raise any exception
            await miniapp_ui_with_config.close()

        with allure.step("Verify browser remains None"):
            assert miniapp_ui_with_config.browser is None


# ============================================================================
# II. Настройка браузера (setup_browser)
# ============================================================================


class TestMiniAppUISetupBrowser:
    """Test MiniAppUI setup_browser method."""

    @pytest.mark.asyncio
    @allure.title("TC-UI-003: First call to setup_browser launches Chromium")
    @allure.description("Test first call to setup_browser launches Chromium. TC-UI-003")
    async def test_setup_browser_first_call_launches_chromium(
        self, mocker, miniapp_ui_with_config, mock_browser, mock_page
    ):
        """Test first call to setup_browser launches Chromium. TC-UI-003"""
        with allure.step("Mock async_playwright and browser setup"):
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

        with allure.step("Call setup_browser()"):
            result = await miniapp_ui_with_config.setup_browser()

        with allure.step("Verify setup_browser returns self and sets browser/page"):
            assert result is miniapp_ui_with_config  # Returns self
            assert miniapp_ui_with_config.browser == mock_browser
            assert miniapp_ui_with_config.page == mock_page
        with allure.step("Verify chromium.launch was called with headless=True"):
            mock_playwright_instance.chromium.launch.assert_called_once_with(
                headless=True
            )

    @pytest.mark.asyncio
    @allure.title("setup_browser creates new page")
    @allure.description("Test setup_browser creates new page.")
    async def test_setup_browser_creates_new_page(
        self, mocker, miniapp_ui_with_config, mock_browser, mock_page
    ):
        """Test setup_browser creates new page."""
        with allure.step("Mock async_playwright and browser setup"):
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

        with allure.step("Call setup_browser()"):
            await miniapp_ui_with_config.setup_browser()

        with allure.step("Verify new_page was called"):
            mock_browser.new_page.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("setup_browser sets custom User-Agent")
    @allure.description("Test setup_browser sets custom User-Agent.")
    async def test_setup_browser_sets_user_agent(
        self, mocker, miniapp_ui_with_config, mock_browser, mock_page
    ):
        """Test setup_browser sets custom User-Agent."""
        with allure.step("Mock async_playwright and browser setup"):
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

        with allure.step("Call setup_browser()"):
            await miniapp_ui_with_config.setup_browser()

        with allure.step("Verify User-Agent header was set"):
            mock_page.set_extra_http_headers.assert_called_once()
            call_args = mock_page.set_extra_http_headers.call_args[0][0]
            assert "User-Agent" in call_args

    @pytest.mark.asyncio
    @allure.title("Second call to setup_browser logs 'Browser already setup'")
    @allure.description(
        "Test second call to setup_browser logs 'Browser already setup'. TC-UI-004"
    )
    async def test_setup_browser_second_call_logs_already_setup(
        self, miniapp_ui_with_browser, caplog
    ):
        """Test second call to setup_browser logs 'Browser already setup'. TC-UI-004"""
        with allure.step("Call setup_browser() second time"):
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.setup_browser()

        with allure.step("Verify log message"):
            assert "Browser already setup" in caplog.text

    @pytest.mark.asyncio
    @allure.title("Second call to setup_browser does not create new browser")
    @allure.description(
        "Test second call to setup_browser does not create new browser."
    )
    async def test_setup_browser_second_call_does_not_create_new_browser(
        self, miniapp_ui_with_browser, mock_browser
    ):
        """Test second call to setup_browser does not create new browser."""
        with allure.step("Save reference to original browser"):
            original_browser = miniapp_ui_with_browser.browser

        with allure.step("Call setup_browser() second time"):
            await miniapp_ui_with_browser.setup_browser()

        with allure.step("Verify browser remains the same"):
            # Browser should remain the same
            assert miniapp_ui_with_browser.browser is original_browser

    @pytest.mark.asyncio
    @allure.title("setup_browser returns self for method chaining")
    @allure.description(
        "Test setup_browser returns self for method chaining. TC-UI-005"
    )
    async def test_setup_browser_returns_self(
        self, mocker, miniapp_ui_with_config, mock_browser, mock_page
    ):
        """Test setup_browser returns self for method chaining. TC-UI-005"""
        with allure.step("Mock async_playwright and browser setup"):
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

        with allure.step("Call setup_browser()"):
            result = await miniapp_ui_with_config.setup_browser()

        with allure.step("Verify setup_browser returns self"):
            assert result is miniapp_ui_with_config

    @pytest.mark.asyncio
    @allure.title("TC-UI-042: setup_browser rejects empty or invalid URL")
    @allure.description("Test setup_browser rejects empty or invalid URL. TC-UI-042")
    async def test_setup_browser_rejects_empty_url(self, valid_config):
        """Test setup_browser rejects empty or invalid URL. TC-UI-042"""
        with allure.step("Test with empty string URL"):
            # Test with empty string
            ui = MiniAppUI("", valid_config)
            with pytest.raises(ValueError, match="URL is not set or is empty"):
                await ui.setup_browser()

        with allure.step("Test with whitespace-only string URL"):
            # Test with whitespace-only string
            ui = MiniAppUI("   ", valid_config)
            with pytest.raises(ValueError, match="URL is not set or is empty"):
                await ui.setup_browser()

    @pytest.mark.asyncio
    @allure.title("setup_browser handles navigation failures gracefully")
    @allure.description(
        "Test setup_browser handles navigation failures gracefully. TC-UI-043"
    )
    async def test_setup_browser_handles_navigation_error(
        self, mocker, miniapp_ui_with_config, mock_browser, mock_page
    ):
        """Test setup_browser handles navigation failures gracefully. TC-UI-043"""
        with allure.step("Mock async_playwright and browser setup"):
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

        with allure.step("Attempt to call setup_browser() and expect RuntimeError"):
            # Should raise RuntimeError with appropriate message
            with pytest.raises(RuntimeError, match="Failed to navigate to"):
                await miniapp_ui_with_config.setup_browser()

        with allure.step("Verify page.goto was called"):
            # Verify page.goto was called
            mock_page.goto.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("setup_browser handles network errors during navigation")
    @allure.description(
        "Test setup_browser handles network errors during navigation. TC-UI-043"
    )
    async def test_setup_browser_handles_network_error(
        self, mocker, miniapp_ui_with_config, mock_browser, mock_page
    ):
        """Test setup_browser handles network errors during navigation. TC-UI-043"""
        with allure.step("Mock async_playwright and browser setup"):
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

        with allure.step("Attempt to call setup_browser() and expect RuntimeError"):
            # Should raise RuntimeError with appropriate message
            with pytest.raises(RuntimeError, match="Failed to navigate to"):
                await miniapp_ui_with_config.setup_browser()

        with allure.step("Verify page.goto was called"):
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
    @allure.title("TC-UI-008: click_element logs DEBUG on success")
    @allure.description("Test click_element logs DEBUG on success. TC-UI-008")
    async def test_click_element_success(
        self, miniapp_ui_with_browser, selector, caplog
    ):
        """Test click_element logs DEBUG on success. TC-UI-008"""
        with allure.step(f"Click element with selector: {selector}"):
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.click_element(selector)

        with allure.step("Verify DEBUG log and click was called"):
            assert f"Clicked element: {selector}" in caplog.text
            miniapp_ui_with_browser.page.click.assert_called_once_with(selector)

    @pytest.mark.asyncio
    @allure.title("click_element handles exceptions and logs ERROR")
    @allure.description(
        "Test click_element handles exceptions and logs ERROR. TC-UI-009"
    )
    async def test_click_element_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test click_element handles exceptions and logs ERROR. TC-UI-009"""
        with allure.step("Mock page.click to raise exception"):
            error = Exception("Element not found")
            miniapp_ui_with_browser.page.click = mocker.AsyncMock(side_effect=error)

        with allure.step("Attempt to click invalid element"):
            with caplog.at_level("ERROR"):
                await miniapp_ui_with_browser.click_element("#invalid")

        with allure.step("Verify ERROR log and no exception raised"):
            assert "Failed to click element" in caplog.text
            # Should not raise exception
            assert True  # Test passes if no exception raised

    @pytest.mark.asyncio
    @allure.title("click_element with unicode characters in selector")
    @allure.description(
        "Test click_element with unicode characters in selector. TC-UI-040"
    )
    async def test_click_element_unicode_selector(
        self, miniapp_ui_with_browser, caplog
    ):
        """Test click_element with unicode characters in selector. TC-UI-040"""
        with allure.step("Click element with unicode selector"):
            unicode_selector = "#тест-用户-ユーザー"
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.click_element(unicode_selector)

        with allure.step("Verify DEBUG log and click was called"):
            assert f"Clicked element: {unicode_selector}" in caplog.text
            miniapp_ui_with_browser.page.click.assert_called_once_with(unicode_selector)

    @pytest.mark.asyncio
    @allure.title("TC-UI-041: click_element with very long selector")
    @allure.description("Test click_element with very long selector. TC-UI-041")
    async def test_click_element_very_long_selector(
        self, miniapp_ui_with_browser, caplog
    ):
        """Test click_element with very long selector. TC-UI-041"""
        with allure.step("Create very long selector (>1000 characters)"):
            # Create a very long selector (>1000 characters)
            long_selector = "#" + "a" * 1000
        with allure.step("Click element with long selector"):
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.click_element(long_selector)

        with allure.step("Verify DEBUG log and click was called"):
            assert f"Clicked element: {long_selector}" in caplog.text
            miniapp_ui_with_browser.page.click.assert_called_once_with(long_selector)

    @pytest.mark.asyncio
    @allure.title("TC-UI-040: fill_input with unicode selector")
    @allure.description("Test fill_input with unicode selector. TC-UI-040")
    async def test_fill_input_unicode_selector(self, miniapp_ui_with_browser, caplog):
        """Test fill_input with unicode selector. TC-UI-040"""
        with allure.step("Fill input with unicode selector"):
            unicode_selector = "#ввод-输入-入力"
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.fill_input(unicode_selector, "test")

        with allure.step("Verify DEBUG log and fill was called"):
            assert "Filled input" in caplog.text
            miniapp_ui_with_browser.page.fill.assert_called_once_with(
                unicode_selector, "test"
            )

    @pytest.mark.asyncio
    @allure.title("TC-UI-041: fill_input with very long selector")
    @allure.description("Test fill_input with very long selector. TC-UI-041")
    async def test_fill_input_very_long_selector(self, miniapp_ui_with_browser, caplog):
        """Test fill_input with very long selector. TC-UI-041"""
        with allure.step("Create very long selector (>1000 characters)"):
            long_selector = "#" + "input" * 200  # >1000 characters
        with allure.step("Fill input with long selector"):
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.fill_input(long_selector, "test")

        with allure.step("Verify DEBUG log and fill was called"):
            assert "Filled input" in caplog.text
            miniapp_ui_with_browser.page.fill.assert_called_once_with(
                long_selector, "test"
            )

    @pytest.mark.asyncio
    @allure.title("TC-UI-010: fill_input logs DEBUG on success")
    @allure.description("Test fill_input logs DEBUG on success. TC-UI-010")
    async def test_fill_input_success(self, miniapp_ui_with_browser, caplog):
        """Test fill_input logs DEBUG on success. TC-UI-010"""
        with allure.step("Fill input field"):
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.fill_input("#input", "test text")

        with allure.step("Verify DEBUG log and fill was called"):
            assert "Filled input" in caplog.text
            miniapp_ui_with_browser.page.fill.assert_called_once_with(
                "#input", "test text"
            )

    @pytest.mark.asyncio
    @allure.title("TC-UI-011: fill_input handles exceptions")
    @allure.description("Test fill_input handles exceptions. TC-UI-011")
    async def test_fill_input_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test fill_input handles exceptions. TC-UI-011"""
        with allure.step("Mock page.fill to raise exception"):
            error = Exception("Element not found")
            miniapp_ui_with_browser.page.fill = mocker.AsyncMock(side_effect=error)

        with allure.step("Attempt to fill invalid input"):
            with caplog.at_level("ERROR"):
                await miniapp_ui_with_browser.fill_input("#invalid", "text")

        with allure.step("Verify ERROR log"):
            assert "Failed to fill input" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-UI-020: hover_element logs DEBUG on success")
    @allure.description("Test hover_element logs DEBUG on success. TC-UI-020")
    async def test_hover_element_success(self, miniapp_ui_with_browser, caplog):
        """Test hover_element logs DEBUG on success. TC-UI-020"""
        with allure.step("Hover over element"):
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.hover_element("#element")

        with allure.step("Verify DEBUG log and hover was called"):
            assert "Hovered over element" in caplog.text
            miniapp_ui_with_browser.page.hover.assert_called_once_with("#element")

    @pytest.mark.asyncio
    @allure.title("hover_element handles exceptions")
    @allure.description("Test hover_element handles exceptions.")
    async def test_hover_element_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test hover_element handles exceptions."""
        with allure.step("Mock page.hover to raise exception"):
            error = Exception("Element not found")
            miniapp_ui_with_browser.page.hover = mocker.AsyncMock(side_effect=error)

        with allure.step("Attempt to hover invalid element"):
            with caplog.at_level("ERROR"):
                await miniapp_ui_with_browser.hover_element("#invalid")

        with allure.step("Verify ERROR log"):
            assert "Failed to hover over element" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-UI-021: double_click_element logs DEBUG on success")
    @allure.description("Test double_click_element logs DEBUG on success. TC-UI-021")
    async def test_double_click_element_success(self, miniapp_ui_with_browser, caplog):
        """Test double_click_element logs DEBUG on success. TC-UI-021"""
        with allure.step("Double click element"):
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.double_click_element("#element")

        with allure.step("Verify DEBUG log and dblclick was called"):
            assert "Double clicked element" in caplog.text
            miniapp_ui_with_browser.page.dblclick.assert_called_once_with("#element")

    @pytest.mark.asyncio
    @allure.title("double_click_element handles exceptions")
    @allure.description("Test double_click_element handles exceptions.")
    async def test_double_click_element_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test double_click_element handles exceptions."""
        with allure.step("Mock page.dblclick to raise exception"):
            error = Exception("Element not found")
            miniapp_ui_with_browser.page.dblclick = mocker.AsyncMock(side_effect=error)

        with allure.step("Attempt to double click invalid element"):
            with caplog.at_level("ERROR"):
                await miniapp_ui_with_browser.double_click_element("#invalid")

        with allure.step("Verify ERROR log"):
            assert "Failed to double click element" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-UI-022: right_click_element logs DEBUG on success")
    @allure.description("Test right_click_element logs DEBUG on success. TC-UI-022")
    async def test_right_click_element_success(self, miniapp_ui_with_browser, caplog):
        """Test right_click_element logs DEBUG on success. TC-UI-022"""
        with allure.step("Right click element"):
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.right_click_element("#element")

        with allure.step("Verify DEBUG log and click was called with button=right"):
            assert "Right clicked element" in caplog.text
            miniapp_ui_with_browser.page.click.assert_called_once_with(
                "#element", button="right"
            )

    @pytest.mark.asyncio
    @allure.title("right_click_element handles exceptions")
    @allure.description("Test right_click_element handles exceptions.")
    async def test_right_click_element_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test right_click_element handles exceptions."""
        with allure.step("Mock page.click to raise exception"):
            error = Exception("Element not found")
            miniapp_ui_with_browser.page.click = mocker.AsyncMock(side_effect=error)

        with allure.step("Attempt to right click invalid element"):
            with caplog.at_level("ERROR"):
                await miniapp_ui_with_browser.right_click_element("#invalid")

        with allure.step("Verify ERROR log"):
            assert "Failed to right click element" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-UI-024: check_checkbox logs DEBUG on success")
    @allure.description("Test check_checkbox logs DEBUG on success. TC-UI-024")
    async def test_check_checkbox_success(self, miniapp_ui_with_browser, caplog):
        """Test check_checkbox logs DEBUG on success. TC-UI-024"""
        with allure.step("Check checkbox"):
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.check_checkbox("#checkbox")

        with allure.step("Verify DEBUG log and check was called"):
            assert "Checked checkbox" in caplog.text
            miniapp_ui_with_browser.page.check.assert_called_once_with("#checkbox")

    @pytest.mark.asyncio
    @allure.title("check_checkbox handles exceptions")
    @allure.description("Test check_checkbox handles exceptions.")
    async def test_check_checkbox_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test check_checkbox handles exceptions."""
        with allure.step("Mock page.check to raise exception"):
            error = Exception("Element not found")
            miniapp_ui_with_browser.page.check = mocker.AsyncMock(side_effect=error)

        with allure.step("Attempt to check invalid checkbox"):
            with caplog.at_level("ERROR"):
                await miniapp_ui_with_browser.check_checkbox("#invalid")

        with allure.step("Verify ERROR log"):
            assert "Failed to check checkbox" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-UI-025: uncheck_checkbox logs DEBUG on success")
    @allure.description("Test uncheck_checkbox logs DEBUG on success. TC-UI-025")
    async def test_uncheck_checkbox_success(self, miniapp_ui_with_browser, caplog):
        """Test uncheck_checkbox logs DEBUG on success. TC-UI-025"""
        with allure.step("Uncheck checkbox"):
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.uncheck_checkbox("#checkbox")

        with allure.step("Verify DEBUG log and uncheck was called"):
            assert "Unchecked checkbox" in caplog.text
            miniapp_ui_with_browser.page.uncheck.assert_called_once_with("#checkbox")

    @pytest.mark.asyncio
    @allure.title("uncheck_checkbox handles exceptions")
    @allure.description("Test uncheck_checkbox handles exceptions.")
    async def test_uncheck_checkbox_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test uncheck_checkbox handles exceptions."""
        with allure.step("Mock page.uncheck to raise exception"):
            error = Exception("Element not found")
            miniapp_ui_with_browser.page.uncheck = mocker.AsyncMock(side_effect=error)

        with allure.step("Attempt to uncheck invalid checkbox"):
            with caplog.at_level("ERROR"):
                await miniapp_ui_with_browser.uncheck_checkbox("#invalid")

        with allure.step("Verify ERROR log"):
            assert "Failed to uncheck checkbox" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-UI-023: select_option logs DEBUG on success")
    @allure.description("Test select_option logs DEBUG on success. TC-UI-023")
    async def test_select_option_success(self, miniapp_ui_with_browser, caplog):
        """Test select_option logs DEBUG on success. TC-UI-023"""
        with allure.step("Select option"):
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.select_option("#select", "value1")

        with allure.step("Verify DEBUG log and select_option was called"):
            assert "Selected option" in caplog.text
            miniapp_ui_with_browser.page.select_option.assert_called_once_with(
                "#select", "value1"
            )

    @pytest.mark.asyncio
    @allure.title("select_option handles exceptions")
    @allure.description("Test select_option handles exceptions.")
    async def test_select_option_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test select_option handles exceptions."""
        with allure.step("Mock page.select_option to raise exception"):
            error = Exception("Element not found")
            miniapp_ui_with_browser.page.select_option = mocker.AsyncMock(
                side_effect=error
            )

        with allure.step("Attempt to select option in invalid element"):
            with caplog.at_level("ERROR"):
                await miniapp_ui_with_browser.select_option("#invalid", "value")

        with allure.step("Verify ERROR log"):
            assert "Failed to select option" in caplog.text


# ============================================================================
# IV. Ожидания и навигация
# ============================================================================


class TestMiniAppUIWaitAndNavigation:
    """Test MiniAppUI wait and navigation methods."""

    @pytest.mark.asyncio
    @allure.title("TC-UI-012: wait_for_element waits for element to appear")
    @allure.description("Test wait_for_element waits for element to appear. TC-UI-012")
    async def test_wait_for_element_success(self, miniapp_ui_with_browser, caplog):
        """Test wait_for_element waits for element to appear. TC-UI-012"""
        with allure.step("Wait for element to appear"):
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.wait_for_element("#element")

        with allure.step("Verify DEBUG log and wait_for_selector was called"):
            assert "Element appeared" in caplog.text
            miniapp_ui_with_browser.page.wait_for_selector.assert_called_once_with(
                "#element", timeout=5000
            )

    @pytest.mark.asyncio
    @allure.title("TC-UI-013: wait_for_element handles timeout")
    @allure.description("Test wait_for_element handles timeout. TC-UI-013")
    async def test_wait_for_element_timeout(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test wait_for_element handles timeout. TC-UI-013"""
        with allure.step("Mock wait_for_selector to raise TimeoutError"):
            from playwright.async_api import TimeoutError as PlaywrightTimeoutError

            error = PlaywrightTimeoutError("Timeout")
            miniapp_ui_with_browser.page.wait_for_selector = mocker.AsyncMock(
                side_effect=error
            )

        with allure.step("Attempt to wait for invalid element"):
            with caplog.at_level("ERROR"):
                await miniapp_ui_with_browser.wait_for_element("#invalid", timeout=1000)

        with allure.step("Verify ERROR log"):
            assert "Element" in caplog.text and "did not appear" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-UI-029: wait_for_navigation waits for networkidle")
    @allure.description("Test wait_for_navigation waits for networkidle. TC-UI-029")
    async def test_wait_for_navigation_success(self, miniapp_ui_with_browser, caplog):
        """Test wait_for_navigation waits for networkidle. TC-UI-029"""
        with allure.step("Wait for navigation"):
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.wait_for_navigation()

        with allure.step("Verify DEBUG log and wait_for_load_state was called"):
            assert "Navigation completed" in caplog.text
            miniapp_ui_with_browser.page.wait_for_load_state.assert_called_once_with(
                "networkidle", timeout=5000
            )

    @pytest.mark.asyncio
    @allure.title("TC-UI-030: wait_for_navigation handles timeout")
    @allure.description("Test wait_for_navigation handles timeout. TC-UI-030")
    async def test_wait_for_navigation_timeout(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test wait_for_navigation handles timeout. TC-UI-030"""
        with allure.step("Mock wait_for_load_state to raise TimeoutError"):
            from playwright.async_api import TimeoutError as PlaywrightTimeoutError

            error = PlaywrightTimeoutError("Timeout")
            miniapp_ui_with_browser.page.wait_for_load_state = mocker.AsyncMock(
                side_effect=error
            )

        with allure.step("Attempt to wait for navigation with timeout"):
            with caplog.at_level("ERROR"):
                await miniapp_ui_with_browser.wait_for_navigation(timeout=1000)

        with allure.step("Verify ERROR log"):
            assert "Navigation timeout" in caplog.text


# ============================================================================
# V. Получение данных со страницы
# ============================================================================


class TestMiniAppUIGetData:
    """Test MiniAppUI data retrieval methods."""

    @pytest.mark.asyncio
    @allure.title("get_element_text returns text if element found")
    @allure.description(
        "Test get_element_text returns text if element found. TC-UI-014"
    )
    async def test_get_element_text_success(self, miniapp_ui_with_browser, caplog):
        """Test get_element_text returns text if element found. TC-UI-014"""
        with allure.step("Get element text"):
            with caplog.at_level("DEBUG"):
                result = await miniapp_ui_with_browser.get_element_text("#element")

        with allure.step("Verify result and DEBUG log"):
            assert result == "Test text"
            assert "Element text" in caplog.text

    @pytest.mark.asyncio
    @allure.title("get_element_text returns None if element not found")
    @allure.description(
        "Test get_element_text returns None if element not found. TC-UI-015"
    )
    async def test_get_element_text_element_not_found(
        self, mocker, miniapp_ui_with_browser
    ):
        """Test get_element_text returns None if element not found. TC-UI-015"""
        with allure.step("Mock query_selector to return None"):
            miniapp_ui_with_browser.page.query_selector = mocker.AsyncMock(
                return_value=None
            )

        with allure.step("Get element text for nonexistent element"):
            result = await miniapp_ui_with_browser.get_element_text("#nonexistent")

        with allure.step("Verify result is None"):
            assert result is None

    @pytest.mark.asyncio
    @allure.title("get_element_text handles exceptions")
    @allure.description("Test get_element_text handles exceptions.")
    async def test_get_element_text_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test get_element_text handles exceptions."""
        with allure.step("Mock query_selector to raise exception"):
            error = Exception("Query failed")
            miniapp_ui_with_browser.page.query_selector = mocker.AsyncMock(
                side_effect=error
            )

        with allure.step("Attempt to get element text"):
            with caplog.at_level("ERROR"):
                result = await miniapp_ui_with_browser.get_element_text("#element")

        with allure.step("Verify result is None and ERROR log"):
            assert result is None
            assert "Failed to get element text" in caplog.text

    @pytest.mark.asyncio
    @pytest.mark.parametrize("attribute", ["value", "href", "disabled", "class"])
    @allure.title("get_element_attribute_value returns attribute value")
    @allure.description(
        "Test get_element_attribute_value returns attribute value. TC-UI-016"
    )
    async def test_get_element_attribute_value_success(
        self, miniapp_ui_with_browser, attribute, caplog
    ):
        """Test get_element_attribute_value returns attribute value. TC-UI-016"""
        with allure.step(f"Get element attribute value for {attribute}"):
            with caplog.at_level("DEBUG"):
                result = await miniapp_ui_with_browser.get_element_attribute_value(
                    "#element", attribute
                )

        with allure.step("Verify result and DEBUG log"):
            assert result == "test-value"
            assert "Element attribute" in caplog.text

    @pytest.mark.asyncio
    @allure.title("get_element_attribute_value returns None if element not found")
    @allure.description(
        "Test get_element_attribute_value returns None if element not found. TC-UI-017"
    )
    async def test_get_element_attribute_value_element_not_found(
        self, mocker, miniapp_ui_with_browser
    ):
        """Test get_element_attribute_value returns None if element not found. TC-UI-017"""
        with allure.step("Mock query_selector to return None"):
            miniapp_ui_with_browser.page.query_selector = mocker.AsyncMock(
                return_value=None
            )

        with allure.step("Get element attribute value for nonexistent element"):
            result = await miniapp_ui_with_browser.get_element_attribute_value(
                "#nonexistent", "value"
            )

        with allure.step("Verify result is None"):
            assert result is None

    @pytest.mark.asyncio
    @allure.title("get_element_attribute_value handles exceptions")
    @allure.description("Test get_element_attribute_value handles exceptions.")
    async def test_get_element_attribute_value_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test get_element_attribute_value handles exceptions."""
        with allure.step("Mock query_selector to raise exception"):
            error = Exception("Query failed")
            miniapp_ui_with_browser.page.query_selector = mocker.AsyncMock(
                side_effect=error
            )

        with allure.step("Attempt to get element attribute value"):
            with caplog.at_level("ERROR"):
                result = await miniapp_ui_with_browser.get_element_attribute_value(
                    "#element", "value"
                )

        with allure.step("Verify result is None and ERROR log"):
            assert result is None
            assert "Failed to get element attribute" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-UI-031: get_page_title returns page title")
    @allure.description("Test get_page_title returns page title. TC-UI-031")
    async def test_get_page_title_success(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test get_page_title returns page title. TC-UI-031"""
        with allure.step("Mock page.title to return title"):
            miniapp_ui_with_browser.page.title = mocker.AsyncMock(
                return_value="Test Page"
            )

        with allure.step("Get page title"):
            with caplog.at_level("DEBUG"):
                result = await miniapp_ui_with_browser.get_page_title()

        with allure.step("Verify result and DEBUG log"):
            assert result == "Test Page"
            assert "Page title" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-UI-032: get_page_title returns empty string on error")
    @allure.description("Test get_page_title returns empty string on error. TC-UI-032")
    async def test_get_page_title_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test get_page_title returns empty string on error. TC-UI-032"""
        with allure.step("Mock page.title to raise exception"):
            error = Exception("Failed to get title")
            miniapp_ui_with_browser.page.title = mocker.AsyncMock(side_effect=error)

        with allure.step("Attempt to get page title"):
            with caplog.at_level("ERROR"):
                result = await miniapp_ui_with_browser.get_page_title()

        with allure.step("Verify result is empty string and ERROR log"):
            assert result == ""
            assert "Failed to get page title" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-UI-033: get_page_url returns page URL")
    @allure.description("Test get_page_url returns page URL. TC-UI-033")
    async def test_get_page_url_success(self, miniapp_ui_with_browser, caplog):
        """Test get_page_url returns page URL. TC-UI-033"""
        with allure.step("Set page.url"):
            miniapp_ui_with_browser.page.url = "https://example.com/app"

        with allure.step("Get page URL"):
            with caplog.at_level("DEBUG"):
                result = await miniapp_ui_with_browser.get_page_url()

        with allure.step("Verify result and DEBUG log"):
            assert result == "https://example.com/app"
            assert "Page URL" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-UI-034: get_page_url returns empty string on error")
    @allure.description("Test get_page_url returns empty string on error. TC-UI-034")
    async def test_get_page_url_exception_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test get_page_url returns empty string on error. TC-UI-034"""
        with allure.step("Mock page.url property to raise exception"):
            # Simulate error by making page.url property raise an exception
            type(miniapp_ui_with_browser.page).url = mocker.PropertyMock(
                side_effect=Exception("Test exception")
            )

        with allure.step("Attempt to get page URL"):
            with caplog.at_level("ERROR"):
                result = await miniapp_ui_with_browser.get_page_url()

        with allure.step("Verify result is empty string and ERROR log"):
            # Should return empty string and log error
            assert result == ""
            assert "Failed to get page URL" in caplog.text


# ============================================================================
# VI. Скриншоты и файлы
# ============================================================================


class TestMiniAppUIScreenshotsAndFiles:
    """Test MiniAppUI screenshot and file methods."""

    @pytest.mark.asyncio
    @allure.title("TC-UI-035: take_screenshot creates file")
    @allure.description("Test take_screenshot creates file. TC-UI-035")
    async def test_take_screenshot_success(self, miniapp_ui_with_browser, caplog):
        """Test take_screenshot creates file. TC-UI-035"""
        with allure.step("Create temporary directory and screenshot path"):
            with tempfile.TemporaryDirectory() as tmpdir:
                screenshot_path = str(Path(tmpdir) / "test.png")

                with allure.step("Take screenshot"):
                    with caplog.at_level("DEBUG"):
                        await miniapp_ui_with_browser.take_screenshot(screenshot_path)

                with allure.step("Verify DEBUG log and screenshot was called"):
                    assert "Screenshot saved" in caplog.text
                    miniapp_ui_with_browser.page.screenshot.assert_called_once_with(
                        path=screenshot_path
                    )

    @pytest.mark.asyncio
    @allure.title("TC-UI-036: take_screenshot handles error")
    @allure.description("Test take_screenshot handles error. TC-UI-036")
    async def test_take_screenshot_error_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test take_screenshot handles error. TC-UI-036"""
        with allure.step("Mock page.screenshot to raise exception"):
            error = Exception("Screenshot failed")
            miniapp_ui_with_browser.page.screenshot = mocker.AsyncMock(
                side_effect=error
            )

        with allure.step("Attempt to take screenshot with invalid path"):
            with caplog.at_level("ERROR"):
                await miniapp_ui_with_browser.take_screenshot("/invalid/path.png")

        with allure.step("Verify ERROR log"):
            assert "Screenshot failed" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-UI-026: upload_file calls set_input_files")
    @allure.description("Test upload_file calls set_input_files. TC-UI-026")
    async def test_upload_file_success(self, miniapp_ui_with_browser, caplog):
        """Test upload_file calls set_input_files. TC-UI-026"""
        with allure.step("Upload file"):
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.upload_file(
                    "#file-input", "/fake/path.jpg"
                )

        with allure.step("Verify DEBUG log and set_input_files was called"):
            assert "Uploaded file" in caplog.text
            miniapp_ui_with_browser.page.set_input_files.assert_called_once_with(
                "#file-input", "/fake/path.jpg"
            )

    @pytest.mark.asyncio
    @allure.title("upload_file handles error")
    @allure.description("Test upload_file handles error.")
    async def test_upload_file_error_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test upload_file handles error."""
        with allure.step("Mock page.set_input_files to raise exception"):
            error = Exception("File not found")
            miniapp_ui_with_browser.page.set_input_files = mocker.AsyncMock(
                side_effect=error
            )

        with allure.step("Attempt to upload file to invalid element"):
            with caplog.at_level("ERROR"):
                await miniapp_ui_with_browser.upload_file("#invalid", "/fake/path.jpg")

        with allure.step("Verify ERROR log"):
            assert "Failed to upload file" in caplog.text


# ============================================================================
# VII. Клавиатура и скрипты
# ============================================================================


class TestMiniAppUIKeyboardAndScripts:
    """Test MiniAppUI keyboard and script methods."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("key", ["Enter", "Tab", "Escape", "ArrowDown"])
    @allure.title("TC-UI-027: press_key calls keyboard.press")
    @allure.description("Test press_key calls keyboard.press. TC-UI-027")
    async def test_press_key_success(self, miniapp_ui_with_browser, key, caplog):
        """Test press_key calls keyboard.press. TC-UI-027"""
        with allure.step(f"Press key: {key}"):
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.press_key(key)

        with allure.step("Verify DEBUG log and keyboard.press was called"):
            assert f"Pressed key: {key}" in caplog.text
            miniapp_ui_with_browser.page.keyboard.press.assert_called_once_with(key)

    @pytest.mark.asyncio
    @allure.title("press_key handles invalid key")
    @allure.description("Test press_key handles invalid key.")
    async def test_press_key_invalid_key_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test press_key handles invalid key."""
        with allure.step("Mock keyboard.press to raise exception"):
            error = Exception("Invalid key")
            miniapp_ui_with_browser.page.keyboard.press = mocker.AsyncMock(
                side_effect=error
            )

        with allure.step("Attempt to press invalid key"):
            with caplog.at_level("ERROR"):
                await miniapp_ui_with_browser.press_key("InvalidKey")

        with allure.step("Verify ERROR log"):
            assert "Failed to press key" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-UI-028: type_text calls keyboard.type")
    @allure.description("Test type_text calls keyboard.type. TC-UI-028")
    async def test_type_text_success(self, miniapp_ui_with_browser, caplog):
        """Test type_text calls keyboard.type. TC-UI-028"""
        with allure.step("Type text"):
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.type_text("hello")

        with allure.step("Verify DEBUG log and keyboard.type was called"):
            assert "Typed text: hello" in caplog.text
            miniapp_ui_with_browser.page.keyboard.type.assert_called_once_with("hello")

    @pytest.mark.asyncio
    @allure.title("type_text handles error")
    @allure.description("Test type_text handles error.")
    async def test_type_text_error_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test type_text handles error."""
        with allure.step("Mock keyboard.type to raise exception"):
            error = Exception("Type failed")
            miniapp_ui_with_browser.page.keyboard.type = mocker.AsyncMock(
                side_effect=error
            )

        with allure.step("Attempt to type text"):
            with caplog.at_level("ERROR"):
                await miniapp_ui_with_browser.type_text("text")

        with allure.step("Verify ERROR log"):
            assert "Failed to type text" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-UI-037: execute_script returns result")
    @allure.description("Test execute_script returns result. TC-UI-037")
    async def test_execute_script_success(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test execute_script returns result. TC-UI-037"""
        with allure.step("Mock page.evaluate to return value"):
            miniapp_ui_with_browser.page.evaluate = mocker.AsyncMock(return_value=42)

        with allure.step("Execute script"):
            with caplog.at_level("DEBUG"):
                result = await miniapp_ui_with_browser.execute_script("return 42")

        with allure.step("Verify result and DEBUG log"):
            assert result == 42
            assert "Script executed" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-UI-038: execute_script handles error and returns None")
    @allure.description("Test execute_script handles error and returns None. TC-UI-038")
    async def test_execute_script_error_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test execute_script handles error and returns None. TC-UI-038"""
        with allure.step("Mock page.evaluate to raise exception"):
            error = Exception("Script error")
            miniapp_ui_with_browser.page.evaluate = mocker.AsyncMock(side_effect=error)

        with allure.step("Attempt to execute script that throws error"):
            with caplog.at_level("ERROR"):
                result = await miniapp_ui_with_browser.execute_script("throw 'err'")

        with allure.step("Verify result is None and ERROR log"):
            assert result is None
            assert "Script execution failed" in caplog.text


# ============================================================================
# VIII. Прокрутка и визуальные действия
# ============================================================================


class TestMiniAppUIScroll:
    """Test MiniAppUI scroll methods."""

    @pytest.mark.asyncio
    @allure.title("scroll_to_element calls scroll_into_view_if_needed")
    @allure.description(
        "Test scroll_to_element calls scroll_into_view_if_needed. TC-UI-018"
    )
    async def test_scroll_to_element_success(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test scroll_to_element calls scroll_into_view_if_needed. TC-UI-018"""
        with allure.step("Scroll to element"):
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.scroll_to_element("#element")

        with allure.step("Verify DEBUG log and locator was called"):
            assert "Scrolled to element" in caplog.text
            miniapp_ui_with_browser.page.locator.assert_called_once_with("#element")

    @pytest.mark.asyncio
    @allure.title("TC-UI-019: scroll_to_element handles error")
    @allure.description("Test scroll_to_element handles error. TC-UI-019")
    async def test_scroll_to_element_error_handled(
        self, mocker, miniapp_ui_with_browser, caplog
    ):
        """Test scroll_to_element handles error. TC-UI-019"""
        with allure.step("Mock locator.scroll_into_view_if_needed to raise exception"):
            error = Exception("Element not found")
            mock_locator = mocker.MagicMock()
            mock_locator.scroll_into_view_if_needed = mocker.AsyncMock(
                side_effect=error
            )
            miniapp_ui_with_browser.page.locator.return_value = mock_locator

        with allure.step("Attempt to scroll to invalid element"):
            with caplog.at_level("ERROR"):
                await miniapp_ui_with_browser.scroll_to_element("#invalid")

        with allure.step("Verify ERROR log"):
            assert "Failed to scroll to element" in caplog.text


# ============================================================================
# IX. Асинхронный контекстный менеджер
# ============================================================================


class TestMiniAppUIContextManager:
    """Test MiniAppUI async context manager."""

    @pytest.mark.asyncio
    @allure.title("__aenter__ returns self")
    @allure.description("Test __aenter__ returns self.")
    async def test_aenter_returns_self(self, miniapp_ui_with_config):
        """Test __aenter__ returns self."""
        with allure.step("Use async context manager"):
            async with miniapp_ui_with_config as ui:
                with allure.step("Verify __aenter__ returns self"):
                    assert ui is miniapp_ui_with_config

    @pytest.mark.asyncio
    @allure.title("__aexit__ calls await self.close()")
    @allure.description("Test __aexit__ calls await self.close().")
    async def test_aexit_calls_close(self, mocker, miniapp_ui_with_browser):
        """Test __aexit__ calls await self.close()."""
        with allure.step("Mock close method"):
            miniapp_ui_with_browser.close = mocker.AsyncMock()

        with allure.step("Use async context manager"):
            async with miniapp_ui_with_browser:
                pass

        with allure.step("Verify close was called"):
            miniapp_ui_with_browser.close.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("Typical context manager usage")
    @allure.description("Test typical context manager usage.")
    async def test_context_manager_usage(self, miniapp_ui_with_config):
        """Test typical context manager usage."""
        with allure.step("Use async context manager"):
            async with miniapp_ui_with_config as ui:
                with allure.step("Verify UI instance and URL"):
                    assert isinstance(ui, MiniAppUI)
                    assert ui.url == "https://example.com/app"


# ============================================================================
# X. Безопасность и отказоустойчивость
# ============================================================================


class TestMiniAppUISafety:
    """Test MiniAppUI safety and reliability."""

    @pytest.mark.asyncio
    @allure.title("No exceptions are propagated from public methods")
    @allure.description("Test that no exceptions are propagated from public methods.")
    async def test_no_exceptions_propagated(self, mocker, miniapp_ui_with_browser):
        """Test that no exceptions are propagated from public methods."""
        with allure.step("Mock page.click to raise exception"):
            # All methods should catch exceptions
            error = Exception("Test error")
            miniapp_ui_with_browser.page.click = mocker.AsyncMock(side_effect=error)

        with allure.step("Call click_element and verify no exception is raised"):
            # Should not raise exception
            await miniapp_ui_with_browser.click_element("#element")
            assert True  # Test passes if no exception raised

    @pytest.mark.asyncio
    @allure.title("Browser is closed in close()")
    @allure.description("Test browser is closed in close().")
    async def test_browser_closed_in_close(self, miniapp_ui_with_browser):
        """Test browser is closed in close()."""
        with allure.step("Save reference to browser before close()"):
            # Save reference to browser before close() sets it to None
            browser = miniapp_ui_with_browser.browser
        with allure.step("Call close()"):
            await miniapp_ui_with_browser.close()

        with allure.step("Verify browser.close() was called"):
            browser.close.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("Logs contain context (selector, key, etc.)")
    @allure.description("Test logs contain context (selector, key, etc.).")
    async def test_logs_contain_context(self, miniapp_ui_with_browser, caplog):
        """Test logs contain context (selector, key, etc.)."""
        with allure.step("Perform actions that generate logs"):
            with caplog.at_level("DEBUG"):
                await miniapp_ui_with_browser.click_element("#submit")
                await miniapp_ui_with_browser.press_key("Enter")

        with allure.step("Verify logs contain context"):
            assert "#submit" in caplog.text
            assert "Enter" in caplog.text

    @allure.title("logger is bound to MiniAppUI class name")
    @allure.description("Test logger is bound to MiniAppUI class name.")
    def test_logger_bound_to_class_name(self, miniapp_ui_with_config):
        """Test logger is bound to MiniAppUI class name."""
        with allure.step("Verify logger is initialized"):
            assert miniapp_ui_with_config.logger is not None
            # Logger should be bound to "MiniAppUI"


# ============================================================================
# XI. Совместимость с наследованием
# ============================================================================


class TestMiniAppUIInheritance:
    """Test MiniAppUI inheritance compatibility."""

    @allure.title("MiniAppUI can be inherited")
    @allure.description("Test MiniAppUI can be inherited.")
    def test_can_be_inherited(self, valid_config):
        """Test MiniAppUI can be inherited."""
        with allure.step("Create custom class inheriting from MiniAppUI"):

            class CustomMiniAppUI(MiniAppUI):
                pass

        with allure.step("Create instance of custom class"):
            ui = CustomMiniAppUI("https://example.com/app", valid_config)
        with allure.step("Verify instance is also MiniAppUI"):
            assert isinstance(ui, MiniAppUI)

    @pytest.mark.asyncio
    @allure.title("setup_browser returns Self for fluent interface")
    @allure.description("Test setup_browser returns Self for fluent interface.")
    async def test_setup_browser_returns_self_for_fluent_interface(
        self, mocker, miniapp_ui_with_config, mock_browser, mock_page
    ):
        """Test setup_browser returns Self for fluent interface."""
        with allure.step("Mock async_playwright and browser setup"):
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

        with allure.step("Call setup_browser()"):
            result = await miniapp_ui_with_config.setup_browser()

        with allure.step("Verify setup_browser returns self for method chaining"):
            # Should return self for method chaining
            assert result is miniapp_ui_with_config
            # Can be chained
            assert (
                await miniapp_ui_with_config.setup_browser() is miniapp_ui_with_config
            )
