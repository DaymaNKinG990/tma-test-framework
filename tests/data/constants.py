"""
Test data constants for TMA Framework tests.
"""

# User info test data
VALID_USER_INFO_DATA = {
    "id": 123456789,
    "first_name": "Test User",
    "username": "test_user",
    "last_name": "Test",
    "phone": "+1234567890",
    "is_bot": False,
    "is_verified": True,
    "is_premium": False,
}

BOT_USER_INFO_DATA = {
    "id": 987654321,
    "first_name": "Test Bot",
    "username": "test_bot",
    "last_name": None,
    "phone": None,
    "is_bot": True,
    "is_verified": False,
    "is_premium": False,
}

MINIMAL_USER_INFO_DATA = {
    "id": 111222333,
    "first_name": "Minimal User",
    "username": None,
    "last_name": None,
    "phone": None,
    "is_bot": False,
    "is_verified": False,
    "is_premium": False,
}

# Chat info test data
VALID_CHAT_INFO_DATA = {
    "id": 987654321,
    "title": "Test Chat",
    "type": "group",
    "username": "test_chat",
    "is_verified": False,
}

PRIVATE_CHAT_INFO_DATA = {
    "id": 111222333,
    "title": "Private Chat",
    "type": "private",
    "username": None,
    "is_verified": False,
}

CHANNEL_CHAT_INFO_DATA = {
    "id": 444555666,
    "title": "Test Channel",
    "type": "channel",
    "username": "test_channel",
    "is_verified": True,
}
VALID_MESSAGE_INFO_DATA = {
    "id": 111222333,
    "chat": None,  # Will be set in fixtures
    "date": "2023-10-20T10:00:00Z",
    "text": "Test message",
    "from_user": None,  # Will be set in fixtures
    "reply_to": None,
    "media": None,
}

REPLY_MESSAGE_INFO_DATA = {
    "id": 222333444,
    "chat": None,  # Will be set in fixtures
    "date": "2023-10-20T10:01:00Z",
    "text": "Reply message",
    "from_user": None,  # Will be set in fixtures
    "reply_to": 111222333,
    "media": None,
}

MEDIA_MESSAGE_INFO_DATA = {
    "id": 333444555,
    "chat": None,  # Will be set in fixtures
    "date": "2023-10-20T10:02:00Z",
    "text": "Message with media",
    "from_user": None,  # Will be set in fixtures
    "reply_to": None,
    "media": {"type": "photo", "url": "https://example.com/photo.jpg", "size": 1024},
}

# Mini App info test data
VALID_MINI_APP_INFO_DATA = {
    "url": "https://example.com/mini-app",
    "start_param": "test_param",
    "theme_params": {"bg_color": "#ffffff", "text_color": "#000000"},
    "platform": "web",
}

MOBILE_MINI_APP_INFO_DATA = {
    "url": "https://example.com/mobile-mini-app",
    "start_param": None,
    "theme_params": None,
    "platform": "mobile",
}

MINIMAL_MINI_APP_INFO_DATA = {
    "url": "https://t.me/mybot/app?start=123"
    # start_param, theme_params default to None, platform defaults to "web"
}

EDGE_CASE_MINI_APP_INFO_DATA = {
    "url": "",  # Empty URL
    "start_param": "",
    "theme_params": {},
    "platform": "web",
}

UNICODE_MINI_APP_INFO_DATA = {
    "url": "https://example.com/тест-приложение",
    "start_param": "параметр_用户_テスト",
    "theme_params": {"title": "Тест", "description": "测试"},
    "platform": "web",
}

# API result test data
VALID_API_RESULT_DATA = {
    "endpoint": "/api/status",
    "method": "GET",
    "status_code": 200,
    "response_time": 0.5,
    "success": True,
    "redirect": False,
    "client_error": False,
    "server_error": False,
    "informational": False,
    "headers": {"content-type": "application/json"},
    "body": b'{"status": "ok"}',
    "content_type": "application/json",
    "reason": "OK",
    "error_message": None,
}

ERROR_API_RESULT_DATA = {
    "endpoint": "/api/error",
    "method": "POST",
    "status_code": 400,
    "response_time": 0.2,
    "success": False,
    "redirect": False,
    "client_error": True,
    "server_error": False,
    "informational": False,
    "headers": {"content-type": "application/json"},
    "body": b'{"error": "Bad Request"}',
    "content_type": "application/json",
    "reason": "Bad Request",
    "error_message": "Bad Request",
}

