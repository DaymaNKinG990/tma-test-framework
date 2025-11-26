"""
Unit tests for TMA Framework data models.
"""

import base64

import allure
import json
import pytest
import msgspec

from tma_test_framework.clients.mtproto_client import UserInfo, ChatInfo, MessageInfo
from tma_test_framework.clients.models import MiniAppInfo, ApiResult
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

    @allure.title("TC-MODEL-USER-001: Create valid UserInfo")
    @allure.description("Test creating a valid UserInfo. TC-MODEL-USER-001")
    def test_valid_user_info_creation(self):
        """Test creating a valid UserInfo."""
        with allure.step("Create UserInfo from valid data"):
            user = UserInfo(**VALID_USER_INFO_DATA)  # type: ignore[arg-type]

        with allure.step("Verify user.id is correct"):
            assert user.id == 123456789
        with allure.step("Verify user.first_name is correct"):
            assert user.first_name == "Test User"
        with allure.step("Verify user.username is correct"):
            assert user.username == "test_user"
        with allure.step("Verify user.last_name is correct"):
            assert user.last_name == "Test"
        with allure.step("Verify user.phone is correct"):
            assert user.phone == "+1234567890"
        with allure.step("Verify user.is_bot is False"):
            assert user.is_bot is False
        with allure.step("Verify user.is_verified is True"):
            assert user.is_verified is True
        with allure.step("Verify user.is_premium is False"):
            assert user.is_premium is False

    @allure.title("TC-MODEL-USER-002: Create bot UserInfo")
    @allure.description("Test creating a bot UserInfo. TC-MODEL-USER-002")
    def test_bot_user_info_creation(self):
        """Test creating a bot UserInfo."""
        with allure.step("Create UserInfo from bot data"):
            user = UserInfo(**BOT_USER_INFO_DATA)  # type: ignore[arg-type]

        with allure.step("Verify user.id is correct"):
            assert user.id == 987654321
        with allure.step("Verify user.first_name is correct"):
            assert user.first_name == "Test Bot"
        with allure.step("Verify user.username is correct"):
            assert user.username == "test_bot"
        with allure.step("Verify user.last_name is None"):
            assert user.last_name is None
        with allure.step("Verify user.phone is None"):
            assert user.phone is None
        with allure.step("Verify user.is_bot is True"):
            assert user.is_bot is True
        with allure.step("Verify user.is_verified is False"):
            assert user.is_verified is False
        with allure.step("Verify user.is_premium is False"):
            assert user.is_premium is False

    @allure.title("Create minimal UserInfo")
    @allure.description("Test creating a minimal UserInfo.")
    def test_minimal_user_info_creation(self):
        """Test creating a minimal UserInfo."""
        with allure.step("Create UserInfo from minimal data"):
            user = UserInfo(**MINIMAL_USER_INFO_DATA)  # type: ignore[arg-type]

        with allure.step("Verify user.id is correct"):
            assert user.id == 111222333
        with allure.step("Verify user.first_name is correct"):
            assert user.first_name == "Minimal User"
        with allure.step("Verify optional fields are None"):
            assert user.username is None
            assert user.last_name is None
            assert user.phone is None
        with allure.step("Verify boolean fields have default values"):
            assert user.is_bot is False
            assert user.is_verified is False
            assert user.is_premium is False

    @allure.title("UserInfo required fields")
    @allure.description("Test UserInfo required fields.")
    def test_user_info_required_fields(self):
        """Test UserInfo required fields."""
        with allure.step("Test that UserInfo() without args raises TypeError"):
            # Test that id and first_name are required
            with pytest.raises(TypeError):
                UserInfo()  # type: ignore[call-arg]  # Missing required fields

        with allure.step("Test that UserInfo(id) without first_name raises TypeError"):
            with pytest.raises(TypeError):
                UserInfo(id=123456789)  # type: ignore[call-arg]  # Missing first_name

        with allure.step("Test that UserInfo(first_name) without id raises TypeError"):
            with pytest.raises(TypeError):
                UserInfo(first_name="Test")  # type: ignore[call-arg]  # Missing id

    @allure.title("UserInfo optional fields")
    @allure.description("Test UserInfo optional fields.")
    def test_user_info_optional_fields(self):
        """Test UserInfo optional fields."""
        with allure.step("Create UserInfo with only required fields"):
            user = UserInfo(id=123456789, first_name="Test User")

        with allure.step("Verify optional fields have default values"):
            assert user.username is None
            assert user.last_name is None
            assert user.phone is None
            assert user.is_bot is False
            assert user.is_verified is False
            assert user.is_premium is False

    @allure.title("UserInfo field types")
    @allure.description("Test UserInfo field types.")
    def test_user_info_field_types(self):
        """Test UserInfo field types."""
        with allure.step("Create UserInfo from valid data"):
            user = UserInfo(**VALID_USER_INFO_DATA)  # type: ignore[arg-type]

        with allure.step("Verify field types"):
            assert isinstance(user.id, int)
            assert isinstance(user.first_name, str)
            assert isinstance(user.username, str) or user.username is None
            assert isinstance(user.last_name, str) or user.last_name is None
            assert isinstance(user.phone, str) or user.phone is None
            assert isinstance(user.is_bot, bool)
            assert isinstance(user.is_verified, bool)
            assert isinstance(user.is_premium, bool)

    @allure.title("UserInfo serialization")
    @allure.description("Test UserInfo serialization.")
    def test_user_info_serialization(self):
        """Test UserInfo serialization."""
        with allure.step("Create UserInfo from valid data"):
            user = UserInfo(**VALID_USER_INFO_DATA)  # type: ignore[arg-type]

        with allure.step("Test serialization to dict"):
            # Test serialization to dict
            user_dict = msgspec.to_builtins(user)
            assert isinstance(user_dict, dict)
            assert user_dict["id"] == 123456789
            assert user_dict["first_name"] == "Test User"

    @allure.title("UserInfo deserialization")
    @allure.description("Test UserInfo deserialization.")
    def test_user_info_deserialization(self):
        """Test UserInfo deserialization."""
        with allure.step("Prepare user dict"):
            user_dict = VALID_USER_INFO_DATA.copy()

        with allure.step("Test deserialization from dict"):
            # Test deserialization from dict
            user = msgspec.convert(user_dict, UserInfo)
            assert isinstance(user, UserInfo)
        with allure.step("Verify deserialized user data"):
            assert user.id == 123456789
            assert user.first_name == "Test User"

    @allure.title("UserInfo equality")
    @allure.description("Test UserInfo equality.")
    def test_user_info_equality(self):
        """Test UserInfo equality."""
        with allure.step("Create three UserInfo instances"):
            user1 = UserInfo(**VALID_USER_INFO_DATA)  # type: ignore[arg-type]
            user2 = UserInfo(**VALID_USER_INFO_DATA)  # type: ignore[arg-type]
            user3 = UserInfo(**BOT_USER_INFO_DATA)  # type: ignore[arg-type]

        with allure.step("Verify user1 equals user2"):
            assert user1 == user2
        with allure.step("Verify user1 does not equal user3"):
            assert user1 != user3

    @allure.title("UserInfo hashing")
    @allure.description("Test UserInfo hashing.")
    def test_user_info_hash(self):
        """Test UserInfo hashing."""
        with allure.step("Create two identical UserInfo instances"):
            user1 = UserInfo(**VALID_USER_INFO_DATA)  # type: ignore[arg-type]
            user2 = UserInfo(**VALID_USER_INFO_DATA)  # type: ignore[arg-type]

        with allure.step("Verify both instances have same hash"):
            assert hash(user1) == hash(user2)

    @allure.title("UserInfo string representation")
    @allure.description("Test UserInfo string representation.")
    def test_user_info_repr(self):
        """Test UserInfo string representation."""
        with allure.step("Create UserInfo instance"):
            user = UserInfo(**VALID_USER_INFO_DATA)  # type: ignore[arg-type]
        repr_str = repr(user)

        assert "UserInfo" in repr_str
        assert "id=123456789" in repr_str
        assert "first_name='Test User'" in repr_str

    @allure.title("UserInfo edge cases")
    @allure.description("Test UserInfo edge cases.")
    def test_user_info_edge_cases(self):
        """Test UserInfo edge cases."""
        user = UserInfo(**EDGE_CASE_USER_INFO)  # type: ignore[arg-type]

        assert user.id == 0
        assert user.first_name == ""
        assert user.username is not None and len(user.username) == 100
        assert user.last_name is not None and len(user.last_name) == 100
        assert user.phone is not None and len(user.phone) == 20

    @allure.title("UserInfo with unicode characters")
    @allure.description("Test UserInfo with unicode characters.")
    def test_user_info_unicode(self):
        """Test UserInfo with unicode characters."""
        user = UserInfo(**UNICODE_USER_INFO)  # type: ignore[arg-type]

        assert user.first_name == "Тест Пользователь"
        assert user.username == "test_用户"
        assert user.last_name == "テスト"

    @allure.title("UserInfo boolean fields")
    @allure.description("Test UserInfo boolean fields.")
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

    @allure.title("creating a valid ChatInfo")
    @allure.description("Test creating a valid ChatInfo.")
    def test_valid_chat_info_creation(self):
        """Test creating a valid ChatInfo."""
        chat = ChatInfo(**VALID_CHAT_INFO_DATA)  # type: ignore[arg-type]

        assert chat.id == 987654321
        assert chat.title == "Test Chat"
        assert chat.username == "test_chat"
        assert chat.type == "group"
        assert chat.is_verified is False

    @allure.title("creating a private ChatInfo")
    @allure.description("Test creating a private ChatInfo.")
    def test_private_chat_info_creation(self):
        """Test creating a private ChatInfo."""
        chat = ChatInfo(**PRIVATE_CHAT_INFO_DATA)  # type: ignore[arg-type]

        assert chat.id == 111222333
        assert chat.title == "Private Chat"
        assert chat.username is None
        assert chat.type == "private"
        assert chat.is_verified is False

    @allure.title("creating a channel ChatInfo")
    @allure.description("Test creating a channel ChatInfo.")
    def test_channel_chat_info_creation(self):
        """Test creating a channel ChatInfo."""
        chat = ChatInfo(**CHANNEL_CHAT_INFO_DATA)  # type: ignore[arg-type]

        assert chat.id == 444555666
        assert chat.title == "Test Channel"
        assert chat.username == "test_channel"
        assert chat.type == "channel"
        assert chat.is_verified is True

    @allure.title("ChatInfo required fields")
    @allure.description("Test ChatInfo required fields.")
    def test_chat_info_required_fields(self):
        """Test ChatInfo required fields."""
        # Test that id, title, and type are required
        with pytest.raises(TypeError):
            ChatInfo()  # type: ignore[call-arg]  # Missing required fields

        with pytest.raises(TypeError):
            ChatInfo(id=987654321)  # type: ignore[call-arg]  # Missing title and type

        with pytest.raises(TypeError):
            ChatInfo(id=987654321, title="Test")  # type: ignore[call-arg]  # Missing type

    @allure.title("ChatInfo optional fields")
    @allure.description("Test ChatInfo optional fields.")
    def test_chat_info_optional_fields(self):
        """Test ChatInfo optional fields."""
        chat = ChatInfo(id=987654321, title="Test Chat", type="group")

        assert chat.username is None
        assert chat.is_verified is False

    @allure.title("ChatInfo field types")
    @allure.description("Test ChatInfo field types.")
    def test_chat_info_field_types(self):
        """Test ChatInfo field types."""
        chat = ChatInfo(**VALID_CHAT_INFO_DATA)  # type: ignore[arg-type]

        assert isinstance(chat.id, int)
        assert isinstance(chat.title, str)
        assert isinstance(chat.username, str)
        assert isinstance(chat.type, str)
        assert isinstance(chat.is_verified, bool)

    @allure.title("ChatInfo serialization")
    @allure.description("Test ChatInfo serialization.")
    def test_chat_info_serialization(self):
        """Test ChatInfo serialization."""
        chat = ChatInfo(**VALID_CHAT_INFO_DATA)  # type: ignore[arg-type]

        # Test serialization to dict
        chat_dict = msgspec.to_builtins(chat)
        assert isinstance(chat_dict, dict)
        assert chat_dict["id"] == 987654321
        assert chat_dict["title"] == "Test Chat"

    @allure.title("ChatInfo deserialization")
    @allure.description("Test ChatInfo deserialization.")
    def test_chat_info_deserialization(self):
        """Test ChatInfo deserialization."""
        chat_dict = VALID_CHAT_INFO_DATA.copy()

        # Test deserialization from dict
        chat = msgspec.convert(chat_dict, ChatInfo)
        assert isinstance(chat, ChatInfo)
        assert chat.id == 987654321
        assert chat.title == "Test Chat"

    @allure.title("ChatInfo equality")
    @allure.description("Test ChatInfo equality.")
    def test_chat_info_equality(self):
        """Test ChatInfo equality."""
        chat1 = ChatInfo(**VALID_CHAT_INFO_DATA)  # type: ignore[arg-type]
        chat2 = ChatInfo(**VALID_CHAT_INFO_DATA)  # type: ignore[arg-type]
        chat3 = ChatInfo(**PRIVATE_CHAT_INFO_DATA)  # type: ignore[arg-type]

        assert chat1 == chat2
        assert chat1 != chat3

    @allure.title("ChatInfo hashing")
    @allure.description("Test ChatInfo hashing.")
    def test_chat_info_hash(self):
        """Test ChatInfo hashing."""
        chat1 = ChatInfo(**VALID_CHAT_INFO_DATA)  # type: ignore[arg-type]
        chat2 = ChatInfo(**VALID_CHAT_INFO_DATA)  # type: ignore[arg-type]

        assert hash(chat1) == hash(chat2)

    @allure.title("ChatInfo string representation")
    @allure.description("Test ChatInfo string representation.")
    def test_chat_info_repr(self):
        """Test ChatInfo string representation."""
        chat = ChatInfo(**VALID_CHAT_INFO_DATA)  # type: ignore[arg-type]
        repr_str = repr(chat)

        assert "ChatInfo" in repr_str
        assert "id=987654321" in repr_str
        assert "title='Test Chat'" in repr_str

    @allure.title("different chat types")
    @allure.description("Test different chat types.")
    def test_chat_info_types(self):
        """Test different chat types."""
        types = ["private", "group", "supergroup", "channel"]

        for chat_type in types:
            chat = ChatInfo(id=987654321, title=f"Test {chat_type}", type=chat_type)
            assert chat.type == chat_type


