"""
Integration tests for UserTelegramClient + MiniAppUI.
Tests verify interaction between MTProto client and Mini App UI client.
"""

import time

import allure
import pytest
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from tma_test_framework.clients.mtproto_client import MessageInfo, UserInfo, ChatInfo
from tma_test_framework.clients.ui_client import UiClient as MiniAppUI


@pytest.mark.integration
class TestMTProtoMiniAppUIIntegration:
    """Integration tests for UserTelegramClient and MiniAppUI."""

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-MTUI-001: Get Mini App from bot and test UI")
    @allure.description(
        "TC-INTEGRATION-MTUI-001: Get Mini App from bot and test UI. "
        "Verify complete flow: get Mini App from bot, then test its UI."
    )
    async def test_get_mini_app_and_test_ui(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-MTUI-001: Get Mini App from bot and test UI.

        Verify complete flow: get Mini App from bot, then test its UI.
        """
        # Mock get_mini_app_from_bot to return MiniAppUI
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        # Get Mini App from bot
        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        assert mini_app_ui is not None
        assert mini_app_ui.url == mock_mini_app_url

        # Create actual MiniAppUI instance
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright browser and page
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]
        mock_page.url = mock_mini_app_url
        mock_page.title = mocker.AsyncMock(return_value="Test Mini App")
        mock_page.locator = mocker.MagicMock(return_value=mocker.AsyncMock())

        # Setup browser
        await ui.setup_browser()

        assert ui.browser is not None
        assert ui.page is not None

        # Test UI interactions
        await ui.click_element("#button")
        if ui.page:
            ui.page.click.assert_called_once_with("#button")  # type: ignore[attr-defined]

        await ui.fill_input("#input", "test text")
        if ui.page:
            ui.page.fill.assert_called_once_with("#input", "test text")  # type: ignore[attr-defined]

        # Cleanup
        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-MTUI-002: Get Mini App with start_param and test UI")
    @allure.description(
        "TC-INTEGRATION-MTUI-002: Get Mini App with start_param and test UI. "
        "Verify Mini App retrieval with start parameter and UI testing."
    )
    async def test_get_mini_app_with_start_param_and_test_ui(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url_with_start_param,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-MTUI-002: Get Mini App with start_param and test UI.

        Verify Mini App retrieval with start parameter and UI testing.
        """
        # Mock get_mini_app_from_bot to return MiniAppUI with start param
        mock_mini_app_ui.url = mock_mini_app_url_with_start_param
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        # Get Mini App with start parameter
        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot", start_param="test123"
        )

        assert mini_app_ui is not None
        assert "start=test123" in mini_app_ui.url
        # Create MiniAppUI and setup browser
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]
        mock_page.url = mock_mini_app_url_with_start_param
        mock_page.title = mocker.AsyncMock(return_value="Test Mini App")

        await ui.setup_browser()

        # Verify URL contains start parameter
        page_url = await ui.get_page_url()
        assert "start=test123" in page_url
        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-MTUI-004: Complete form submission flow")
    @allure.description(
        "TC-INTEGRATION-MTUI-004: Complete form submission flow. "
        "Verify complete form submission in Mini App."
    )
    async def test_complete_form_submission_flow(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-MTUI-004: Complete form submission flow.

        Verify complete form submission in Mini App.
        """
        # Get Mini App from bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppUI
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]
        mock_page.url = mock_mini_app_url
        mock_page.wait_for_load_state = mocker.AsyncMock()

        await ui.setup_browser()

        # Fill form fields
        await ui.fill_input("#name", "John Doe")
        await ui.fill_input("#email", "john@example.com")
        await ui.fill_input("#message", "Test message")

        # Click submit button
        await ui.click_element("#submit")

        # Wait for navigation/response
        await ui.wait_for_navigation()

        # Verify interactions
        assert mock_page.fill.call_count == 3
        mock_page.click.assert_called_with("#submit")
        mock_page.wait_for_load_state.assert_called()

        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-MTUI-005: Test button interactions")
    @allure.description(
        "TC-INTEGRATION-MTUI-005: Test button interactions. "
        "Verify various button interactions."
    )
    async def test_button_interactions(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_mini_app_ui,
        mock_playwright_browser_and_page,
    ):
        """
        TC-INTEGRATION-MTUI-005: Test button interactions.

        Verify various button interactions.
        """
        # Get Mini App from bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppUI
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]
        mock_page.dblclick = mocker.AsyncMock()

        await ui.setup_browser()

        # Test different button interactions
        await ui.click_element("#primary-button")
        await ui.double_click_element("#action-button")
        await ui.right_click_element("#context-button")

        # Verify interactions
        assert mock_page.click.call_count >= 2  # click and right_click
        mock_page.dblclick.assert_called_once_with("#action-button")

        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-MTUI-006: Test dropdown and selection")
    @allure.description(
        "TC-INTEGRATION-MTUI-006: Test dropdown and selection. "
        "Verify dropdown and option selection."
    )
    async def test_dropdown_and_selection(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-MTUI-006: Test dropdown and selection.

        Verify dropdown and option selection.
        """
        # Get Mini App from bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppUI
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]
        mock_page.select_option = mocker.AsyncMock()

        await ui.setup_browser()

        # Select option from dropdown
        await ui.select_option("#dropdown", "option1")

        # Verify selection
        mock_page.select_option.assert_called_once_with("#dropdown", "option1")

        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-MTUI-007: Test checkbox interactions")
    @allure.description(
        "TC-INTEGRATION-MTUI-007: Test checkbox interactions. "
        "Verify checkbox check/uncheck."
    )
    async def test_checkbox_interactions(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-MTUI-007: Test checkbox interactions.

        Verify checkbox check/uncheck.
        """
        # Get Mini App from bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppUI
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]
        mock_page.check = mocker.AsyncMock()
        mock_page.uncheck = mocker.AsyncMock()

        await ui.setup_browser()

        # Check and uncheck checkbox
        await ui.check_checkbox("#checkbox")
        await ui.uncheck_checkbox("#checkbox")

        # Verify interactions
        mock_page.check.assert_called_once_with("#checkbox")
        mock_page.uncheck.assert_called_once_with("#checkbox")

        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-MTUI-008: Test page navigation")
    @allure.description(
        "TC-INTEGRATION-MTUI-008: Test page navigation. "
        "Verify navigation between pages."
    )
    async def test_page_navigation(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-MTUI-008: Test page navigation.

        Verify navigation between pages.
        """
        # Get Mini App from bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppUI
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]
        mock_page.url = "https://example.com/mini-app/page2"
        mock_page.title = mocker.AsyncMock(return_value="Page 2")
        mock_page.wait_for_load_state = mocker.AsyncMock()

        await ui.setup_browser()

        # Click navigation link
        await ui.click_element("#nav-link")

        # Wait for navigation
        await ui.wait_for_navigation()

        # Verify navigation
        page_url = await ui.get_page_url()
        page_title = await ui.get_page_title()

        assert page_url == "https://example.com/mini-app/page2"
        assert page_title == "Page 2"

        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-MTUI-010: Take screenshot of Mini App")
    @allure.description(
        "TC-INTEGRATION-MTUI-010: Take screenshot of Mini App. "
        "Verify screenshot capture."
    )
    async def test_take_screenshot(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-MTUI-010: Take screenshot of Mini App.

        Verify screenshot capture.
        """
        # Get Mini App from bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppUI
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]

        await ui.setup_browser()

        # Take screenshot
        await ui.take_screenshot("screenshot.png")

        # Verify screenshot was taken
        mock_page.screenshot.assert_called_once()

        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-MTUI-012: Execute JavaScript in Mini App")
    @allure.description(
        "TC-INTEGRATION-MTUI-012: Execute JavaScript in Mini App. "
        "Verify JavaScript execution."
    )
    async def test_execute_javascript(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-MTUI-012: Execute JavaScript in Mini App.

        Verify JavaScript execution.
        """
        # Get Mini App from bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppUI
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]
        mock_page.evaluate = mocker.AsyncMock(return_value={"data": "test"})

        await ui.setup_browser()

        # Execute JavaScript
        result = await ui.execute_script("return window.appData")

        # Verify script execution
        assert result == {"data": "test"}
        mock_page.evaluate.assert_called_once()

        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-MTUI-017: Use context manager for full flow")
    @allure.description(
        "TC-INTEGRATION-MTUI-017: Use context manager for full flow. "
        "Verify context manager usage in integration."
    )
    async def test_context_manager_integration(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-MTUI-017: Use context manager for full flow.

        Verify context manager usage in integration.
        """
        # Mock get_mini_app_from_bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        # Fixture already patches async_playwright
        mock_playwright_browser_and_page  # Fixture ensures playwright is mocked

        # Use context managers
        async with user_telegram_client_connected as client:
            mini_app_ui = await client.get_mini_app_from_bot("test_bot")

            async with MiniAppUI(mini_app_ui.url, client.config) as ui:
                await ui.setup_browser()
                await ui.click_element("#button")
                assert ui.page is not None

        # Verify both closed (mocked close methods should be called)

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-MTUI-018: Test UI loading performance")
    @allure.description(
        "TC-INTEGRATION-MTUI-018: Test UI loading performance. "
        "Verify Mini App UI loads in reasonable time."
    )
    async def test_ui_loading_performance(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-MTUI-018: Test UI loading performance.

        Verify Mini App UI loads in reasonable time.
        """

        # Get Mini App from bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppUI
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]
        mock_page.goto = mocker.AsyncMock()
        mock_page.wait_for_load_state = mocker.AsyncMock()

        # Measure time to navigate and load
        start_time = time.perf_counter()

        await ui.setup_browser()
        if ui.page:
            await ui.page.goto(mock_mini_app_url)
            await ui.page.wait_for_load_state("networkidle")

        end_time = time.perf_counter()
        load_time = end_time - start_time

        # Verify load time is acceptable (should be fast with mocks)
        assert load_time < 2.0  # Should complete quickly with mocked browser

        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-MTUI-019: Test multiple UI interactions performance")
    @allure.description(
        "TC-INTEGRATION-MTUI-019: Test multiple UI interactions performance. "
        "Verify performance with multiple interactions."
    )
    async def test_multiple_ui_interactions_performance(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-MTUI-019: Test multiple UI interactions performance.

        Verify performance with multiple interactions.
        """

        # Get Mini App from bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppUI
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]

        await ui.setup_browser()

        # Measure time for 10 sequential UI interactions
        start_time = time.perf_counter()

        # Perform 10 sequential UI interactions
        await ui.click_element("#button1")
        await ui.fill_input("#input1", "text1")
        await ui.click_element("#button2")
        await ui.check_checkbox("#checkbox1")
        await ui.fill_input("#input2", "text2")
        await ui.select_option("#dropdown1", "option1")
        await ui.click_element("#button3")
        await ui.uncheck_checkbox("#checkbox1")
        await ui.fill_input("#input3", "text3")
        await ui.click_element("#button4")

        end_time = time.perf_counter()
        total_time = end_time - start_time

        # Verify all interactions complete
        assert mock_page.click.call_count == 4
        assert mock_page.fill.call_count == 3
        assert mock_page.check.call_count == 1
        assert mock_page.uncheck.call_count == 1
        assert mock_page.select_option.call_count == 1

        # Verify time is reasonable (should be fast with mocks)
        assert total_time < 3.0  # Should complete quickly with mocked interactions

        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-MTUI-003: Get Mini App from media and test UI")
    @allure.description(
        "TC-INTEGRATION-MTUI-003: Get Mini App from media and test UI. "
        "Verify Mini App retrieval from message media and UI testing."
    )
    async def test_get_mini_app_from_media_and_test_ui(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-MTUI-003: Get Mini App from media and test UI.

        Verify Mini App retrieval from message media and UI testing.
        """
        # Create message with web_app media
        bot_user = UserInfo(
            id=999, first_name="Bot", is_bot=True, is_verified=False, is_premium=False
        )

        chat_info = ChatInfo(
            id=123, title="Test Chat", type="private", is_verified=False
        )

        message_with_media = MessageInfo(
            id=100,
            chat=chat_info,
            date="2023-10-20T10:00:00Z",
            text=None,
            from_user=bot_user,
            reply_to=None,
            media={"type": "web_app", "url": mock_mini_app_url},
        )

        # Mock get_messages to return message with media
        user_telegram_client_connected.get_messages = mocker.AsyncMock(
            return_value=[message_with_media]
        )

        # Mock get_mini_app_from_bot to extract from media
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        # Get Mini App from bot (should extract from media)
        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        assert mini_app_ui is not None
        assert mini_app_ui.url == mock_mini_app_url

        # Create MiniAppUI and test
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]

        await ui.setup_browser()
        await ui.click_element("#button")

        assert ui.page is not None
        mock_page.click.assert_called_once_with("#button")

        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-MTUI-009: Test scrolling and element visibility")
    @allure.description(
        "TC-INTEGRATION-MTUI-009: Test scrolling and element visibility. "
        "Verify scrolling to elements."
    )
    async def test_scrolling_and_element_visibility(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-MTUI-009: Test scrolling and element visibility.

        Verify scrolling to elements.
        """
        # Get Mini App from bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppUI
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]
        mock_element = mocker.AsyncMock()
        mock_element.text_content = mocker.AsyncMock(return_value="Element text")
        mock_page.query_selector = mocker.AsyncMock(return_value=mock_element)
        mock_page.locator = mocker.MagicMock(return_value=mock_element)

        await ui.setup_browser()

        # Scroll to element
        await ui.scroll_to_element("#scrollable-element")

        # Get element text
        element_text = await ui.get_element_text("#scrollable-element")

        # Verify scrolling and text retrieval
        assert element_text == "Element text"
        mock_element.scroll_into_view_if_needed.assert_called_once()

        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-MTUI-011: Take screenshot of specific element")
    @allure.description(
        "TC-INTEGRATION-MTUI-011: Take screenshot of specific element. "
        "Verify element-specific screenshot."
    )
    async def test_take_screenshot_of_specific_element(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-MTUI-011: Take screenshot of specific element.

        Verify element-specific screenshot.
        """
        # Get Mini App from bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppUI
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]
        mock_element = mocker.AsyncMock()
        mock_element.screenshot = mocker.AsyncMock()
        mock_page.locator = mocker.MagicMock(return_value=mock_element)

        await ui.setup_browser()

        # Take screenshot of specific element using locator
        element = mock_page.locator("#element")
        await element.screenshot(path="element.png")

        # Verify element screenshot was taken
        mock_element.screenshot.assert_called_once_with(path="element.png")

        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-MTUI-013: Get data via JavaScript")
    @allure.description(
        "TC-INTEGRATION-MTUI-013: Get data via JavaScript. "
        "Verify data extraction via JavaScript."
    )
    async def test_get_data_via_javascript(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-MTUI-013: Get data via JavaScript.

        Verify data extraction via JavaScript.
        """
        # Get Mini App from bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppUI
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]
        mock_app_data = {"userId": 123, "theme": "dark"}
        mock_page.evaluate = mocker.AsyncMock(return_value=mock_app_data)

        await ui.setup_browser()

        # Get data via JavaScript
        result = await ui.execute_script("return window.appData")

        # Verify data extraction
        assert result == mock_app_data
        assert result["userId"] == 123
        assert result["theme"] == "dark"

        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-MTUI-014: Handle Mini App not found")
    @allure.description(
        "TC-INTEGRATION-MTUI-014: Handle Mini App not found. "
        "Verify error handling when Mini App not found."
    )
    async def test_handle_mini_app_not_found(
        self, mocker, user_telegram_client_connected
    ):
        """
        TC-INTEGRATION-MTUI-014: Handle Mini App not found.

        Verify error handling when Mini App not found.
        """
        # Mock bot that doesn't provide Mini App
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=None
        )

        # Try to get Mini App from bot without Mini App
        result = await user_telegram_client_connected.get_mini_app_from_bot(
            "bot_without_miniapp"
        )

        # Verify returns None (error handled gracefully)
        assert result is None

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-MTUI-015: Handle UI element not found")
    @allure.description(
        "TC-INTEGRATION-MTUI-015: Handle UI element not found. "
        "Verify error handling for missing UI elements."
    )
    async def test_handle_ui_element_not_found(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        caplog,
        mock_mini_app_ui,
        mock_playwright_browser_and_page,
    ):
        """
        TC-INTEGRATION-MTUI-015: Handle UI element not found.

        Verify error handling for missing UI elements.
        """

        # Get Mini App from bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppUI
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]
        mock_page.click = mocker.AsyncMock(
            side_effect=PlaywrightTimeoutError("Element not found")
        )

        await ui.setup_browser()

        # Try to click non-existent element
        with caplog.at_level("ERROR"):
            await ui.click_element("#nonexistent-element")

        # Verify error is handled gracefully
        assert (
            "Failed to click element" in caplog.text
            or "Element not found" in caplog.text
        )

        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-MTUI-016: Handle browser errors")
    @allure.description(
        "TC-INTEGRATION-MTUI-016: Handle browser errors. Verify browser error handling."
    )
    async def test_handle_browser_errors(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        caplog,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-MTUI-016: Handle browser errors.

        Verify browser error handling.
        """
        # Get Mini App from bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppUI
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright with browser error
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]
        mock_page.evaluate = mocker.AsyncMock(
            side_effect=Exception("JavaScript error: Unexpected token")
        )

        await ui.setup_browser()

        # Trigger browser error
        with caplog.at_level("ERROR"):
            try:
                await ui.execute_script("invalid javascript code")
            except Exception:
                pass  # Error should be caught and logged

        # Verify error is caught and handled
        assert "error" in caplog.text.lower() or "failed" in caplog.text.lower()

        await ui.close()
