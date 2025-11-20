"""
Fixtures for UserTelegramClient testing.
"""

import copy
import itertools
from datetime import datetime
from pytest import fixture
from telethon.tl.types import User, Channel, Chat, Message

from src.config import Config
from src.mtproto_client import UserTelegramClient, UserInfo


def _get_base_config_data() -> dict:
    """Get base config data for creating Config instances."""
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session_string_123456789",
        "timeout": 30,
        "retry_count": 3,
        "retry_delay": 1.0,
        "log_level": "DEBUG",
    }


@fixture
def valid_config() -> Config:
    """Create a valid Config instance."""
    return Config(**_get_base_config_data())


@fixture
def config_with_session_string() -> Config:
    """Create Config with session_string."""
    data = _get_base_config_data()
    data["session_string"] = "test_session_string_123456789"
    return Config(**data)


@fixture
def config_with_session_file() -> Config:
    """Create Config with session_file."""
    data = _get_base_config_data()
    data.pop("session_string", None)
    data["session_file"] = "test_session.session"
    return Config(**data)


@fixture
def config_without_session(mocker) -> Config:
    """Create Config without session (will use fallback)."""
    # Mock SQLiteSession to avoid file system operations
    mocker.patch("src.mtproto_client.SQLiteSession")
    data = _get_base_config_data()
    # For testing, we need a session, so use session_string
    # The actual code will use SQLiteSession fallback, but Config validation requires a session
    data["session_string"] = "test_session"
    return Config(**data)


@fixture
def mock_telegram_user(mocker) -> User:
    """Create a mock Telegram User object."""
    user = mocker.MagicMock(spec=User)
    user.id = 123456789
    user.username = "test_user"
    user.first_name = "Test User"
    user.last_name = "Test"
    user.phone = "+1234567890"
    user.bot = False
    user.verified = True
    user.premium = False
    return user


@fixture
def mock_telegram_bot(mocker) -> User:
    """Create a mock Telegram Bot (User with bot=True)."""
    bot = mocker.MagicMock(spec=User)
    bot.id = 987654321
    bot.username = "test_bot"
    bot.first_name = "Test Bot"
    bot.last_name = None
    bot.phone = None
    bot.bot = True
    bot.verified = False
    bot.premium = False
    return bot


@fixture
def mock_telegram_channel(mocker) -> Channel:
    """Create a mock Telegram Channel object."""
    channel = mocker.MagicMock(spec=Channel)
    channel.id = 444555666
    channel.title = "Test Channel"
    channel.username = "test_channel"
    channel.verified = True
    channel.broadcast = True
    channel.megagroup = False
    return channel


@fixture
def mock_telegram_chat(mocker) -> Chat:
    """Create a mock Telegram Chat object."""
    # Create a mock that only has Chat-specific attributes
    chat = mocker.MagicMock()
    # Set only Chat-specific attributes
    chat.id = 987654321
    chat.title = "Test Chat"
    chat.username = "test_chat"
    chat.verified = False
    # Ensure broadcast attribute is False for Chat (not True like Channel)
    chat.broadcast = False
    # Explicitly set first_name to None to distinguish from User
    chat.first_name = None
    return chat


@fixture
def mock_telegram_message(mocker, mock_telegram_user, mock_telegram_chat) -> Message:
    """Create a mock Telegram Message object."""
    message = mocker.MagicMock(spec=Message)
    message.id = 111222333
    message.text = "Test message"
    message.from_id = mocker.MagicMock()
    message.from_id.user_id = mock_telegram_user.id
    message.chat_id = mock_telegram_chat.id
    message.date = datetime(2023, 10, 20, 10, 0, 0)
    message.reply_to_msg_id = None
    message.media = None
    return message


@fixture
def mock_telegram_message_with_reply(mock_telegram_message) -> Message:
    """Create a mock Telegram Message with reply."""
    message = copy.deepcopy(mock_telegram_message)
    message.reply_to_msg_id = 111222332
    return message


@fixture
def mock_telegram_message_with_media(mocker, mock_telegram_message) -> Message:
    """Create a mock Telegram Message with media."""
    message = copy.deepcopy(mock_telegram_message)
    media = mocker.MagicMock()
    media.url = "https://example.com/photo.jpg"
    media.webpage = None
    message.media = media
    return message


