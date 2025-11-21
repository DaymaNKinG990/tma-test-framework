"""
Telegram Mini App UI testing client using Playwright.
"""

# Python imports
from typing import Optional, Any, Self
from playwright.async_api import async_playwright, Browser, Page, Playwright

# Local imports
from .base import BaseMiniApp
from ..config import Config


class MiniAppUI(BaseMiniApp):
    """
    Telegram Mini App UI testing client.

    Provides comprehensive UI testing capabilities using Playwright:
    - Element interaction (click, fill, wait)
    - Screenshots and visual testing
    - JavaScript execution
    - Navigation and page state
    - Advanced Playwright features
    """

    def __init__(self, url: str, config: Optional[Config] = None) -> None:
        """
        Initialize Mini App UI client.

        Args:
            url: Mini App URL
            config: Configuration object
        """
        super().__init__(url, config)
        self._playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def close(self) -> None:
        """Close browser and stop Playwright."""
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None
        self.page = None

    async def setup_browser(self) -> Self:
        """Setup Playwright browser for UI testing."""
        if self.browser:
            self.logger.debug("Browser already setup")
        else:
            # Verify URL is set
            if not self.url or not isinstance(self.url, str) or not self.url.strip():
                error_msg = "URL is not set or is empty. Cannot setup browser without a valid URL."
                self.logger.error(error_msg)
                raise ValueError(error_msg)

            self._playwright = await async_playwright().start()
            self.browser = await self._playwright.chromium.launch(headless=True)
            self.logger.debug("Browser launched")
            self.page = await self.browser.new_page()
            self.logger.debug("New page created")
            # Set user agent to simulate Telegram WebApp
            await self.page.set_extra_http_headers(
                {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }
            )
            self.logger.debug("User agent set")

            # Navigate to the Mini App URL
            try:
                self.logger.debug(f"Navigating to {self.url}")
                await self.page.goto(self.url, wait_until="networkidle")
                self.logger.info(f"Successfully navigated to {self.url}")
            except Exception as e:
                error_msg = f"Failed to navigate to {self.url}: {e}"
                self.logger.error(error_msg)
                raise RuntimeError(error_msg) from e
        return self

    async def click_element(self, selector: str) -> None:
        """
        Click element in Mini App.

        Args:
            selector: CSS selector for element
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.click(selector)
            self.logger.debug(f"Clicked element: {selector}")
        except Exception as e:
            self.logger.error(f"Failed to click element {selector}: {e}")

    async def fill_input(self, selector: str, text: str) -> None:
        """
        Fill input field in Mini App.

        Args:
            selector: CSS selector for input
            text: Text to fill
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.fill(selector, text)
            self.logger.debug(f"Filled input {selector} with: {text}")
        except Exception as e:
            self.logger.error(f"Failed to fill input {selector}: {e}")

    async def wait_for_element(self, selector: str, timeout: int = 5000) -> None:
        """
        Wait for element to appear in Mini App.

        Args:
            selector: CSS selector for element
            timeout: Timeout in milliseconds
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            self.logger.debug(f"Element appeared: {selector}")
        except Exception as e:
            self.logger.error(f"Element {selector} did not appear: {e}")

    async def take_screenshot(self, path: str) -> None:
        """
        Take screenshot of the current page.

        Args:
            path: Path to save screenshot
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.screenshot(path=path)
            self.logger.debug(f"Screenshot saved: {path}")
        except Exception as e:
            self.logger.error(f"Screenshot failed: {e}")

    async def get_element_text(self, selector: str) -> Optional[str]:
        """
        Get text content of an element.

        Args:
            selector: CSS selector for element

        Returns:
            Element text content or None
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return None
        try:
            element = await self.page.query_selector(selector)
            if element:
                text = await element.text_content()
                self.logger.debug(f"Element text ({selector}): {text}")
                return str(text) if text is not None else None
            return None
        except Exception as e:
            self.logger.error(f"Failed to get element text {selector}: {e}")
            return None

    async def get_element_attribute_value(
        self, selector: str, attribute: str
    ) -> Optional[str]:
        """
        Get attribute value of an element.

        Args:
            selector: CSS selector for element
            attribute: Attribute name

        Returns:
            Attribute value or None
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return None
        try:
            element = await self.page.query_selector(selector)
            if element:
                value = await element.get_attribute(attribute)
                self.logger.debug(
                    f"Element attribute ({selector}.{attribute}): {value}"
                )
                return str(value) if value is not None else None
            return None
        except Exception as e:
            self.logger.error(
                f"Failed to get element attribute {selector}.{attribute}: {e}"
            )
            return None

    async def scroll_to_element(self, selector: str) -> None:
        """
        Scroll to element in Mini App.

        Args:
            selector: CSS selector for element
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.locator(selector).scroll_into_view_if_needed()
            self.logger.debug(f"Scrolled to element: {selector}")
        except Exception as e:
            self.logger.error(f"Failed to scroll to element {selector}: {e}")

    async def wait_for_navigation(self, timeout: int = 5000) -> None:
        """
        Wait for page navigation to complete.

        Args:
            timeout: Timeout in milliseconds
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.wait_for_load_state("networkidle", timeout=timeout)
            self.logger.debug("Navigation completed")
        except Exception as e:
            self.logger.error(f"Navigation timeout: {e}")

    async def execute_script(self, script: str) -> Any:
        """
        Execute JavaScript in Mini App.

        Args:
            script: JavaScript code to execute

        Returns:
            Script execution result
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return None
        try:
            result = await self.page.evaluate(script)
            self.logger.debug(f"Script executed, result: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Script execution failed: {e}")
            return None

    async def get_page_title(self) -> str:
        """
        Get page title.

        Returns:
            Page title
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return ""
        try:
            title = await self.page.title()
            self.logger.debug(f"Page title: {title}")
            return str(title)
        except Exception as e:
            self.logger.error(f"Failed to get page title: {e}")
            return ""

    async def get_page_url(self) -> str:
        """
        Get current page URL.

        Returns:
            Current page URL
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return ""
        try:
            url = self.page.url
            self.logger.debug(f"Page URL: {url}")
            return str(url)
        except Exception as e:
            self.logger.error(f"Failed to get page URL: {e}")
            return ""

    async def hover_element(self, selector: str) -> None:
        """
        Hover over element in Mini App.

        Args:
            selector: CSS selector for element
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.hover(selector)
            self.logger.debug(f"Hovered over element: {selector}")
        except Exception as e:
            self.logger.error(f"Failed to hover over element {selector}: {e}")

    async def double_click_element(self, selector: str) -> None:
        """
        Double click element in Mini App.

        Args:
            selector: CSS selector for element
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.dblclick(selector)
            self.logger.debug(f"Double clicked element: {selector}")
        except Exception as e:
            self.logger.error(f"Failed to double click element {selector}: {e}")

    async def right_click_element(self, selector: str) -> None:
        """
        Right click element in Mini App.

        Args:
            selector: CSS selector for element
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.click(selector, button="right")
            self.logger.debug(f"Right clicked element: {selector}")
        except Exception as e:
            self.logger.error(f"Failed to right click element {selector}: {e}")

    async def select_option(self, selector: str, value: str) -> None:
        """
        Select option from dropdown.

        Args:
            selector: CSS selector for select element
            value: Option value to select
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.select_option(selector, value)
            self.logger.debug(f"Selected option {value} in {selector}")
        except Exception as e:
            self.logger.error(f"Failed to select option {value} in {selector}: {e}")

    async def check_checkbox(self, selector: str) -> None:
        """
        Check checkbox in Mini App.

        Args:
            selector: CSS selector for checkbox
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.check(selector)
            self.logger.debug(f"Checked checkbox: {selector}")
        except Exception as e:
            self.logger.error(f"Failed to check checkbox {selector}: {e}")

    async def uncheck_checkbox(self, selector: str) -> None:
        """
        Uncheck checkbox in Mini App.

        Args:
            selector: CSS selector for checkbox
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.uncheck(selector)
            self.logger.debug(f"Unchecked checkbox: {selector}")
        except Exception as e:
            self.logger.error(f"Failed to uncheck checkbox {selector}: {e}")

    async def upload_file(self, selector: str, file_path: str) -> None:
        """
        Upload file to file input.

        Args:
            selector: CSS selector for file input
            file_path: Path to file to upload
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.set_input_files(selector, file_path)
            self.logger.debug(f"Uploaded file {file_path} to {selector}")
        except Exception as e:
            self.logger.error(f"Failed to upload file {file_path} to {selector}: {e}")

    async def press_key(self, key: str) -> None:
        """
        Press key on page.

        Args:
            key: Key to press (e.g., 'Enter', 'Escape', 'Tab')
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.keyboard.press(key)
            self.logger.debug(f"Pressed key: {key}")
        except Exception as e:
            self.logger.error(f"Failed to press key {key}: {e}")

    async def type_text(self, text: str) -> None:
        """
        Type text on page.

        Args:
            text: Text to type
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.keyboard.type(text)
            self.logger.debug(f"Typed text: {text}")
        except Exception as e:
            self.logger.error(f"Failed to type text: {e}")
