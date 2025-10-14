"""
Basic usage example of TMA Framework.

This example demonstrates the basic usage of TMA Framework with
separate MiniAppApi and MiniAppUI classes.
"""

import asyncio
import os
from tma_framework import TelegramBot, MiniAppApi, MiniAppUI, Config


async def main():
    """Main function demonstrating basic usage."""
    
    # Create configuration
    config = Config(
        bot_token=os.getenv("TMA_BOT_TOKEN", "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"),
        log_level="INFO"
    )
    
    # Initialize Telegram Bot
    bot = TelegramBot(config.bot_token, config)
    
    try:
        # Get bot information
        print("Getting bot information...")
        bot_info = await bot.get_me()
        print(f"Bot: {bot_info.first_name} (@{bot_info.username})")
        
        # Get Mini App from bot
        print("\nGetting Mini App...")
        mini_app_ui = await bot.get_mini_app(user_id=123456789)
        print(f"Mini App URL: {mini_app_ui.url}")
        
        # Example 1: API Testing
        print("\n=== Example 1: API Testing ===")
        async with MiniAppApi(mini_app_ui.url, config) as api:
            # Test API endpoints
            result = await api.make_request("/api/status", "GET")
            print(f"API Test: {'PASSED' if result.success else 'FAILED'}")
            print(f"Status Code: {result.status_code}")
            print(f"Response Time: {result.response_time:.3f}s")
            
            # Validate initData
            sample_init_data = "user=%7B%22id%22%3A123%2C%22first_name%22%3A%22Test%22%7D&auth_date=1234567890&hash=test_hash"
            is_valid = await api.validate_init_data(sample_init_data, config.bot_token)
            print(f"InitData validation: {'VALID' if is_valid else 'INVALID'}")
        
        # Example 2: UI Testing
        print("\n=== Example 2: UI Testing ===")
        async with MiniAppUI(mini_app_ui.url, config) as ui:
            # Setup browser and navigate
            await ui.setup_browser()
            await ui.page.goto(mini_app_ui.url, wait_until="networkidle")
            
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
        # Clean up Bot
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