@fixture
def mock_telegram_message_with_webapp(mocker, mock_telegram_message) -> Message:
    """Create a mock Telegram Message with web_app media."""
    message = copy.deepcopy(mock_telegram_message)
    media = mocker.MagicMock()
    media.url = None
    media.webpage = mocker.MagicMock()
    media.webpage.url = "https://t.me/mybot/app?start=123"
    message.media = media
    return message


@fixture
def mock_telegram_client_authorized(mocker, mock_telegram_user):
    """Create a mock TelegramClient that is authorized."""
    client = mocker.AsyncMock()
    client.is_connected.return_value = True
    client.is_user_authorized = mocker.AsyncMock(return_value=True)
    client.connect = mocker.AsyncMock()
    client.disconnect = mocker.AsyncMock()
    client.get_me = mocker.AsyncMock(return_value=mock_telegram_user)
    client.get_entity = mocker.AsyncMock(return_value=mock_telegram_user)
    client.send_message = mocker.AsyncMock()
    client.get_messages = mocker.AsyncMock(return_value=[])
    client.add_event_handler = mocker.MagicMock()
    client.run_until_disconnected = mocker.AsyncMock()

    # Mock loop for interact_with_bot
    loop = mocker.MagicMock()
    time_counter = itertools.count()
    loop.time = mocker.AsyncMock(
        side_effect=lambda: next(time_counter)
    )  # Simulate unbounded time progression
    client.loop = loop

    return client


@fixture
def mock_telegram_client_unauthorized(mocker):
    """Create a mock TelegramClient that is not authorized."""
    client = mocker.AsyncMock()
    client.is_connected.return_value = True
    client.is_user_authorized = mocker.AsyncMock(return_value=False)
    client.connect = mocker.AsyncMock()
    client.disconnect = mocker.AsyncMock()
    return client


@fixture
def mock_telegram_client_not_connected(mocker):
    """Create a mock TelegramClient that is not connected."""
    client = mocker.AsyncMock()
    client.is_connected.return_value = False
    client.is_user_authorized = mocker.AsyncMock(return_value=False)
    client.connect = mocker.AsyncMock()
    client.disconnect = mocker.AsyncMock()
    return client


@fixture
def user_telegram_client(
    mocker, valid_config, mock_telegram_client_authorized
) -> UserTelegramClient:
    """Create UserTelegramClient with mocked TelegramClient."""
    # Mock StringSession to avoid validation error
    # Patch StringSession where it's used in the module
    mock_session = mocker.MagicMock()
    mocker.patch("src.mtproto_client.StringSession", return_value=mock_session)
    # Create client with patched TelegramClient
    mocker.patch(
        "src.mtproto_client.TelegramClient",
        return_value=mock_telegram_client_authorized,
    )
    client = UserTelegramClient(valid_config)
    # Replace the client with our mock
    client.client = mock_telegram_client_authorized
    return client


@fixture
def user_telegram_client_with_session_file(
    mocker, config_with_session_file, mock_telegram_client_authorized
) -> UserTelegramClient:
    """Create UserTelegramClient with session_file."""
    mocker.patch(
        "src.mtproto_client.TelegramClient",
        return_value=mock_telegram_client_authorized,
    )
    client = UserTelegramClient(config_with_session_file)
    client.client = mock_telegram_client_authorized
    return client


@fixture
def user_telegram_client_without_session(
    mocker, config_without_session, mock_telegram_client_authorized
) -> UserTelegramClient:
    """Create UserTelegramClient without session (fallback)."""
    mocker.patch(
        "src.mtproto_client.TelegramClient",
        return_value=mock_telegram_client_authorized,
    )
    client = UserTelegramClient(config_without_session)
    client.client = mock_telegram_client_authorized
    return client


@fixture
def user_telegram_client_connected(
    user_telegram_client, mock_telegram_user
) -> UserTelegramClient:
    """Create UserTelegramClient that is connected and authorized."""
    user_telegram_client._is_connected = True
    user_telegram_client._me = UserInfo(
        id=mock_telegram_user.id,
        username=mock_telegram_user.username,
        first_name=mock_telegram_user.first_name,
        last_name=mock_telegram_user.last_name,
        phone=mock_telegram_user.phone,
        is_bot=mock_telegram_user.bot,
        is_verified=mock_telegram_user.verified,
        is_premium=mock_telegram_user.premium,
    )
    return user_telegram_client
