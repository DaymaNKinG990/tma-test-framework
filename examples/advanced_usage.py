"""
Advanced usage example of TMA Framework.

This example demonstrates advanced usage patterns with separate
MiniAppApi and MiniAppUI classes, including error handling,
retry logic, and comprehensive testing scenarios.
"""

import asyncio
import os
from tma_test_framework.mini_app import MiniAppApi, MiniAppUI
from tma_test_framework.config import Config


async def main():
    """Main function demonstrating advanced usage."""

    # Create configuration with custom settings
    config = Config(
        api_id=int(os.getenv("TMA_API_ID", "12345678")),
        api_hash=os.getenv("TMA_API_HASH", "0123456789abcdef0123456789abcdef"),
        session_string=os.getenv("TMA_SESSION_STRING"),
        log_level="DEBUG",
        timeout=30,
        retry_count=3,
        retry_delay=1.0,
    )
    bot_token = os.getenv("TMA_BOT_TOKEN", "123456789:ABCdefGHIjklMNOpqrsTUVwxyz")

    # Note: TelegramBot class is not available in this version
    # Using direct Mini App URL for demonstration
    mini_app_url = "https://t.me/mybot/app?start=test"
    print(f"Mini App URL: {mini_app_url}")

    try:
        # Example 1: Advanced API Testing
        print("\n=== Example 1: Advanced API Testing ===")
        async with MiniAppApi(mini_app_url, config) as api:
            # Test multiple API endpoints
            endpoints = [
                ("/api/status", "GET"),
                ("/api/users", "GET"),
                ("/api/data", "POST", {"key": "value"}),
                ("/api/upload", "POST", {"file": "test.txt"}),
            ]

            for endpoint_info in endpoints:
                if len(endpoint_info) == 2:
                    endpoint, method = endpoint_info
                    data = None
                else:
                    endpoint, method, data = endpoint_info

                print(f"Testing {method} {endpoint}...")
                result = await api.make_request(endpoint, method, data)

                print(f"  Status: {'PASSED' if result.success else 'FAILED'}")
                print(f"  Code: {result.status_code}")
                print(f"  Time: {result.response_time:.3f}s")

                if not result.success and result.error_message:
                    print(f"  Error: {result.error_message}")

            # Validate initData with retry logic
            print("\nTesting initData validation with retry...")
            sample_init_data = "user=%7B%22id%22%3A123%2C%22first_name%22%3A%22Test%22%7D&auth_date=1234567890&hash=test_hash"

            for attempt in range(3):
                try:
                    is_valid = await api.validate_init_data(sample_init_data, bot_token)
                    print(
                        f"  Attempt {attempt + 1}: {'VALID' if is_valid else 'INVALID'}"
                    )
                    break
                except Exception as e:
                    print(f"  Attempt {attempt + 1} failed: {e}")
                    if attempt < 2:
                        await asyncio.sleep(1)

        # Example 2: Advanced UI Testing
        print("\n=== Example 2: Advanced UI Testing ===")
        async with MiniAppUI(mini_app_url, config) as ui:
            # Setup browser and navigate
            await ui.setup_browser()
            await ui.page.goto(mini_app_url, wait_until="networkidle")

            # Comprehensive UI testing
            print("Running comprehensive UI tests...")

            # Form interactions
            print("Testing form interactions...")
            await ui.fill_input("#name", "John Doe")
            await ui.fill_input("#email", "john@example.com")
            await ui.select_option("#country", "US")
            await ui.check_checkbox("#terms")

            # Mouse interactions
            print("Testing mouse interactions...")
            await ui.hover_element("#hover-target")
            await ui.double_click_element("#double-click-target")
            await ui.right_click_element("#context-menu-target")

            # Keyboard interactions
            print("Testing keyboard interactions...")
            await ui.type_text("Hello, World!")
            await ui.press_key("Enter")

            # File upload
            print("Testing file upload...")
            await ui.upload_file("#file-input", "test_file.txt")

            # Element information
            print("Getting element information...")
            element_text = await ui.get_element_text("#status-message")
            element_class = await ui.get_element_attribute_value(
                "#main-button", "class"
            )

            print(f"  Element text: {element_text or 'N/A'}")
            print(f"  Element class: {element_class or 'N/A'}")

            # Page information
            print("Getting page information...")
            page_title = await ui.get_page_title()
            page_url = await ui.get_page_url()

            print(f"  Page title: {page_title}")
            print(f"  Page URL: {page_url}")

            # JavaScript execution
            print("Testing JavaScript execution...")
            script_result = await ui.execute_script("return document.title;")
            print(f"  JavaScript result: {script_result}")

            # Screenshots
            print("Taking screenshots...")
            await ui.take_screenshot("advanced_ui_screenshot.png")

            print("Advanced UI interactions completed")

        # Example 3: Error Handling and Recovery
        print("\n=== Example 3: Error Handling and Recovery ===")

        # Test with invalid URL
        print("Testing error handling with invalid URL...")
        async with MiniAppApi(
            "https://invalid-url-that-does-not-exist.com", config
        ) as api:
            result = await api.make_request("/api/test", "GET")
            print(f"  Invalid URL test: {'PASSED' if result.success else 'FAILED'}")
            print(f"  Error message: {result.error_message}")

        # Test UI with timeout
        print("Testing UI timeout handling...")
        async with MiniAppUI(mini_app_url, config) as ui:
            await ui.setup_browser()
            await ui.page.goto(mini_app_url, wait_until="networkidle")

            try:
                # This will timeout since element doesn't exist
                await ui.wait_for_element("#non-existent-element", timeout=2000)
                print("  Timeout test: FAILED (should have timed out)")
            except Exception as e:
                print(f"  Timeout test: PASSED (expected timeout: {e})")

        # Example 4: Performance Testing
        print("\n=== Example 4: Performance Testing ===")

        # API performance test
        print("Testing API performance...")
        async with MiniAppApi(mini_app_url, config) as api:
            start_time = asyncio.get_event_loop().time()

            # Make multiple concurrent requests
            tasks = []
            for i in range(5):
                task = api.make_request(f"/api/test-{i}", "GET")
                tasks.append(task)

            results = await asyncio.gather(*tasks, return_exceptions=True)

            end_time = asyncio.get_event_loop().time()
            total_time = end_time - start_time

            print(f"  Made 5 concurrent requests in {total_time:.3f}s")
            print(f"  Average time per request: {total_time / 5:.3f}s")

            successful_requests = sum(
                1
                for r in results
                if not isinstance(r, Exception) and hasattr(r, "success") and r.success
            )
            print(f"  Successful requests: {successful_requests}/5")

        # UI performance test
        print("Testing UI performance...")
        async with MiniAppUI(mini_app_url, config) as ui:
            await ui.setup_browser()

            start_time = asyncio.get_event_loop().time()
            await ui.page.goto(mini_app_url, wait_until="networkidle")
            end_time = asyncio.get_event_loop().time()

            load_time = end_time - start_time
            print(f"  Page load time: {load_time:.3f}s")

            # Test screenshot performance
            start_time = asyncio.get_event_loop().time()
            await ui.take_screenshot("performance_test.png")
            end_time = asyncio.get_event_loop().time()

            screenshot_time = end_time - start_time
            print(f"  Screenshot time: {screenshot_time:.3f}s")

        print("\nAdvanced usage example completed!")

    finally:
        # Cleanup is handled by context managers
        pass


if __name__ == "__main__":
    asyncio.run(main())
