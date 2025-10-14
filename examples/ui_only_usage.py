"""
Example: Using only MiniAppUI for UI testing.

This example demonstrates how to use MiniAppUI class independently
for comprehensive UI testing of Telegram Mini Apps.
"""

import asyncio
import os
from tma_framework import MiniAppUI, Config


async def test_mini_app_ui_only():
    """Test Mini App using only UI functionality."""
    
    # Create config
    config = Config(
        bot_token=os.getenv("TMA_BOT_TOKEN", "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"),
        log_level="INFO"
    )
    
    # Initialize UI client
    ui = MiniAppUI("https://example.com/mini-app", config)
    
    try:
        print("=== MiniAppUI Testing ===")
        
        # Setup browser and navigate
        print("\n1. Setting up browser and navigating...")
        await ui.setup_browser()
        await ui.page.goto(ui.url, wait_until="networkidle")
        print("   Browser setup and navigation: [OK]")
        
        # 2. Element interaction
        print("\n2. Testing element interactions...")
        
        # Wait for main content to load
        try:
            await ui.wait_for_element("#main-content", timeout=10000)
            print("   Main content loaded: [OK]")
        except Exception as e:
            print(f"   Main content loaded: [ERROR] - {e}")
        
        # Fill input field
        try:
            await ui.fill_input("#username", "test_user")
            print("   Username input filled: [OK]")
        except Exception as e:
            print(f"   Username input filled: [ERROR] - {e}")
        
        # Click button
        try:
            await ui.click_element("#submit-button")
            print("   Submit button clicked: [OK]")
        except Exception as e:
            print(f"   Submit button clicked: [ERROR] - {e}")
        
        # Wait for success message
        try:
            await ui.wait_for_element("#success-message", timeout=5000)
            print("   Success message shown: [OK]")
        except Exception as e:
            print(f"   Success message shown: [ERROR] - {e}")
        
        # 3. Advanced UI interactions
        print("\n3. Testing advanced UI interactions...")
        
        try:
            await ui.hover_element("#hover-target")
            print("   Element hovered: [OK]")
        except Exception as e:
            print(f"   Element hovered: [ERROR] - {e}")
        
        try:
            await ui.double_click_element("#double-click-target")
            print("   Element double-clicked: [OK]")
        except Exception as e:
            print(f"   Element double-clicked: [ERROR] - {e}")
        
        try:
            await ui.right_click_element("#context-menu-target")
            print("   Element right-clicked: [OK]")
        except Exception as e:
            print(f"   Element right-clicked: [ERROR] - {e}")
        
        # 4. Form interactions
        print("\n4. Testing form interactions...")
        
        try:
            await ui.select_option("#country-select", "US")
            print("   Dropdown option selected: [OK]")
        except Exception as e:
            print(f"   Dropdown option selected: [ERROR] - {e}")
        
        try:
            await ui.check_checkbox("#terms-checkbox")
            print("   Checkbox checked: [OK]")
        except Exception as e:
            print(f"   Checkbox checked: [ERROR] - {e}")
        
        # 5. Keyboard interactions
        print("\n5. Testing keyboard interactions...")
        
        try:
            await ui.type_text("Hello, World!")
            print("   Text typed: [OK]")
        except Exception as e:
            print(f"   Text typed: [ERROR] - {e}")
        
        try:
            await ui.press_key("Enter")
            print("   Enter key pressed: [OK]")
        except Exception as e:
            print(f"   Enter key pressed: [ERROR] - {e}")
        
        # 6. Element information
        print("\n6. Getting element information...")
        element_text = await ui.get_element_text("h1")
        print(f"   H1 text: {element_text}")
        
        element_attribute = await ui.get_element_attribute_value("a", "href")
        print(f"   Link href: {element_attribute}")
        
        # 7. Page information
        print("\n7. Getting page information...")
        page_title = await ui.get_page_title()
        print(f"   Page title: {page_title}")
        
        page_url = await ui.get_page_url()
        print(f"   Page URL: {page_url}")
        
        # 8. Screenshots
        print("\n8. Taking screenshots...")
        try:
            await ui.take_screenshot("custom_screenshot.png")
            print("   Custom screenshot taken: [OK]")
        except Exception as e:
            print(f"   Custom screenshot taken: [ERROR] - {e}")
        
        # 9. JavaScript execution
        print("\n9. Executing JavaScript...")
        try:
            script_result = await ui.execute_script("return 1 + 1;")
            print(f"   JavaScript result: {script_result}")
        except Exception as e:
            print(f"   JavaScript execution: [ERROR] - {e}")
        
        # 10. Navigation
        print("\n10. Testing navigation...")
        try:
            await ui.wait_for_navigation(timeout=5000)
            print("   Navigation completed: [OK]")
        except Exception as e:
            print(f"   Navigation completed: [ERROR] - {e}")
        
        try:
            await ui.scroll_to_element("#footer")
            print("   Scrolled to footer: [OK]")
        except Exception as e:
            print(f"   Scrolled to footer: [ERROR] - {e}")
        
        print("\n=== UI Testing Complete ===")
        
    except Exception as e:
        print(f"[ERROR] Error during UI testing: {e}")
    
    finally:
        await ui.close()
    
    print("\n=== Context Manager Testing ===")
    async with MiniAppUI("https://example.com/mini-app", config) as ui_context:
        await ui_context.setup_browser()
        await ui_context.page.goto("https://example.com/mini-app", wait_until="networkidle")
        await ui_context.take_screenshot("context_manager_screenshot.png")
        print("Screenshot taken in context manager")
    print("Context manager cleanup completed")
    
    print("\n=== Workflow Testing ===")
    async with MiniAppUI("https://example.com/mini-app", config) as ui_workflow:
        print("Step 1: Navigate to Mini App...")
        await ui_workflow.setup_browser()
        await ui_workflow.page.goto("https://example.com/mini-app", wait_until="networkidle")
        print("[OK] Navigated to Mini App")
        
        print("Step 2: Fill form...")
        await ui_workflow.fill_input("#username", "workflow_user")
        await ui_workflow.fill_input("#password", "workflow_pass")
        print("[OK] Form filled")
        
        print("Step 3: Submit form...")
        await ui_workflow.click_element("#login-button")
        print("[OK] Form submitted")
        
        print("Step 4: Wait for success message...")
        try:
            await ui_workflow.wait_for_element("#welcome-message", timeout=10000)
            print("[OK] Success message shown")
        except Exception as e:
            print(f"[ERROR] Success message not shown: {e}")
        
        print("Step 5: Take final screenshot...")
        await ui_workflow.take_screenshot("workflow_complete.png")
        print("[OK] Workflow completed successfully!")
    print("Workflow testing completed")


async def main():
    await test_mini_app_ui_only()
    print("\nAll examples completed!")


if __name__ == "__main__":
    os.environ.setdefault("TMA_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    os.environ.setdefault("TMA_LOG_LEVEL", "INFO")
    asyncio.run(main())