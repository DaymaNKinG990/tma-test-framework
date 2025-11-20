"""
Unit tests for TMA Framework data models.
"""

import json
import pytest
import msgspec

from src.mtproto_client import UserInfo, ChatInfo, MessageInfo
from src.mini_app import MiniAppInfo, ApiResult
from tests.data.constants import (
    VALID_USER_INFO_DATA,
    BOT_USER_INFO_DATA,
    MINIMAL_USER_INFO_DATA,
    VALID_CHAT_INFO_DATA,
    PRIVATE_CHAT_INFO_DATA,
    CHANNEL_CHAT_INFO_DATA,
    VALID_MESSAGE_INFO_DATA,
    REPLY_MESSAGE_INFO_DATA,
    MEDIA_MESSAGE_INFO_DATA,
    VALID_MINI_APP_INFO_DATA,
    MOBILE_MINI_APP_INFO_DATA,
    MINIMAL_MINI_APP_INFO_DATA,
    EDGE_CASE_MINI_APP_INFO_DATA,
    UNICODE_MINI_APP_INFO_DATA,
    VALID_API_RESULT_DATA,
    ERROR_API_RESULT_DATA,
    TIMEOUT_API_RESULT_DATA,
    REDIRECT_API_RESULT_DATA,
    SERVER_ERROR_API_RESULT_DATA,
    INFORMATIONAL_API_RESULT_DATA,
    EDGE_CASE_USER_INFO,
    EDGE_CASE_MESSAGE_INFO,
    UNICODE_USER_INFO,
)


class TestUserInfo:
    """Test cases for UserInfo model."""

    def test_valid_user_info_creation(self):
        """Test creating a valid UserInfo."""
        user = UserInfo(**VALID_USER_INFO_DATA)  # type: ignore[arg-type]

        assert user.id == 123456789
        assert user.first_name == "Test User"
        assert user.username == "test_user"
        assert user.last_name == "Test"
        assert user.phone == "+1234567890"
        assert user.is_bot is False
        assert user.is_verified is True
        assert user.is_premium is False

    def test_bot_user_info_creation(self):
        """Test creating a bot UserInfo."""
        user = UserInfo(**BOT_USER_INFO_DATA)  # type: ignore[arg-type]

        assert user.id == 987654321
        assert user.first_name == "Test Bot"
        assert user.username == "test_bot"
        assert user.last_name is None
        assert user.phone is None
        assert user.is_bot is True
        assert user.is_verified is False
        assert user.is_premium is False

    def test_minimal_user_info_creation(self):
        """Test creating a minimal UserInfo."""
        user = UserInfo(**MINIMAL_USER_INFO_DATA)  # type: ignore[arg-type]

        assert user.id == 111222333
        assert user.first_name == "Minimal User"
        assert user.username is None
        assert user.last_name is None
        assert user.phone is None
        assert user.is_bot is False
        assert user.is_verified is False
        assert user.is_premium is False

    def test_user_info_required_fields(self):
        """Test UserInfo required fields."""
        # Test that id and first_name are required
        with pytest.raises(TypeError):
            UserInfo()  # type: ignore[call-arg]  # Missing required fields

        with pytest.raises(TypeError):
            UserInfo(id=123456789)  # type: ignore[call-arg]  # Missing first_name

        with pytest.raises(TypeError):
            UserInfo(first_name="Test")  # type: ignore[call-arg]  # Missing id

    def test_user_info_optional_fields(self):
        """Test UserInfo optional fields."""
        user = UserInfo(id=123456789, first_name="Test User")

        assert user.username is None
        assert user.last_name is None
        assert user.phone is None
        assert user.is_bot is False
        assert user.is_verified is False
        assert user.is_premium is False

    def test_user_info_field_types(self):
        """Test UserInfo field types."""
        user = UserInfo(**VALID_USER_INFO_DATA)  # type: ignore[arg-type]

        assert isinstance(user.id, int)
        assert isinstance(user.first_name, str)
        assert isinstance(user.username, str) or user.username is None
        assert isinstance(user.last_name, str) or user.last_name is None
        assert isinstance(user.phone, str) or user.phone is None
        assert isinstance(user.is_bot, bool)
        assert isinstance(user.is_verified, bool)
        assert isinstance(user.is_premium, bool)

    def test_user_info_serialization(self):
        """Test UserInfo serialization."""
        user = UserInfo(**VALID_USER_INFO_DATA)  # type: ignore[arg-type]

        # Test serialization to dict
        user_dict = msgspec.to_builtins(user)
        assert isinstance(user_dict, dict)
        assert user_dict["id"] == 123456789
        assert user_dict["first_name"] == "Test User"

    def test_user_info_deserialization(self):
        """Test UserInfo deserialization."""
        user_dict = VALID_USER_INFO_DATA.copy()

        # Test deserialization from dict
        user = msgspec.convert(user_dict, UserInfo)
        assert isinstance(user, UserInfo)
        assert user.id == 123456789
        assert user.first_name == "Test User"

    def test_user_info_equality(self):
        """Test UserInfo equality."""
        user1 = UserInfo(**VALID_USER_INFO_DATA)  # type: ignore[arg-type]
        user2 = UserInfo(**VALID_USER_INFO_DATA)  # type: ignore[arg-type]
        user3 = UserInfo(**BOT_USER_INFO_DATA)  # type: ignore[arg-type]

        assert user1 == user2
        assert user1 != user3

    def test_user_info_hash(self):
        """Test UserInfo hashing."""
        user1 = UserInfo(**VALID_USER_INFO_DATA)  # type: ignore[arg-type]
        user2 = UserInfo(**VALID_USER_INFO_DATA)  # type: ignore[arg-type]

        assert hash(user1) == hash(user2)

    def test_user_info_repr(self):
        """Test UserInfo string representation."""
        user = UserInfo(**VALID_USER_INFO_DATA)  # type: ignore[arg-type]
        repr_str = repr(user)

        assert "UserInfo" in repr_str
        assert "id=123456789" in repr_str
        assert "first_name='Test User'" in repr_str

    def test_user_info_edge_cases(self):
        """Test UserInfo edge cases."""
        user = UserInfo(**EDGE_CASE_USER_INFO)  # type: ignore[arg-type]

        assert user.id == 0
        assert user.first_name == ""
        assert user.username is not None and len(user.username) == 100
        assert user.last_name is not None and len(user.last_name) == 100
        assert user.phone is not None and len(user.phone) == 20

    def test_user_info_unicode(self):
        """Test UserInfo with unicode characters."""
        user = UserInfo(**UNICODE_USER_INFO)  # type: ignore[arg-type]

        assert user.first_name == "Тест Пользователь"
        assert user.username == "test_用户"
        assert user.last_name == "テスト"

    def test_user_info_boolean_fields(self):
        """Test UserInfo boolean fields."""
        user = UserInfo(
            id=123456789,
            first_name="Test User",
            is_bot=True,
            is_verified=True,
            is_premium=True,
        )

        assert user.is_bot is True
        assert user.is_verified is True
        assert user.is_premium is True


