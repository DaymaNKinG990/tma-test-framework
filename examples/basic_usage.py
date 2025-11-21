"""
Basic usage example of TMA Framework.

This example demonstrates the basic usage of TMA Framework with
separate MiniAppApi and MiniAppUI classes.
"""

import asyncio
import os
from tma_test_framework.mini_app import MiniAppApi, MiniAppUI
from tma_test_framework.config import Config


async def main():
    """Main function demonstrating basic usage."""

    # Create configuration
    config = Config(
        api_id=int(os.getenv("TMA_API_ID", "12345678")),
        api_hash=os.getenv("TMA_API_HASH", "0123456789abcdef0123456789abcdef"),
        session_string=os.getenv("TMA_SESSION_STRING"),
        log_level="INFO",
    )
    bot_token = os.getenv("TMA_BOT_TOKEN", "123456789:ABCdefGHIjklMNOpqrsTUVwxyz")

    # Note: TelegramBot class is not available in this version
    # Using direct Mini App URL for demonstration
    mini_app_url = "https://t.me/mybot/app?start=test"
    print(f"Mini App URL: {mini_app_url}")

    try:
        # Example 1: API Testing
        print("\n=== Example 1: API Testing ===")
        async with MiniAppApi(mini_app_url, config) as api:
            # Test API endpoints
            result = await api.make_request("/api/status", "GET")
            print(f"API Test: {'PASSED' if result.success else 'FAILED'}")
            print(f"Status Code: {result.status_code}")
            print(f"Response Time: {result.response_time:.3f}s")

            # Validate initData
            sample_init_data = "user=%7B%22id%22%3A123%2C%22first_name%22%3A%22Test%22%7D&auth_date=1234567890&hash=test_hash"
            is_valid = await api.validate_init_data(sample_init_data, bot_token)
            print(f"InitData validation: {'VALID' if is_valid else 'INVALID'}")

        # Example 2: UI Testing
        print("\n=== Example 2: UI Testing ===")
        async with MiniAppUI(mini_app_url, config) as ui:
            # Setup browser and navigate
            await ui.setup_browser()
            await ui.page.goto(mini_app_url, wait_until="networkidle")

            # Basic UI interactions
            print("Testing UI interactions...")
            await ui.fill_input("#username", "test_user")
            await ui.click_element("#submit-button")
            await ui.take_screenshot("basic_ui_test.png")

            # Get page information
            title = await ui.get_page_title()
            url = await ui.get_page_url()
            print(f"Page title: {title}")
            print(f"Page URL: {url}")

        print("\nBasic usage example completed!")

    finally:
        # Cleanup is handled by context managers
        pass


if __name__ == "__main__":
    asyncio.run(main())
