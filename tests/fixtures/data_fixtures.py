"""
Pytest fixtures for test data.
"""

# Python imports
import pytest

# Local imports
from tma_test_framework.config import Config
from tma_test_framework.clients.mtproto_client import UserInfo, ChatInfo, MessageInfo
from tma_test_framework.clients.models import MiniAppInfo, ApiResult
from tests.data.constants import (
    ERROR_API_RESULT_DATA,
    TIMEOUT_API_RESULT_DATA,
    PERFORMANCE_TEST_DATA,
    VALID_ENV_VARS,
    INVALID_ENV_VARS,
    MISSING_ENV_VARS,
    VALID_SESSION_STRING,
    INVALID_SESSION_STRING,
    BOT_START_RESPONSE,
    BOT_HELP_RESPONSE,
    BOT_ERROR_RESPONSE,
    MINI_APP_HTML_CONTENT,
    MINI_APP_API_ENDPOINTS,
    CONNECTION_ERROR,
    TIMEOUT_ERROR,
    AUTHENTICATION_ERROR,
    VALIDATION_ERROR,
    NETWORK_ERROR,
    UNKNOWN_ERROR,
)


# Module-level constants for dynamic factories
# These are defined at module level so dynamic factories can reference them directly
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

VALID_CHAT_INFO_DATA = {
    "id": 987654321,
    "title": "Test Chat",
    "type": "group",
    "username": "test_chat",
    "is_bot": False,
    "is_verified": False,
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

VALID_MINI_APP_INFO_DATA = {
    "url": "https://example.com/mini-app",
    "start_param": "test_param",
    "theme_params": {"bg_color": "#ffffff", "text_color": "#000000"},
    "platform": "web",
}

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


# User info fixtures
@pytest.fixture
def valid_user_info_data() -> dict[str, int | str | bool]:
    """
    Valid user info data.

    Returns:
        dict[str, int | str | bool]: Valid user info data.
    """
    return {
        "id": 123456789,
        "first_name": "Test User",
        "username": "test_user",
        "last_name": "Test",
        "phone": "+1234567890",
        "is_bot": False,
        "is_verified": True,
        "is_premium": False,
    }


@pytest.fixture
def bot_user_info_data() -> dict[str, int | str | bool]:
    """
    Bot user info data.

    Returns:
        dict[str, int | str | bool]: Bot user info data.
    """
    return {
        "id": 987654321,
        "first_name": "Test Bot",
        "username": "test_bot",
        "last_name": None,
        "phone": None,
        "is_bot": True,
        "is_verified": False,
        "is_premium": False,
    }


@pytest.fixture
def minimal_user_info_data() -> dict[str, int | str | bool]:
    """
    Minimal user info data.

    Returns:
        dict[str, int | str | bool]: Minimal user info data.
    """
    return {
        "id": 111222333,
        "first_name": "Minimal User",
        "username": None,
        "last_name": None,
        "phone": None,
        "is_bot": False,
        "is_verified": False,
        "is_premium": False,
    }


@pytest.fixture
def edge_case_user_info_data():
    """Edge case user info data."""
    return {
        "id": 0,  # Edge case: minimum ID
        "first_name": "",  # Edge case: empty first name
        "username": "a" * 100,  # Edge case: very long username
        "last_name": "b" * 100,  # Edge case: very long last name
        "phone": "+12345678901234567890",  # Edge case: very long phone
        "is_bot": False,
        "is_verified": False,
        "is_premium": False,
    }


@pytest.fixture
def unicode_user_info_data():
    """Unicode user info data."""
    return {
        "id": 123456789,
        "first_name": "Тест Пользователь",  # Cyrillic
        "username": "test_用户",  # Mixed Latin and Chinese
        "last_name": "テスト",  # Japanese
        "phone": "+1234567890",
        "is_bot": False,
        "is_verified": True,
        "is_premium": False,
    }


# User info object fixtures
@pytest.fixture
def valid_user_info(valid_user_info_data) -> UserInfo:
    """
    Valid UserInfo instance.

    Returns:
        UserInfo: Valid UserInfo object.
    """
    return UserInfo(**valid_user_info_data)


@pytest.fixture
def unicode_user_info(unicode_user_info_data) -> UserInfo:
    """
    Unicode UserInfo instance.

    Returns:
        UserInfo: Unicode UserInfo object.
    """
    return UserInfo(**unicode_user_info_data)


# Chat info fixtures
@pytest.fixture
def valid_chat_info_data() -> dict[str, int | str | bool]:
    """
    Valid chat info data.

    Returns:
        dict[str, int | str | bool]: Valid chat info data.
    """
    return {
        "id": 987654321,
        "title": "Test Chat",
        "type": "group",
        "username": "test_chat",
        "is_bot": False,
        "is_verified": False,
    }


@pytest.fixture
def private_chat_info_data() -> dict[str, int | str | bool]:
    """
    Private chat info data.

    Returns:
        dict[str, int | str | bool]: Private chat info data.
    """
    return {
        "id": 111222333,
        "title": "Private Chat",
        "type": "private",
        "username": None,
        "is_bot": False,
        "is_verified": False,
    }


@pytest.fixture
def channel_chat_info_data() -> dict[str, int | str | bool]:
    """
    Channel chat info data.

    Returns:
        dict[str, int | str | bool]: Channel chat info data.
    """
    return {
        "id": 444555666,
        "title": "Test Channel",
        "type": "channel",
        "username": "test_channel",
        "is_bot": False,
        "is_verified": True,
    }


# Chat info object fixtures
@pytest.fixture
def valid_chat_info(valid_chat_info_data) -> ChatInfo:
    """
    Valid ChatInfo instance.

    Returns:
        ChatInfo: Valid ChatInfo object.
    """
    return ChatInfo(**valid_chat_info_data)


# Message info fixtures
@pytest.fixture
def valid_message_info_data(valid_chat_info_data, valid_user_info_data):
    """Valid message info data with chat and user."""
    data = {
        "id": 111222333,
        "chat": None,  # Will be set below
        "date": "2023-10-20T10:00:00Z",
        "text": "Test message",
        "from_user": None,  # Will be set below
        "reply_to": None,
        "media": None,
    }
    data["chat"] = valid_chat_info_data
    data["from_user"] = valid_user_info_data
    return data


@pytest.fixture
def reply_message_info_data(valid_chat_info_data, valid_user_info_data):
    """Reply message info data with chat and user."""
    data = {
        "id": 222333444,
        "chat": None,  # Will be set below
        "date": "2023-10-20T10:01:00Z",
        "text": "Reply message",
        "from_user": None,  # Will be set below
        "reply_to": 111222333,
        "media": None,
    }
    data["chat"] = valid_chat_info_data
    data["from_user"] = valid_user_info_data
    return data


@pytest.fixture
def media_message_info_data(valid_chat_info_data, valid_user_info_data):
    """Media message info data with chat and user."""
    data = {
        "id": 333444555,
        "chat": None,  # Will be set below
        "date": "2023-10-20T10:02:00Z",
        "text": "Message with media",
        "from_user": None,  # Will be set below
        "reply_to": None,
        "media": {
            "type": "photo",
            "url": "https://example.com/photo.jpg",
            "size": 1024,
        },
    }
    data["chat"] = valid_chat_info_data
    data["from_user"] = valid_user_info_data
    return data


@pytest.fixture
def edge_case_message_info_data(valid_chat_info_data, valid_user_info_data):
    """Edge case message info data with chat and user."""
    data = {
        "id": 0,  # Edge case: minimum ID
        "chat": None,  # Will be set below
        "date": "1970-01-01T00:00:00Z",  # Edge case: epoch time
        "text": "a" * 10000,  # Edge case: very long text
        "from_user": None,  # Will be set below
        "reply_to": None,
        "media": None,
    }
    data["chat"] = valid_chat_info_data
    data["from_user"] = valid_user_info_data
    return data


@pytest.fixture
def unicode_message_info_data(valid_chat_info_data, unicode_user_info_data):
    """Unicode message info data with chat and user."""
    data = {
        "id": 111222333,
        "chat": None,  # Will be set below
        "date": "2023-10-20T10:00:00Z",
        "text": "Hello 世界! Привет мир! こんにちは世界!",  # Mixed languages
        "from_user": None,  # Will be set below
        "reply_to": None,
        "media": None,
    }
    data["chat"] = valid_chat_info_data
    data["from_user"] = unicode_user_info_data
    return data


@pytest.fixture
def valid_message_info(valid_chat_info, valid_user_info):
    """Valid MessageInfo instance."""
    data = {
        "id": 111222333,
        "chat": valid_chat_info,
        "date": "2023-10-20T10:00:00Z",
        "text": "Test message",
        "from_user": valid_user_info,
        "reply_to": None,
        "media": None,
    }
    return MessageInfo(**data)


@pytest.fixture
def reply_message_info(valid_chat_info, valid_user_info):
    """Reply MessageInfo instance."""
    data = {
        "id": 222333444,
        "chat": valid_chat_info,
        "date": "2023-10-20T10:01:00Z",
        "text": "Reply message",
        "from_user": valid_user_info,
        "reply_to": 111222333,
        "media": None,
    }
    return MessageInfo(**data)


@pytest.fixture
def media_message_info(valid_chat_info, valid_user_info):
    """Media MessageInfo instance."""
    data = {
        "id": 333444555,
        "chat": valid_chat_info,
        "date": "2023-10-20T10:02:00Z",
        "text": "Message with media",
        "from_user": valid_user_info,
        "reply_to": None,
        "media": {
            "type": "photo",
            "url": "https://example.com/photo.jpg",
            "size": 1024,
        },
    }
    return MessageInfo(**data)


@pytest.fixture
def edge_case_message_info(valid_chat_info, valid_user_info):
    """Edge case MessageInfo instance."""
    data = {
        "id": 0,  # Edge case: minimum ID
        "chat": valid_chat_info,
        "date": "1970-01-01T00:00:00Z",  # Edge case: epoch time
        "text": "a" * 10000,  # Edge case: very long text
        "from_user": valid_user_info,
        "reply_to": None,
        "media": None,
    }
    return MessageInfo(**data)


@pytest.fixture
def unicode_message_info(valid_chat_info, unicode_user_info):
    """Unicode MessageInfo instance."""
    data = {
        "id": 111222333,
        "chat": valid_chat_info,
        "date": "2023-10-20T10:00:00Z",
        "text": "Hello 世界! Привет мир! こんにちは世界!",  # Mixed languages
        "from_user": unicode_user_info,
        "reply_to": None,
        "media": None,
    }
    return MessageInfo(**data)


# Mini App info fixtures
@pytest.fixture
def valid_mini_app_info_data():
    """Valid mini app info data."""
    return {
        "url": "https://example.com/mini-app",
        "title": "Test Mini App",
        "description": "Test Mini App Description",
        "platform": "web",
    }


@pytest.fixture
def mobile_mini_app_info_data():
    """Mobile mini app info data."""
    return {
        "url": "https://example.com/mobile-mini-app",
        "title": "Mobile Mini App",
        "description": "Mobile Mini App Description",
        "platform": "mobile",
    }


@pytest.fixture
def valid_mini_app_info(valid_mini_app_info_data):
    """Valid MiniAppInfo instance."""
    return MiniAppInfo(**valid_mini_app_info_data)


@pytest.fixture
def mobile_mini_app_info(mobile_mini_app_info_data):
    """Mobile MiniAppInfo instance."""
    return MiniAppInfo(**mobile_mini_app_info_data)


# API result fixtures
@pytest.fixture
def valid_api_result_data():
    """Valid API result data."""
    return VALID_API_RESULT_DATA.copy()


@pytest.fixture
def error_api_result_data():
    """Error API result data."""
    return ERROR_API_RESULT_DATA.copy()


@pytest.fixture
def timeout_api_result_data():
    """Timeout API result data."""
    return TIMEOUT_API_RESULT_DATA.copy()


@pytest.fixture
def valid_api_result(valid_api_result_data):
    """Valid ApiResult instance."""
    return ApiResult(**valid_api_result_data)


@pytest.fixture
def error_api_result(error_api_result_data):
    """Error ApiResult instance."""
    return ApiResult(**error_api_result_data)


@pytest.fixture
def timeout_api_result(timeout_api_result_data):
    """Timeout ApiResult instance."""
    return ApiResult(**timeout_api_result_data)


# Config fixtures
@pytest.fixture
def valid_config_data() -> dict:
    """
    Valid config data.

    Returns:
        dict: Valid config data.
    """
    return VALID_CONFIG_DATA.copy()


@pytest.fixture
def valid_config(valid_config_data) -> Config:
    """
    Valid Config instance.

    Returns:
        Config: Valid Config object.
    """
    return Config(**valid_config_data)


# Environment variables fixtures
@pytest.fixture
def valid_env_vars():
    """Valid environment variables."""
    return VALID_ENV_VARS.copy()


@pytest.fixture
def invalid_env_vars():
    """Invalid environment variables."""
    return INVALID_ENV_VARS.copy()


@pytest.fixture
def missing_env_vars():
    """Missing environment variables."""
    return MISSING_ENV_VARS.copy()


# Session fixtures
@pytest.fixture
def valid_session_string():
    """Valid session string."""
    return VALID_SESSION_STRING


@pytest.fixture
def invalid_session_string():
    """Invalid session string."""
    return INVALID_SESSION_STRING


# Bot interaction fixtures
@pytest.fixture
def bot_start_response():
    """Bot start response data."""
    return BOT_START_RESPONSE.copy()


@pytest.fixture
def bot_help_response():
    """Bot help response data."""
    return BOT_HELP_RESPONSE.copy()


@pytest.fixture
def bot_error_response():
    """Bot error response data."""
    return BOT_ERROR_RESPONSE.copy()


# Mini App fixtures
@pytest.fixture
def mini_app_html_content():
    """Mini App HTML content."""
    return MINI_APP_HTML_CONTENT


@pytest.fixture
def mini_app_api_endpoints():
    """Mini App API endpoints data."""
    return MINI_APP_API_ENDPOINTS.copy()


# Error fixtures
@pytest.fixture
def connection_error():
    """Connection error message."""
    return CONNECTION_ERROR


@pytest.fixture
def timeout_error():
    """Timeout error message."""
    return TIMEOUT_ERROR


@pytest.fixture
def authentication_error():
    """Authentication error message."""
    return AUTHENTICATION_ERROR


@pytest.fixture
def validation_error():
    """Validation error message."""
    return VALIDATION_ERROR


@pytest.fixture
def network_error():
    """Network error message."""
    return NETWORK_ERROR


@pytest.fixture
def unknown_error():
    """Unknown error message."""
    return UNKNOWN_ERROR


# Performance fixtures
@pytest.fixture
def performance_test_data():
    """Performance test data."""
    return PERFORMANCE_TEST_DATA.copy()


# Collection fixtures
@pytest.fixture
def user_info_list(valid_user_info):
    """List of UserInfo instances."""
    users = []
    for i in range(5):
        user_data = VALID_USER_INFO_DATA.copy()
        user_data.update(
            {
                "id": 123456789 + i,
                "username": f"test_user_{i}",
                "first_name": f"Test User {i}",
            }
        )
        users.append(UserInfo(**user_data))
    return users


@pytest.fixture
def chat_info_list(valid_chat_info):
    """List of ChatInfo instances."""
    chats = []
    for i in range(3):
        chat_data = VALID_CHAT_INFO_DATA.copy()
        chat_data.update(
            {
                "id": 987654321 + i,
                "title": f"Test Chat {i}",
                "username": f"test_chat_{i}",
            }
        )
        chats.append(ChatInfo(**chat_data))
    return chats


@pytest.fixture
def message_info_list(valid_message_info):
    """List of MessageInfo instances."""
    messages = []
    for i in range(5):
        message_data = VALID_MESSAGE_INFO_DATA.copy()
        message_data.update(
            {
                "id": 111222333 + i,
                "text": f"Test message {i}",
                "date": f"2023-10-20T10:0{i}:00Z",
            }
        )
        # Create chat and user for each message
        chat_data = VALID_CHAT_INFO_DATA.copy()
        chat_data["id"] = 987654321 + i
        chat = ChatInfo(**chat_data)

        user_data = VALID_USER_INFO_DATA.copy()
        user_data["id"] = 123456789 + i
        user = UserInfo(**user_data)

        message_data["chat"] = chat
        message_data["from_user"] = user
        messages.append(MessageInfo(**message_data))
    return messages


@pytest.fixture
def api_result_list(valid_api_result):
    """List of ApiResult instances."""
    results = []
    for i in range(5):
        result_data = VALID_API_RESULT_DATA.copy()
        result_data.update(
            {
                "data": {"test": f"data_{i}", "value": i},
                "response_time": 0.1 + (i * 0.1),
            }
        )
        results.append(ApiResult(**result_data))
    return results


# JSON fixtures
@pytest.fixture
def json_test_data(
    valid_user_info_data,
    valid_chat_info_data,
    valid_message_info_data,
    valid_mini_app_info_data,
    valid_api_result_data,
    valid_config_data,
):
    """JSON test data for serialization testing."""
    return {
        "user": valid_user_info_data,
        "chat": valid_chat_info_data,
        "message": valid_message_info_data,
        "mini_app": valid_mini_app_info_data,
        "api_result": valid_api_result_data,
        "config": valid_config_data,
    }


@pytest.fixture
def large_json_test_data(
    valid_user_info_data,
    valid_chat_info_data,
    valid_message_info_data,
    valid_config_data,
):
    """Large JSON test data for performance testing."""
    return {
        "users": [valid_user_info_data for _ in range(100)],
        "chats": [valid_chat_info_data for _ in range(50)],
        "messages": [valid_message_info_data for _ in range(1000)],
        "config": valid_config_data,
    }


# Parametrized fixtures
@pytest.fixture(params=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
def valid_log_level(request):
    """Valid log level."""
    return request.param


@pytest.fixture(params=["private", "group", "supergroup", "channel"])
def valid_chat_type(request):
    """Valid chat type."""
    return request.param


@pytest.fixture(params=["web", "mobile", "desktop", "tv"])
def valid_platform(request):
    """Valid platform."""
    return request.param


@pytest.fixture(params=[200, 201, 400, 401, 403, 404, 500, 502, 503])
def valid_status_code(request):
    """Valid HTTP status code."""
    return request.param


# Dynamic fixtures
@pytest.fixture
def config_with_custom_values():
    """Config with custom values."""

    def _create_config(**kwargs):
        base_data = VALID_CONFIG_DATA.copy()
        base_data.update(kwargs)
        return Config(**base_data)

    return _create_config


@pytest.fixture
def user_info_with_custom_values():
    """UserInfo with custom values."""

    def _create_user(**kwargs):
        base_data = VALID_USER_INFO_DATA.copy()
        base_data.update(kwargs)
        return UserInfo(**base_data)

    return _create_user


@pytest.fixture
def chat_info_with_custom_values():
    """ChatInfo with custom values."""

    def _create_chat(**kwargs):
        base_data = VALID_CHAT_INFO_DATA.copy()
        base_data.update(kwargs)
        return ChatInfo(**base_data)

    return _create_chat


@pytest.fixture
def message_info_with_custom_values(valid_chat_info, valid_user_info):
    """MessageInfo with custom values."""

    def _create_message(**kwargs):
        base_data = VALID_MESSAGE_INFO_DATA.copy()
        base_data.update(kwargs)
        # Convert dict chat/user to objects if needed
        if isinstance(base_data.get("chat"), dict):
            base_data["chat"] = ChatInfo(**base_data["chat"])
        elif base_data.get("chat") is None:
            base_data["chat"] = valid_chat_info
        if isinstance(base_data.get("from_user"), dict):
            base_data["from_user"] = UserInfo(**base_data["from_user"])
        elif base_data.get("from_user") is None:
            base_data["from_user"] = valid_user_info
        return MessageInfo(**base_data)

    return _create_message


@pytest.fixture
def mini_app_info_with_custom_values():
    """MiniAppInfo with custom values."""

    def _create_mini_app(**kwargs):
        base_data = VALID_MINI_APP_INFO_DATA.copy()
        base_data.update(kwargs)
        return MiniAppInfo(**base_data)

    return _create_mini_app


@pytest.fixture
def api_result_with_custom_values():
    """ApiResult with custom values."""

    def _create_api_result(**kwargs):
        base_data = VALID_API_RESULT_DATA.copy()
        base_data.update(kwargs)
        return ApiResult(**base_data)

    return _create_api_result
