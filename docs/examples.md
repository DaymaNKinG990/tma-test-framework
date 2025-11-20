# Examples

This document provides comprehensive examples of using TMA Framework for various testing scenarios.

## Table of Contents

- [Basic Usage](#basic-usage)
- [API Testing](#api-testing)
- [UI Testing](#ui-testing)
- [Error Handling](#error-handling)
- [Configuration Examples](#configuration-examples)
- [Advanced Patterns](#advanced-patterns)
- [Real-world Scenarios](#real-world-scenarios)

## Basic Usage

### Simple User Simulation

> **Note:** The following example demonstrates raw Telethon client usage for basic operations. This is **not** using TMA Framework helpers.
>
> For Mini App testing with TMA Framework, use the framework's classes instead:
> - **`Config`** - Configuration management for API credentials and session data
> - **`MiniAppApi`** - API testing utilities for making requests to Mini App endpoints
> - **`MiniAppUI`** - UI testing utilities for interacting with Mini App interfaces
>
> See the [API Testing](#api-testing) and [UI Testing](#ui-testing) sections below for examples using TMA Framework utilities.

```python
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

async def basic_user_example():
    # Initialize Telegram client with session string
    api_id = 12345  # Your API ID from https://my.telegram.org
    api_hash = "your_api_hash"  # Your API hash
    session_string = "your_session_string"  # Session string from StringSession

    async with TelegramClient(
        StringSession(session_string),
        api_id,
        api_hash
    ) as client:
        # Get user information
        user_info = await client.get_me()
        print(f"User: {user_info.first_name} (@{user_info.username})")

        # Send a message
        message = await client.send_message(
            entity="me",
            message="Hello from TMA Framework!"
        )
        print(f"Message sent with ID: {message.id}")

asyncio.run(basic_user_example())
```

### Getting Mini App from Bot

> **Note:** This is an executable TMA Framework example. The `UserTelegramClient` class extends Telethon's `TelegramClient` with Mini App-specific capabilities. For basic Telegram operations (sending messages, getting user info), you can use raw Telethon. However, for Mini App interactions (getting Mini App URLs from bots, handling Web App data), use TMA Framework's `UserTelegramClient` as it provides specialized methods like `get_mini_app_from_bot()` that are not available in standard Telethon.

```python
# TMA Framework example - executable code
import asyncio
from tma_framework import UserTelegramClient, Config  # TMA Framework package

async def get_mini_app_example():
    config = Config(
        api_id=12345,
        api_hash="your_api_hash",
        session_string="your_session_string"
    )

    async with UserTelegramClient(config) as client:
        # Get Mini App from bot interaction
        # This method is specific to TMA Framework
        mini_app = await client.get_mini_app_from_bot(
            bot_username="example_bot",
            start_param="test_param"
        )

        if mini_app:
            print(f"Mini App URL: {mini_app.url}")
            print(f"Start Param: {mini_app.start_param}")
        else:
            print("No Mini App found")

asyncio.run(get_mini_app_example())
```

## API Testing

### Basic API Testing

```python
import asyncio
from tma_framework import MiniAppApi, Config

async def basic_api_test():
    config = Config.from_env()

    async with MiniAppApi("https://your-mini-app.com", config) as api:
        # Test GET endpoint
        result = await api.make_request("/api/status", "GET")
        print(f"Status: {result.status_code}")
        print(f"Success: {result.success}")
        print(f"Response time: {result.response_time:.3f}s")

        if result.error_message:
            print(f"Error: {result.error_message}")

asyncio.run(basic_api_test())
```

### POST Request with Data

```python
import asyncio
from tma_framework import MiniAppApi, Config

async def post_request_example():
    config = Config.from_env()

    async with MiniAppApi("https://your-mini-app.com", config) as api:
        # Test POST endpoint with data
        data = {
            "username": "test_user",
            "email": "test@example.com",
            "preferences": {
                "theme": "dark",
                "notifications": True
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer token123"
        }

        result = await api.make_request(
            "/api/users",
            "POST",
            data=data,
            headers=headers
        )

        print(f"Response: {result.status_code}")
        print(f"Success: {result.success}")

asyncio.run(post_request_example())
```

### initData Validation

```python
import asyncio
from tma_framework import MiniAppApi, Config

async def init_data_validation_example():
    config = Config.from_env()

    # Sample initData from Telegram WebApp
    init_data = (
        "user=%7B%22id%22%3A123456789%2C%22first_name%22%3A%22John%22%2C"
        "%22last_name%22%3A%22Doe%22%2C%22username%22%3A%22johndoe%22%7D"
        "&chat_instance=-1234567890123456789"
        "&chat_type=private"
        "&auth_date=1640995200"
        "&hash=abc123def456..."
    )

    async with MiniAppApi("https://your-mini-app.com", config) as api:
        is_valid = await api.validate_init_data(init_data, config.bot_token)
        print(f"InitData valid: {is_valid}")

asyncio.run(init_data_validation_example())
```

### Multiple API Endpoints

```python
import asyncio
from tma_framework import MiniAppApi, Config

async def multiple_endpoints_example():
    config = Config.from_env()

    endpoints = [
        ("/api/health", "GET"),
        ("/api/users", "GET"),
        ("/api/profile", "GET"),
        ("/api/settings", "GET"),
    ]

    async with MiniAppApi("https://your-mini-app.com", config) as api:
        results = []

        for endpoint, method in endpoints:
            result = await api.make_request(endpoint, method)
            results.append({
                "endpoint": endpoint,
                "method": method,
                "status": result.status_code,
                "success": result.success,
                "time": result.response_time
            })

        # Print results
        for result in results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['method']} {result['endpoint']} - "
                  f"{result['status']} ({result['time']:.3f}s)")

asyncio.run(multiple_endpoints_example())
```

## UI Testing

### Basic UI Testing

```python
import asyncio
from tma_framework import MiniAppUI, Config

async def basic_ui_test():
    config = Config.from_env()

    async with MiniAppUI("https://your-mini-app.com", config) as ui:
        # Setup browser and navigate
        await ui.setup_browser()
        await ui.page.goto("https://your-mini-app.com", wait_until="networkidle")

        # Take initial screenshot
        await ui.take_screenshot("initial_state.png")

        # Get page information
        title = await ui.get_page_title()
        url = await ui.get_page_url()
        print(f"Page: {title} - {url}")

asyncio.run(basic_ui_test())
```

### Form Interaction

```python
import asyncio
from tma_framework import MiniAppUI, Config

async def form_interaction_example():
    config = Config.from_env()

    async with MiniAppUI("https://your-mini-app.com", config) as ui:
        await ui.setup_browser()
        await ui.page.goto("https://your-mini-app.com", wait_until="networkidle")

        # Fill form fields
        await ui.fill_input("#username", "test_user")
        await ui.fill_input("#email", "test@example.com")
        await ui.fill_input("#password", "secure_password")

        # Select dropdown option
        await ui.select_option("#country", "US")

        # Check checkbox
        await ui.check_checkbox("#terms")

        # Take screenshot before submission
        await ui.take_screenshot("form_filled.png")

        # Submit form
        await ui.click_element("#submit-button")

        # Wait for success message
        await ui.wait_for_element("#success-message", timeout=10000)

        # Take final screenshot
        await ui.take_screenshot("form_submitted.png")

asyncio.run(form_interaction_example())
```

### Advanced UI Interactions

```python
import asyncio
from tma_framework import MiniAppUI, Config

async def advanced_ui_interactions():
    config = Config.from_env()

    async with MiniAppUI("https://your-mini-app.com", config) as ui:
        await ui.setup_browser()
        await ui.page.goto("https://your-mini-app.com", wait_until="networkidle")

        # Mouse interactions
        await ui.hover_element("#menu-item")
        await ui.double_click_element("#file-item")
        await ui.right_click_element("#context-menu-target")

        # Keyboard interactions
        await ui.type_text("Hello, World!")
        await ui.press_key("Enter")
        await ui.press_key("Tab")
        await ui.press_key("Escape")

        # File upload
        await ui.upload_file("#file-input", "test_file.txt")

        # Scroll to element
        await ui.scroll_to_element("#footer")

        # Wait for navigation
        await ui.wait_for_navigation(timeout=5000)

        # Execute JavaScript
        result = await ui.execute_script("return document.title;")
        print(f"Page title via JS: {result}")

        # Get element information
        element_text = await ui.get_element_text("h1")
        element_class = await ui.get_element_attribute_value("button", "class")

        print(f"Element text: {element_text}")
        print(f"Element class: {element_class}")

asyncio.run(advanced_ui_interactions())
```

## Error Handling

### Robust API Testing

```python
import asyncio
from tma_framework import MiniAppApi, Config

async def robust_api_testing():
    config = Config.from_env()

    endpoints = [
        "/api/health",
        "/api/users",
        "/api/nonexistent",
        "/api/error"
    ]

    async with MiniAppApi("https://your-mini-app.com", config) as api:
        for endpoint in endpoints:
            try:
                result = await api.make_request(endpoint, "GET")

                if result.success:
                    print(f"✅ {endpoint}: {result.status_code}")
                else:
                    print(f"❌ {endpoint}: {result.status_code} - {result.error_message}")

            except Exception as e:
                print(f"💥 {endpoint}: Exception - {e}")

asyncio.run(robust_api_testing())
```

### UI Testing with Error Recovery

```python
import asyncio
from tma_framework import MiniAppUI, Config

async def ui_error_recovery():
    config = Config.from_env()

    async with MiniAppUI("https://your-mini-app.com", config) as ui:
        await ui.setup_browser()
        await ui.page.goto("https://your-mini-app.com", wait_until="networkidle")

        # Try to interact with elements that might not exist
        selectors = [
            "#username",
            "#email",
            "#nonexistent-element",
            "#submit-button"
        ]

        for selector in selectors:
            try:
                await ui.fill_input(selector, "test_value")
                print(f"✅ Filled {selector}")
            except Exception as e:
                print(f"❌ Failed to fill {selector}: {e}")

        # Take screenshot regardless of errors
        await ui.take_screenshot("error_recovery_test.png")

asyncio.run(ui_error_recovery())
```

### Retry Logic

```python
import asyncio
from tma_framework import MiniAppApi, Config

async def retry_logic_example():
    config = Config.from_env()

    async with MiniAppApi("https://your-mini-app.com", config) as api:
        max_retries = 3
        retry_delay = 1.0

        for attempt in range(max_retries):
            try:
                result = await api.make_request("/api/unstable", "GET")

                if result.success:
                    print(f"✅ Success on attempt {attempt + 1}")
                    break
                else:
                    print(f"❌ Attempt {attempt + 1} failed: {result.error_message}")

            except Exception as e:
                print(f"💥 Attempt {attempt + 1} exception: {e}")

            if attempt < max_retries - 1:
                print(f"⏳ Waiting {retry_delay}s before retry...")
                await asyncio.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
        else:
            print("❌ All retry attempts failed")

asyncio.run(retry_logic_example())
```

## Configuration Examples

### Environment-based Configuration

```python
import os
from tma_framework import Config

# Using environment variables
config = Config.from_env()

# Custom environment variables
config = Config(
    bot_token=os.getenv("TMA_BOT_TOKEN"),
    log_level=os.getenv("TMA_LOG_LEVEL", "INFO"),
    timeout=float(os.getenv("TMA_TIMEOUT", "30")),
    retry_count=int(os.getenv("TMA_RETRY_COUNT", "3"))
)
```

### Multiple Environment Configurations

```python
import os
from tma_framework import Config

def get_config_for_environment(env: str) -> Config:
    """Get configuration for specific environment."""

    if env == "development":
        return Config(
            bot_token=os.getenv("DEV_BOT_TOKEN"),
            log_level="DEBUG",
            timeout=60.0,
            retry_count=1
        )
    elif env == "staging":
        return Config(
            bot_token=os.getenv("STAGING_BOT_TOKEN"),
            log_level="INFO",
            timeout=30.0,
            retry_count=3
        )
    elif env == "production":
        return Config(
            bot_token=os.getenv("PROD_BOT_TOKEN"),
            log_level="WARNING",
            timeout=15.0,
            retry_count=5
        )
    else:
        raise ValueError(f"Unknown environment: {env}")

# Usage
config = get_config_for_environment("development")
```

## Advanced Patterns

### Parallel Testing

```python
import asyncio
from tma_framework import MiniAppApi, Config

async def parallel_api_testing():
    config = Config.from_env()

    endpoints = [
        "/api/health",
        "/api/users",
        "/api/profile",
        "/api/settings",
        "/api/notifications"
    ]

    async def test_endpoint(endpoint: str):
        async with MiniAppApi("https://your-mini-app.com", config) as api:
            result = await api.make_request(endpoint, "GET")
            return {
                "endpoint": endpoint,
                "status": result.status_code,
                "success": result.success,
                "time": result.response_time
            }

    # Run all tests in parallel
    tasks = [test_endpoint(endpoint) for endpoint in endpoints]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Process results
    for result in results:
        if isinstance(result, Exception):
            print(f"💥 Exception: {result}")
        else:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['endpoint']} - "
                  f"{result['status']} ({result['time']:.3f}s)")

asyncio.run(parallel_api_testing())
```

### Test Suite Pattern

```python
import asyncio
from typing import List, Dict, Any
from tma_framework import MiniAppApi, MiniAppUI, Config

class MiniAppTestSuite:
    def __init__(self, config: Config):
        self.config = config
        self.results: List[Dict[str, Any]] = []

    async def run_api_tests(self, url: str) -> List[Dict[str, Any]]:
        """Run all API tests."""
        tests = [
            self.test_health_endpoint,
            self.test_users_endpoint,
            self.test_auth_endpoint
        ]

        async with MiniAppApi(url, self.config) as api:
            for test in tests:
                try:
                    result = await test(api)
                    self.results.append(result)
                except Exception as e:
                    self.results.append({
                        "test": test.__name__,
                        "status": "error",
                        "error": str(e)
                    })

        return self.results

    async def test_health_endpoint(self, api: MiniAppApi) -> Dict[str, Any]:
        """Test health endpoint."""
        result = await api.make_request("/api/health", "GET")
        return {
            "test": "health_endpoint",
            "status": "passed" if result.success else "failed",
            "status_code": result.status_code,
            "response_time": result.response_time
        }

    async def test_users_endpoint(self, api: MiniAppApi) -> Dict[str, Any]:
        """Test users endpoint."""
        result = await api.make_request("/api/users", "GET")
        return {
            "test": "users_endpoint",
            "status": "passed" if result.success else "failed",
            "status_code": result.status_code,
            "response_time": result.response_time
        }

    async def test_auth_endpoint(self, api: MiniAppApi) -> Dict[str, Any]:
        """Test authentication endpoint."""
        data = {"username": "test", "password": "test"}
        result = await api.make_request("/api/auth", "POST", data=data)
        return {
            "test": "auth_endpoint",
            "status": "passed" if result.success else "failed",
            "status_code": result.status_code,
            "response_time": result.response_time
        }

    async def run_ui_tests(self, url: str) -> List[Dict[str, Any]]:
        """Run all UI tests."""
        async with MiniAppUI(url, self.config) as ui:
            await ui.setup_browser()
            await ui.page.goto(url, wait_until="networkidle")

            # Run UI tests
            await self.test_login_form(ui)
            await self.test_navigation(ui)
            await self.test_responsive_design(ui)

        return self.results

    async def test_login_form(self, ui: MiniAppUI):
        """Test login form functionality."""
        try:
            await ui.fill_input("#username", "test_user")
            await ui.fill_input("#password", "test_password")
            await ui.click_element("#login-button")
            await ui.wait_for_element("#dashboard", timeout=10000)

            self.results.append({
                "test": "login_form",
                "status": "passed"
            })
        except Exception as e:
            self.results.append({
                "test": "login_form",
                "status": "failed",
                "error": str(e)
            })

    async def test_navigation(self, ui: MiniAppUI):
        """Test navigation functionality."""
        try:
            await ui.click_element("#nav-profile")
            await ui.wait_for_element("#profile-page", timeout=5000)

            await ui.click_element("#nav-settings")
            await ui.wait_for_element("#settings-page", timeout=5000)

            self.results.append({
                "test": "navigation",
                "status": "passed"
            })
        except Exception as e:
            self.results.append({
                "test": "navigation",
                "status": "failed",
                "error": str(e)
            })

    async def test_responsive_design(self, ui: MiniAppUI):
        """Test responsive design."""
        try:
            # Test mobile viewport
            await ui.page.set_viewport_size({"width": 375, "height": 667})
            await ui.take_screenshot("mobile_view.png")

            # Test tablet viewport
            await ui.page.set_viewport_size({"width": 768, "height": 1024})
            await ui.take_screenshot("tablet_view.png")

            # Test desktop viewport
            await ui.page.set_viewport_size({"width": 1920, "height": 1080})
            await ui.take_screenshot("desktop_view.png")

            self.results.append({
                "test": "responsive_design",
                "status": "passed"
            })
        except Exception as e:
            self.results.append({
                "test": "responsive_design",
                "status": "failed",
                "error": str(e)
            })

    def print_results(self):
        """Print test results."""
        print("\n=== Test Results ===")
        for result in self.results:
            status = "✅" if result["status"] == "passed" else "❌"
            print(f"{status} {result['test']}")
            if "error" in result:
                print(f"   Error: {result['error']}")

# Usage
async def run_test_suite():
    config = Config.from_env()
    suite = MiniAppTestSuite(config)

    # Run API tests
    await suite.run_api_tests("https://your-mini-app.com")

    # Run UI tests
    await suite.run_ui_tests("https://your-mini-app.com")

    # Print results
    suite.print_results()

asyncio.run(run_test_suite())
```

## Real-world Scenarios

### E-commerce Mini App Testing

```python
import asyncio
from tma_framework import MiniAppApi, MiniAppUI, Config

async def ecommerce_testing():
    config = Config.from_env()

    # Test product API
    async with MiniAppApi("https://shop-mini-app.com", config) as api:
        # Test product listing
        products = await api.make_request("/api/products", "GET")
        print(f"Products API: {products.status_code}")

        # Test product details
        product = await api.make_request("/api/products/123", "GET")
        print(f"Product details: {product.status_code}")

        # Test add to cart
        cart_data = {"product_id": 123, "quantity": 2}
        cart = await api.make_request("/api/cart", "POST", data=cart_data)
        print(f"Add to cart: {cart.status_code}")

    # Test shopping flow UI
    async with MiniAppUI("https://shop-mini-app.com", config) as ui:
        await ui.setup_browser()
        await ui.page.goto("https://shop-mini-app.com", wait_until="networkidle")

        # Browse products
        await ui.click_element("#products-tab")
        await ui.wait_for_element(".product-item", timeout=10000)

        # Select product
        await ui.click_element(".product-item:first-child")
        await ui.wait_for_element("#product-details", timeout=5000)

        # Add to cart
        await ui.click_element("#add-to-cart")
        await ui.wait_for_element("#cart-notification", timeout=5000)

        # Go to cart
        await ui.click_element("#cart-icon")
        await ui.wait_for_element("#cart-items", timeout=5000)

        # Proceed to checkout
        await ui.click_element("#checkout-button")
        await ui.wait_for_element("#checkout-form", timeout=5000)

        # Fill checkout form
        await ui.fill_input("#name", "John Doe")
        await ui.fill_input("#email", "john@example.com")
        await ui.fill_input("#address", "123 Main St")

        # Take final screenshot
        await ui.take_screenshot("checkout_form.png")

asyncio.run(ecommerce_testing())
```

### Social Media Mini App Testing

```python
import asyncio
from tma_framework import MiniAppApi, MiniAppUI, Config

async def social_media_testing():
    config = Config.from_env()

    # Test social API
    async with MiniAppApi("https://social-mini-app.com", config) as api:
        # Test user profile
        profile = await api.make_request("/api/profile", "GET")
        print(f"Profile API: {profile.status_code}")

        # Test posts feed
        posts = await api.make_request("/api/posts", "GET")
        print(f"Posts API: {posts.status_code}")

        # Test create post
        post_data = {"content": "Hello from TMA Framework!", "type": "text"}
        new_post = await api.make_request("/api/posts", "POST", data=post_data)
        print(f"Create post: {new_post.status_code}")

    # Test social interactions UI
    async with MiniAppUI("https://social-mini-app.com", config) as ui:
        await ui.setup_browser()
        await ui.page.goto("https://social-mini-app.com", wait_until="networkidle")

        # Login
        await ui.fill_input("#username", "test_user")
        await ui.fill_input("#password", "test_password")
        await ui.click_element("#login-button")
        await ui.wait_for_element("#feed", timeout=10000)

        # Create post
        await ui.click_element("#create-post-button")
        await ui.fill_input("#post-content", "Testing with TMA Framework!")
        await ui.click_element("#publish-button")
        await ui.wait_for_element("#post-published", timeout=5000)

        # Like a post
        await ui.click_element(".like-button:first-child")
        await ui.wait_for_element(".like-button.liked", timeout=3000)

        # Comment on post
        await ui.click_element(".comment-button:first-child")
        await ui.fill_input("#comment-input", "Great post!")
        await ui.click_element("#submit-comment")
        await ui.wait_for_element(".comment", timeout=5000)

        # Take screenshot of feed
        await ui.take_screenshot("social_feed.png")

asyncio.run(social_media_testing())
```

### Game Mini App Testing

```python
import asyncio
from tma_framework import MiniAppApi, MiniAppUI, Config

async def game_testing():
    config = Config.from_env()

    # Test game API
    async with MiniAppApi("https://game-mini-app.com", config) as api:
        # Test game state
        game_state = await api.make_request("/api/game/state", "GET")
        print(f"Game state: {game_state.status_code}")

        # Test save score
        score_data = {"score": 1500, "level": 5, "time": 120}
        save_result = await api.make_request("/api/game/save", "POST", data=score_data)
        print(f"Save score: {save_result.status_code}")

        # Test leaderboard
        leaderboard = await api.make_request("/api/leaderboard", "GET")
        print(f"Leaderboard: {leaderboard.status_code}")

    # Test game UI
    async with MiniAppUI("https://game-mini-app.com", config) as ui:
        await ui.setup_browser()
        await ui.page.goto("https://game-mini-app.com", wait_until="networkidle")

        # Start game
        await ui.click_element("#start-game")
        await ui.wait_for_element("#game-canvas", timeout=10000)

        # Simulate game interactions
        await ui.press_key("ArrowUp")
        await ui.press_key("ArrowRight")
        await ui.press_key("Space")

        # Wait for game over
        await ui.wait_for_element("#game-over", timeout=30000)

        # Enter high score
        await ui.fill_input("#player-name", "TMA Tester")
        await ui.click_element("#save-score")
        await ui.wait_for_element("#score-saved", timeout=5000)

        # View leaderboard
        await ui.click_element("#leaderboard")
        await ui.wait_for_element("#leaderboard-list", timeout=5000)

        # Take screenshot
        await ui.take_screenshot("game_leaderboard.png")

asyncio.run(game_testing())
```

These examples demonstrate the flexibility and power of TMA Framework for testing various types of Telegram Mini Apps. The framework's separation of concerns allows you to focus on either API testing, UI testing, or both, depending on your needs.
