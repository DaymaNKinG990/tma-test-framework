# API Reference

Complete API documentation for TMA Framework.

## Core Classes

### UserTelegramClient

Main class for full user simulation with MTProto API.

#### Constructor

```python
UserTelegramClient(config: Config)
```

**Parameters:**
- `config` (Config): Configuration object with MTProto credentials

#### Methods

##### `get_me() -> UserInfo`

Get current user information.

**Returns:** `UserInfo` object with user details

**Example:**
```python
user_info = await client.get_me()
print(f"User: {user_info.first_name} (@{user_info.username})")
```

##### `get_entity(entity: Union[str, int]) -> ChatInfo`

Get entity (user, chat, channel) information.

**Parameters:**
- `entity` (Union[str, int]): Username, phone number, or ID

**Returns:** `ChatInfo` object

**Example:**
```python
entity_info = await client.get_entity("username")
print(f"Entity: {entity_info.title} ({entity_info.type})")
```

##### `send_message(entity: Union[str, int], text: str, reply_to: Optional[int] = None, parse_mode: Optional[str] = None) -> MessageInfo`

Send message to entity.

**Parameters:**
- `entity` (Union[str, int]): Username, phone number, or ID
- `text` (str): Message text
- `reply_to` (Optional[int]): Message ID to reply to
- `parse_mode` (Optional[str]): Parse mode (HTML, Markdown)

**Returns:** `MessageInfo` object

**Example:**
```python
message = await client.send_message("username", "Hello!")
```

##### `get_messages(entity: Union[str, int], limit: int = 10, offset_id: int = 0) -> List[MessageInfo]`

Get messages from entity.

**Parameters:**
- `entity` (Union[str, int]): Username, phone number, or ID
- `limit` (int): Maximum number of messages
- `offset_id` (int): Offset message ID

**Returns:** List of `MessageInfo` objects

**Example:**
```python
messages = await client.get_messages("username", limit=10)
```

##### `interact_with_bot(bot_username: str, command: str, wait_for_response: bool = True, timeout: int = 30) -> Optional[MessageInfo]`

Interact with a bot by sending a command.

**Parameters:**
- `bot_username` (str): Bot username (without @)
- `command` (str): Command to send (e.g., "/start")
- `wait_for_response` (bool): Whether to wait for bot response
- `timeout` (int): Timeout for waiting response

**Returns:** Bot response message or None

**Example:**
```python
response = await client.interact_with_bot("example_bot", "/start")
```

##### `get_mini_app_from_bot(bot_username: str, start_param: Optional[str] = None) -> Optional[MiniAppUI]`

Get Mini App from bot by interacting with it.

**Parameters:**
- `bot_username` (str): Bot username (without @)
- `start_param` (Optional[str]): Start parameter for Mini App

**Returns:** `MiniAppUI` object if Mini App is found

**Example:**
```python
mini_app = await client.get_mini_app_from_bot("example_bot")
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
    api_id: int,
    api_hash: str,
    session_string: Optional[str] = None,
    session_file: Optional[str] = None,
    mini_app_url: Optional[str] = None,
    mini_app_start_param: Optional[str] = None,
    timeout: int = 30,
    retry_count: int = 3,
    retry_delay: float = 1.0,
    log_level: str = "INFO"
)
```

**Parameters:**
- `api_id` (int): Telegram API ID (from my.telegram.org)
- `api_hash` (str): Telegram API Hash (from my.telegram.org)
- `session_string` (Optional[str]): Saved session string
- `session_file` (Optional[str]): Path to session file
- `mini_app_url` (Optional[str]): Default Mini App URL
- `mini_app_start_param` (Optional[str]): Default start parameter
- `timeout` (int): Request timeout in seconds
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

### UserInfo

User information model.

```python
class UserInfo(msgspec.Struct):
    id: int
    username: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None
    phone: Optional[str] = None
    is_bot: bool = False
    is_verified: bool = False
    is_premium: bool = False
```

### ChatInfo

Chat information model.

```python
class ChatInfo(msgspec.Struct):
    id: int
    title: str
    username: Optional[str] = None
    type: str  # 'private', 'group', 'supergroup', 'channel'
    is_bot: bool = False
    is_verified: bool = False
```

### MessageInfo

Message information model.

```python
class MessageInfo(msgspec.Struct):
    id: int
    text: Optional[str] = None
    from_user: Optional[UserInfo] = None
    chat: ChatInfo
    date: str
    reply_to: Optional[int] = None
    media: Optional[Dict[str, Any]] = None
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
# UserTelegramClient
async with UserTelegramClient(config) as client:
    user_info = await client.get_me()

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
