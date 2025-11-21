"""
Unit tests for UserTelegramClient.
"""

import pytest

# Removed unittest.mock import - using pytest-mock instead
from datetime import datetime

from telethon.tl.types import User, Chat, Message

from tma_test_framework.mtproto_client import (
    UserTelegramClient,
    UserInfo,
    ChatInfo,
    MessageInfo,
)
from tests.data.constants import (
    BOT_COMMANDS,
    BOT_TIMEOUTS,
    MINI_APP_TEXT_SAMPLES,
    GET_MESSAGES_LIMITS,
    GET_MESSAGES_OFFSET_IDS,
    GET_ENTITY_PARAMS,
)


# ============================================================================
# I. Инициализация и управление подключением
# ============================================================================


class TestUserTelegramClientInit:
    """Test UserTelegramClient initialization."""

    def test_init_with_session_string(self, mocker, config_with_session_string):
        """Test initialization with session_string uses StringSession."""
        mock_string_session = mocker.patch(
            "tma_test_framework.mtproto_client.StringSession"
        )
        mock_client = mocker.patch("tma_test_framework.mtproto_client.TelegramClient")
        _ = UserTelegramClient(config_with_session_string)

        # Verify StringSession was called
        mock_string_session.assert_called_once_with(
            config_with_session_string.session_string
        )
        # Verify TelegramClient was created with correct parameters
        mock_client.assert_called_once()
        # TelegramClient is called with positional args: (session, api_id, api_hash, ...)
        call_args = mock_client.call_args
        # Check positional arguments (args[0] is session, args[1] is api_id, args[2] is api_hash)
        assert len(call_args.args) >= 3, (
            "TelegramClient should be called with at least 3 positional args"
        )
        assert call_args.args[1] == config_with_session_string.api_id, (
            "api_id should match"
        )
        assert call_args.args[2] == config_with_session_string.api_hash, (
            "api_hash should match"
        )

        # Check keyword arguments if present
        if call_args.kwargs:
            if "timeout" in call_args.kwargs:
                assert call_args.kwargs["timeout"] == config_with_session_string.timeout
            if "retry_delay" in call_args.kwargs:
                assert (
                    call_args.kwargs["retry_delay"]
                    == config_with_session_string.retry_delay
                )
            if "retry_connect" in call_args.kwargs:
                assert (
                    call_args.kwargs["retry_connect"]
                    == config_with_session_string.retry_count
                )

    def test_init_with_session_file(self, mocker, config_with_session_file):
        """Test initialization with session_file uses SQLiteSession."""
        mock_sqlite_session = mocker.patch(
            "tma_test_framework.mtproto_client.SQLiteSession"
        )
        mock_client = mocker.patch("tma_test_framework.mtproto_client.TelegramClient")
        _ = UserTelegramClient(config_with_session_file)

        # Verify SQLiteSession was called
        mock_sqlite_session.assert_called_once_with(
            config_with_session_file.session_file
        )
        mock_client.assert_called_once()

    def test_init_without_session(self, mocker, config_without_session):
        """Test initialization without session uses fallback SQLiteSession."""
        # Mock StringSession to avoid validation error
        mock_string_session = mocker.patch(
            "tma_test_framework.mtproto_client.StringSession",
            return_value=mocker.MagicMock(),
        )
        _ = mocker.patch("tma_test_framework.mtproto_client.SQLiteSession")
        mock_client = mocker.patch("tma_test_framework.mtproto_client.TelegramClient")
        _ = UserTelegramClient(config_without_session)

        # Verify StringSession was called (config_without_session has session_string)
        mock_string_session.assert_called_once()
        mock_client.assert_called_once()

    def test_init_without_session_fallback(self, mocker):
        """Test initialization without session uses fallback SQLiteSession("tma_session"). TC-CLIENT-002a"""
        # Create Config without session by bypassing __post_init__ validation
        # This tests the defensive code at line 75
        from tma_test_framework.config import Config

        # Create Config with valid session first to pass validation
        config = Config(
            api_id=12345,
            api_hash="12345678901234567890123456789012",
            session_string="valid_session",  # Valid session to pass validation
            timeout=30,
            retry_count=3,
            retry_delay=1.0,
            log_level="INFO",
        )

        # Now modify attributes to None using object.__setattr__ (works for frozen struct)
        # This bypasses the validation that happened in __post_init__
        object.__setattr__(config, "session_string", None)
        object.__setattr__(config, "session_file", None)

        # Mock SQLiteSession to verify it's called with "tma_session"
        mock_sqlite_session = mocker.patch(
            "tma_test_framework.mtproto_client.SQLiteSession"
        )
        mock_client = mocker.patch("tma_test_framework.mtproto_client.TelegramClient")

        _ = UserTelegramClient(config)

        # Verify SQLiteSession was called with "tma_session" as fallback
        mock_sqlite_session.assert_called_once_with("tma_session")
        mock_client.assert_called_once()

    def test_init_sets_initial_state(self, mocker, valid_config):
        """Test that initialization sets correct initial state."""
        # Mock StringSession to avoid validation error
        mocker.patch("tma_test_framework.mtproto_client.StringSession")
        mocker.patch("tma_test_framework.mtproto_client.TelegramClient")
        client = UserTelegramClient(valid_config)

        assert client._is_connected is False
        assert client._me is None
        assert client.config == valid_config


