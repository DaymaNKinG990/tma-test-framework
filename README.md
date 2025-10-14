# TMA Framework

Simple Python framework for working with Telegram API and Mini Apps.

## Features

- 🤖 **Telegram Bot API Integration** - Easy interaction with Telegram Bot API
- 📱 **Mini App Testing** - Separate API and UI testing classes
- 🎭 **Playwright Integration** - Automated UI testing with Playwright
- 🔌 **HTTP Client** - API testing with httpx
- ⚙️ **Simple Configuration** - Environment variables and config objects
- 🔄 **Async Support** - Full async/await support
- 📊 **Logging** - Built-in logging with loguru
- 🚀 **High Performance** - Powered by msgspec for fast serialization and validation

## Installation

```bash
# Install dependencies
uv add httpx python-telegram-bot playwright msgspec loguru pyyaml aiofiles cryptography

# Install Playwright browsers
playwright install
```

## Quick Start

### 1. Basic Bot Usage

```python
import asyncio
from tma_framework import TelegramBot, Config

async def main():
    # Load config from environment
    config = Config.from_env()
    
    # Initialize bot
    async with TelegramBot(token=config.bot_token, config=config) as bot:
        # Get bot info
        bot_info = await bot.get_me()
        print(f"Bot: @{bot_info.username}")
        
        # Send message
        await bot.send_message(chat_id=123456789, text="Hello from TMA Framework!")

asyncio.run(main())
```

### 2. Mini App API Testing

```python
import asyncio
from tma_framework import TelegramBot, MiniAppApi, Config

async def main():
    config = Config.from_env()
    
    async with TelegramBot(token=config.bot_token, config=config) as bot:
        # Get Mini App from bot
        mini_app_ui = await bot.get_mini_app(user_id=123456789)
        
        # Test API endpoints
        async with MiniAppApi(mini_app_ui.url, config) as api:
            result = await api.make_request("/api/status", "GET")
            print(f"API Test: {'✅ PASSED' if result.success else '❌ FAILED'}")
            
            # Validate initData
            is_valid = await api.validate_init_data(init_data, config.bot_token)
            print(f"InitData validation: {'✅ VALID' if is_valid else '❌ INVALID'}")

asyncio.run(main())
```

### 3. Mini App UI Testing

```python
import asyncio
from tma_framework import MiniAppUI, Config

async def main():
    config = Config()
    
    # Test Mini App UI directly
    async with MiniAppUI("https://your-mini-app.com", config) as ui:
        # Setup browser and navigate
        await ui.setup_browser()
        await ui.page.goto("https://your-mini-app.com", wait_until="networkidle")
        
        # UI interactions
        await ui.fill_input("#username", "test_user")
        await ui.click_element("#submit-button")
        await ui.take_screenshot("test_screenshot.png")

asyncio.run(main())
```

## Configuration

### Environment Variables

```bash
# Required
export TMA_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"

# Optional
export TMA_BOT_USERNAME="your_bot_username"
export TMA_MINI_APP_URL="https://your-mini-app.com"
export TMA_MINI_APP_START_PARAM="start_param_value"
export TMA_TIMEOUT="30"
export TMA_RETRY_COUNT="3"
export TMA_RETRY_DELAY="1.0"
export TMA_LOG_LEVEL="INFO"
```

### Config Object

```python
from tma_framework import Config

config = Config(
    bot_token="your_bot_token",
    mini_app_url="https://your-mini-app.com",
    timeout=60,
    retry_count=5,
    retry_delay=2.0,
    log_level="DEBUG"
)
```

## API Reference

### TelegramBot

- `get_me()` - Get bot information
- `request_simple_webview()` - Request Mini App from bot
- `get_mini_app()` - Get Mini App object
- `send_message()` - Send message to chat
- `get_updates()` - Get bot updates

### MiniAppApi

- `make_request()` - Make HTTP request to API endpoint
- `validate_init_data()` - Validate Telegram initData with HMAC

### MiniAppUI

- `setup_browser()` - Setup Playwright browser
- `click_element()` - Click element
- `fill_input()` - Fill input field
- `wait_for_element()` - Wait for element
- `take_screenshot()` - Take screenshot
- `get_page_title()` - Get page title
- `get_page_url()` - Get page URL
- `execute_script()` - Execute JavaScript

## Examples

See the `examples/` directory for more detailed examples:

- `basic_usage.py` - Basic framework usage with separate API and UI classes
- `advanced_usage.py` - Advanced features, error handling, and performance testing
- `api_only_usage.py` - API-only testing examples
- `ui_only_usage.py` - UI-only testing examples

## Requirements

- Python 3.12+
- httpx
- python-telegram-bot
- playwright
- msgspec
- loguru
- pyyaml
- aiofiles
- cryptography

## Performance

TMA Framework uses msgspec for high-performance data validation and serialization:

- **2-4x faster** JSON serialization compared to Pydantic
- **2-3x faster** data validation
- **2-3x less** memory usage
- **Runtime type checking** with zero-cost validation

Run the performance benchmarks:
```bash
uv run python tests/test_performance.py
```

## License

MIT License
