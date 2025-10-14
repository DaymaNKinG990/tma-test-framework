# API Reference

Complete API documentation for TMA Framework.

## Core Classes

### TelegramBot

Main class for interacting with Telegram Bot API.

#### Constructor

```python
TelegramBot(token: str, config: Optional[Config] = None)
```

**Parameters:**
- `token` (str): Telegram bot token
- `config` (Optional[Config]): Configuration object

#### Methods

##### `get_me() -> BotInfo`

Get bot information.

**Returns:** `BotInfo` object with bot details

**Example:**
```python
bot_info = await bot.get_me()
print(f"Bot: {bot_info.first_name} (@{bot_info.username})")
```

##### `get_mini_app(user_id: int, url: Optional[str] = None, start_param: Optional[str] = None) -> MiniAppUI`

Get Mini App from bot.

**Parameters:**
- `user_id` (int): Telegram user ID
- `url` (Optional[str]): Custom Mini App URL
- `start_param` (Optional[str]): Start parameter

**Returns:** `MiniAppUI` object

**Example:**
```python
mini_app = await bot.get_mini_app(user_id=123456789)
```

##### `send_message(chat_id: int, text: str, **kwargs) -> Message`

Send message to chat.

**Parameters:**
- `chat_id` (int): Chat ID
- `text` (str): Message text
- `**kwargs`: Additional message parameters

**Returns:** `Message` object

**Example:**
```python
message = await bot.send_message(chat_id=123456789, text="Hello!")
```

##### `get_updates(offset: Optional[int] = None, limit: Optional[int] = None) -> List[Update]`

Get bot updates.

**Parameters:**
- `offset` (Optional[int]): Offset for pagination
- `limit` (Optional[int]): Maximum number of updates

**Returns:** List of `Update` objects

**Example:**
```python
updates = await bot.get_updates(limit=10)
```

### MiniAppApi

Class for testing Mini App HTTP API endpoints.

#### Constructor

```python
MiniAppApi(url: str, config: Optional[Config] = None)
```

**Parameters:**
- `url` (str): Mini App URL
- `config` (Optional[Config]): Configuration object

#### Methods

##### `make_request(endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> ApiResult`

Make HTTP request to Mini App API endpoint.

**Parameters:**
- `endpoint` (str): API endpoint path
- `method` (str): HTTP method (GET, POST, PUT, DELETE, etc.)
- `data` (Optional[Dict[str, Any]]): Request data
- `headers` (Optional[Dict[str, str]]): Request headers

**Returns:** `ApiResult` object

**Example:**
```python
result = await api.make_request("/api/status", "GET")
print(f"Status: {result.status_code}, Success: {result.success}")
```

##### `validate_init_data(init_data: str, bot_token: str) -> bool`

Validate Telegram initData using HMAC-SHA256.

**Parameters:**
- `init_data` (str): Telegram initData string
- `bot_token` (str): Bot token for validation

**Returns:** `bool` - True if valid, False otherwise

**Example:**
```python
is_valid = await api.validate_init_data(init_data, bot_token)
print(f"InitData valid: {is_valid}")
```

##### `close() -> None`

Close HTTP client and cleanup resources.

**Example:**
```python
await api.close()
```

### MiniAppUI

Class for testing Mini App user interface using Playwright.

#### Constructor

```python
MiniAppUI(url: str, config: Optional[Config] = None)
```

**Parameters:**
- `url` (str): Mini App URL
- `config` (Optional[Config]): Configuration object

#### Methods

##### `setup_browser() -> Self`

Setup Playwright browser for UI testing.

**Returns:** `Self` for method chaining

**Example:**
```python
await ui.setup_browser()
```

##### `click_element(selector: str) -> None`

Click element in Mini App.

**Parameters:**
- `selector` (str): CSS selector for element

**Example:**
```python
await ui.click_element("#submit-button")
```

##### `fill_input(selector: str, text: str) -> None`

Fill input field in Mini App.