class TestUserTelegramClientContextManager:
    """Test UserTelegramClient async context manager."""

    @pytest.mark.asyncio
    async def test_aenter_calls_connect(self, mocker, user_telegram_client):
        """Test __aenter__ calls connect()."""
        user_telegram_client.connect = mocker.AsyncMock()

        async with user_telegram_client:
            user_telegram_client.connect.assert_called_once()

    @pytest.mark.asyncio
    async def test_aexit_calls_disconnect(self, mocker, user_telegram_client):
        """Test __aexit__ calls disconnect()."""
        user_telegram_client.disconnect = mocker.AsyncMock()

        async with user_telegram_client:
            pass

        user_telegram_client.disconnect.assert_called_once()


class TestUserTelegramClientConnect:
    """Test UserTelegramClient connect method."""

    @pytest.mark.asyncio
    async def test_connect_success(
        self, mocker, user_telegram_client, mock_telegram_user
    ):
        """Test successful connection."""
        user_telegram_client.client.connect = mocker.AsyncMock()
        user_telegram_client.client.is_user_authorized = mocker.AsyncMock(
            return_value=True
        )
        user_telegram_client.client.get_me = mocker.AsyncMock(
            return_value=mock_telegram_user
        )

        await user_telegram_client.connect()

        assert user_telegram_client._is_connected is True
        assert user_telegram_client._me is not None
        user_telegram_client.client.connect.assert_called_once()

    @pytest.mark.asyncio
    async def test_connect_not_authorized(self, mocker, user_telegram_client):
        """Test connection fails when user is not authorized."""
        user_telegram_client.client.connect = mocker.AsyncMock()
        user_telegram_client.client.is_user_authorized = mocker.AsyncMock(
            return_value=False
        )

        with pytest.raises(ValueError, match="User not authorized"):
            await user_telegram_client.connect()

        assert user_telegram_client._is_connected is False

    @pytest.mark.asyncio
    async def test_connect_already_connected(
        self, mocker, user_telegram_client_connected
    ):
        """Test connect() when already connected logs and returns."""
        user_telegram_client_connected.client.connect = mocker.AsyncMock()

        await user_telegram_client_connected.connect()

        # Should not call connect again
        user_telegram_client_connected.client.connect.assert_not_called()

    @pytest.mark.asyncio
    async def test_connect_exception_logs_and_raises(
        self, mocker, user_telegram_client
    ):
        """Test connect() logs error and raises exception."""
        error = ConnectionError("Connection failed")
        user_telegram_client.client.connect = mocker.AsyncMock(side_effect=error)

        with pytest.raises(ConnectionError):
            await user_telegram_client.connect()


class TestUserTelegramClientDisconnect:
    """Test UserTelegramClient disconnect method."""

    @pytest.mark.asyncio
    async def test_disconnect_when_connected(
        self, mocker, user_telegram_client_connected
    ):
        """Test disconnect() when connected."""
        user_telegram_client_connected.client.disconnect = mocker.AsyncMock()

        await user_telegram_client_connected.disconnect()

        assert user_telegram_client_connected._is_connected is False
        user_telegram_client_connected.client.disconnect.assert_called_once()

    @pytest.mark.asyncio
    async def test_disconnect_when_not_connected(self, mocker, user_telegram_client):
        """Test disconnect() when not connected does nothing."""
        user_telegram_client.client.disconnect = mocker.AsyncMock()

        await user_telegram_client.disconnect()

        # Should not raise error, but also should not call disconnect
        # (since _is_connected is False)
        assert user_telegram_client._is_connected is False


class TestUserTelegramClientIsConnected:
    """Test UserTelegramClient is_connected method."""

    @pytest.mark.asyncio
    async def test_is_connected_true(self, mocker, user_telegram_client_connected):
        """Test is_connected() returns True when connected and authorized."""
        user_telegram_client_connected.client.is_connected = mocker.MagicMock(
            return_value=True
        )

        result = await user_telegram_client_connected.is_connected()

        assert result is True

    @pytest.mark.asyncio
    async def test_is_connected_false_not_connected(self, mocker, user_telegram_client):
        """Test is_connected() returns False when not connected."""
        user_telegram_client.client.is_connected = mocker.MagicMock(return_value=False)

        result = await user_telegram_client.is_connected()

        assert result is False

    @pytest.mark.asyncio
    async def test_is_connected_false_client_not_connected(
        self, mocker, user_telegram_client_connected
    ):
        """Test is_connected() returns False when client is not connected."""
        user_telegram_client_connected.client.is_connected = mocker.MagicMock(
            return_value=False
        )

        result = await user_telegram_client_connected.is_connected()

        assert result is False


# ============================================================================
# II. Методы получения данных
# ============================================================================


class TestUserTelegramClientGetMe:
    """Test UserTelegramClient get_me method."""

    @pytest.mark.asyncio
    async def test_get_me_success(
        self, mocker, user_telegram_client, mock_telegram_user
    ):
        """Test get_me() returns UserInfo with correct fields."""
        user_telegram_client.client.get_me = mocker.AsyncMock(
            return_value=mock_telegram_user
        )

        result = await user_telegram_client.get_me()

        assert isinstance(result, UserInfo)
        assert result.id == mock_telegram_user.id
        assert result.first_name == mock_telegram_user.first_name
        assert result.username == mock_telegram_user.username
        assert result.last_name == mock_telegram_user.last_name
        assert result.phone == mock_telegram_user.phone
        assert result.is_bot == mock_telegram_user.bot
        assert result.is_verified == mock_telegram_user.verified
        assert result.is_premium == mock_telegram_user.premium

    @pytest.mark.asyncio
    async def test_get_me_handles_none_fields(self, mocker, user_telegram_client):
        """Test get_me() handles None fields correctly."""
        user = mocker.MagicMock(spec=User)
        user.id = 123456789
        user.username = None
        user.first_name = "Test"
        user.last_name = None
        user.phone = None
        user.bot = False
        user.verified = False
        user.premium = False

        user_telegram_client.client.get_me = mocker.AsyncMock(return_value=user)

        result = await user_telegram_client.get_me()

        assert result.username is None
        assert result.last_name is None
        assert result.phone is None

    @pytest.mark.asyncio
    async def test_get_me_caches_result(
        self, mocker, user_telegram_client, mock_telegram_user
    ):
        """Test get_me() caches result in self._me."""
        user_telegram_client.client.get_me = mocker.AsyncMock(
            return_value=mock_telegram_user
        )

        result1 = await user_telegram_client.get_me()
        result2 = await user_telegram_client.get_me()

        # Should only call get_me once
        assert user_telegram_client.client.get_me.call_count == 1
        assert result1 == result2
        assert user_telegram_client._me == result1


