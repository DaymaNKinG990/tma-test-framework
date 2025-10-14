# Quick Start Guide

Get up and running with TMA Framework in just a few minutes.

## Basic Setup

### 1. Import the Framework

```python
import asyncio
from tma_framework import TelegramBot, MiniAppApi, MiniAppUI, Config
```

### 2. Create Configuration

```python
# Using environment variables
config = Config.from_env()

# Or create manually
config = Config(
    bot_token="your_bot_token_here",
    log_level="INFO"
)
```

### 3. Initialize Telegram Bot

```python
async def main():
    bot = TelegramBot(config.bot_token, config)
    
    try:
        # Get bot information
        bot_info = await bot.get_me()
        print(f"Bot: {bot_info.first_name} (@{bot_info.username})")
        
        # Get Mini App from bot
        mini_app_ui = await bot.get_mini_app(user_id=123456789)
        print(f"Mini App URL: {mini_app_ui.url}")
        
    finally:
        await bot.close()

asyncio.run(main())
```

## API Testing

Test your Mini App's HTTP API endpoints:

```python
async def test_api():
    config = Config.from_env()
    
    async with MiniAppApi("https://your-mini-app.com", config) as api:
        # Test GET endpoint
        result = await api.make_request("/api/status", "GET")
        print(f"Status: {result.status_code}")
        print(f"Success: {result.success}")
        
        # Test POST endpoint
        result = await api.make_request(
            "/api/data", 
            "POST", 
            data={"key": "value"}
        )
        print(f"Response: {result.response_time:.3f}s")
        
        # Validate initData
        is_valid = await api.validate_init_data(init_data, config.bot_token)
        print(f"InitData valid: {is_valid}")

asyncio.run(test_api())
```

## UI Testing

Test your Mini App's user interface:

```python
async def test_ui():
    config = Config.from_env()
    
    async with MiniAppUI("https://your-mini-app.com", config) as ui:
        # Setup browser and navigate
        await ui.setup_browser()
        await ui.page.goto("https://your-mini-app.com", wait_until="networkidle")
        
        # Basic interactions
        await ui.fill_input("#username", "test_user")
        await ui.click_element("#submit-button")
        
        # Take screenshot
        await ui.take_screenshot("test_result.png")
        
        # Get page information
        title = await ui.get_page_title()
        url = await ui.get_page_url()
        print(f"Page: {title} - {url}")

asyncio.run(test_ui())
```

## Complete Example

Here's a complete example that combines bot interaction, API testing, and UI testing:

```python
import asyncio
from tma_framework import TelegramBot, MiniAppApi, MiniAppUI, Config

async def complete_example():
    # Setup
    config = Config.from_env()
    bot = TelegramBot(config.bot_token, config)
    
    try:
        # Get bot and Mini App info
        bot_info = await bot.get_me()
        mini_app_ui = await bot.get_mini_app(user_id=123456789)
        
        print(f"Testing Mini App: {mini_app_ui.url}")
        
        # API Testing
        print("\n=== API Testing ===")
        async with MiniAppApi(mini_app_ui.url, config) as api:
            result = await api.make_request("/api/health", "GET")
            print(f"Health check: {'✅ OK' if result.success else '❌ FAILED'}")
        
        # UI Testing
        print("\n=== UI Testing ===")
        async with MiniAppUI(mini_app_ui.url, config) as ui:
            await ui.setup_browser()
            await ui.page.goto(mini_app_ui.url, wait_until="networkidle")
            
            # Test form interaction
            await ui.fill_input("#email", "test@example.com")
            await ui.click_element("#submit")
            await ui.take_screenshot("form_test.png")
            
            print("UI test completed")
        
        print("\n✅ All tests completed successfully!")
        
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(complete_example())
```

## Environment Variables

Set up your environment variables:

```bash
# Required
export TMA_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"

# Optional
export TMA_LOG_LEVEL="INFO"
export TMA_TIMEOUT="30"
```

## Next Steps

1. **Explore Examples**: Check out the `examples/` directory for more detailed examples
2. **Read API Reference**: See [API Reference](api-reference.md) for complete method documentation
3. **Configuration**: Learn about all configuration options in [Configuration Guide](configuration.md)
4. **Advanced Usage**: Discover advanced patterns in [Examples](examples.md)

## Common Patterns

### Error Handling

```python
async def robust_testing():
    config = Config.from_env()
    
    try:
        async with MiniAppApi("https://your-mini-app.com", config) as api:
            result = await api.make_request("/api/test", "GET")
            
            if result.success:
                print("✅ API test passed")
            else:
                print(f"❌ API test failed: {result.error_message}")
                
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
```

### Retry Logic

```python
async def retry_test():
    config = Config.from_env()
    
    for attempt in range(3):
        try:
            async with MiniAppApi("https://your-mini-app.com", config) as api:
                result = await api.make_request("/api/test", "GET")
                if result.success:
                    print("✅ Test passed")
                    break
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                await asyncio.sleep(1)
```

### Context Managers

Always use context managers for proper resource cleanup:

```python
# ✅ Good
async with MiniAppApi(url, config) as api:
    result = await api.make_request("/api/test", "GET")

# ❌ Avoid
api = MiniAppApi(url, config)
result = await api.make_request("/api/test", "GET")
# Don't forget to call await api.close()
```

## Tips

1. **Use async/await**: All TMA Framework methods are async
2. **Context managers**: Use `async with` for automatic cleanup
3. **Error handling**: Always handle exceptions in your tests
4. **Logging**: Use the built-in logging for debugging
5. **Screenshots**: Take screenshots for visual verification
6. **Timeouts**: Set appropriate timeouts for your tests

Ready to dive deeper? Check out the [Examples](examples.md) for more advanced use cases!