**Parameters:**
- `selector` (str): CSS selector for input
- `text` (str): Text to fill

**Example:**
```python
await ui.fill_input("#username", "test_user")
```

##### `wait_for_element(selector: str, timeout: int = 5000) -> None`

Wait for element to appear in Mini App.

**Parameters:**
- `selector` (str): CSS selector for element
- `timeout` (int): Timeout in milliseconds

**Example:**
```python
await ui.wait_for_element("#loading", timeout=10000)
```

##### `take_screenshot(path: str) -> None`

Take screenshot of the current page.

**Parameters:**
- `path` (str): Path to save screenshot

**Example:**
```python
await ui.take_screenshot("test_result.png")
```

##### `get_element_text(selector: str) -> Optional[str]`

Get text content of an element.

**Parameters:**
- `selector` (str): CSS selector for element

**Returns:** Element text or None

**Example:**
```python
text = await ui.get_element_text("h1")
print(f"Title: {text}")
```

##### `get_element_attribute_value(selector: str, attribute: str) -> Optional[str]`

Get attribute value of an element.

**Parameters:**
- `selector` (str): CSS selector for element
- `attribute` (str): Attribute name

**Returns:** Attribute value or None

**Example:**
```python
href = await ui.get_element_attribute_value("a", "href")
print(f"Link: {href}")
```

##### `get_page_title() -> str`

Get page title.

**Returns:** Page title

**Example:**
```python
title = await ui.get_page_title()
print(f"Page title: {title}")
```

##### `get_page_url() -> str`

Get current page URL.

**Returns:** Page URL

**Example:**
```python
url = await ui.get_page_url()
print(f"Current URL: {url}")
```

##### `execute_script(script: str) -> Any`

Execute JavaScript on the page.

**Parameters:**
- `script` (str): JavaScript code to execute

**Returns:** Script result

**Example:**
```python
result = await ui.execute_script("return document.title;")
print(f"Script result: {result}")
```

##### `hover_element(selector: str) -> None`

Hover over element in Mini App.

**Parameters:**
- `selector` (str): CSS selector for element

**Example:**
```python
await ui.hover_element("#menu-item")
```

##### `double_click_element(selector: str) -> None`

Double click element in Mini App.

**Parameters:**
- `selector` (str): CSS selector for element

**Example:**
```python
await ui.double_click_element("#file-item")
```

##### `right_click_element(selector: str) -> None`

Right click element in Mini App.

**Parameters:**
- `selector` (str): CSS selector for element

**Example:**
```python
await ui.right_click_element("#context-menu-target")
```

##### `select_option(selector: str, value: str) -> None`

Select option from dropdown.

**Parameters:**
- `selector` (str): CSS selector for select element
- `value` (str): Option value to select

**Example:**
```python
await ui.select_option("#country", "US")
```

##### `check_checkbox(selector: str) -> None`

Check checkbox in Mini App.

**Parameters:**
- `selector` (str): CSS selector for checkbox

**Example:**
```python
await ui.check_checkbox("#terms")
```

##### `uncheck_checkbox(selector: str) -> None`

Uncheck checkbox in Mini App.

**Parameters:**
- `selector` (str): CSS selector for checkbox

**Example:**
```python
await ui.uncheck_checkbox("#terms")
```

##### `upload_file(selector: str, file_path: str) -> None`

Upload file to file input.

**Parameters:**
- `selector` (str): CSS selector for file input
- `file_path` (str): Path to file to upload

**Example:**
```python
await ui.upload_file("#file-input", "test.txt")
```

##### `press_key(key: str) -> None`

Press key on page.

**Parameters:**
- `key` (str): Key to press (e.g., 'Enter', 'Escape', 'Tab')

**Example:**
```python
await ui.press_key("Enter")
```

##### `type_text(text: str) -> None`

Type text on page.

**Parameters:**
- `text` (str): Text to type

**Example:**
```python
await ui.type_text("Hello, World!")
```

##### `scroll_to_element(selector: str) -> None`