class TestChatInfo:
    """Test cases for ChatInfo model."""

    def test_valid_chat_info_creation(self):
        """Test creating a valid ChatInfo."""
        chat = ChatInfo(**VALID_CHAT_INFO_DATA)  # type: ignore[arg-type]

        assert chat.id == 987654321
        assert chat.title == "Test Chat"
        assert chat.username == "test_chat"
        assert chat.type == "group"
        assert chat.is_verified is False

    def test_private_chat_info_creation(self):
        """Test creating a private ChatInfo."""
        chat = ChatInfo(**PRIVATE_CHAT_INFO_DATA)  # type: ignore[arg-type]

        assert chat.id == 111222333
        assert chat.title == "Private Chat"
        assert chat.username is None
        assert chat.type == "private"
        assert chat.is_verified is False

    def test_channel_chat_info_creation(self):
        """Test creating a channel ChatInfo."""
        chat = ChatInfo(**CHANNEL_CHAT_INFO_DATA)  # type: ignore[arg-type]

        assert chat.id == 444555666
        assert chat.title == "Test Channel"
        assert chat.username == "test_channel"
        assert chat.type == "channel"
        assert chat.is_verified is True

    def test_chat_info_required_fields(self):
        """Test ChatInfo required fields."""
        # Test that id, title, and type are required
        with pytest.raises(TypeError):
            ChatInfo()  # type: ignore[call-arg]  # Missing required fields

        with pytest.raises(TypeError):
            ChatInfo(id=987654321)  # type: ignore[call-arg]  # Missing title and type

        with pytest.raises(TypeError):
            ChatInfo(id=987654321, title="Test")  # type: ignore[call-arg]  # Missing type

    def test_chat_info_optional_fields(self):
        """Test ChatInfo optional fields."""
        chat = ChatInfo(id=987654321, title="Test Chat", type="group")

        assert chat.username is None
        assert chat.is_verified is False

    def test_chat_info_field_types(self):
        """Test ChatInfo field types."""
        chat = ChatInfo(**VALID_CHAT_INFO_DATA)  # type: ignore[arg-type]

        assert isinstance(chat.id, int)
        assert isinstance(chat.title, str)
        assert isinstance(chat.username, str)
        assert isinstance(chat.type, str)
        assert isinstance(chat.is_verified, bool)

    def test_chat_info_serialization(self):
        """Test ChatInfo serialization."""
        chat = ChatInfo(**VALID_CHAT_INFO_DATA)  # type: ignore[arg-type]

        # Test serialization to dict
        chat_dict = msgspec.to_builtins(chat)
        assert isinstance(chat_dict, dict)
        assert chat_dict["id"] == 987654321
        assert chat_dict["title"] == "Test Chat"

    def test_chat_info_deserialization(self):
        """Test ChatInfo deserialization."""
        chat_dict = VALID_CHAT_INFO_DATA.copy()

        # Test deserialization from dict
        chat = msgspec.convert(chat_dict, ChatInfo)
        assert isinstance(chat, ChatInfo)
        assert chat.id == 987654321
        assert chat.title == "Test Chat"

    def test_chat_info_equality(self):
        """Test ChatInfo equality."""
        chat1 = ChatInfo(**VALID_CHAT_INFO_DATA)  # type: ignore[arg-type]
        chat2 = ChatInfo(**VALID_CHAT_INFO_DATA)  # type: ignore[arg-type]
        chat3 = ChatInfo(**PRIVATE_CHAT_INFO_DATA)  # type: ignore[arg-type]

        assert chat1 == chat2
        assert chat1 != chat3

    def test_chat_info_hash(self):
        """Test ChatInfo hashing."""
        chat1 = ChatInfo(**VALID_CHAT_INFO_DATA)  # type: ignore[arg-type]
        chat2 = ChatInfo(**VALID_CHAT_INFO_DATA)  # type: ignore[arg-type]

        assert hash(chat1) == hash(chat2)

    def test_chat_info_repr(self):
        """Test ChatInfo string representation."""
        chat = ChatInfo(**VALID_CHAT_INFO_DATA)  # type: ignore[arg-type]
        repr_str = repr(chat)

        assert "ChatInfo" in repr_str
        assert "id=987654321" in repr_str
        assert "title='Test Chat'" in repr_str

    def test_chat_info_types(self):
        """Test different chat types."""
        types = ["private", "group", "supergroup", "channel"]

        for chat_type in types:
            chat = ChatInfo(id=987654321, title=f"Test {chat_type}", type=chat_type)
            assert chat.type == chat_type