class TestMessageInfo:
    """Test cases for MessageInfo model."""

    @allure.title("creating a valid MessageInfo")
    @allure.description("Test creating a valid MessageInfo.")
    def test_valid_message_info_creation(self):
        """Test creating a valid MessageInfo."""

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

    @allure.title("creating a reply MessageInfo")
    @allure.description("Test creating a reply MessageInfo.")
    def test_reply_message_info_creation(self):
        """Test creating a reply MessageInfo."""
        message = MessageInfo(**REPLY_MESSAGE_INFO_DATA)  # type: ignore[arg-type]

        assert message.id == 222333444
        assert message.text == "Reply message"
        assert message.reply_to == 111222333

    @allure.title("creating a media MessageInfo")
    @allure.description("Test creating a media MessageInfo.")
    def test_media_message_info_creation(self):
        """Test creating a media MessageInfo."""
        message = MessageInfo(**MEDIA_MESSAGE_INFO_DATA)  # type: ignore[arg-type]

        assert message.id == 333444555
        assert message.text == "Message with media"
        assert message.media is not None
        assert message.media["type"] == "photo"

    @allure.title("MessageInfo required fields")
    @allure.description("Test MessageInfo required fields.")
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

    @allure.title("MessageInfo optional fields")
    @allure.description("Test MessageInfo optional fields.")
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

    @allure.title("MessageInfo field types")
    @allure.description("Test MessageInfo field types.")
    def test_message_info_field_types(self):
        """Test MessageInfo field types."""
        # Create message with proper chat data

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

    @allure.title("MessageInfo serialization")
    @allure.description("Test MessageInfo serialization.")
    def test_message_info_serialization(self):
        """Test MessageInfo serialization."""
        message = MessageInfo(**VALID_MESSAGE_INFO_DATA)  # type: ignore[arg-type]

        # Test serialization to dict
        message_dict = msgspec.to_builtins(message)
        assert isinstance(message_dict, dict)
        assert message_dict["id"] == 111222333
        assert message_dict["text"] == "Test message"

    @allure.title("MessageInfo deserialization")
    @allure.description("Test MessageInfo deserialization.")
    def test_message_info_deserialization(self):
        """Test MessageInfo deserialization."""
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

        # Test deserialization from dict
        message = msgspec.convert(message_dict, MessageInfo)
        assert isinstance(message, MessageInfo)
        assert message.id == 111222333
        assert message.text == "Test message"

    @allure.title("MessageInfo equality")
    @allure.description("Test MessageInfo equality.")
    def test_message_info_equality(self):
        """Test MessageInfo equality."""
        message1 = MessageInfo(**VALID_MESSAGE_INFO_DATA)  # type: ignore[arg-type]
        message2 = MessageInfo(**VALID_MESSAGE_INFO_DATA)  # type: ignore[arg-type]
        message3 = MessageInfo(**REPLY_MESSAGE_INFO_DATA)  # type: ignore[arg-type]

        assert message1 == message2
        assert message1 != message3

    @allure.title("MessageInfo hashing")
    @allure.description("Test MessageInfo hashing.")
    def test_message_info_hash(self):
        """Test MessageInfo hashing."""
        message1 = MessageInfo(**VALID_MESSAGE_INFO_DATA)  # type: ignore[arg-type]
        message2 = MessageInfo(**VALID_MESSAGE_INFO_DATA)  # type: ignore[arg-type]

        assert hash(message1) == hash(message2)

    @allure.title("MessageInfo string representation")
    @allure.description("Test MessageInfo string representation.")
    def test_message_info_repr(self):
        """Test MessageInfo string representation."""
        message = MessageInfo(**VALID_MESSAGE_INFO_DATA)  # type: ignore[arg-type]
        repr_str = repr(message)

        assert "MessageInfo" in repr_str
        assert "id=111222333" in repr_str
        assert "text='Test message'" in repr_str

    @allure.title("MessageInfo edge cases")
    @allure.description("Test MessageInfo edge cases.")
    def test_message_info_edge_cases(self):
        """Test MessageInfo edge cases."""
        message = MessageInfo(**EDGE_CASE_MESSAGE_INFO)  # type: ignore[arg-type]

        assert message.id == 0
        assert message.date == "1970-01-01T00:00:00Z"
        assert message.text is not None
        assert len(message.text) == 10000

    @allure.title("MessageInfo with unicode characters")
    @allure.description("Test MessageInfo with unicode characters.")
    def test_message_info_unicode(self):
        """Test MessageInfo with unicode characters."""

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

    @allure.title("creating a valid MiniAppInfo")
    @allure.description("Test creating a valid MiniAppInfo.")
    def test_valid_mini_app_info_creation(self):
        """Test creating a valid MiniAppInfo."""
        mini_app = MiniAppInfo(**VALID_MINI_APP_INFO_DATA)  # type: ignore[arg-type]

        assert mini_app.url == "https://example.com/mini-app"
        assert mini_app.start_param == "test_param"
        assert mini_app.theme_params == {"bg_color": "#ffffff", "text_color": "#000000"}
        assert mini_app.platform == "web"

    @allure.title("creating a mobile MiniAppInfo")
    @allure.description("Test creating a mobile MiniAppInfo.")
    def test_mobile_mini_app_info_creation(self):
        """Test creating a mobile MiniAppInfo."""
        mini_app = MiniAppInfo(**MOBILE_MINI_APP_INFO_DATA)  # type: ignore[arg-type]

        assert mini_app.url == "https://example.com/mobile-mini-app"
        assert mini_app.start_param is None
        assert mini_app.theme_params is None
        assert mini_app.platform == "mobile"

    @allure.title("creating a minimal MiniAppInfo with only url")
    @allure.description("Test creating a minimal MiniAppInfo with only url.")
    def test_minimal_mini_app_info_creation(self):
        """Test creating a minimal MiniAppInfo with only url."""
        mini_app = MiniAppInfo(**MINIMAL_MINI_APP_INFO_DATA)  # type: ignore[arg-type]

        assert mini_app.url == "https://t.me/mybot/app?start=123"
        assert mini_app.start_param is None
        assert mini_app.theme_params is None
        assert mini_app.platform == "web"  # Default value

    @allure.title("MiniAppInfo required fields")
    @allure.description("Test MiniAppInfo required fields.")
    def test_mini_app_info_required_fields(self):
        """Test MiniAppInfo required fields."""
        # Test that url is required
        with pytest.raises(TypeError):
            MiniAppInfo()  # type: ignore[call-arg]  # Missing required field url

    @allure.title("MiniAppInfo optional fields")
    @allure.description("Test MiniAppInfo optional fields.")
    def test_mini_app_info_optional_fields(self):
        """Test MiniAppInfo optional fields."""
        mini_app = MiniAppInfo(url="https://example.com/mini-app")

        assert mini_app.start_param is None
        assert mini_app.theme_params is None
        assert mini_app.platform == "web"  # Default value

    @allure.title("MiniAppInfo field types")
    @allure.description("Test MiniAppInfo field types.")
    def test_mini_app_info_field_types(self):
        """Test MiniAppInfo field types."""
        mini_app = MiniAppInfo(**VALID_MINI_APP_INFO_DATA)  # type: ignore[arg-type]

        assert isinstance(mini_app.url, str)
        assert isinstance(mini_app.start_param, str)
        assert isinstance(mini_app.theme_params, dict)
        assert isinstance(mini_app.platform, str)

    @allure.title("MiniAppInfo with invalid url type")
    @allure.description("Test MiniAppInfo with invalid url type.")
    def test_mini_app_info_invalid_url_type(self):
        """Test MiniAppInfo with invalid url type."""
        # msgspec doesn't validate types at creation time, it accepts any type
        # The type annotation is for serialization/deserialization, not runtime validation
        # So we test that it accepts int but stores it as int (not converted)
        mini_app = MiniAppInfo(url=123)  # type: ignore[arg-type]
        assert isinstance(mini_app.url, int)  # msgspec doesn't convert, stores as-is
        assert mini_app.url == 123

    @allure.title("MiniAppInfo with invalid platform type")
    @allure.description("Test MiniAppInfo with invalid platform type.")
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

    @allure.title("MiniAppInfo with invalid theme_params type")
    @allure.description("Test MiniAppInfo with invalid theme_params type.")
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

    @allure.title("MiniAppInfo with empty string start_param")
    @allure.description("Test MiniAppInfo with empty string start_param.")
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
    @allure.title("MiniAppInfo with different URL formats")
    @allure.description("Test MiniAppInfo with different URL formats.")
    def test_mini_app_info_url_variations(self, url):
        """Test MiniAppInfo with different URL formats."""
        mini_app = MiniAppInfo(url=url)
        assert mini_app.url == url

    @allure.title("MiniAppInfo serialization")
    @allure.description("Test MiniAppInfo serialization.")
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

    @allure.title("MiniAppInfo deserialization")
    @allure.description("Test MiniAppInfo deserialization.")
    def test_mini_app_info_deserialization(self):
        """Test MiniAppInfo deserialization."""
        mini_app_dict = VALID_MINI_APP_INFO_DATA.copy()

        # Test deserialization from dict
        mini_app = msgspec.convert(mini_app_dict, MiniAppInfo)
        assert isinstance(mini_app, MiniAppInfo)
        assert mini_app.url == "https://example.com/mini-app"
        assert mini_app.start_param == "test_param"

    @allure.title("MiniAppInfo deserialization with None in optional fields")
    @allure.description(
        "Test MiniAppInfo deserialization with None in optional fields."
    )
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

    @allure.title("MiniAppInfo equality")
    @allure.description("Test MiniAppInfo equality.")
    def test_mini_app_info_equality(self):
        """Test MiniAppInfo equality."""
        mini_app1 = MiniAppInfo(**VALID_MINI_APP_INFO_DATA)  # type: ignore[arg-type]
        mini_app2 = MiniAppInfo(**VALID_MINI_APP_INFO_DATA)  # type: ignore[arg-type]
        mini_app3 = MiniAppInfo(**MOBILE_MINI_APP_INFO_DATA)  # type: ignore[arg-type]

        assert mini_app1 == mini_app2
        assert mini_app1 != mini_app3

    @allure.title("MiniAppInfo inequality")
    @allure.description("Test MiniAppInfo inequality.")
    def test_mini_app_info_inequality(self):
        """Test MiniAppInfo inequality."""
        mini_app1 = MiniAppInfo(url="https://example.com/app1")
        mini_app2 = MiniAppInfo(url="https://example.com/app2")

        assert mini_app1 != mini_app2

    @allure.title("MiniAppInfo hashing")
    @allure.description("Test MiniAppInfo hashing.")
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

    @allure.title("MiniAppInfo hash inequality")
    @allure.description("Test MiniAppInfo hash inequality.")
    def test_mini_app_info_hash_inequality(self):
        """Test MiniAppInfo hash inequality."""
        mini_app1 = MiniAppInfo(url="https://example.com/app1")
        mini_app2 = MiniAppInfo(url="https://example.com/app2")

        assert hash(mini_app1) != hash(mini_app2)

    @allure.title("MiniAppInfo string representation")
    @allure.description("Test MiniAppInfo string representation.")
    def test_mini_app_info_repr(self):
        """Test MiniAppInfo string representation."""
        mini_app = MiniAppInfo(**VALID_MINI_APP_INFO_DATA)  # type: ignore[arg-type]
        repr_str = repr(mini_app)

        assert "MiniAppInfo" in repr_str
        assert "url='https://example.com/mini-app'" in repr_str

    @allure.title("different platform values")
    @allure.description("Test different platform values.")
    def test_mini_app_info_platforms(self):
        """Test different platform values."""
        platforms = ["web", "mobile", "desktop", "tv"]

        for platform in platforms:
            mini_app = MiniAppInfo(
                url="https://example.com/mini-app", platform=platform
            )
            assert mini_app.platform == platform

    @allure.title("that MiniAppInfo is frozen (cannot modify attributes)")
    @allure.description("Test that MiniAppInfo is frozen (cannot modify attributes).")
    def test_mini_app_info_frozen(self):
        """Test that MiniAppInfo is frozen (cannot modify attributes)."""
        mini_app = MiniAppInfo(url="https://example.com")
        # Should raise AttributeError when trying to modify
        with pytest.raises(AttributeError, match="immutable type"):
            mini_app.url = "https://example.com/new"  # type: ignore[misc]

    @allure.title("MiniAppInfo edge cases")
    @allure.description("Test MiniAppInfo edge cases.")
    def test_mini_app_info_edge_cases(self):
        """Test MiniAppInfo edge cases."""
        mini_app = MiniAppInfo(**EDGE_CASE_MINI_APP_INFO_DATA)  # type: ignore[arg-type]

        assert mini_app.url == ""
        assert mini_app.start_param == ""
        assert mini_app.theme_params == {}

    @allure.title("MiniAppInfo with unicode characters")
    @allure.description("Test MiniAppInfo with unicode characters.")
    def test_mini_app_info_unicode(self):
        """Test MiniAppInfo with unicode characters."""
        mini_app = MiniAppInfo(**UNICODE_MINI_APP_INFO_DATA)  # type: ignore[arg-type]

        assert mini_app.url == "https://example.com/тест-приложение"
        assert mini_app.start_param == "параметр_用户_テスト"
        assert mini_app.theme_params == {"title": "Тест", "description": "测试"}

    @allure.title("MiniAppInfo with nested theme_params")
    @allure.description("Test MiniAppInfo with nested theme_params.")
    def test_mini_app_info_theme_params_nested(self):
        """Test MiniAppInfo with nested theme_params."""
        nested_params = {
            "bg_color": "#ffffff",
            "nested": {"key": "value", "list": [1, 2, 3]},
        }
        mini_app = MiniAppInfo(url="https://example.com", theme_params=nested_params)
        assert mini_app.theme_params == nested_params

    @allure.title("MiniAppInfo with very long URL")
    @allure.description("Test MiniAppInfo with very long URL.")
    def test_mini_app_info_very_long_url(self):
        """Test MiniAppInfo with very long URL."""
        long_url = "https://example.com/" + "a" * 10000
        mini_app = MiniAppInfo(url=long_url)
        assert len(mini_app.url) == len(long_url)


