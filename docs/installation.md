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
git clone https://github.com/DaymaNKinG990/tma-test-framework.git
cd tma-test-framework

# Install dependencies using uv
uv sync

# Install Playwright browsers
uv run playwright install
```

### Method 2: Using pip

```bash
# Clone the repository
git clone https://github.com/DaymaNKinG990/tma-test-framework.git
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

### 1. API Credentials Configuration

Create a `.env` file in your project root:

```bash
# Required
TMA_API_ID="12345"
TMA_API_HASH="your_api_hash"

# Session (choose one)
TMA_SESSION_STRING="your_session_string"
# OR
TMA_SESSION_FILE="session.session"

# Optional
TMA_MINI_APP_URL="https://your-mini-app.com"
TMA_MINI_APP_START_PARAM="start_param_value"
TMA_TIMEOUT="30"
TMA_RETRY_COUNT="3"
TMA_RETRY_DELAY="1.0"
TMA_LOG_LEVEL="INFO"
```

### 2. API Credentials Setup

1. Go to [my.telegram.org](https://my.telegram.org)
2. Log in with your phone number
3. Go to "API development tools"
4. Create a new application
5. Copy `api_id` and `api_hash`
6. Add them to your environment variables

### 3. Session Setup

1. Run `python examples/get_session.py` to generate a session string
2. Enter your API credentials and phone number
3. Complete authentication (SMS code + 2FA if needed)
4. Copy the generated session string to your environment variables

### 4. Mini App Setup

Your Mini App should:
- Be accessible via HTTPS
- Include the Telegram WebApp script: `<script src="https://telegram.org/js/telegram-web-app.js"></script>`
- Handle Telegram WebApp API calls properly

## Verification

Test your installation:

```bash
# Generate session string (first time only)
uv run python examples/get_session.py

# Run MTProto user simulation tests
uv run python examples/mtproto_usage.py

# Run simple authentication example
uv run python examples/simple_auth.py

# Run error handling examples
uv run python examples/error_handling.py
```

## Troubleshooting

### Common Issues

1. **Playwright browser installation fails**
   ```bash
   # Try installing browsers manually
   uv run playwright install chromium
   ```

2. **API credentials not found**
   - Ensure `TMA_API_ID` and `TMA_API_HASH` are set in your environment
   - Check that the API ID is a number and API hash is a string

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