TIMEOUT_API_RESULT_DATA = {
    "endpoint": "/api/timeout",
    "method": "GET",
    "status_code": 408,
    "response_time": 30.0,
    "success": False,
    "redirect": False,
    "client_error": True,
    "server_error": False,
    "informational": False,
    "headers": {},
    "body": b"",
    "content_type": None,
    "reason": "Request Timeout",
    "error_message": "Request timeout",
}

REDIRECT_API_RESULT_DATA = {
    "endpoint": "/api/redirect",
    "method": "GET",
    "status_code": 301,
    "response_time": 0.1,
    "success": False,
    "redirect": True,
    "client_error": False,
    "server_error": False,
    "informational": False,
    "headers": {"location": "https://example.com/new"},
    "body": b"",
    "content_type": None,
    "reason": "Moved Permanently",
    "error_message": None,
}

SERVER_ERROR_API_RESULT_DATA = {
    "endpoint": "/api/server-error",
    "method": "POST",
    "status_code": 500,
    "response_time": 1.5,
    "success": False,
    "redirect": False,
    "client_error": False,
    "server_error": True,
    "informational": False,
    "headers": {"content-type": "text/html"},
    "body": b"Internal Server Error",
    "content_type": "text/html",
    "reason": "Internal Server Error",
    "error_message": "Internal Server Error",
}

INFORMATIONAL_API_RESULT_DATA = {
    "endpoint": "/api/info",
    "method": "GET",
    "status_code": 101,
    "response_time": 0.05,
    "success": False,
    "redirect": False,
    "client_error": False,
    "server_error": False,
    "informational": True,
    "headers": {},
    "body": b"",
    "content_type": None,
    "reason": "Switching Protocols",
    "error_message": None,
}

# Environment variables test data
VALID_ENV_VARS = {
    "TMA_API_ID": "12345",
    "TMA_API_HASH": "test_api_hash",
    "TMA_SESSION_STRING": "test_session_string",
    "TMA_MINI_APP_URL": "https://example.com/mini-app",
    "TMA_MINI_APP_START_PARAM": "test_param",
    "TMA_TIMEOUT": "30",
    "TMA_RETRY_COUNT": "3",
    "TMA_RETRY_DELAY": "1.0",
    "TMA_LOG_LEVEL": "DEBUG",
}

INVALID_ENV_VARS = {
    "TMA_API_ID": "invalid",  # Not a number
    "TMA_API_HASH": "",  # Empty
    "TMA_TIMEOUT": "invalid",  # Not a number
    "TMA_RETRY_COUNT": "invalid",  # Not a number
    "TMA_RETRY_DELAY": "invalid",  # Not a number
    "TMA_LOG_LEVEL": "INVALID",  # Invalid level
}

MISSING_ENV_VARS = {
    "TMA_API_ID": "12345",
    # Missing TMA_API_HASH
    # Missing TMA_SESSION_STRING
}

# Session test data
VALID_SESSION_STRING = "test_session_string_123456789_abcdefghijklmnopqrstuvwxyz"
INVALID_SESSION_STRING = "invalid_session_string"

# Bot interaction test data
BOT_START_RESPONSE = {
    "text": "Welcome to Test Bot! Use /help for commands.",
    "keyboard": {
        "inline_keyboard": [
            [{"text": "Help", "callback_data": "help"}],
            [{"text": "Settings", "callback_data": "settings"}],
        ]
    },
}

BOT_HELP_RESPONSE = {
    "text": "Available commands:\n/start - Start the bot\n/help - Show this help\n/settings - Bot settings",
    "keyboard": None,
}

BOT_ERROR_RESPONSE = {"text": "Error: Bot is not available", "keyboard": None}

# Mini App test data
MINI_APP_HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Mini App</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <div id="app">
        <h1>Test Mini App</h1>
        <button id="test-button">Click Me</button>
        <input id="test-input" type="text" placeholder="Enter text">
        <div id="test-output"></div>
    </div>
    <script>
        document.getElementById('test-button').addEventListener('click', function() {
            const input = document.getElementById('test-input').value;
            document.getElementById('test-output').textContent = 'You entered: ' + input;
        });
    </script>