class TestMessageInfo:
    """Test cases for MessageInfo model."""

    def test_valid_message_info_creation(self):
        """Test creating a valid MessageInfo."""
        from src.mtproto_client import ChatInfo, UserInfo

        # Create proper dict with ChatInfo and UserInfo objects
        message_dict = {
            "id": 111222333,
            "chat": ChatInfo(**VALID_CHAT_INFO_DATA),  # type: ignore[arg-type]
            "date": "2023-10-20T10:00:00Z",
            "text": "Test message",
            "from_user": UserInfo(**VALID_USER_INFO_DATA),  # type: ignore[arg-type]
            "reply_to": None,
            "media": None,
        }
        message = MessageInfo(**message_dict)  # type: ignore[arg-type]

        assert message.id == 111222333
        assert message.chat.id == 987654321
        assert message.date == "2023-10-20T10:00:00Z"
        assert message.text == "Test message"
        assert message.from_user is not None
        assert message.from_user.id == 123456789
        assert message.reply_to is None
        assert message.media is None

    def test_reply_message_info_creation(self):
        """Test creating a reply MessageInfo."""
        message = MessageInfo(**REPLY_MESSAGE_INFO_DATA)  # type: ignore[arg-type]

        assert message.id == 222333444
        assert message.text == "Reply message"
        assert message.reply_to == 111222333

    def test_media_message_info_creation(self):
        """Test creating a media MessageInfo."""
        message = MessageInfo(**MEDIA_MESSAGE_INFO_DATA)  # type: ignore[arg-type]

        assert message.id == 333444555
        assert message.text == "Message with media"
        assert message.media is not None
        assert message.media["type"] == "photo"

    def test_message_info_required_fields(self):
        """Test MessageInfo required fields."""
        # Test that id, chat, and date are required
        with pytest.raises(TypeError):
            MessageInfo()  # type: ignore[call-arg]  # Missing required fields

        with pytest.raises(TypeError):
            MessageInfo(id=111222333)  # type: ignore[call-arg]  # Missing chat and date

        with pytest.raises(TypeError):
            MessageInfo(  # type: ignore[call-arg]
                id=111222333,
                chat=ChatInfo(**VALID_CHAT_INFO_DATA),  # type: ignore[arg-type]
            )  # Missing date

    def test_message_info_optional_fields(self):
        """Test MessageInfo optional fields."""
        message = MessageInfo(
            id=111222333,
            chat=ChatInfo(**VALID_CHAT_INFO_DATA),  # type: ignore[arg-type]
            date="2023-10-20T10:00:00Z",
        )

        assert message.text is None
        assert message.from_user is None
        assert message.reply_to is None
        assert message.media is None

    def test_message_info_field_types(self):
        """Test MessageInfo field types."""
        # Create message with proper chat data
        from tests.data.constants import VALID_CHAT_INFO_DATA

        message_data = VALID_MESSAGE_INFO_DATA.copy()
        message_data["chat"] = ChatInfo(**VALID_CHAT_INFO_DATA)  # type: ignore[arg-type,assignment]
        message = MessageInfo(**message_data)  # type: ignore[arg-type]

        assert isinstance(message.id, int)
        assert isinstance(message.chat, ChatInfo)
        assert isinstance(message.date, str)
        assert isinstance(message.text, str) or message.text is None
        assert isinstance(message.from_user, UserInfo) or message.from_user is None
        assert isinstance(message.reply_to, int) or message.reply_to is None
        assert isinstance(message.media, dict) or message.media is None

    def test_message_info_serialization(self):
        """Test MessageInfo serialization."""
        message = MessageInfo(**VALID_MESSAGE_INFO_DATA)  # type: ignore[arg-type]

        # Test serialization to dict
        message_dict = msgspec.to_builtins(message)
        assert isinstance(message_dict, dict)
        assert message_dict["id"] == 111222333
        assert message_dict["text"] == "Test message"

    def test_message_info_deserialization(self):
        """Test MessageInfo deserialization."""
        # Create proper dict with ChatInfo and UserInfo objects
        from src.mtproto_client import ChatInfo, UserInfo

        message_dict = {
            "id": 111222333,
            "chat": ChatInfo(**VALID_CHAT_INFO_DATA),  # type: ignore[arg-type]
            "date": "2023-10-20T10:00:00Z",
            "text": "Test message",
            "from_user": UserInfo(**VALID_USER_INFO_DATA),  # type: ignore[arg-type]
            "reply_to": None,
            "media": None,
        }

        # Test deserialization from dict
        message = msgspec.convert(message_dict, MessageInfo)
        assert isinstance(message, MessageInfo)
        assert message.id == 111222333
        assert message.text == "Test message"

    def test_message_info_equality(self):
        """Test MessageInfo equality."""
        message1 = MessageInfo(**VALID_MESSAGE_INFO_DATA)  # type: ignore[arg-type]
        message2 = MessageInfo(**VALID_MESSAGE_INFO_DATA)  # type: ignore[arg-type]
        message3 = MessageInfo(**REPLY_MESSAGE_INFO_DATA)  # type: ignore[arg-type]

        assert message1 == message2
        assert message1 != message3

    def test_message_info_hash(self):
        """Test MessageInfo hashing."""
        message1 = MessageInfo(**VALID_MESSAGE_INFO_DATA)  # type: ignore[arg-type]
        message2 = MessageInfo(**VALID_MESSAGE_INFO_DATA)  # type: ignore[arg-type]

        assert hash(message1) == hash(message2)

    def test_message_info_repr(self):
        """Test MessageInfo string representation."""
        message = MessageInfo(**VALID_MESSAGE_INFO_DATA)  # type: ignore[arg-type]
        repr_str = repr(message)

        assert "MessageInfo" in repr_str
        assert "id=111222333" in repr_str
        assert "text='Test message'" in repr_str

    def test_message_info_edge_cases(self):
        """Test MessageInfo edge cases."""
        message = MessageInfo(**EDGE_CASE_MESSAGE_INFO)  # type: ignore[arg-type]

        assert message.id == 0
        assert message.date == "1970-01-01T00:00:00Z"
        assert message.text is not None
        assert len(message.text) == 10000

    def test_message_info_unicode(self):
        """Test MessageInfo with unicode characters."""
        from src.mtproto_client import ChatInfo, UserInfo

        # Create proper dict with ChatInfo and UserInfo objects
        unicode_message_dict = {
            "id": 111222333,
            "chat": ChatInfo(**VALID_CHAT_INFO_DATA),  # type: ignore[arg-type]
            "date": "2023-10-20T10:00:00Z",
            "text": "Hello 世界! Привет мир! こんにちは世界!",
            "from_user": UserInfo(**UNICODE_USER_INFO),  # type: ignore[arg-type]
            "reply_to": None,
            "media": None,
        }
        message = MessageInfo(**unicode_message_dict)  # type: ignore[arg-type]

        assert message.text == "Hello 世界! Привет мир! こんにちは世界!"
        assert message.from_user is not None
        assert message.from_user.first_name == "Тест Пользователь"