Scroll to element in Mini App.

**Parameters:**
- `selector` (str): CSS selector for element

**Example:**
```python
await ui.scroll_to_element("#footer")
```

##### `wait_for_navigation(timeout: int = 5000) -> None`

Wait for page navigation to complete.

**Parameters:**
- `timeout` (int): Timeout in milliseconds

**Example:**
```python
await ui.wait_for_navigation(timeout=10000)
```

##### `close() -> None`

Close browser and cleanup resources.

**Example:**
```python
await ui.close()
```

### Config

Configuration class for TMA Framework.

#### Constructor

```python
Config(
    bot_token: str,
    bot_username: Optional[str] = None,
    mini_app_url: Optional[str] = None,
    mini_app_start_param: Optional[str] = None,
    timeout: float = 30.0,
    retry_count: int = 3,
    retry_delay: float = 1.0,
    log_level: str = "INFO"
)
```

**Parameters:**
- `bot_token` (str): Telegram bot token
- `bot_username` (Optional[str]): Bot username
- `mini_app_url` (Optional[str]): Default Mini App URL
- `mini_app_start_param` (Optional[str]): Default start parameter
- `timeout` (float): Request timeout in seconds
- `retry_count` (int): Number of retry attempts
- `retry_delay` (float): Delay between retries in seconds
- `log_level` (str): Logging level (DEBUG, INFO, WARNING, ERROR)

#### Class Methods

##### `from_env() -> Config`

Create configuration from environment variables.

**Returns:** `Config` object

**Example:**
```python
config = Config.from_env()
```

## Data Models

### BotInfo

Bot information model.

```python
class BotInfo(msgspec.Struct):
    id: int
    is_bot: bool
    first_name: str
    username: Optional[str] = None
    can_join_groups: bool = True
    can_read_all_group_messages: bool = False
    supports_inline_queries: bool = False
```

### WebViewResult

WebView result model.

```python
class WebViewResult(msgspec.Struct):
    url: str
    start_param: Optional[str] = None
```

### MiniAppInfo

Mini App information model.

```python
class MiniAppInfo(msgspec.Struct):
    url: str
    start_param: Optional[str] = None
    theme_params: Optional[Dict[str, Any]] = None
    platform: str = "web"
```

### ApiResult

API request result model.

```python
class ApiResult(msgspec.Struct):
    endpoint: str
    method: str
    status_code: int
    response_time: float
    success: bool
    redirect: bool
    client_error: bool
    server_error: bool
    informational: bool
    response: Optional[Response] = None
    error_message: Optional[str] = None
```

## Context Managers

All classes support context managers for automatic resource cleanup:

```python
# TelegramBot
async with TelegramBot(token, config) as bot:
    bot_info = await bot.get_me()

# MiniAppApi
async with MiniAppApi(url, config) as api:
    result = await api.make_request("/api/test", "GET")

# MiniAppUI
async with MiniAppUI(url, config) as ui:
    await ui.setup_browser()
    await ui.click_element("#button")
```

## Error Handling

All methods may raise exceptions. Always use try-catch blocks:

```python
try:
    async with MiniAppApi(url, config) as api:
        result = await api.make_request("/api/test", "GET")
        if result.success:
            print("✅ Success")
        else:
            print(f"❌ Failed: {result.error_message}")
except Exception as e:
    print(f"❌ Exception: {e}")
```

## Async/Await

All TMA Framework methods are async and must be awaited:

```python
# ✅ Correct
result = await api.make_request("/api/test", "GET")

# ❌ Incorrect
result = api.make_request("/api/test", "GET")  # Returns coroutine, not result
```

## Type Hints

TMA Framework uses type hints for better IDE support and code clarity:

```python
from typing import Optional, Dict, Any
from tma_framework import MiniAppApi, ApiResult

async def test_api(api: MiniAppApi) -> Optional[ApiResult]:
    try:
        return await api.make_request("/api/test", "GET")
    except Exception:
        return None
```