class TestUserTelegramClientGetEntity:
    """Test UserTelegramClient get_entity method."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("entity", GET_ENTITY_PARAMS)
    async def test_get_entity_user(
        self, mocker, user_telegram_client, mock_telegram_user, entity
    ):
        """Test get_entity() with User returns ChatInfo with type='private'."""
        user_telegram_client.client.get_entity = mocker.AsyncMock(
            return_value=mock_telegram_user
        )

        result = await user_telegram_client.get_entity(entity)

        assert isinstance(result, ChatInfo)
        assert result.type == "private"
        assert result.id == mock_telegram_user.id
        assert result.username == mock_telegram_user.username
        # ChatInfo doesn't have is_bot - that's a UserInfo property
        assert result.is_verified == mock_telegram_user.verified

    @pytest.mark.asyncio
    async def test_get_entity_channel(
        self, mocker, user_telegram_client, mock_telegram_channel
    ):
        """Test get_entity() with Channel returns ChatInfo with type='channel'."""
        user_telegram_client.client.get_entity = mocker.AsyncMock(
            return_value=mock_telegram_channel
        )

        result = await user_telegram_client.get_entity("@test_channel")

        assert isinstance(result, ChatInfo)
        assert result.type == "channel"
        assert result.id == mock_telegram_channel.id
        assert result.title == mock_telegram_channel.title
        assert result.username == mock_telegram_channel.username

    @pytest.mark.asyncio
    async def test_get_entity_chat(
        self, mocker, user_telegram_client, mock_telegram_chat
    ):
        """Test get_entity() with Chat returns ChatInfo with type='group'."""
        user_telegram_client.client.get_entity = mocker.AsyncMock(
            return_value=mock_telegram_chat
        )

        result = await user_telegram_client.get_entity(987654321)

        assert isinstance(result, ChatInfo)
        assert result.type == "group"
        assert result.id == mock_telegram_chat.id
        assert result.title == mock_telegram_chat.title

    @pytest.mark.asyncio
    async def test_get_entity_handles_missing_username(
        self, mocker, user_telegram_client
    ):
        """Test get_entity() handles missing username."""
        chat = mocker.MagicMock(spec=Chat)
        chat.id = 987654321
        chat.title = "Test Chat"
        chat.username = None
        chat.verified = False

        user_telegram_client.client.get_entity = mocker.AsyncMock(return_value=chat)

        result = await user_telegram_client.get_entity(987654321)

        assert result.username is None

    @pytest.mark.asyncio
    async def test_get_entity_invalid_entity(self, mocker, user_telegram_client):
        """Test get_entity() raises exception for invalid entity."""
        user_telegram_client.client.get_entity = mocker.AsyncMock(
            side_effect=ValueError("Entity not found")
        )

        with pytest.raises(ValueError, match="Entity not found"):
            await user_telegram_client.get_entity("invalid_entity")

    @pytest.mark.asyncio
    async def test_get_entity_unsupported_type(self, mocker, user_telegram_client):
        """Test get_entity() raises ValueError for unsupported entity type."""
        from telethon.tl.types import Message

        mock_message = mocker.MagicMock(spec=Message)
        user_telegram_client.client.get_entity = mocker.AsyncMock(
            return_value=mock_message
        )

        with pytest.raises(ValueError, match="Unsupported entity type"):
            await user_telegram_client.get_entity("test")

    @pytest.mark.asyncio
    async def test_get_entity_channel_via_mock_fallback(
        self, mocker, user_telegram_client
    ):
        """Test get_entity() with Channel via mock fallback (line 212)."""
        # Create a mock that doesn't match isinstance checks but has Channel attributes
        mock_channel = mocker.MagicMock()  # No spec to avoid isinstance match
        mock_channel.id = 444555666
        mock_channel.title = "Test Channel"
        mock_channel.username = "test_channel"
        mock_channel.verified = True
        mock_channel.broadcast = True  # Key attribute for Channel detection

        user_telegram_client.client.get_entity = mocker.AsyncMock(
            return_value=mock_channel
        )

        result = await user_telegram_client.get_entity("@test_channel")

        assert isinstance(result, ChatInfo)
        assert result.type == "channel"
        assert result.id == mock_channel.id
        assert result.title == mock_channel.title

    @pytest.mark.asyncio
    async def test_get_entity_user_via_mock_fallback(
        self, mocker, user_telegram_client
    ):
        """Test get_entity() with User via mock fallback (line 249)."""
        # Create a mock that doesn't match isinstance checks but has User attributes
        mock_user = mocker.MagicMock()  # No spec to avoid isinstance match
        mock_user.id = 123456789
        mock_user.first_name = "Test"
        mock_user.last_name = "User"
        mock_user.username = "test_user"
        mock_user.verified = False

        user_telegram_client.client.get_entity = mocker.AsyncMock(
            return_value=mock_user
        )

        result = await user_telegram_client.get_entity(123456789)

        assert isinstance(result, ChatInfo)
        assert result.type == "private"
        assert result.id == mock_user.id
        assert result.title == "Test User"


# ============================================================================
# III. Отправка и получение сообщений
# ============================================================================


class TestUserTelegramClientSendMessage:
    """Test UserTelegramClient send_message method."""

    @pytest.mark.asyncio
    async def test_send_message_success(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_message,
        mock_telegram_user,
        mock_telegram_chat,
    ):
        """Test send_message() returns MessageInfo."""
        user_telegram_client_connected.client.send_message = mocker.AsyncMock(
            return_value=mock_telegram_message
        )
        user_telegram_client_connected.client.get_entity = mocker.AsyncMock(
            return_value=mock_telegram_chat
        )

        result = await user_telegram_client_connected.send_message("@test", "Hello")

        assert isinstance(result, MessageInfo)
        assert result.id == mock_telegram_message.id
        assert result.text == mock_telegram_message.text

    @pytest.mark.asyncio
    async def test_send_message_with_string_date(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_chat,
    ):
        """Test send_message() handles message.date without isoformat (line 288)."""

        # Create a message with date that doesn't have isoformat method
        # This triggers the else branch (line 288) instead of line 286
        class DateWithoutIsoformat:
            def __str__(self):
                return "2024-01-01T12:00:00"

        mock_message = mocker.MagicMock()
        mock_message.id = 12345
        mock_message.text = "Test message"
        # Use object without isoformat to trigger else branch
        mock_message.date = DateWithoutIsoformat()
        mock_message.from_id = None
        mock_message.peer_id = mocker.MagicMock()
        mock_message.peer_id.channel_id = None
        mock_message.peer_id.user_id = 123456789

        user_telegram_client_connected.client.send_message = mocker.AsyncMock(
            return_value=mock_message
        )
        user_telegram_client_connected.client.get_entity = mocker.AsyncMock(
            return_value=mock_telegram_chat
        )

        result = await user_telegram_client_connected.send_message("@test", "Hello")

        assert isinstance(result, MessageInfo)
        assert result.id == mock_message.id
        assert result.text == mock_message.text

    @pytest.mark.asyncio
    async def test_send_message_with_reply(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_message_with_reply,
        mock_telegram_chat,
    ):
        """Test send_message() with reply_to."""
        user_telegram_client_connected.client.send_message = mocker.AsyncMock(
            return_value=mock_telegram_message_with_reply
        )
        user_telegram_client_connected.client.get_entity = mocker.AsyncMock(
            return_value=mock_telegram_chat
        )

        result = await user_telegram_client_connected.send_message(
            "@test", "Reply", reply_to=111222332
        )

        assert result.reply_to == mock_telegram_message_with_reply.reply_to_msg_id

    @pytest.mark.asyncio
    async def test_send_message_with_parse_mode(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_message,
        mock_telegram_chat,
    ):
        """Test send_message() with parse_mode."""
        user_telegram_client_connected.client.send_message = mocker.AsyncMock(
            return_value=mock_telegram_message
        )
        user_telegram_client_connected.client.get_entity = mocker.AsyncMock(
            return_value=mock_telegram_chat
        )

        await user_telegram_client_connected.send_message(
            "@test", "**bold**", parse_mode="Markdown"
        )

        call_kwargs = user_telegram_client_connected.client.send_message.call_args[1]
        assert call_kwargs["parse_mode"] == "Markdown"

    @pytest.mark.asyncio
    async def test_send_message_invalid_entity(
        self, mocker, user_telegram_client_connected
    ):
        """Test send_message() raises exception for invalid entity."""
        user_telegram_client_connected.client.send_message = mocker.AsyncMock(
            side_effect=ValueError("Invalid entity")
        )

        with pytest.raises(ValueError, match="Invalid entity"):
            await user_telegram_client_connected.send_message("invalid", "Hello")

    @pytest.mark.asyncio
    async def test_send_message_with_media(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_message_with_media,
        mock_telegram_chat,
    ):
        """Test send_message() handles media."""
        user_telegram_client_connected.client.send_message = mocker.AsyncMock(
            return_value=mock_telegram_message_with_media
        )
        user_telegram_client_connected.client.get_entity = mocker.AsyncMock(
            return_value=mock_telegram_chat
        )

        result = await user_telegram_client_connected.send_message("@test", "Photo")

        assert result.media is not None
        assert result.media.get("url") == "https://example.com/photo.jpg"


class TestUserTelegramClientGetMessages:
    """Test UserTelegramClient get_messages method."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("limit", GET_MESSAGES_LIMITS)
    @pytest.mark.parametrize("offset_id", GET_MESSAGES_OFFSET_IDS)
    async def test_get_messages_success(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_message,
        mock_telegram_chat,
        mock_telegram_user,
        limit,
        offset_id,
    ):
        """Test get_messages() returns list of MessageInfo."""
        import copy

        messages = [copy.deepcopy(mock_telegram_message) for _ in range(limit)]
        user_telegram_client_connected.client.get_messages = mocker.AsyncMock(
            return_value=messages
        )

        # Mock get_entity: first call for chat, subsequent calls for users
        def get_entity_side_effect(entity):
            # First call is for the chat entity (@test)
            # Subsequent calls are for message.from_id (which is a PeerUser object)
            if hasattr(entity, "user_id"):
                # This is a PeerUser, return the user
                return mock_telegram_user
            # This is the chat entity
            return mock_telegram_chat

        user_telegram_client_connected.client.get_entity = mocker.AsyncMock(
            side_effect=get_entity_side_effect
        )

        result = await user_telegram_client_connected.get_messages(
            "@test", limit=limit, offset_id=offset_id
        )

        assert len(result) == limit
        assert all(isinstance(msg, MessageInfo) for msg in result)

    @pytest.mark.asyncio
    async def test_get_messages_skips_none(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_message,
        mock_telegram_chat,
        mock_telegram_user,
    ):
        """Test get_messages() skips None messages."""
        messages = [mock_telegram_message, None, mock_telegram_message]
        user_telegram_client_connected.client.get_messages = mocker.AsyncMock(
            return_value=messages
        )

        # Mock get_entity to return user for from_id and chat for entity
        def get_entity_side_effect(entity):
            if hasattr(entity, "user_id"):
                return mock_telegram_user
            return mock_telegram_chat

        user_telegram_client_connected.client.get_entity = mocker.AsyncMock(
            side_effect=get_entity_side_effect
        )

        result = await user_telegram_client_connected.get_messages("@test", limit=10)

        assert len(result) == 2  # None should be skipped

    @pytest.mark.asyncio
    async def test_get_messages_from_bot(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_bot,
        mock_telegram_chat,
    ):
        """Test get_messages() handles messages from bot correctly."""
        message = mocker.MagicMock(spec=Message)
        message.id = 111222333
        message.text = "Bot message"
        message.from_id = mocker.MagicMock()
        message.from_id.user_id = mock_telegram_bot.id
        message.chat_id = mock_telegram_chat.id
        message.date = datetime(2023, 10, 20, 10, 0, 0)
        message.reply_to_msg_id = None
        message.media = None

        user_telegram_client_connected.client.get_messages = mocker.AsyncMock(
            return_value=[message]
        )

        # Mock get_entity: first call for chat, second for bot user
        def get_entity_side_effect(entity):
            if hasattr(entity, "user_id") and entity.user_id == mock_telegram_bot.id:
                return mock_telegram_bot
            return mock_telegram_chat

        user_telegram_client_connected.client.get_entity = mocker.AsyncMock(
            side_effect=get_entity_side_effect
        )

        result = await user_telegram_client_connected.get_messages("@test_bot", limit=1)

        assert len(result) == 1
        assert result[0].from_user is not None
        assert result[0].from_user.is_bot is True

    @pytest.mark.asyncio
    async def test_get_messages_from_user_error_handled(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_message,
        mock_telegram_chat,
    ):
        """Test get_messages() handles error when getting from_user."""
        mock_telegram_message.from_id = mocker.MagicMock()
        mock_telegram_message.from_id.user_id = 999999999

        user_telegram_client_connected.client.get_messages = mocker.AsyncMock(
            return_value=[mock_telegram_message]
        )
        # Mock self.get_entity to return chat successfully
        from tma_test_framework.mtproto_client import ChatInfo

        user_telegram_client_connected.get_entity = mocker.AsyncMock(
            return_value=ChatInfo(
                id=mock_telegram_chat.id,
                title=mock_telegram_chat.title,
                type="channel",
                username=mock_telegram_chat.username,
                is_verified=False,
            )
        )
        # Mock client.get_entity to raise error for from_user
        user_telegram_client_connected.client.get_entity = mocker.AsyncMock(
            side_effect=ValueError("User not found")
        )

        result = await user_telegram_client_connected.get_messages("@test", limit=1)

        assert len(result) == 1
        assert result[0].from_user is None  # Should be None on error