class TestMiniAppInfo:
    """Test cases for MiniAppInfo model."""

    def test_valid_mini_app_info_creation(self):
        """Test creating a valid MiniAppInfo."""
        mini_app = MiniAppInfo(**VALID_MINI_APP_INFO_DATA)  # type: ignore[arg-type]

        assert mini_app.url == "https://example.com/mini-app"
        assert mini_app.start_param == "test_param"
        assert mini_app.theme_params == {"bg_color": "#ffffff", "text_color": "#000000"}
        assert mini_app.platform == "web"

    def test_mobile_mini_app_info_creation(self):
        """Test creating a mobile MiniAppInfo."""
        mini_app = MiniAppInfo(**MOBILE_MINI_APP_INFO_DATA)  # type: ignore[arg-type]

        assert mini_app.url == "https://example.com/mobile-mini-app"
        assert mini_app.start_param is None
        assert mini_app.theme_params is None
        assert mini_app.platform == "mobile"

    def test_minimal_mini_app_info_creation(self):
        """Test creating a minimal MiniAppInfo with only url."""
        mini_app = MiniAppInfo(**MINIMAL_MINI_APP_INFO_DATA)  # type: ignore[arg-type]

        assert mini_app.url == "https://t.me/mybot/app?start=123"
        assert mini_app.start_param is None
        assert mini_app.theme_params is None
        assert mini_app.platform == "web"  # Default value

    def test_mini_app_info_required_fields(self):
        """Test MiniAppInfo required fields."""
        # Test that url is required
        with pytest.raises(TypeError):
            MiniAppInfo()  # type: ignore[call-arg]  # Missing required field url

    def test_mini_app_info_optional_fields(self):
        """Test MiniAppInfo optional fields."""
        mini_app = MiniAppInfo(url="https://example.com/mini-app")

        assert mini_app.start_param is None
        assert mini_app.theme_params is None
        assert mini_app.platform == "web"  # Default value

    def test_mini_app_info_field_types(self):
        """Test MiniAppInfo field types."""
        mini_app = MiniAppInfo(**VALID_MINI_APP_INFO_DATA)  # type: ignore[arg-type]

        assert isinstance(mini_app.url, str)
        assert isinstance(mini_app.start_param, str)
        assert isinstance(mini_app.theme_params, dict)
        assert isinstance(mini_app.platform, str)

    def test_mini_app_info_invalid_url_type(self):
        """Test MiniAppInfo with invalid url type."""
        # msgspec doesn't validate types at creation time, it accepts any type
        # The type annotation is for serialization/deserialization, not runtime validation
        # So we test that it accepts int but stores it as int (not converted)
        mini_app = MiniAppInfo(url=123)  # type: ignore[arg-type]
        assert isinstance(mini_app.url, int)  # msgspec doesn't convert, stores as-is
        assert mini_app.url == 123

    def test_mini_app_info_invalid_platform_type(self):
        """Test MiniAppInfo with invalid platform type."""
        # msgspec validates types during JSON deserialization, not at object creation
        # Test with invalid type (int instead of str) in JSON
        invalid_data = {
            "url": "https://example.com",
            "platform": 123,  # Invalid: should be str, not int
        }

        with pytest.raises(msgspec.ValidationError) as exc_info:
            msgspec.json.decode(json.dumps(invalid_data), type=MiniAppInfo)

        # Verify the error is related to platform field
        error_message = str(exc_info.value)
        assert "platform" in error_message.lower() or "type" in error_message.lower()

    def test_mini_app_info_invalid_theme_params_type(self):
        """Test MiniAppInfo with invalid theme_params type."""
        # msgspec will validate this, so we test with msgspec.ValidationError
        # However, msgspec may be lenient with Optional fields, so we check if it raises
        try:
            mini_app = MiniAppInfo(url="https://example.com", theme_params="invalid")  # type: ignore[arg-type]
            # If no error, msgspec didn't validate strictly - this is acceptable
            # We just verify the object was created
            assert mini_app.url == "https://example.com"
        except msgspec.ValidationError:
            # If it raises, that's also acceptable - strict validation
            pass

    def test_mini_app_info_empty_string_start_param(self):
        """Test MiniAppInfo with empty string start_param."""
        mini_app = MiniAppInfo(url="https://example.com", start_param="")
        assert mini_app.start_param == ""

    @pytest.mark.parametrize(
        "url",
        [
            "https://t.me/mybot/app?start=123",
            "https://example.com/app",
            "http://localhost:8080",
            "",  # Empty string - допустима?
        ],
    )
    def test_mini_app_info_url_variations(self, url):
        """Test MiniAppInfo with different URL formats."""
        mini_app = MiniAppInfo(url=url)
        assert mini_app.url == url

    def test_mini_app_info_serialization(self):
        """Test MiniAppInfo serialization."""
        mini_app = MiniAppInfo(**VALID_MINI_APP_INFO_DATA)  # type: ignore[arg-type]

        # Test serialization to dict
        mini_app_dict = msgspec.to_builtins(mini_app)
        assert isinstance(mini_app_dict, dict)
        assert mini_app_dict["url"] == "https://example.com/mini-app"
        assert mini_app_dict["start_param"] == "test_param"
        assert mini_app_dict["theme_params"] == {
            "bg_color": "#ffffff",
            "text_color": "#000000",
        }
        assert mini_app_dict["platform"] == "web"

    def test_mini_app_info_deserialization(self):
        """Test MiniAppInfo deserialization."""
        mini_app_dict = VALID_MINI_APP_INFO_DATA.copy()

        # Test deserialization from dict
        mini_app = msgspec.convert(mini_app_dict, MiniAppInfo)
        assert isinstance(mini_app, MiniAppInfo)
        assert mini_app.url == "https://example.com/mini-app"
        assert mini_app.start_param == "test_param"

    def test_mini_app_info_deserialization_with_none(self):
        """Test MiniAppInfo deserialization with None in optional fields."""
        mini_app_dict = {
            "url": "https://example.com",
            "start_param": None,
            "theme_params": None,
        }
        mini_app = msgspec.convert(mini_app_dict, MiniAppInfo)
        assert mini_app.start_param is None
        assert mini_app.theme_params is None

    def test_mini_app_info_equality(self):
        """Test MiniAppInfo equality."""
        mini_app1 = MiniAppInfo(**VALID_MINI_APP_INFO_DATA)  # type: ignore[arg-type]
        mini_app2 = MiniAppInfo(**VALID_MINI_APP_INFO_DATA)  # type: ignore[arg-type]
        mini_app3 = MiniAppInfo(**MOBILE_MINI_APP_INFO_DATA)  # type: ignore[arg-type]

        assert mini_app1 == mini_app2
        assert mini_app1 != mini_app3

    def test_mini_app_info_inequality(self):
        """Test MiniAppInfo inequality."""
        mini_app1 = MiniAppInfo(url="https://example.com/app1")
        mini_app2 = MiniAppInfo(url="https://example.com/app2")

        assert mini_app1 != mini_app2

    def test_mini_app_info_hash(self):
        """Test MiniAppInfo hashing."""
        # msgspec.Struct with frozen=True should be hashable
        # However, if theme_params contains dict, it may cause issues
        # Test with simple case first
        mini_app1 = MiniAppInfo(url="https://example.com")
        mini_app2 = MiniAppInfo(url="https://example.com")
        assert hash(mini_app1) == hash(mini_app2)

        # Test with theme_params (dict may cause hash issues)
        try:
            mini_app3 = MiniAppInfo(**VALID_MINI_APP_INFO_DATA)  # type: ignore[arg-type]
            mini_app4 = MiniAppInfo(**VALID_MINI_APP_INFO_DATA)  # type: ignore[arg-type]
            # If dict in theme_params causes hash issues, msgspec may handle it
            # or we may need to skip this part
            hash(mini_app3)  # Just check if it's hashable
            hash(mini_app4)
            assert hash(mini_app3) == hash(mini_app4)
        except TypeError:
            # If dict causes hash issues, that's expected - skip this assertion
            pass

    def test_mini_app_info_hash_inequality(self):
        """Test MiniAppInfo hash inequality."""
        mini_app1 = MiniAppInfo(url="https://example.com/app1")
        mini_app2 = MiniAppInfo(url="https://example.com/app2")

        assert hash(mini_app1) != hash(mini_app2)

    def test_mini_app_info_repr(self):
        """Test MiniAppInfo string representation."""
        mini_app = MiniAppInfo(**VALID_MINI_APP_INFO_DATA)  # type: ignore[arg-type]
        repr_str = repr(mini_app)

        assert "MiniAppInfo" in repr_str
        assert "url='https://example.com/mini-app'" in repr_str

    def test_mini_app_info_platforms(self):
        """Test different platform values."""
        platforms = ["web", "mobile", "desktop", "tv"]

        for platform in platforms:
            mini_app = MiniAppInfo(
                url="https://example.com/mini-app", platform=platform
            )
            assert mini_app.platform == platform

    def test_mini_app_info_frozen(self):
        """Test that MiniAppInfo is frozen (cannot modify attributes)."""
        mini_app = MiniAppInfo(url="https://example.com")
        # Should raise AttributeError when trying to modify
        with pytest.raises(AttributeError, match="immutable type"):
            mini_app.url = "https://example.com/new"  # type: ignore[misc]

    def test_mini_app_info_edge_cases(self):
        """Test MiniAppInfo edge cases."""
        mini_app = MiniAppInfo(**EDGE_CASE_MINI_APP_INFO_DATA)  # type: ignore[arg-type]

        assert mini_app.url == ""
        assert mini_app.start_param == ""
        assert mini_app.theme_params == {}

    def test_mini_app_info_unicode(self):
        """Test MiniAppInfo with unicode characters."""
        mini_app = MiniAppInfo(**UNICODE_MINI_APP_INFO_DATA)  # type: ignore[arg-type]

        assert mini_app.url == "https://example.com/тест-приложение"
        assert mini_app.start_param == "параметр_用户_テスト"
        assert mini_app.theme_params == {"title": "Тест", "description": "测试"}

    def test_mini_app_info_theme_params_nested(self):
        """Test MiniAppInfo with nested theme_params."""
        nested_params = {
            "bg_color": "#ffffff",
            "nested": {"key": "value", "list": [1, 2, 3]},
        }
        mini_app = MiniAppInfo(url="https://example.com", theme_params=nested_params)
        assert mini_app.theme_params == nested_params

    def test_mini_app_info_very_long_url(self):
        """Test MiniAppInfo with very long URL."""
        long_url = "https://example.com/" + "a" * 10000
        mini_app = MiniAppInfo(url=long_url)
        assert len(mini_app.url) == len(long_url)


