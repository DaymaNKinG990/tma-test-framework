# Installation Guide

This guide will help you install and set up TMA Framework for testing Telegram Mini Apps.

## Prerequisites

- Python 3.12 or higher
- pip or uv package manager
- Git (for cloning the repository)

## Installation Methods

### Method 1: Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-org/tma-test-framework.git
cd tma-test-framework

# Install dependencies using uv
uv sync

# Install Playwright browsers
uv run playwright install
```

### Method 2: Using pip

```bash
# Clone the repository
git clone https://github.com/your-org/tma-test-framework.git
cd tma-test-framework

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Install Playwright browsers
playwright install
```

## Dependencies

TMA Framework requires the following packages:

### Core Dependencies
- `httpx` - HTTP client for API testing
- `python-telegram-bot` - Telegram Bot API integration
- `playwright` - Browser automation for UI testing
- `msgspec` - High-performance data validation and serialization
- `loguru` - Logging framework
- `pyyaml` - YAML configuration support
- `aiofiles` - Async file operations
- `cryptography` - HMAC validation for initData

### Development Dependencies
- `pytest` - Testing framework
- `pytest-asyncio` - Async testing support
- `pytest-playwright` - Playwright testing integration

## Environment Setup

### 1. Bot Token Configuration

Create a `.env` file in your project root:

```bash
# Required
TMA_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"

# Optional
TMA_BOT_USERNAME="your_bot_username"
TMA_MINI_APP_URL="https://your-mini-app.com"
TMA_MINI_APP_START_PARAM="start_param_value"
TMA_TIMEOUT="30"
TMA_RETRY_COUNT="3"
TMA_RETRY_DELAY="1.0"
TMA_LOG_LEVEL="INFO"
```

### 2. Bot Setup

1. Create a new bot using [@BotFather](https://t.me/BotFather)
2. Get your bot token
3. Set up your Mini App URL in BotFather using `/setdomain`
4. Add the bot token to your environment variables

### 3. Mini App Setup

Your Mini App should:
- Be accessible via HTTPS
- Include the Telegram WebApp script: `<script src="https://telegram.org/js/telegram-web-app.js"></script>`
- Handle Telegram WebApp API calls properly

## Verification

Test your installation:

```bash
# Run basic tests
uv run python examples/basic_usage.py

# Run API-only tests
uv run python examples/api_only_usage.py

# Run UI-only tests
uv run python examples/ui_only_usage.py
```

## Troubleshooting

### Common Issues

1. **Playwright browser installation fails**
   ```bash
   # Try installing browsers manually
   uv run playwright install chromium
   ```

2. **Bot token not found**
   - Ensure `TMA_BOT_TOKEN` is set in your environment
   - Check that the token format is correct: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

3. **Mini App not accessible**
   - Verify the Mini App URL is correct and accessible
   - Check that the domain is set in BotFather
   - Ensure the Mini App uses HTTPS

4. **Import errors**
   - Make sure you're using the correct Python version (3.12+)
   - Verify all dependencies are installed correctly
   - Check that you're in the correct virtual environment

### Getting Help

If you encounter issues:
1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Review the [Examples](examples.md) for working code
3. Open an issue on the project repository

## Next Steps

After successful installation:
1. Read the [Quick Start Guide](quickstart.md)
2. Explore the [Examples](examples.md)
3. Check the [API Reference](api-reference.md) for detailed documentation
