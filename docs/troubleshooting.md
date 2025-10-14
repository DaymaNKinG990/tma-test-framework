# Troubleshooting

This guide helps you resolve common issues when using TMA Framework.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Configuration Problems](#configuration-problems)
- [Bot API Issues](#bot-api-issues)
- [Mini App Testing Issues](#mini-app-testing-issues)
- [Performance Issues](#performance-issues)
- [Browser Issues](#browser-issues)
- [Common Error Messages](#common-error-messages)
- [Debugging Tips](#debugging-tips)

## Installation Issues

### Python Version Compatibility

**Problem**: Framework doesn't work with Python version

**Solution**: Ensure you're using Python 3.12 or higher

```bash
# Check Python version
python --version

# If using older version, upgrade Python
# On Windows: Download from python.org
# On macOS: brew install python@3.12
# On Linux: sudo apt install python3.12
```

### Dependency Installation Failures

**Problem**: `uv sync` or `pip install` fails

**Solutions**:

1. **Update package managers**:
   ```bash
   # Update uv
   uv self update
   
   # Update pip
   pip install --upgrade pip
   ```

2. **Clear cache**:
   ```bash
   # Clear uv cache
   uv cache clean
   
   # Clear pip cache
   pip cache purge
   ```

3. **Install with verbose output**:
   ```bash
   uv sync --verbose
   # or
   pip install -e . -v
   ```

### Playwright Browser Installation

**Problem**: Playwright browsers fail to install

**Solutions**:

1. **Install browsers manually**:
   ```bash
   uv run playwright install chromium
   uv run playwright install firefox
   uv run playwright install webkit
   ```

2. **Install with system dependencies**:
   ```bash
   uv run playwright install --with-deps
   ```

3. **Check system requirements**:
   - Windows: Visual Studio Build Tools
   - macOS: Xcode Command Line Tools
   - Linux: Build essentials

## Configuration Problems

### Bot Token Issues

**Problem**: `ValueError: Bot token is required`

**Solutions**:

1. **Check environment variable**:
   ```bash
   # Check if token is set
   echo $TMA_BOT_TOKEN
   
   # Set token
   export TMA_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
   ```

2. **Verify token format**:
   ```python
   # Token should be in format: BOT_ID:BOT_TOKEN
   token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
   assert ":" in token, "Token must contain colon"
   assert len(token.split(":")[0]) > 0, "Bot ID cannot be empty"
   assert len(token.split(":")[1]) > 0, "Bot token cannot be empty"
   ```

3. **Use Config object directly**:
   ```python
   from tma_framework import Config
   
   config = Config(
       bot_token="your_token_here",
       log_level="INFO"
   )
   ```

### Invalid Log Level

**Problem**: `ValueError: Invalid log level`

**Solution**: Use valid log levels (uppercase)

```python
# Valid log levels
config = Config(
    bot_token="your_token",
    log_level="DEBUG"    # DEBUG, INFO, WARNING, ERROR
)
```

### Environment Variable Loading

**Problem**: Environment variables not loaded

**Solutions**:

1. **Use .env file**:
   ```bash
   # Create .env file
   echo "TMA_BOT_TOKEN=your_token_here" > .env
   echo "TMA_LOG_LEVEL=INFO" >> .env
   ```

2. **Load manually**:
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   config = Config.from_env()
   ```

## Bot API Issues

### Bot Token Invalid

**Problem**: `Unauthorized` or `401` errors

**Solutions**:

1. **Verify token with BotFather**:
   - Go to [@BotFather](https://t.me/BotFather)
   - Use `/mybots` command
   - Check if token is correct

2. **Test token manually**:
   ```python
   import httpx
   
   async def test_token(token):
       async with httpx.AsyncClient() as client:
           response = await client.get(
               f"https://api.telegram.org/bot{token}/getMe"
           )
           print(f"Status: {response.status_code}")
           print(f"Response: {response.json()}")
   
   # Test your token
   await test_token("your_token_here")
   ```

### Bot Not Found

**Problem**: Bot doesn't exist or is deleted

**Solutions**:

1. **Create new bot**:
   - Go to [@BotFather](https://t.me/BotFather)
   - Use `/newbot` command
   - Follow instructions

2. **Check bot status**:
   - Use `/mybots` in BotFather
   - Ensure bot is active

### Mini App URL Issues

**Problem**: Mini App URL not accessible

**Solutions**:

1. **Set domain in BotFather**:
   ```
   /setdomain
   @your_bot
   your-domain.com
   ```

2. **Verify HTTPS**:
   - Mini App must use HTTPS
   - Check SSL certificate

3. **Test URL manually**:
   ```bash
   curl -I https://your-mini-app.com
   ```

## Mini App Testing Issues

### API Endpoint Not Found

**Problem**: `404 Not Found` for API endpoints

**Solutions**:

1. **Check endpoint URL**:
   ```python
   # Ensure correct endpoint
   result = await api.make_request("/api/status", "GET")
   # Not: await api.make_request("api/status", "GET")
   ```

2. **Verify Mini App has API**:
   - Check if Mini App implements API endpoints
   - Test endpoints manually with curl/Postman

3. **Check CORS settings**:
   - Ensure Mini App allows cross-origin requests
   - Add proper CORS headers

### initData Validation Fails

**Problem**: `validate_init_data` returns False

**Solutions**:

1. **Check initData format**:
   ```python
   # initData should be URL-encoded
   init_data = "user=%7B%22id%22%3A123%7D&auth_date=1234567890&hash=abc123"
   ```

2. **Verify bot token**:
   ```python
   # Use correct bot token for validation
   is_valid = await api.validate_init_data(init_data, correct_bot_token)
   ```

3. **Check auth_date**:
   - initData expires after 24 hours
   - Ensure auth_date is recent

### UI Elements Not Found

**Problem**: `Element not found` errors

**Solutions**:

1. **Wait for page load**:
   ```python
   await ui.page.goto(url, wait_until="networkidle")
   await ui.wait_for_element("#element", timeout=10000)
   ```

2. **Check selector**:
   ```python
   # Use correct CSS selector
   await ui.click_element("#submit-button")  # ID selector
   await ui.click_element(".btn-primary")    # Class selector
   await ui.click_element("button[type='submit']")  # Attribute selector
   ```

3. **Debug element existence**:
   ```python
   # Check if element exists
   element = await ui.page.query_selector("#element")
   if element:
       print("Element found")
   else:
       print("Element not found")
   ```

## Performance Issues

### Slow API Requests

**Problem**: API requests are slow

**Solutions**:

1. **Optimize timeout settings**:
   ```python
   config = Config(
       bot_token="your_token",
       timeout=10.0  # Reduce timeout
   )
   ```

2. **Use connection pooling**:
   ```python
   # Framework already uses connection pooling
   # But you can configure limits
   async with MiniAppApi(url, config) as api:
       # Multiple requests reuse connections
       for i in range(10):
           result = await api.make_request(f"/api/test-{i}", "GET")
   ```

3. **Parallel requests**:
   ```python
   import asyncio
   
   async def parallel_requests():
       tasks = []
       for i in range(5):
           task = api.make_request(f"/api/test-{i}", "GET")
           tasks.append(task)
       
       results = await asyncio.gather(*tasks)
       return results
   ```

### Slow Browser Operations

**Problem**: UI tests are slow

**Solutions**:

1. **Use headless mode** (default):
   ```python
   # Browser runs in headless mode by default
   await ui.setup_browser()
   ```

2. **Optimize wait conditions**:
   ```python
   # Use specific wait conditions
   await ui.page.goto(url, wait_until="domcontentloaded")  # Faster than networkidle
   ```

3. **Reduce screenshot size**:
   ```python
   # Take smaller screenshots
   await ui.page.screenshot(path="screenshot.png", full_page=False)
   ```

## Browser Issues

### Browser Launch Fails

**Problem**: Playwright browser fails to launch

**Solutions**:

1. **Install system dependencies**:
   ```bash
   # Linux
   sudo apt-get install libnss3-dev libatk-bridge2.0-dev libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libxss1 libasound2
   
   # macOS
   xcode-select --install
   
   # Windows
   # Install Visual Studio Build Tools
   ```

2. **Check browser installation**:
   ```bash
   uv run playwright install --force
   ```

3. **Use different browser**:
   ```python
   # Framework uses Chromium by default
   # You can modify the code to use Firefox or WebKit
   ```

### Browser Crashes

**Problem**: Browser crashes during tests

**Solutions**:

1. **Increase memory limits**:
   ```python
   # Add to your test
   await ui.page.set_viewport_size({"width": 1920, "height": 1080})
   ```

2. **Handle crashes gracefully**:
   ```python
   try:
       await ui.setup_browser()
       await ui.page.goto(url)
   except Exception as e:
       print(f"Browser crashed: {e}")
       # Restart browser
       await ui.setup_browser()
   ```

3. **Use browser context**:
   ```python
   # Framework handles browser context automatically
   # But you can add custom context options if needed
   ```

## Common Error Messages

### `'MiniAppApi' object has no attribute 'test_api'`

**Problem**: Using old method name

**Solution**: Use new method name
```python
# Old (incorrect)
result = await api.test_api("/api/test", "GET")

# New (correct)
result = await api.make_request("/api/test", "GET")
```

### `'MiniAppUI' object has no attribute 'get_telegram_data'`

**Problem**: Method removed from MiniAppUI

**Solution**: Use MiniAppApi for initData validation
```python
# Old (incorrect)
telegram_data = await ui.get_telegram_data()

# New (correct)
async with MiniAppApi(url, config) as api:
    is_valid = await api.validate_init_data(init_data, bot_token)
```

### `ImportError: cannot import name 'MiniApp'`

**Problem**: Using removed composite class

**Solution**: Use separate classes
```python
# Old (incorrect)
from tma_framework import MiniApp

# New (correct)
from tma_framework import MiniAppApi, MiniAppUI
```

### `UnicodeEncodeError: 'charmap' codec can't encode character`

**Problem**: Unicode characters in output

**Solution**: Remove emoji characters
```python
# Old (incorrect)
print("✅ Test passed")

# New (correct)
print("[OK] Test passed")
```

## Debugging Tips

### Enable Debug Logging

```python
config = Config(
    bot_token="your_token",
    log_level="DEBUG"  # Enable debug logging
)
```

### Add Print Statements

```python
async def debug_test():
    print("Starting test...")
    
    async with MiniAppApi(url, config) as api:
        print("API client created")
        
        result = await api.make_request("/api/test", "GET")
        print(f"Request completed: {result.status_code}")
        
        if result.error_message:
            print(f"Error: {result.error_message}")
```

### Use Browser DevTools

```python
async def debug_ui():
    async with MiniAppUI(url, config) as ui:
        await ui.setup_browser()
        
        # Enable console logging
        ui.page.on("console", lambda msg: print(f"Console: {msg.text}"))
        
        # Enable network logging
        ui.page.on("request", lambda req: print(f"Request: {req.url}"))
        ui.page.on("response", lambda resp: print(f"Response: {resp.status} {resp.url}"))
        
        await ui.page.goto(url)
```

### Take Screenshots for Debugging

```python
async def debug_with_screenshots():
    async with MiniAppUI(url, config) as ui:
        await ui.setup_browser()
        await ui.page.goto(url)
        
        # Take screenshot at each step
        await ui.take_screenshot("step1_initial.png")
        
        await ui.fill_input("#username", "test")
        await ui.take_screenshot("step2_filled.png")
        
        await ui.click_element("#submit")
        await ui.take_screenshot("step3_clicked.png")
```

### Check Network Requests

```python
async def debug_network():
    async with MiniAppUI(url, config) as ui:
        await ui.setup_browser()
        
        # Log all network requests
        requests = []
        responses = []
        
        ui.page.on("request", lambda req: requests.append(req))
        ui.page.on("response", lambda resp: responses.append(resp))
        
        await ui.page.goto(url)
        
        print(f"Total requests: {len(requests)}")
        print(f"Total responses: {len(responses)}")
        
        for req in requests:
            print(f"Request: {req.method} {req.url}")
        
        for resp in responses:
            print(f"Response: {resp.status} {resp.url}")
```

## Getting Help

If you're still experiencing issues:

1. **Check the logs**: Enable debug logging and review the output
2. **Review examples**: Look at working examples in the `examples/` directory
3. **Test manually**: Try the same operations manually (curl for API, browser for UI)
4. **Check dependencies**: Ensure all dependencies are correctly installed
5. **Update framework**: Make sure you're using the latest version
6. **Open an issue**: Create an issue on the project repository with:
   - Error message
   - Code that reproduces the issue
   - Environment details (OS, Python version, etc.)
   - Debug logs (if applicable)

## Performance Optimization

### API Testing Optimization

```python
# Use connection pooling
async with MiniAppApi(url, config) as api:
    # Multiple requests reuse the same connection
    for i in range(100):
        result = await api.make_request(f"/api/test-{i}", "GET")
```

### UI Testing Optimization

```python
# Reuse browser instance
async with MiniAppUI(url, config) as ui:
    await ui.setup_browser()
    
    # Multiple operations on the same browser
    for i in range(10):
        await ui.page.goto(f"{url}/page-{i}")
        await ui.take_screenshot(f"page_{i}.png")
```

### Memory Optimization

```python
# Use context managers for automatic cleanup
async with MiniAppApi(url, config) as api:
    # Resources automatically cleaned up
    result = await api.make_request("/api/test", "GET")

# Don't forget to close manually if not using context manager
api = MiniAppApi(url, config)
try:
    result = await api.make_request("/api/test", "GET")
finally:
    await api.close()
```
