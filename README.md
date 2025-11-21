# TMA Framework

Advanced Python framework for Telegram user simulation and Mini App testing with full MTProto capabilities.

## Features

- 👤 **Full User Simulation** - Act as a real Telegram user with MTProto
- 🤖 **Bot Interaction** - Send messages to bots and receive responses
- 📱 **Automatic Mini App Discovery** - Find and interact with Mini Apps from bots
- 🎭 **Playwright Integration** - Automated UI testing with Playwright
- 🔌 **HTTP Client** - API testing with httpx
- ⚙️ **Simple Configuration** - Environment variables and config objects
- 🔄 **Async Support** - Full async/await support
- 📊 **Logging** - Built-in logging with loguru
- 🚀 **High Performance** - Powered by msgspec for fast serialization and validation

## Installation

```bash
# Install dependencies
uv add httpx telethon playwright msgspec loguru pyyaml aiofiles cryptography

# Install Playwright browsers
playwright install
```

## Quick Start

### Setup Requirements

Before using TMA Framework, you need:

1. **Telegram API Credentials** (from [my.telegram.org](https://my.telegram.org)):
   - Go to "API development tools"
   - Create new application
   - Copy `api_id` and `api_hash`

2. **Get Session String** (one-time setup):
   - Run: `python examples/get_session.py`
   - Enter your API credentials and phone number
   - Complete authentication (SMS code + 2FA if needed)
   - Copy the generated session string

3. **Environment Variables**:
   ```bash
   export TMA_API_ID="your_api_id"
   export TMA_API_HASH="your_api_hash"
   export TMA_SESSION_STRING="your_session_string"
   ```

### Basic Usage

```python
import asyncio
from tma_framework import UserTelegramClient, Config

async def main():
    # Configuration with session string
    config = Config(
        api_id=12345,
        api_hash="your_api_hash",
        session_string="your_session_string"  # From get_session.py
    )

    # Initialize client (no authentication needed)
    async with UserTelegramClient(config) as client:
        user_info = await client.get_me()
        print(f"User: {user_info.first_name} (@{user_info.username})")

        # Interact with any bot
        response = await client.interact_with_bot(
            bot_username="example_bot",
            command="/start",
            wait_for_response=True
        )

        if response:
            print(f"Bot response: {response.text}")

asyncio.run(main())
```

### Mini App API Testing

```python
import asyncio
from tma_framework import UserTelegramClient, MiniAppApi, Config

async def main():
    config = Config(
        api_id=12345,
        api_hash="your_api_hash",
        session_string="your_session_string"
    )

    async with UserTelegramClient(config) as client:
        # Get Mini App from bot
        mini_app = await client.get_mini_app_from_bot("example_bot")

        if mini_app:
            # Test API endpoints
            async with MiniAppApi(mini_app.url, config) as api:
                result = await api.make_request("/api/status", "GET")
                print(f"API Test: {'✅ PASSED' if result.success else '❌ FAILED'}")

                # Validate initData
                is_valid = await api.validate_init_data(init_data, "bot_token")
                print(f"InitData validation: {'✅ VALID' if is_valid else '❌ INVALID'}")

asyncio.run(main())
```

### Mini App UI Testing

```python
import asyncio
from tma_framework import UserTelegramClient, MiniAppUI, Config

async def main():
    config = Config(
        api_id=12345,
        api_hash="your_api_hash",
        session_string="your_session_string"
    )

    async with UserTelegramClient(config) as client:
        # Get Mini App from bot
        mini_app = await client.get_mini_app_from_bot("example_bot")

        if mini_app:
            # Test Mini App UI
            async with MiniAppUI(mini_app.url, config) as ui:
                # Setup browser and navigate
                await ui.setup_browser()
                await ui.page.goto(mini_app.url, wait_until="networkidle")

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
export TMA_API_ID="12345"
export TMA_API_HASH="your_api_hash"

# Session (choose one)
export TMA_SESSION_STRING="session_string"   # For saved sessions
export TMA_SESSION_FILE="session.session"    # For file sessions

# Optional
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

# Using session string
config = Config(
    api_id=12345,
    api_hash="your_api_hash",
    session_string="your_session_string"
)

# Using session file
config = Config(
    api_id=12345,
    api_hash="your_api_hash",
    session_file="my_session.session"
)
```

## API Reference

### UserTelegramClient

#### Core Methods
- `get_me()` - Get current user information
- `get_entity()` - Get entity (user/chat) information
- `send_message()` - Send message to user/chat
- `get_messages()` - Get messages from chat
- `interact_with_bot()` - Interact with any bot
- `get_mini_app_from_bot()` - Get Mini App from bot
- `add_event_handler()` - Add event handler
- `start_listening()` - Start listening for messages

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

- `mtproto_usage.py` - Complete MTProto user simulation examples
- `get_session.py` - Script to generate session string for authentication
- `simple_auth.py` - Simple authentication example
- `error_handling.py` - Error handling and validation examples
- `advanced_auth.py` - Advanced authentication with step-by-step process

## Documentation

For detailed information about TMA Framework, see:
- [MTProto Migration Guide](docs/mtproto-migration.md) - Complete migration documentation
- [API Reference](docs/api-reference.md) - Detailed API documentation
- [Examples](examples/) - Comprehensive usage examples

## Requirements

- Python 3.12+
- httpx
- telethon
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

## CI/CD and Test Reports

This project uses GitHub Actions to run tests and publish Allure reports to GitHub Pages.

### Test Reports

After each push to `main` or `master` branch, tests are automatically run and Allure reports are published to GitHub Pages.

**View test reports**: `https://<your-username>.github.io/<repo-name>/`

### Setting up GitHub Pages

1. Go to your repository **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. The workflow will automatically deploy reports after each successful test run

### Local Test Execution

Run tests locally with Allure:

```bash
# Run tests and generate Allure results
uv run pytest --alluredir=allure-results

# Generate and serve Allure report locally
uv run allure serve allure-results
```

### GitHub Actions Workflow

The workflow (`.github/workflows/tests.yml`) automatically:
- Runs tests on push/PR to main branches
- Generates Allure test reports
- Publishes reports to GitHub Pages
- Uploads coverage reports as artifacts

## License

MIT License