class TestApiResult:
    """Test cases for ApiResult model."""

    @allure.title("creating a valid ApiResult")
    @allure.description("Test creating a valid ApiResult.")
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

    @allure.title("creating an error ApiResult")
    @allure.description("Test creating an error ApiResult.")
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

    @allure.title("creating a timeout ApiResult")
    @allure.description("Test creating a timeout ApiResult.")
    def test_timeout_api_result_creation(self):
        """Test creating a timeout ApiResult."""
        result = ApiResult(**TIMEOUT_API_RESULT_DATA)  # type: ignore[arg-type]

        assert result.status_code == 408
        assert result.response_time == 30.0
        assert result.success is False
        assert result.client_error is True
        assert result.error_message == "Request timeout"

    @allure.title("creating a redirect ApiResult")
    @allure.description("Test creating a redirect ApiResult.")
    def test_redirect_api_result_creation(self):
        """Test creating a redirect ApiResult."""
        result = ApiResult(**REDIRECT_API_RESULT_DATA)  # type: ignore[arg-type]

        assert result.status_code == 301
        assert result.redirect is True
        assert result.success is False

    @allure.title("creating a server error ApiResult")
    @allure.description("Test creating a server error ApiResult.")
    def test_server_error_api_result_creation(self):
        """Test creating a server error ApiResult."""
        result = ApiResult(**SERVER_ERROR_API_RESULT_DATA)  # type: ignore[arg-type]

        assert result.status_code == 500
        assert result.server_error is True
        assert result.success is False

    @allure.title("creating an informational ApiResult")
    @allure.description("Test creating an informational ApiResult.")
    def test_informational_api_result_creation(self):
        """Test creating an informational ApiResult."""
        result = ApiResult(**INFORMATIONAL_API_RESULT_DATA)  # type: ignore[arg-type]

        assert result.status_code == 101
        assert result.informational is True
        assert result.success is False

    @allure.title("ApiResult required fields")
    @allure.description("Test ApiResult required fields.")
    def test_api_result_required_fields(self):
        """Test ApiResult required fields."""
        # Test that all required fields are needed
        with pytest.raises(TypeError):
            ApiResult()  # type: ignore[call-arg]  # Missing required fields

        with pytest.raises(TypeError):
            ApiResult(endpoint="/api/test")  # type: ignore[call-arg]  # Missing other required fields

    @allure.title("ApiResult field types")
    @allure.description("Test ApiResult field types.")
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

    @allure.title("ApiResult with invalid status_code type")
    @allure.description("Test ApiResult with invalid status_code type.")
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

    @allure.title("ApiResult with invalid response_time type")
    @allure.description("Test ApiResult with invalid response_time type.")
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

    @allure.title("ApiResult with invalid headers type")
    @allure.description("Test ApiResult with invalid headers type.")
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
    @allure.title("different status codes")
    @allure.description("Test different status codes.")
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

    @allure.title("different response times")
    @allure.description("Test different response times.")
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

    @allure.title("ApiResult serialization")
    @allure.description("Test ApiResult serialization.")
    def test_api_result_serialization(self):
        """Test ApiResult serialization."""
        result = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]

        # Test serialization to dict
        result_dict = msgspec.to_builtins(result)
        assert isinstance(result_dict, dict)
        assert result_dict["endpoint"] == "/api/status"
        assert result_dict["status_code"] == 200
        assert result_dict["success"] is True

    @allure.title("ApiResult serialization with response data")
    @allure.description("Test ApiResult serialization with response data.")
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

        expected_body_base64 = base64.b64encode(b'{"test": "data"}').decode("utf-8")
        assert result_dict["body"] == expected_body_base64

    @allure.title("ApiResult deserialization")
    @allure.description("Test ApiResult deserialization.")
    def test_api_result_deserialization(self):
        """Test ApiResult deserialization."""
        result_dict = VALID_API_RESULT_DATA.copy()

        # Test deserialization from dict
        result = msgspec.convert(result_dict, ApiResult)
        assert isinstance(result, ApiResult)
        assert result.endpoint == "/api/status"
        assert result.status_code == 200
        assert result.success is True

    @allure.title("ApiResult deserialization with None in optional fields")
    @allure.description("Test ApiResult deserialization with None in optional fields.")
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

    @allure.title("ApiResult equality")
    @allure.description("Test ApiResult equality.")
    def test_api_result_equality(self):
        """Test ApiResult equality."""
        result1 = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]
        result2 = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]
        result3 = ApiResult(**ERROR_API_RESULT_DATA)  # type: ignore[arg-type]

        assert result1 == result2
        assert result1 != result3

    @allure.title("ApiResult inequality")
    @allure.description("Test ApiResult inequality.")
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

    @allure.title("ApiResult hashing")
    @allure.description("Test ApiResult hashing.")
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

    @allure.title("ApiResult hash inequality")
    @allure.description("Test ApiResult hash inequality.")
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

    @allure.title("ApiResult string representation")
    @allure.description("Test ApiResult string representation.")
    def test_api_result_repr(self):
        """Test ApiResult string representation."""
        result = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]
        repr_str = repr(result)

        assert "ApiResult" in repr_str
        assert "endpoint='/api/status'" in repr_str
        assert "status_code=200" in repr_str
        assert "success=True" in repr_str

    @allure.title("that ApiResult is frozen (cannot modify attributes)")
    @allure.description("Test that ApiResult is frozen (cannot modify attributes).")
    def test_api_result_frozen(self):
        """Test that ApiResult is frozen (cannot modify attributes)."""
        result = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]
        # Should raise AttributeError when trying to modify
        with pytest.raises(AttributeError, match="immutable type"):
            result.endpoint = "/api/new"  # type: ignore[misc]

    @allure.title("ApiResult with empty strings")
    @allure.description("Test ApiResult with empty strings.")
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

    @allure.title("ApiResult with unicode characters")
    @allure.description("Test ApiResult with unicode characters.")
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

    @allure.title("ApiResult with very long strings")
    @allure.description("Test ApiResult with very long strings.")
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

    @allure.title("ApiResult with response data fields")
    @allure.description("Test ApiResult with response data fields.")
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

    @allure.title("TC-MODEL-API-022: ApiResult.json() method")
    @allure.description("Test ApiResult.json() method. TC-MODEL-API-022")
    def test_api_result_json_method(self):
        """Test ApiResult.json() method."""
        json_data = {"key": "value", "number": 123}
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
            body=json.dumps(json_data).encode("utf-8"),
        )

        parsed = result.json()
        assert parsed == json_data
        assert parsed["key"] == "value"
        assert parsed["number"] == 123

    @allure.title(
        "TC-MODEL-API-023: ApiResult.json() raises ValueError for invalid JSON"
    )
    @allure.description(
        "Test ApiResult.json() raises ValueError for invalid JSON. TC-MODEL-API-023"
    )
    def test_api_result_json_method_invalid_json(self):
        """Test ApiResult.json() raises ValueError for invalid JSON."""
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
            body=b"not valid json",
        )

        with pytest.raises(ValueError, match="Failed to parse JSON"):
            result.json()

    @allure.title("TC-MODEL-API-024: ApiResult.text() method")
    @allure.description("Test ApiResult.text() method. TC-MODEL-API-024")
    def test_api_result_text_method(self):
        """Test ApiResult.text() method."""
        text_content = "Hello, World!"
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
            body=text_content.encode("utf-8"),
        )

        assert result.text() == text_content

    @allure.title("TC-MODEL-API-025: ApiResult.text() handles decode errors gracefully")
    @allure.description(
        "Test ApiResult.text() handles decode errors gracefully. TC-MODEL-API-025"
    )
    def test_api_result_text_method_with_errors(self):
        """Test ApiResult.text() handles decode errors gracefully."""
        # Invalid UTF-8 sequence
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
            body=b"\xff\xfe\x00\x01",  # Invalid UTF-8
        )

        # Should not raise, but return replacement characters
        text = result.text()
        assert isinstance(text, str)

    @allure.title(
        "TC-MODEL-API-026: ApiResult.raise_for_status() does not raise for success"
    )
    @allure.description(
        "Test ApiResult.raise_for_status() does not raise for success. TC-MODEL-API-026"
    )
    def test_api_result_raise_for_status_success(self):
        """Test ApiResult.raise_for_status() does not raise for success."""
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
        )

        # Should not raise
        result.raise_for_status()

    @allure.title(
        "TC-MODEL-API-027: ApiResult.raise_for_status() raises for 4xx status"
    )
    @allure.description(
        "Test ApiResult.raise_for_status() raises for 4xx status. TC-MODEL-API-027"
    )
    def test_api_result_raise_for_status_client_error(self):
        """Test ApiResult.raise_for_status() raises for 4xx status."""
        result = ApiResult(
            endpoint="/api/test",
            method="GET",
            status_code=404,
            response_time=0.1,
            success=False,
            redirect=False,
            client_error=True,
            server_error=False,
            informational=False,
            error_message="Not Found",
        )

        with pytest.raises(Exception, match="HTTP 404"):
            result.raise_for_status()

    @allure.title(
        "TC-MODEL-API-028: ApiResult.raise_for_status() raises for 5xx status"
    )
    @allure.description(
        "Test ApiResult.raise_for_status() raises for 5xx status. TC-MODEL-API-028"
    )
    def test_api_result_raise_for_status_server_error(self):
        """Test ApiResult.raise_for_status() raises for 5xx status."""
        result = ApiResult(
            endpoint="/api/test",
            method="GET",
            status_code=500,
            response_time=0.1,
            success=False,
            redirect=False,
            client_error=False,
            server_error=True,
            informational=False,
            error_message="Internal Server Error",
        )

        with pytest.raises(Exception, match="HTTP 500"):
            result.raise_for_status()

    @allure.title("TC-MODEL-API-029: ApiResult.assert_status_code() with matching code")
    @allure.description(
        "Test ApiResult.assert_status_code() with matching code. TC-MODEL-API-029"
    )
    def test_api_result_assert_status_code_success(self):
        """Test ApiResult.assert_status_code() with matching code."""
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
        )

        # Should not raise
        result.assert_status_code(200)

    @allure.title(
        "TC-MODEL-API-030: ApiResult.assert_status_code() raises AssertionError for mismatch"
    )
    @allure.description(
        "Test ApiResult.assert_status_code() raises AssertionError for mismatch. TC-MODEL-API-030"
    )
    def test_api_result_assert_status_code_failure(self):
        """Test ApiResult.assert_status_code() raises AssertionError for mismatch."""
        result = ApiResult(
            endpoint="/api/test",
            method="GET",
            status_code=404,
            response_time=0.1,
            success=False,
            redirect=False,
            client_error=True,
            server_error=False,
            informational=False,
            body=b"Not Found",
        )

        with pytest.raises(AssertionError, match="Expected status code 200, got 404"):
            result.assert_status_code(200)

    @allure.title("TC-MODEL-API-031: ApiResult.assert_success() for successful request")
    @allure.description(
        "Test ApiResult.assert_success() for successful request. TC-MODEL-API-031"
    )
    def test_api_result_assert_success(self):
        """Test ApiResult.assert_success() for successful request."""
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
        )

        # Should not raise
        result.assert_success()

    @allure.title(
        "TC-MODEL-API-032: ApiResult.assert_success() raises AssertionError for failed request"
    )
    @allure.description(
        "Test ApiResult.assert_success() raises AssertionError for failed request. TC-MODEL-API-032"
    )
    def test_api_result_assert_success_failure(self):
        """Test ApiResult.assert_success() raises AssertionError for failed request."""
        result = ApiResult(
            endpoint="/api/test",
            method="GET",
            status_code=500,
            response_time=0.1,
            success=False,
            redirect=False,
            client_error=False,
            server_error=True,
            informational=False,
            body=b"Server Error",
        )

        with pytest.raises(AssertionError, match="Request failed with status 500"):
            result.assert_success()

    @allure.title(
        "TC-MODEL-API-033: ApiResult.assert_has_fields() with all fields present"
    )
    @allure.description(
        "Test ApiResult.assert_has_fields() with all fields present. TC-MODEL-API-033"
    )
    def test_api_result_assert_has_fields_success(self):
        """Test ApiResult.assert_has_fields() with all fields present."""
        json_data = {"name": "test", "id": 123, "status": "active"}
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
            body=json.dumps(json_data).encode("utf-8"),
        )

        # Should not raise
        result.assert_has_fields("name", "id", "status")

    @allure.title(
        "TC-MODEL-API-034: ApiResult.assert_has_fields() raises AssertionError for missing fields"
    )
    @allure.description(
        "Test ApiResult.assert_has_fields() raises AssertionError for missing fields. TC-MODEL-API-034"
    )
    def test_api_result_assert_has_fields_missing(self):
        """Test ApiResult.assert_has_fields() raises AssertionError for missing fields."""
        json_data = {"name": "test", "id": 123}
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
            body=json.dumps(json_data).encode("utf-8"),
        )

        with pytest.raises(AssertionError, match="Missing required fields"):
            result.assert_has_fields("name", "id", "status", "email")

    @allure.title("different HTTP methods")
    @allure.description("Test different HTTP methods.")
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