</body>
</html>
"""

MINI_APP_API_ENDPOINTS = {
    "/api/status": {"method": "GET", "response": {"status": "ok", "version": "1.0.0"}},
    "/api/data": {"method": "GET", "response": {"data": [1, 2, 3, 4, 5]}},
    "/api/submit": {"method": "POST", "response": {"success": True, "id": 123}},
}

# Error test data
CONNECTION_ERROR = "Connection failed"
TIMEOUT_ERROR = "Operation timed out"
AUTHENTICATION_ERROR = "Authentication failed"
VALIDATION_ERROR = "Validation failed"
NETWORK_ERROR = "Network error"
UNKNOWN_ERROR = "Unknown error occurred"

# Performance test data
PERFORMANCE_TEST_DATA = {
    "small": {"size": 100, "iterations": 1000},
    "medium": {"size": 1000, "iterations": 100},
    "large": {"size": 10000, "iterations": 10},
}

# Edge case test data
EDGE_CASE_USER_INFO = {
    "id": 0,  # Edge case: minimum ID
    "first_name": "",  # Edge case: empty first name
    "username": "a" * 100,  # Edge case: very long username
    "last_name": "b" * 100,  # Edge case: very long last name
    "phone": "+1234567890123456789",  # Edge case: very long phone (20 chars)
    "is_bot": False,
    "is_verified": False,
    "is_premium": False,
}

EDGE_CASE_MESSAGE_INFO = {
    "id": 0,  # Edge case: minimum ID
    "chat": None,  # Will be set in fixtures
    "date": "1970-01-01T00:00:00Z",  # Edge case: epoch time
    "text": "a" * 10000,  # Edge case: very long text
    "from_user": None,  # Will be set in fixtures
    "reply_to": None,
    "media": None,
}

# Unicode test data
UNICODE_USER_INFO = {
    "id": 123456789,
    "first_name": "Тест Пользователь",  # Cyrillic
    "username": "test_用户",  # Mixed Latin and Chinese
    "last_name": "テスト",  # Japanese
    "phone": "+1234567890",
    "is_bot": False,
    "is_verified": True,
    "is_premium": False,
}

UNICODE_MESSAGE_INFO = {
    "id": 111222333,
    "chat": None,  # Will be set in fixtures
    "date": "2023-10-20T10:00:00Z",
    "text": "Hello 世界! Привет мир! こんにちは世界!",  # Mixed languages
    "from_user": None,  # Will be set in fixtures
    "reply_to": None,
    "media": None,
}

# UserTelegramClient test data
BOT_COMMANDS = ["/start", "/help", "/start param123"]
BOT_TIMEOUTS = [1, 5, 30]
BOT_USERNAMES = ["test_bot", "mybot", "example_bot"]

MINI_APP_URLS_VALID = [
    "https://t.me/mybot/app?start=abc",
    "https://mybot.t.me/start",
    "https://mybot.telegram.app/start",
    "https://t.me/mybot/app?start=123&ref=test",
]

MINI_APP_URLS_INVALID = [
    "https://example.com",
    "No link here",
    "http://not-telegram.com/app",
    "",
]

MINI_APP_TEXT_SAMPLES = [
    ("Click https://t.me/mybot/app?start=abc", "https://t.me/mybot/app?start=abc"),
    ("No link here", None),
    ("https://example.com", None),
    ("https://mybot.t.me/start", "https://mybot.t.me/start"),
    (
        "Visit https://mybot.telegram.app/start?param=value",
        "https://mybot.telegram.app/start?param=value",
    ),
    ("", None),
]

GET_MESSAGES_LIMITS = [1, 5, 10]
GET_MESSAGES_OFFSET_IDS = [0, 100, 1000]

GET_ENTITY_PARAMS = ["@username", 123456789, "+1234567890"]

# Config test data
VALID_CONFIG_DATA = {
    "api_id": 12345,
    "api_hash": "0123456789abcdef0123456789abcdef",  # 32 characters
    "session_string": "test_session_string_123456789",
    "session_file": None,
    "mini_app_url": "https://example.com/mini-app",
    "mini_app_start_param": "test_param",
    "timeout": 30,
    "retry_count": 3,
    "retry_delay": 1.0,
    "log_level": "INFO",
}