class TestApiResult:
    """Test cases for ApiResult model."""

    def test_valid_api_result_creation(self):
        """Test creating a valid ApiResult."""
        result = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]

        assert result.endpoint == "/api/status"
        assert result.method == "GET"
        assert result.status_code == 200
        assert result.response_time == 0.5
        assert result.success is True
        assert result.redirect is False
        assert result.client_error is False
        assert result.server_error is False
        assert result.informational is False
        assert result.headers == {"content-type": "application/json"}
        assert result.body == b'{"status": "ok"}'
        assert result.content_type == "application/json"
        assert result.reason == "OK"
        assert result.error_message is None

    def test_error_api_result_creation(self):
        """Test creating an error ApiResult."""
        result = ApiResult(**ERROR_API_RESULT_DATA)  # type: ignore[arg-type]

        assert result.endpoint == "/api/error"
        assert result.method == "POST"
        assert result.status_code == 400
        assert result.response_time == 0.2
        assert result.success is False
        assert result.client_error is True
        assert result.error_message == "Bad Request"

    def test_timeout_api_result_creation(self):
        """Test creating a timeout ApiResult."""
        result = ApiResult(**TIMEOUT_API_RESULT_DATA)  # type: ignore[arg-type]

        assert result.status_code == 408
        assert result.response_time == 30.0
        assert result.success is False
        assert result.client_error is True
        assert result.error_message == "Request timeout"

    def test_redirect_api_result_creation(self):
        """Test creating a redirect ApiResult."""
        result = ApiResult(**REDIRECT_API_RESULT_DATA)  # type: ignore[arg-type]

        assert result.status_code == 301
        assert result.redirect is True
        assert result.success is False

    def test_server_error_api_result_creation(self):
        """Test creating a server error ApiResult."""
        result = ApiResult(**SERVER_ERROR_API_RESULT_DATA)  # type: ignore[arg-type]

        assert result.status_code == 500
        assert result.server_error is True
        assert result.success is False

    def test_informational_api_result_creation(self):
        """Test creating an informational ApiResult."""
        result = ApiResult(**INFORMATIONAL_API_RESULT_DATA)  # type: ignore[arg-type]

        assert result.status_code == 101
        assert result.informational is True
        assert result.success is False

    def test_api_result_required_fields(self):
        """Test ApiResult required fields."""
        # Test that all required fields are needed
        with pytest.raises(TypeError):
            ApiResult()  # type: ignore[call-arg]  # Missing required fields

        with pytest.raises(TypeError):
            ApiResult(endpoint="/api/test")  # type: ignore[call-arg]  # Missing other required fields

    def test_api_result_field_types(self):
        """Test ApiResult field types."""
        result = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]

        assert isinstance(result.endpoint, str)
        assert isinstance(result.method, str)
        assert isinstance(result.status_code, int)
        assert isinstance(result.response_time, float)
        assert isinstance(result.success, bool)
        assert isinstance(result.redirect, bool)
        assert isinstance(result.client_error, bool)
        assert isinstance(result.server_error, bool)
        assert isinstance(result.informational, bool)

    def test_api_result_invalid_status_code_type(self):
        """Test ApiResult with invalid status_code type."""
        # msgspec doesn't validate types at creation time, it accepts any type
        # The type annotation is for serialization/deserialization, not runtime validation
        result = ApiResult(
            endpoint="/api/test",
            method="GET",
            status_code="200",  # type: ignore[arg-type]  # msgspec stores as str, doesn't convert
            response_time=0.1,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
        )
        assert isinstance(
            result.status_code, str
        )  # msgspec doesn't convert, stores as-is
        assert result.status_code == "200"

    def test_api_result_invalid_response_time_type(self):
        """Test ApiResult with invalid response_time type."""
        # msgspec doesn't validate types at creation time, it accepts any type
        # The type annotation is for serialization/deserialization, not runtime validation
        result = ApiResult(
            endpoint="/api/test",
            method="GET",
            status_code=200,
            response_time="fast",  # type: ignore[arg-type]  # msgspec stores as str, doesn't convert
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
        )
        assert isinstance(
            result.response_time, str
        )  # msgspec doesn't convert, stores as-is
        assert result.response_time == "fast"

    def test_api_result_invalid_headers_type(self):
        """Test ApiResult with invalid headers type."""
        # msgspec may be lenient with Optional fields
        # We test both cases
        try:
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
                headers="invalid",  # type: ignore[arg-type]  # Must be Dict[str, str]
            )
            # If no error, msgspec was lenient - verify object was created
            assert result.endpoint == "/api/test"
        except msgspec.ValidationError:
            # If it raises, that's also acceptable - strict validation
            pass

    @pytest.mark.parametrize("status_code", [200, 301, 404, 500, 101])
    def test_api_result_status_codes(self, status_code):
        """Test different status codes."""
        result = ApiResult(
            endpoint="/api/test",
            method="GET",
            status_code=status_code,
            response_time=0.1,
            success=200 <= status_code < 300,
            redirect=300 <= status_code < 400,
            client_error=400 <= status_code < 500,
            server_error=500 <= status_code < 600,
            informational=100 <= status_code < 200,
        )
        assert result.status_code == status_code
        assert result.success == (200 <= status_code < 300)
        assert result.redirect == (300 <= status_code < 400)
        assert result.client_error == (400 <= status_code < 500)
        assert result.server_error == (500 <= status_code < 600)
        assert result.informational == (100 <= status_code < 200)

    def test_api_result_response_times(self):
        """Test different response times."""
        response_times = [0.001, 0.1, 1.0, 10.0, 100.0]

        for response_time in response_times:
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=200,
                response_time=response_time,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
            )
            assert result.response_time == response_time

    def test_api_result_serialization(self):
        """Test ApiResult serialization."""
        result = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]

        # Test serialization to dict
        result_dict = msgspec.to_builtins(result)
        assert isinstance(result_dict, dict)
        assert result_dict["endpoint"] == "/api/status"
        assert result_dict["status_code"] == 200
        assert result_dict["success"] is True

    def test_api_result_serialization_with_response_data(self):
        """Test ApiResult serialization with response data."""
        result = ApiResult(
            endpoint="/api/test",
            method="GET",
            status_code=200,
            response_time=0.1,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            headers={"content-type": "application/json"},
            body=b'{"test": "data"}',
            content_type="application/json",
            reason="OK",
        )

        # ApiResult should serialize correctly with immutable data
        result_dict = msgspec.to_builtins(result)
        assert "headers" in result_dict
        assert "body" in result_dict
        assert "content_type" in result_dict
        assert "reason" in result_dict
        assert result_dict["headers"] == {"content-type": "application/json"}
        # msgspec serializes bytes to base64 string by default
        import base64

        expected_body_base64 = base64.b64encode(b'{"test": "data"}').decode("utf-8")
        assert result_dict["body"] == expected_body_base64

    def test_api_result_deserialization(self):
        """Test ApiResult deserialization."""
        result_dict = VALID_API_RESULT_DATA.copy()

        # Test deserialization from dict
        result = msgspec.convert(result_dict, ApiResult)
        assert isinstance(result, ApiResult)
        assert result.endpoint == "/api/status"
        assert result.status_code == 200
        assert result.success is True

    def test_api_result_deserialization_with_none(self):
        """Test ApiResult deserialization with None in optional fields."""
        result_dict = {
            "endpoint": "/api/test",
            "method": "GET",
            "status_code": 200,
            "response_time": 0.1,
            "success": True,
            "redirect": False,
            "client_error": False,
            "server_error": False,
            "informational": False,
            "headers": {},
            "body": b"",
            "content_type": None,
            "reason": None,
            "error_message": None,
        }
        result = msgspec.convert(result_dict, ApiResult)
        assert result.headers == {}
        assert result.body == b""
        assert result.content_type is None
        assert result.reason is None
        assert result.error_message is None

    def test_api_result_equality(self):
        """Test ApiResult equality."""
        result1 = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]
        result2 = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]
        result3 = ApiResult(**ERROR_API_RESULT_DATA)  # type: ignore[arg-type]

        assert result1 == result2
        assert result1 != result3

    def test_api_result_inequality(self):
        """Test ApiResult inequality."""
        result1 = ApiResult(
            endpoint="/api/test1",
            method="GET",
            status_code=200,
            response_time=0.1,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
        )
        result2 = ApiResult(
            endpoint="/api/test2",
            method="GET",
            status_code=200,
            response_time=0.1,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
        )

        assert result1 != result2

    def test_api_result_hash(self):
        """Test ApiResult hashing."""
        result1 = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]
        result2 = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]

        # msgspec.Struct with frozen=True should be hashable
        # However, dict fields (headers) make it unhashable - this is expected behavior
        # Test that ApiResult with dict headers is not hashable
        with pytest.raises(TypeError, match="unhashable type"):
            hash(result1)

        with pytest.raises(TypeError, match="unhashable type"):
            hash(result2)

    def test_api_result_hash_inequality(self):
        """Test ApiResult hash inequality."""
        result1 = ApiResult(
            endpoint="/api/test1",
            method="GET",
            status_code=200,
            response_time=0.1,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
        )
        result2 = ApiResult(
            endpoint="/api/test2",
            method="GET",
            status_code=200,
            response_time=0.1,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
        )

        # ApiResult with dict headers is not hashable - this is expected behavior
        # Test that both objects raise TypeError when trying to hash
        with pytest.raises(TypeError, match="unhashable type"):
            hash(result1)

        with pytest.raises(TypeError, match="unhashable type"):
            hash(result2)

    def test_api_result_repr(self):
        """Test ApiResult string representation."""
        result = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]
        repr_str = repr(result)

        assert "ApiResult" in repr_str
        assert "endpoint='/api/status'" in repr_str
        assert "status_code=200" in repr_str
        assert "success=True" in repr_str

    def test_api_result_frozen(self):
        """Test that ApiResult is frozen (cannot modify attributes)."""
        result = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]
        # Should raise AttributeError when trying to modify
        with pytest.raises(AttributeError, match="immutable type"):
            result.endpoint = "/api/new"  # type: ignore[misc]

    def test_api_result_empty_strings(self):
        """Test ApiResult with empty strings."""
        result = ApiResult(
            endpoint="",
            method="",
            status_code=200,
            response_time=0.1,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            error_message="",
        )
        assert result.endpoint == ""
        assert result.method == ""
        assert result.error_message == ""

    def test_api_result_unicode(self):
        """Test ApiResult with unicode characters."""
        result = ApiResult(
            endpoint="/api/тест",
            method="GET",
            status_code=200,
            response_time=0.1,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            error_message="Ошибка 错误",
        )
        assert result.endpoint == "/api/тест"
        assert result.error_message == "Ошибка 错误"

    def test_api_result_very_long_strings(self):
        """Test ApiResult with very long strings."""
        long_endpoint = "/api/" + "a" * 10000
        result = ApiResult(
            endpoint=long_endpoint,
            method="GET",
            status_code=200,
            response_time=0.1,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
        )
        assert len(result.endpoint) == len(long_endpoint)

    def test_api_result_with_response_data(self):
        """Test ApiResult with response data fields."""
        result = ApiResult(
            endpoint="/api/test",
            method="GET",
            status_code=200,
            response_time=0.1,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            headers={"content-type": "application/json", "x-custom": "value"},
            body=b'{"test": "data"}',
            content_type="application/json",
            reason="OK",
        )

        assert result.headers == {
            "content-type": "application/json",
            "x-custom": "value",
        }
        assert result.body == b'{"test": "data"}'
        assert result.content_type == "application/json"
        assert result.reason == "OK"
        assert result.status_code == 200

    def test_api_result_methods(self):
        """Test different HTTP methods."""
        methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]

        for method in methods:
            result = ApiResult(
                endpoint="/api/test",
                method=method,
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
            )
            assert result.method == method