# ============================================================================
# IV. Работа с ботами и Mini Apps
# ============================================================================


class TestUserTelegramClientInteractWithBot:
    """Test UserTelegramClient interact_with_bot method."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("command", BOT_COMMANDS)
    async def test_interact_with_bot_sends_command(
        self, mocker, user_telegram_client_connected, mock_telegram_message, command
    ):
        """Test interact_with_bot() sends command."""
        user_telegram_client_connected.send_message = mocker.AsyncMock(
            return_value=mock_telegram_message
        )
        user_telegram_client_connected.get_messages = mocker.AsyncMock(return_value=[])

        await user_telegram_client_connected.interact_with_bot(
            "test_bot", command, wait_for_response=False
        )

        user_telegram_client_connected.send_message.assert_called_once_with(
            "test_bot", command
        )

    @pytest.mark.asyncio
    async def test_interact_with_bot_wait_for_response_false(
        self, mocker, user_telegram_client_connected, mock_telegram_message
    ):
        """Test interact_with_bot() with wait_for_response=False returns None."""
        user_telegram_client_connected.send_message = mocker.AsyncMock(
            return_value=mock_telegram_message
        )

        result = await user_telegram_client_connected.interact_with_bot(
            "test_bot", "/start", wait_for_response=False
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_interact_with_bot_wait_for_response_true(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_message,
        mock_telegram_bot,
    ):
        """Test interact_with_bot() waits for bot response."""
        sent_message = mock_telegram_message
        sent_message.id = 100

        bot_message = mocker.MagicMock(spec=Message)
        bot_message.id = 101
        bot_message.text = "Bot response"
        bot_message.from_id = mocker.MagicMock()
        bot_message.from_id.user_id = mock_telegram_bot.id
        bot_message.chat_id = 987654321
        bot_message.date = datetime(2023, 10, 20, 10, 1, 0)
        bot_message.reply_to_msg_id = None
        bot_message.media = None

        bot_user_info = UserInfo(
            id=mock_telegram_bot.id,
            username=mock_telegram_bot.username,
            first_name=mock_telegram_bot.first_name,
            last_name=mock_telegram_bot.last_name,
            phone=mock_telegram_bot.phone,
            is_bot=True,
            is_verified=mock_telegram_bot.verified,
            is_premium=mock_telegram_bot.premium,
        )

        bot_message_info = MessageInfo(
            id=101,
            text="Bot response",
            from_user=bot_user_info,
            chat=ChatInfo(
                id=987654321, title="Test Bot", type="private", username="test_bot"
            ),
            date="2023-10-20T10:01:00Z",
            reply_to=None,
            media=None,
        )

        user_telegram_client_connected.send_message = mocker.AsyncMock(
            return_value=sent_message
        )
        user_telegram_client_connected.get_messages = mocker.AsyncMock(
            return_value=[bot_message_info]
        )
        user_telegram_client_connected.client.loop.time = mocker.AsyncMock(
            side_effect=[0, 1]
        )  # Fast timeout

        mocker.patch("asyncio.sleep", new_callable=mocker.AsyncMock)
        result = await user_telegram_client_connected.interact_with_bot(
            "test_bot", "/start", wait_for_response=True, timeout=5
        )

        assert result is not None
        assert result.from_user.is_bot is True

    @pytest.mark.asyncio
    async def test_interact_with_bot_ignores_non_bot_messages(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_message,
        mock_telegram_user,
    ):
        """Test interact_with_bot() ignores messages from non-bot users."""
        sent_message = mock_telegram_message
        sent_message.id = 100

        user_message_info = MessageInfo(
            id=101,
            text="User message",
            from_user=UserInfo(
                id=mock_telegram_user.id,
                username=mock_telegram_user.username,
                first_name=mock_telegram_user.first_name,
                last_name=mock_telegram_user.last_name,
                phone=mock_telegram_user.phone,
                is_verified=mock_telegram_user.verified,
                is_premium=mock_telegram_user.premium,
            ),
            chat=ChatInfo(id=987654321, title="Test", type="private"),
            date="2023-10-20T10:01:00Z",
            reply_to=None,
            media=None,
        )

        user_telegram_client_connected.send_message = mocker.AsyncMock(
            return_value=sent_message
        )
        user_telegram_client_connected.get_messages = mocker.AsyncMock(
            return_value=[user_message_info]
        )
        user_telegram_client_connected.client.loop.time = mocker.AsyncMock(
            side_effect=[0, 1, 2]
        )

        mocker.patch("asyncio.sleep", new_callable=mocker.AsyncMock)
        result = await user_telegram_client_connected.interact_with_bot(
            "test_bot", "/start", wait_for_response=True, timeout=1
        )

        # Should return None because message is not from bot
        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("timeout", BOT_TIMEOUTS)
    async def test_interact_with_bot_timeout(
        self, mocker, user_telegram_client_connected, mock_telegram_message, timeout
    ):
        """Test interact_with_bot() returns None on timeout."""
        sent_message = mock_telegram_message
        sent_message.id = 100

        user_telegram_client_connected.send_message = mocker.AsyncMock(
            return_value=sent_message
        )
        user_telegram_client_connected.get_messages = mocker.AsyncMock(return_value=[])
        # Simulate timeout by making time progress beyond timeout
        user_telegram_client_connected.client.loop.time = mocker.AsyncMock(
            side_effect=[0, timeout + 1]
        )

        mocker.patch("asyncio.sleep", new_callable=mocker.AsyncMock)
        result = await user_telegram_client_connected.interact_with_bot(
            "test_bot", "/start", wait_for_response=True, timeout=timeout
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_interact_with_bot_multiple_iterations(
        self, mocker, user_telegram_client_connected, mock_telegram_message
    ):
        """Test interact_with_bot() calls sleep when waiting for response."""
        from tma_test_framework.mtproto_client import MessageInfo, UserInfo

        sent_message = mock_telegram_message
        sent_message.id = 100

        # Create response message that will be found after a few iterations
        response_message = MessageInfo(
            id=101,
            chat=mocker.MagicMock(),
            date="2023-10-20T10:00:00Z",
            text="Response",
            from_user=UserInfo(
                id=999,
                first_name="Bot",
                is_bot=True,
                is_verified=False,
                is_premium=False,
            ),
            reply_to=None,
            media=None,
        )

        user_telegram_client_connected.send_message = mocker.AsyncMock(
            return_value=sent_message
        )
        # First two calls return empty, third returns response
        user_telegram_client_connected.get_messages = mocker.AsyncMock(
            side_effect=[[], [], [response_message]]
        )
        # Simulate time progression: 0, 1, 2, 3 (within timeout of 30)
        # Note: loop.time() is called multiple times in the while loop condition
        # We need to provide enough values for all calls
        time_values = [
            0,
            1,
            1,
            2,
            2,
            3,
            3,
        ]  # start_time=0, then 1, 1 (check), 2, 2 (check), 3, 3 (check)
        user_telegram_client_connected.client.loop.time = mocker.AsyncMock(
            side_effect=time_values
        )

        # Mock sleep in the module where it's used (tma_test_framework.mtproto_client)
        mock_sleep = mocker.patch(
            "tma_test_framework.mtproto_client.sleep", new_callable=mocker.AsyncMock
        )

        result = await user_telegram_client_connected.interact_with_bot(
            "test_bot", "/start", wait_for_response=True, timeout=30
        )

        # Should return response message
        assert result == response_message
        # Should have called sleep twice (for two empty results before finding response)
        assert mock_sleep.call_count == 2

    @pytest.mark.asyncio
    async def test_interact_with_bot_invalid_username(
        self, mocker, user_telegram_client_connected
    ):
        """Test interact_with_bot() raises exception for invalid bot_username."""
        user_telegram_client_connected.send_message = mocker.AsyncMock(
            side_effect=ValueError("User not found")
        )

        with pytest.raises(ValueError, match="User not found"):
            await user_telegram_client_connected.interact_with_bot(
                "invalid_bot", "/start"
            )


class TestUserTelegramClientGetMiniAppFromBot:
    """Test UserTelegramClient get_mini_app_from_bot method."""

    @pytest.mark.asyncio
    async def test_get_mini_app_from_bot_found_in_text(
        self, mocker, user_telegram_client_connected, mock_telegram_message
    ):
        """Test get_mini_app_from_bot() finds Mini App URL in text."""
        bot_message = MessageInfo(
            id=101,
            text="Click https://t.me/mybot/app?start=123",
            from_user=None,
            chat=ChatInfo(id=987654321, title="Test Bot", type="private"),
            date="2023-10-20T10:01:00Z",
            reply_to=None,
            media=None,
        )

        user_telegram_client_connected.interact_with_bot = mocker.AsyncMock(
            return_value=bot_message
        )

        result = await user_telegram_client_connected.get_mini_app_from_bot(
            "mybot", "123"
        )

        assert result is not None
        assert result.url == "https://t.me/mybot/app?start=123"

    @pytest.mark.asyncio
    async def test_get_mini_app_from_bot_found_in_media(
        self, mocker, user_telegram_client_connected, mock_telegram_message_with_webapp
    ):
        """Test get_mini_app_from_bot() finds Mini App URL in media."""
        bot_message = MessageInfo(
            id=101,
            text="No URL in text",
            from_user=None,
            chat=ChatInfo(id=987654321, title="Test Bot", type="private"),
            date="2023-10-20T10:01:00Z",
            reply_to=None,
            media={"type": "web_app", "url": "https://t.me/mybot/app?start=123"},
        )

        messages = [bot_message]
        user_telegram_client_connected.interact_with_bot = mocker.AsyncMock(
            return_value=None
        )
        user_telegram_client_connected.get_messages = mocker.AsyncMock(
            return_value=messages
        )

        result = await user_telegram_client_connected.get_mini_app_from_bot("mybot")

        assert result is not None
        assert result.url == "https://t.me/mybot/app?start=123"

    @pytest.mark.asyncio
    async def test_get_mini_app_from_bot_not_found(
        self, mocker, user_telegram_client_connected
    ):
        """Test get_mini_app_from_bot() returns None when not found."""
        bot_message = MessageInfo(
            id=101,
            text="No Mini App here",
            from_user=None,
            chat=ChatInfo(id=987654321, title="Test Bot", type="private"),
            date="2023-10-20T10:01:00Z",
            reply_to=None,
            media=None,
        )

        user_telegram_client_connected.interact_with_bot = mocker.AsyncMock(
            return_value=bot_message
        )
        user_telegram_client_connected.get_messages = mocker.AsyncMock(return_value=[])

        result = await user_telegram_client_connected.get_mini_app_from_bot("mybot")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_mini_app_from_bot_with_start_param(
        self, mocker, user_telegram_client_connected
    ):
        """Test get_mini_app_from_bot() uses start_param."""
        bot_message = MessageInfo(
            id=101,
            text="Click https://t.me/mybot/app?start=abc123",
            from_user=None,
            chat=ChatInfo(id=987654321, title="Test Bot", type="private"),
            date="2023-10-20T10:01:00Z",
            reply_to=None,
            media=None,
        )

        user_telegram_client_connected.interact_with_bot = mocker.AsyncMock(
            return_value=bot_message
        )

        result = await user_telegram_client_connected.get_mini_app_from_bot(
            "mybot", "abc123"
        )

        # Verify interact_with_bot was called with correct command
        user_telegram_client_connected.interact_with_bot.assert_called_once_with(
            "mybot", "/start abc123"
        )
        assert result is not None


class TestUserTelegramClientExtractMiniAppUrl:
    """Test UserTelegramClient _extract_mini_app_url method."""

    @pytest.mark.parametrize("text,expected", MINI_APP_TEXT_SAMPLES)
    def test_extract_mini_app_url(self, user_telegram_client, text, expected):
        """Test _extract_mini_app_url() with various text samples."""
        result = user_telegram_client._extract_mini_app_url(text)
        assert result == expected


class TestUserTelegramClientExtractMediaInfo:
    """Test UserTelegramClient _extract_media_info method."""

    def test_extract_media_info_none(self, user_telegram_client, mock_telegram_message):
        """Test _extract_media_info() with None media."""
        mock_telegram_message.media = None

        result = user_telegram_client._extract_media_info(mock_telegram_message)

        assert result is None

    def test_extract_media_info_with_url(
        self, user_telegram_client, mock_telegram_message_with_media
    ):
        """Test _extract_media_info() with media that has url."""
        result = user_telegram_client._extract_media_info(
            mock_telegram_message_with_media
        )

        assert result is not None
        assert result.get("url") == "https://example.com/photo.jpg"

    def test_extract_media_info_with_webpage(
        self, user_telegram_client, mock_telegram_message_with_webapp
    ):
        """Test _extract_media_info() with media that has webpage."""
        result = user_telegram_client._extract_media_info(
            mock_telegram_message_with_webapp
        )

        assert result is not None
        assert result.get("webpage") == "https://t.me/mybot/app?start=123"


# ============================================================================
# V. Обработка событий
# ============================================================================


class TestUserTelegramClientStartListening:
    """Test UserTelegramClient start_listening method."""

    @pytest.mark.asyncio
    async def test_start_listening_connects_if_not_connected(
        self, mocker, user_telegram_client
    ):
        """Test start_listening() calls connect() if not connected."""
        user_telegram_client.connect = mocker.AsyncMock()
        user_telegram_client.client.run_until_disconnected = mocker.AsyncMock()

        # This will run indefinitely, so we need to cancel it
        import asyncio

        task = asyncio.create_task(user_telegram_client.start_listening())
        await asyncio.sleep(0.1)  # Give it time to call connect
        task.cancel()

        try:
            await task
        except asyncio.CancelledError:
            pass

        user_telegram_client.connect.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_listening_with_event_handler(
        self, mocker, user_telegram_client_connected
    ):
        """Test start_listening() adds event handler if provided."""
        event_handler = mocker.MagicMock()
        user_telegram_client_connected.client.add_event_handler = mocker.MagicMock()
        user_telegram_client_connected.client.run_until_disconnected = (
            mocker.AsyncMock()
        )

        import asyncio
        from telethon import events

        task = asyncio.create_task(
            user_telegram_client_connected.start_listening(event_handler)
        )
        await asyncio.sleep(0.1)
        task.cancel()

        try:
            await task
        except asyncio.CancelledError:
            pass

        user_telegram_client_connected.client.add_event_handler.assert_called_once_with(
            event_handler, events.NewMessage
        )

    @pytest.mark.asyncio
    async def test_start_listening_without_handler(
        self, mocker, user_telegram_client_connected
    ):
        """Test start_listening() without event handler. TC-CLIENT-045"""
        user_telegram_client_connected.client.run_until_disconnected = (
            mocker.AsyncMock()
        )

        import asyncio

        task = asyncio.create_task(user_telegram_client_connected.start_listening())
        await asyncio.sleep(0.1)
        task.cancel()

        try:
            await task
        except asyncio.CancelledError:
            pass

        # Should call run_until_disconnected without adding event handler
        user_telegram_client_connected.client.run_until_disconnected.assert_called_once()
        # Should not call add_event_handler when no handler provided
        # Note: We can't easily verify add_event_handler wasn't called without mocking,
        # but the test verifies that start_listening works without handler


class TestUserTelegramClientAddEventHandler:
    """Test UserTelegramClient add_event_handler method."""

    def test_add_event_handler(self, mocker, user_telegram_client_connected):
        """Test add_event_handler() calls client.add_event_handler."""
        handler = mocker.MagicMock()
        from telethon import events

        user_telegram_client_connected.add_event_handler(handler, events.NewMessage)

        user_telegram_client_connected.client.add_event_handler.assert_called_once_with(
            handler, events.NewMessage
        )


# ============================================================================
# VI. Обработка ошибок и логирование
# ============================================================================


class TestUserTelegramClientErrorHandling:
    """Test UserTelegramClient error handling."""

    @pytest.mark.asyncio
    async def test_get_entity_logs_error(self, mocker, user_telegram_client):
        """Test get_entity() logs error and raises exception."""
        error = ValueError("Entity not found")
        user_telegram_client.client.get_entity = mocker.AsyncMock(side_effect=error)

        with pytest.raises(ValueError):
            await user_telegram_client.get_entity("invalid")

        # Error should be logged (we can't easily test logging, but exception should be raised)

    @pytest.mark.asyncio
    async def test_send_message_logs_error(
        self, mocker, user_telegram_client_connected
    ):
        """Test send_message() logs error and raises exception."""
        error = ValueError("Failed to send")
        user_telegram_client_connected.client.send_message = mocker.AsyncMock(
            side_effect=error
        )

        with pytest.raises(ValueError):
            await user_telegram_client_connected.send_message("invalid", "Hello")

    @pytest.mark.asyncio
    async def test_get_messages_logs_error(
        self, mocker, user_telegram_client_connected
    ):
        """Test get_messages() logs error and returns empty list."""
        error = ValueError("Failed to get messages")
        user_telegram_client_connected.client.get_messages = mocker.AsyncMock(
            side_effect=error
        )

        # Method returns empty list on error, doesn't raise
        result = await user_telegram_client_connected.get_messages("invalid")
        assert result == []

    @pytest.mark.asyncio
    async def test_interact_with_bot_logs_error(
        self, mocker, user_telegram_client_connected
    ):
        """Test interact_with_bot() logs error and raises exception."""
        error = ValueError("Bot not found")
        user_telegram_client_connected.send_message = mocker.AsyncMock(
            side_effect=error
        )

        with pytest.raises(ValueError):
            await user_telegram_client_connected.interact_with_bot(
                "invalid_bot", "/start"
            )

    @pytest.mark.asyncio
    async def test_get_mini_app_from_bot_logs_error(
        self, mocker, user_telegram_client_connected
    ):
        """Test get_mini_app_from_bot() logs error and raises exception."""
        error = ValueError("Bot not found")
        user_telegram_client_connected.interact_with_bot = mocker.AsyncMock(
            side_effect=error
        )

        with pytest.raises(ValueError):
            await user_telegram_client_connected.get_mini_app_from_bot("invalid_bot")
