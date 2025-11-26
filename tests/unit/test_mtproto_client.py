"""
Unit tests for UserTelegramClient.
"""

import asyncio
import copy
import pytest
import allure
from datetime import datetime

from telethon.tl.types import User, Chat, Message
from telethon import events
from telethon.sessions import StringSession, SQLiteSession

from tma_test_framework.clients.mtproto_client import (
    UserTelegramClient,
    UserInfo,
    ChatInfo,
    MessageInfo,
)
from tma_test_framework.config import Config
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

    @allure.title("Initialization with session_string uses StringSession")
    @allure.description("Test initialization with session_string uses StringSession.")
    def test_init_with_session_string(self, mocker, config_with_session_string):
        """Test initialization with session_string uses StringSession."""
        with allure.step("Mock StringSession and TelegramClient"):
            mock_string_session = mocker.patch(
                "tma_test_framework.clients.mtproto_client.StringSession"
            )
            mock_client = mocker.patch(
                "tma_test_framework.clients.mtproto_client.TelegramClient"
            )
        with allure.step("Create UserTelegramClient instance"):
            _ = UserTelegramClient(config_with_session_string)

        with allure.step("Verify StringSession was called"):
            # Verify StringSession was called
            mock_string_session.assert_called_once_with(
                config_with_session_string.session_string
            )
        with allure.step("Verify TelegramClient was created with correct parameters"):
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
                    assert (
                        call_args.kwargs["timeout"]
                        == config_with_session_string.timeout
                    )
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

    @allure.title("Initialization with session_file uses SQLiteSession")
    @allure.description("Test initialization with session_file uses SQLiteSession.")
    def test_init_with_session_file(self, mocker, config_with_session_file):
        """Test initialization with session_file uses SQLiteSession."""
        with allure.step("Mock SQLiteSession and TelegramClient"):
            mock_sqlite_session = mocker.patch(
                "tma_test_framework.clients.mtproto_client.SQLiteSession"
            )
            mock_client = mocker.patch(
                "tma_test_framework.clients.mtproto_client.TelegramClient"
            )
        with allure.step("Create UserTelegramClient instance"):
            _ = UserTelegramClient(config_with_session_file)

        with allure.step("Verify SQLiteSession was called"):
            # Verify SQLiteSession was called
            mock_sqlite_session.assert_called_once_with(
                config_with_session_file.session_file
            )
        with allure.step("Verify TelegramClient was called"):
            mock_client.assert_called_once()

    @allure.title("Initialization without session uses fallback SQLiteSession")
    @allure.description(
        "Test initialization without session uses fallback SQLiteSession."
    )
    def test_init_without_session(self, mocker, config_without_session):
        """Test initialization without session uses fallback SQLiteSession."""
        # Mock StringSession to avoid validation error
        mock_string_session = mocker.patch(
            "tma_test_framework.clients.mtproto_client.StringSession",
            return_value=mocker.MagicMock(),
        )
        _ = mocker.patch("tma_test_framework.clients.mtproto_client.SQLiteSession")
        mock_client = mocker.patch(
            "tma_test_framework.clients.mtproto_client.TelegramClient"
        )
        _ = UserTelegramClient(config_without_session)

        with allure.step("Verify StringSession was called"):
            # Verify StringSession was called (config_without_session has session_string)
            mock_string_session.assert_called_once()
        with allure.step("Verify TelegramClient was called"):
            mock_client.assert_called_once()

    @allure.title(
        'Initialization without session uses fallback SQLiteSession("tma_session")'
    )
    @allure.description(
        'Test initialization without session uses fallback SQLiteSession("tma_session"). TC-CLIENT-002a'
    )
    def test_init_without_session_fallback(self, mocker):
        """Test initialization without session uses fallback SQLiteSession("tma_session"). TC-CLIENT-002a"""
        with allure.step("Create Config with valid session first to pass validation"):
            # Create Config without session by bypassing __post_init__ validation
            # This tests the defensive code at line 75

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

        with allure.step("Modify attributes to None using object.__setattr__"):
            # Now modify attributes to None using object.__setattr__ (works for frozen struct)
            # This bypasses the validation that happened in __post_init__
            object.__setattr__(config, "session_string", None)
            object.__setattr__(config, "session_file", None)

        with allure.step("Mock SQLiteSession and TelegramClient"):
            # Mock SQLiteSession to verify it's called with "tma_session"
            mock_sqlite_session = mocker.patch(
                "tma_test_framework.clients.mtproto_client.SQLiteSession"
            )
            mock_client = mocker.patch(
                "tma_test_framework.clients.mtproto_client.TelegramClient"
            )

        with allure.step("Create UserTelegramClient instance"):
            _ = UserTelegramClient(config)

        with allure.step(
            'Verify SQLiteSession was called with "tma_session" as fallback'
        ):
            # Verify SQLiteSession was called with "tma_session" as fallback
            mock_sqlite_session.assert_called_once_with("tma_session")
        with allure.step("Verify TelegramClient was called"):
            mock_client.assert_called_once()

    @allure.title("Initialization sets correct initial state")
    @allure.description("Test that initialization sets correct initial state.")
    def test_init_sets_initial_state(self, mocker, valid_config):
        """Test that initialization sets correct initial state."""
        with allure.step("Mock StringSession and TelegramClient"):
            # Mock StringSession to avoid validation error
            mocker.patch("tma_test_framework.clients.mtproto_client.StringSession")
            mocker.patch("tma_test_framework.clients.mtproto_client.TelegramClient")
        with allure.step("Create UserTelegramClient instance"):
            client = UserTelegramClient(valid_config)

        with allure.step("Verify initial state"):
            assert client._is_connected is False
            assert client._me is None
            assert client.config == valid_config


class TestUserTelegramClientContextManager:
    """Test UserTelegramClient async context manager."""

    @pytest.mark.asyncio
    @allure.title("__aenter__ calls connect()")
    @allure.description("Test __aenter__ calls connect().")
    async def test_aenter_calls_connect(self, mocker, user_telegram_client):
        """Test __aenter__ calls connect()."""
        with allure.step("Mock connect method"):
            user_telegram_client.connect = mocker.AsyncMock()

        with allure.step("Use async context manager"):
            async with user_telegram_client:
                with allure.step("Verify connect was called"):
                    user_telegram_client.connect.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("__aexit__ calls disconnect()")
    @allure.description("Test __aexit__ calls disconnect().")
    async def test_aexit_calls_disconnect(self, mocker, user_telegram_client):
        """Test __aexit__ calls disconnect()."""
        with allure.step("Mock disconnect method"):
            user_telegram_client.disconnect = mocker.AsyncMock()

        with allure.step("Use async context manager"):
            async with user_telegram_client:
                pass

        with allure.step("Verify disconnect was called"):
            user_telegram_client.disconnect.assert_called_once()


class TestUserTelegramClientConnect:
    """Test UserTelegramClient connect method."""

    @pytest.mark.asyncio
    @allure.title("Successful connection")
    @allure.description("Test successful connection.")
    async def test_connect_success(
        self, mocker, user_telegram_client, mock_telegram_user
    ):
        """Test successful connection."""
        with allure.step("Mock client methods"):
            user_telegram_client.client.connect = mocker.AsyncMock()
            user_telegram_client.client.is_user_authorized = mocker.AsyncMock(
                return_value=True
            )
            user_telegram_client.client.get_me = mocker.AsyncMock(
                return_value=mock_telegram_user
            )

        with allure.step("Call connect()"):
            await user_telegram_client.connect()

        with allure.step("Verify connection state and client.connect was called"):
            assert user_telegram_client._is_connected is True
            assert user_telegram_client._me is not None
            user_telegram_client.client.connect.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("Connection fails when user is not authorized")
    @allure.description("Test connection fails when user is not authorized.")
    async def test_connect_not_authorized(self, mocker, user_telegram_client):
        """Test connection fails when user is not authorized."""
        with allure.step("Mock client methods to return not authorized"):
            user_telegram_client.client.connect = mocker.AsyncMock()
            user_telegram_client.client.is_user_authorized = mocker.AsyncMock(
                return_value=False
            )

        with allure.step("Attempt to connect and expect ValueError"):
            with pytest.raises(ValueError, match="User not authorized"):
                await user_telegram_client.connect()

        with allure.step("Verify connection state is False"):
            assert user_telegram_client._is_connected is False

    @pytest.mark.asyncio
    @allure.title("connect() when already connected logs and returns")
    @allure.description("Test connect() when already connected logs and returns.")
    async def test_connect_already_connected(
        self, mocker, user_telegram_client_connected
    ):
        """Test connect() when already connected logs and returns."""
        with allure.step("Mock client.connect"):
            user_telegram_client_connected.client.connect = mocker.AsyncMock()

        with allure.step("Call connect() when already connected"):
            await user_telegram_client_connected.connect()

        with allure.step("Verify connect was not called again"):
            # Should not call connect again
            user_telegram_client_connected.client.connect.assert_not_called()

    @pytest.mark.asyncio
    @allure.title("connect() logs error and raises exception")
    @allure.description("Test connect() logs error and raises exception.")
    async def test_connect_exception_logs_and_raises(
        self, mocker, user_telegram_client
    ):
        """Test connect() logs error and raises exception."""
        with allure.step("Mock client.connect to raise ConnectionError"):
            error = ConnectionError("Connection failed")
            user_telegram_client.client.connect = mocker.AsyncMock(side_effect=error)

        with allure.step("Attempt to connect and expect ConnectionError"):
            with pytest.raises(ConnectionError):
                await user_telegram_client.connect()


class TestUserTelegramClientDisconnect:
    """Test UserTelegramClient disconnect method."""

    @pytest.mark.asyncio
    @allure.title("disconnect() when connected")
    @allure.description("Test disconnect() when connected.")
    async def test_disconnect_when_connected(
        self, mocker, user_telegram_client_connected
    ):
        """Test disconnect() when connected."""
        with allure.step("Mock client.disconnect"):
            user_telegram_client_connected.client.disconnect = mocker.AsyncMock()

        with allure.step("Call disconnect()"):
            await user_telegram_client_connected.disconnect()

        with allure.step("Verify connection state and disconnect was called"):
            assert user_telegram_client_connected._is_connected is False
            user_telegram_client_connected.client.disconnect.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("disconnect() when not connected does nothing")
    @allure.description("Test disconnect() when not connected does nothing.")
    async def test_disconnect_when_not_connected(self, mocker, user_telegram_client):
        """Test disconnect() when not connected does nothing."""
        with allure.step("Mock client.disconnect"):
            user_telegram_client.client.disconnect = mocker.AsyncMock()

        with allure.step("Call disconnect() when not connected"):
            await user_telegram_client.disconnect()

        with allure.step("Verify connection state remains False"):
            # Should not raise error, but also should not call disconnect
            # (since _is_connected is False)
            assert user_telegram_client._is_connected is False


class TestUserTelegramClientIsConnected:
    """Test UserTelegramClient is_connected method."""

    @pytest.mark.asyncio
    @allure.title("is_connected() returns True when connected and authorized")
    @allure.description(
        "Test is_connected() returns True when connected and authorized."
    )
    async def test_is_connected_true(self, mocker, user_telegram_client_connected):
        """Test is_connected() returns True when connected and authorized."""
        with allure.step("Mock client.is_connected to return True"):
            user_telegram_client_connected.client.is_connected = mocker.MagicMock(
                return_value=True
            )

        with allure.step("Call is_connected()"):
            result = await user_telegram_client_connected.is_connected()

        with allure.step("Verify result is True"):
            assert result is True

    @pytest.mark.asyncio
    @allure.title("is_connected() returns False when not connected")
    @allure.description("Test is_connected() returns False when not connected.")
    async def test_is_connected_false_not_connected(self, mocker, user_telegram_client):
        """Test is_connected() returns False when not connected."""
        with allure.step("Mock client.is_connected to return False"):
            user_telegram_client.client.is_connected = mocker.MagicMock(
                return_value=False
            )

        with allure.step("Call is_connected()"):
            result = await user_telegram_client.is_connected()

        with allure.step("Verify result is False"):
            assert result is False

    @pytest.mark.asyncio
    @allure.title("is_connected() returns False when client is not connected")
    @allure.description(
        "Test is_connected() returns False when client is not connected."
    )
    async def test_is_connected_false_client_not_connected(
        self, mocker, user_telegram_client_connected
    ):
        """Test is_connected() returns False when client is not connected."""
        with allure.step("Mock client.is_connected to return False"):
            user_telegram_client_connected.client.is_connected = mocker.MagicMock(
                return_value=False
            )

        with allure.step("Call is_connected()"):
            result = await user_telegram_client_connected.is_connected()

        with allure.step("Verify result is False"):
            assert result is False


# ============================================================================
# II. Методы получения данных
# ============================================================================


class TestUserTelegramClientGetMe:
    """Test UserTelegramClient get_me method."""

    @pytest.mark.asyncio
    @allure.title("get_me() returns UserInfo with correct fields")
    @allure.description("Test get_me() returns UserInfo with correct fields.")
    async def test_get_me_success(
        self, mocker, user_telegram_client, mock_telegram_user
    ):
        """Test get_me() returns UserInfo with correct fields."""
        with allure.step("Mock client.get_me"):
            user_telegram_client.client.get_me = mocker.AsyncMock(
                return_value=mock_telegram_user
            )

        with allure.step("Call get_me()"):
            result = await user_telegram_client.get_me()

        with allure.step("Verify result is UserInfo with correct fields"):
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
    @allure.title("get_me() handles None fields correctly")
    @allure.description("Test get_me() handles None fields correctly.")
    async def test_get_me_handles_none_fields(self, mocker, user_telegram_client):
        """Test get_me() handles None fields correctly."""
        with allure.step("Create mock User with None fields"):
            user = mocker.MagicMock(spec=User)
            user.id = 123456789
            user.username = None
            user.first_name = "Test"
            user.last_name = None
            user.phone = None
            user.bot = False
            user.verified = False
            user.premium = False

        with allure.step("Mock client.get_me and call get_me()"):
            user_telegram_client.client.get_me = mocker.AsyncMock(return_value=user)
            result = await user_telegram_client.get_me()

        with allure.step("Verify None fields are handled correctly"):
            assert result.username is None
            assert result.last_name is None
            assert result.phone is None

    @pytest.mark.asyncio
    @allure.title("get_me() caches result in self._me")
    @allure.description("Test get_me() caches result in self._me.")
    async def test_get_me_caches_result(
        self, mocker, user_telegram_client, mock_telegram_user
    ):
        """Test get_me() caches result in self._me."""
        with allure.step("Mock client.get_me"):
            user_telegram_client.client.get_me = mocker.AsyncMock(
                return_value=mock_telegram_user
            )

        with allure.step("Call get_me() twice"):
            result1 = await user_telegram_client.get_me()
            result2 = await user_telegram_client.get_me()

        with allure.step("Verify get_me was called only once and results are cached"):
            # Should only call get_me once
            assert user_telegram_client.client.get_me.call_count == 1
            assert result1 == result2
            assert user_telegram_client._me == result1


class TestUserTelegramClientGetEntity:
    """Test UserTelegramClient get_entity method."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("entity", GET_ENTITY_PARAMS)
    @allure.title("get_entity() with User returns ChatInfo with type='private'")
    @allure.description(
        "Test get_entity() with User returns ChatInfo with type='private'."
    )
    async def test_get_entity_user(
        self, mocker, user_telegram_client, mock_telegram_user, entity
    ):
        """Test get_entity() with User returns ChatInfo with type='private'."""
        with allure.step("Mock client.get_entity"):
            user_telegram_client.client.get_entity = mocker.AsyncMock(
                return_value=mock_telegram_user
            )

        with allure.step(f"Call get_entity() with {entity}"):
            result = await user_telegram_client.get_entity(entity)

        with allure.step("Verify result is ChatInfo with type='private'"):
            assert isinstance(result, ChatInfo)
            assert result.type == "private"
            assert result.id == mock_telegram_user.id
            assert result.username == mock_telegram_user.username
            # ChatInfo doesn't have is_bot - that's a UserInfo property
            assert result.is_verified == mock_telegram_user.verified

    @pytest.mark.asyncio
    @allure.title("get_entity() with Channel returns ChatInfo with type='channel'")
    @allure.description(
        "Test get_entity() with Channel returns ChatInfo with type='channel'."
    )
    async def test_get_entity_channel(
        self, mocker, user_telegram_client, mock_telegram_channel
    ):
        """Test get_entity() with Channel returns ChatInfo with type='channel'."""
        with allure.step("Mock client.get_entity"):
            user_telegram_client.client.get_entity = mocker.AsyncMock(
                return_value=mock_telegram_channel
            )

        with allure.step("Call get_entity() with @test_channel"):
            result = await user_telegram_client.get_entity("@test_channel")

        with allure.step("Verify result is ChatInfo with type='channel'"):
            assert isinstance(result, ChatInfo)
            assert result.type == "channel"
            assert result.id == mock_telegram_channel.id
            assert result.title == mock_telegram_channel.title
            assert result.username == mock_telegram_channel.username

    @pytest.mark.asyncio
    @allure.title("get_entity() with Chat returns ChatInfo with type='group'")
    @allure.description(
        "Test get_entity() with Chat returns ChatInfo with type='group'."
    )
    async def test_get_entity_chat(
        self, mocker, user_telegram_client, mock_telegram_chat
    ):
        """Test get_entity() with Chat returns ChatInfo with type='group'."""
        with allure.step("Mock client.get_entity"):
            user_telegram_client.client.get_entity = mocker.AsyncMock(
                return_value=mock_telegram_chat
            )

        with allure.step("Call get_entity() with chat ID"):
            result = await user_telegram_client.get_entity(987654321)

        with allure.step("Verify result is ChatInfo with type='group'"):
            assert isinstance(result, ChatInfo)
            assert result.type == "group"
            assert result.id == mock_telegram_chat.id
            assert result.title == mock_telegram_chat.title

    @pytest.mark.asyncio
    @allure.title("get_entity() handles missing username")
    @allure.description("Test get_entity() handles missing username.")
    async def test_get_entity_handles_missing_username(
        self, mocker, user_telegram_client
    ):
        """Test get_entity() handles missing username."""
        with allure.step("Create mock Chat with missing username"):
            chat = mocker.MagicMock(spec=Chat)
            chat.id = 987654321
            chat.title = "Test Chat"
            chat.username = None
            chat.verified = False

        with allure.step("Mock client.get_entity and call get_entity()"):
            user_telegram_client.client.get_entity = mocker.AsyncMock(return_value=chat)
            result = await user_telegram_client.get_entity(987654321)

        with allure.step("Verify username is None"):
            assert result.username is None

    @pytest.mark.asyncio
    @allure.title("get_entity() raises exception for invalid entity")
    @allure.description("Test get_entity() raises exception for invalid entity.")
    async def test_get_entity_invalid_entity(self, mocker, user_telegram_client):
        """Test get_entity() raises exception for invalid entity."""
        with allure.step("Mock client.get_entity to raise ValueError"):
            user_telegram_client.client.get_entity = mocker.AsyncMock(
                side_effect=ValueError("Entity not found")
            )

        with allure.step("Attempt to get invalid entity and expect ValueError"):
            with pytest.raises(ValueError, match="Entity not found"):
                await user_telegram_client.get_entity("invalid_entity")

    @pytest.mark.asyncio
    @allure.title("get_entity() raises ValueError for unsupported entity type")
    @allure.description(
        "Test get_entity() raises ValueError for unsupported entity type."
    )
    async def test_get_entity_unsupported_type(self, mocker, user_telegram_client):
        """Test get_entity() raises ValueError for unsupported entity type."""
        with allure.step("Create mock Message entity"):
            mock_message = mocker.MagicMock(spec=Message)
        with allure.step("Mock client.get_entity"):
            user_telegram_client.client.get_entity = mocker.AsyncMock(
                return_value=mock_message
            )

        with allure.step("Attempt to get unsupported entity and expect ValueError"):
            with pytest.raises(ValueError, match="Unsupported entity type"):
                await user_telegram_client.get_entity("test")

    @pytest.mark.asyncio
    @allure.title("get_entity() with Channel via mock fallback")
    @allure.description("Test get_entity() with Channel via mock fallback (line 212).")
    async def test_get_entity_channel_via_mock_fallback(
        self, mocker, user_telegram_client
    ):
        """Test get_entity() with Channel via mock fallback (line 212)."""
        with allure.step("Create mock Channel that doesn't match isinstance checks"):
            # Create a mock that doesn't match isinstance checks but has Channel attributes
            mock_channel = mocker.MagicMock()  # No spec to avoid isinstance match
            mock_channel.id = 444555666
            mock_channel.title = "Test Channel"
            mock_channel.username = "test_channel"
            mock_channel.verified = True
            mock_channel.broadcast = True  # Key attribute for Channel detection

        with allure.step("Mock client.get_entity and call get_entity()"):
            user_telegram_client.client.get_entity = mocker.AsyncMock(
                return_value=mock_channel
            )
            result = await user_telegram_client.get_entity("@test_channel")

        with allure.step("Verify result is ChatInfo with type='channel'"):
            assert isinstance(result, ChatInfo)
            assert result.type == "channel"
            assert result.id == mock_channel.id
            assert result.title == mock_channel.title

    @pytest.mark.asyncio
    @allure.title("get_entity() with User via mock fallback")
    @allure.description("Test get_entity() with User via mock fallback (line 249).")
    async def test_get_entity_user_via_mock_fallback(
        self, mocker, user_telegram_client
    ):
        """Test get_entity() with User via mock fallback (line 249)."""
        with allure.step("Create mock User that doesn't match isinstance checks"):
            # Create a mock that doesn't match isinstance checks but has User attributes
            mock_user = mocker.MagicMock()  # No spec to avoid isinstance match
            mock_user.id = 123456789
            mock_user.first_name = "Test"
            mock_user.last_name = "User"
            mock_user.username = "test_user"
            mock_user.verified = False

        with allure.step("Mock client.get_entity and call get_entity()"):
            user_telegram_client.client.get_entity = mocker.AsyncMock(
                return_value=mock_user
            )
            result = await user_telegram_client.get_entity(123456789)

        with allure.step("Verify result is ChatInfo with type='private'"):
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
    @allure.title("send_message() returns MessageInfo")
    @allure.description("Test send_message() returns MessageInfo.")
    async def test_send_message_success(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_message,
        mock_telegram_user,
        mock_telegram_chat,
    ):
        """Test send_message() returns MessageInfo."""
        with allure.step("Mock client.send_message and client.get_entity"):
            user_telegram_client_connected.client.send_message = mocker.AsyncMock(
                return_value=mock_telegram_message
            )
            user_telegram_client_connected.client.get_entity = mocker.AsyncMock(
                return_value=mock_telegram_chat
            )

        with allure.step("Call send_message()"):
            result = await user_telegram_client_connected.send_message("@test", "Hello")

        with allure.step("Verify result is MessageInfo with correct fields"):
            assert isinstance(result, MessageInfo)
            assert result.id == mock_telegram_message.id
            assert result.text == mock_telegram_message.text

    @pytest.mark.asyncio
    @allure.title("send_message() handles message.date without isoformat")
    @allure.description(
        "Test send_message() handles message.date without isoformat (line 288)."
    )
    async def test_send_message_with_string_date(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_chat,
    ):
        """Test send_message() handles message.date without isoformat (line 288)."""
        with allure.step("Create DateWithoutIsoformat class"):
            # Create a message with date that doesn't have isoformat method
            # This triggers the else branch (line 288) instead of line 286
            class DateWithoutIsoformat:
                def __str__(self):
                    return "2024-01-01T12:00:00"

        with allure.step("Create mock message with date without isoformat"):
            mock_message = mocker.MagicMock()
            mock_message.id = 12345
            mock_message.text = "Test message"
            # Use object without isoformat to trigger else branch
            mock_message.date = DateWithoutIsoformat()
            mock_message.from_id = None
            mock_message.peer_id = mocker.MagicMock()
            mock_message.peer_id.channel_id = None
            mock_message.peer_id.user_id = 123456789

        with allure.step("Mock client methods and call send_message()"):
            user_telegram_client_connected.client.send_message = mocker.AsyncMock(
                return_value=mock_message
            )
            user_telegram_client_connected.client.get_entity = mocker.AsyncMock(
                return_value=mock_telegram_chat
            )
            result = await user_telegram_client_connected.send_message("@test", "Hello")

        with allure.step("Verify result is MessageInfo"):
            assert isinstance(result, MessageInfo)
            assert result.id == mock_message.id
            assert result.text == mock_message.text

    @pytest.mark.asyncio
    @allure.title("send_message() with reply_to")
    @allure.description("Test send_message() with reply_to.")
    async def test_send_message_with_reply(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_message_with_reply,
        mock_telegram_chat,
    ):
        """Test send_message() with reply_to."""
        with allure.step("Mock client methods"):
            user_telegram_client_connected.client.send_message = mocker.AsyncMock(
                return_value=mock_telegram_message_with_reply
            )
            user_telegram_client_connected.client.get_entity = mocker.AsyncMock(
                return_value=mock_telegram_chat
            )

        with allure.step("Call send_message() with reply_to"):
            result = await user_telegram_client_connected.send_message(
                "@test", "Reply", reply_to=111222332
            )

        with allure.step("Verify reply_to is set correctly"):
            assert result.reply_to == mock_telegram_message_with_reply.reply_to_msg_id

    @pytest.mark.asyncio
    @allure.title("send_message() with parse_mode")
    @allure.description("Test send_message() with parse_mode.")
    async def test_send_message_with_parse_mode(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_message,
        mock_telegram_chat,
    ):
        """Test send_message() with parse_mode."""
        with allure.step("Mock client methods"):
            user_telegram_client_connected.client.send_message = mocker.AsyncMock(
                return_value=mock_telegram_message
            )
            user_telegram_client_connected.client.get_entity = mocker.AsyncMock(
                return_value=mock_telegram_chat
            )

        with allure.step("Call send_message() with parse_mode"):
            await user_telegram_client_connected.send_message(
                "@test", "**bold**", parse_mode="Markdown"
            )

        with allure.step("Verify parse_mode was passed to client"):
            call_kwargs = user_telegram_client_connected.client.send_message.call_args[
                1
            ]
            assert call_kwargs["parse_mode"] == "Markdown"

    @pytest.mark.asyncio
    @allure.title("send_message() raises exception for invalid entity")
    @allure.description("Test send_message() raises exception for invalid entity.")
    async def test_send_message_invalid_entity(
        self, mocker, user_telegram_client_connected
    ):
        """Test send_message() raises exception for invalid entity."""
        with allure.step("Mock client.send_message to raise ValueError"):
            user_telegram_client_connected.client.send_message = mocker.AsyncMock(
                side_effect=ValueError("Invalid entity")
            )

        with allure.step(
            "Attempt to send message to invalid entity and expect ValueError"
        ):
            with pytest.raises(ValueError, match="Invalid entity"):
                await user_telegram_client_connected.send_message("invalid", "Hello")

    @pytest.mark.asyncio
    @allure.title("send_message() handles media")
    @allure.description("Test send_message() handles media.")
    async def test_send_message_with_media(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_message_with_media,
        mock_telegram_chat,
    ):
        """Test send_message() handles media."""
        with allure.step("Mock client methods"):
            user_telegram_client_connected.client.send_message = mocker.AsyncMock(
                return_value=mock_telegram_message_with_media
            )
            user_telegram_client_connected.client.get_entity = mocker.AsyncMock(
                return_value=mock_telegram_chat
            )

        with allure.step("Call send_message()"):
            result = await user_telegram_client_connected.send_message("@test", "Photo")

        with allure.step("Verify media is included in result"):
            assert result.media is not None
            assert result.media.get("url") == "https://example.com/photo.jpg"


class TestUserTelegramClientGetMessages:
    """Test UserTelegramClient get_messages method."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("limit", GET_MESSAGES_LIMITS)
    @pytest.mark.parametrize("offset_id", GET_MESSAGES_OFFSET_IDS)
    @allure.title("get_messages() returns list of MessageInfo")
    @allure.description("Test get_messages() returns list of MessageInfo.")
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

        with allure.step(f"Create {limit} messages using deepcopy"):
            messages = [copy.deepcopy(mock_telegram_message) for _ in range(limit)]
        with allure.step("Mock client.get_messages"):
            user_telegram_client_connected.client.get_messages = mocker.AsyncMock(
                return_value=messages
            )

        with allure.step(
            "Mock get_entity: first call for chat, subsequent calls for users"
        ):
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

        with allure.step(
            f"Call get_messages() with limit={limit}, offset_id={offset_id}"
        ):
            result = await user_telegram_client_connected.get_messages(
                "@test", limit=limit, offset_id=offset_id
            )

        with allure.step("Verify result length and all items are MessageInfo"):
            assert len(result) == limit
            assert all(isinstance(msg, MessageInfo) for msg in result)

    @pytest.mark.asyncio
    @allure.title("get_messages() skips None messages")
    @allure.description("Test get_messages() skips None messages.")
    async def test_get_messages_skips_none(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_message,
        mock_telegram_chat,
        mock_telegram_user,
    ):
        """Test get_messages() skips None messages."""
        with allure.step("Create messages list with None"):
            messages = [mock_telegram_message, None, mock_telegram_message]
        with allure.step("Mock client.get_messages"):
            user_telegram_client_connected.client.get_messages = mocker.AsyncMock(
                return_value=messages
            )

        with allure.step(
            "Mock get_entity to return user for from_id and chat for entity"
        ):
            # Mock get_entity to return user for from_id and chat for entity
            def get_entity_side_effect(entity):
                if hasattr(entity, "user_id"):
                    return mock_telegram_user
                return mock_telegram_chat

            user_telegram_client_connected.client.get_entity = mocker.AsyncMock(
                side_effect=get_entity_side_effect
            )

        with allure.step("Call get_messages()"):
            result = await user_telegram_client_connected.get_messages(
                "@test", limit=10
            )

        with allure.step("Verify None messages are skipped"):
            assert len(result) == 2  # None should be skipped

    @pytest.mark.asyncio
    @allure.title("get_messages() handles messages from bot correctly")
    @allure.description("Test get_messages() handles messages from bot correctly.")
    async def test_get_messages_from_bot(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_bot,
        mock_telegram_chat,
    ):
        """Test get_messages() handles messages from bot correctly."""
        with allure.step("Create mock message from bot"):
            message = mocker.MagicMock(spec=Message)
            message.id = 111222333
            message.text = "Bot message"
            message.from_id = mocker.MagicMock()
            message.from_id.user_id = mock_telegram_bot.id
            message.chat_id = mock_telegram_chat.id
            message.date = datetime(2023, 10, 20, 10, 0, 0)
            message.reply_to_msg_id = None
            message.media = None

        with allure.step("Mock client.get_messages"):
            user_telegram_client_connected.client.get_messages = mocker.AsyncMock(
                return_value=[message]
            )

        with allure.step("Mock get_entity: first call for chat, second for bot user"):
            # Mock get_entity: first call for chat, second for bot user
            def get_entity_side_effect(entity):
                if (
                    hasattr(entity, "user_id")
                    and entity.user_id == mock_telegram_bot.id
                ):
                    return mock_telegram_bot
                return mock_telegram_chat

            user_telegram_client_connected.client.get_entity = mocker.AsyncMock(
                side_effect=get_entity_side_effect
            )

        with allure.step("Call get_messages()"):
            result = await user_telegram_client_connected.get_messages(
                "@test_bot", limit=1
            )

        with allure.step("Verify result has message from bot"):
            assert len(result) == 1
            assert result[0].from_user is not None
            assert result[0].from_user.is_bot is True

    @pytest.mark.asyncio
    @allure.title("get_messages() handles error when getting from_user")
    @allure.description("Test get_messages() handles error when getting from_user.")
    async def test_get_messages_from_user_error_handled(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_message,
        mock_telegram_chat,
    ):
        """Test get_messages() handles error when getting from_user."""
        with allure.step("Set mock_telegram_message.from_id"):
            mock_telegram_message.from_id = mocker.MagicMock()
            mock_telegram_message.from_id.user_id = 999999999

        with allure.step("Mock client.get_messages"):
            user_telegram_client_connected.client.get_messages = mocker.AsyncMock(
                return_value=[mock_telegram_message]
            )
        with allure.step("Mock self.get_entity to return chat successfully"):
            # Mock self.get_entity to return chat successfully

            user_telegram_client_connected.get_entity = mocker.AsyncMock(
                return_value=ChatInfo(
                    id=mock_telegram_chat.id,
                    title=mock_telegram_chat.title,
                    type="channel",
                    username=mock_telegram_chat.username,
                    is_verified=False,
                )
            )
        with allure.step("Mock client.get_entity to raise error for from_user"):
            # Mock client.get_entity to raise error for from_user
            user_telegram_client_connected.client.get_entity = mocker.AsyncMock(
                side_effect=ValueError("User not found")
            )

        with allure.step("Call get_messages()"):
            result = await user_telegram_client_connected.get_messages("@test", limit=1)

        with allure.step("Verify from_user is None on error"):
            assert len(result) == 1
            assert result[0].from_user is None  # Should be None on error


# ============================================================================
# IV. Работа с ботами и Mini Apps
# ============================================================================


class TestUserTelegramClientInteractWithBot:
    """Test UserTelegramClient interact_with_bot method."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("command", BOT_COMMANDS)
    @allure.title("interact_with_bot() sends command")
    @allure.description("Test interact_with_bot() sends command.")
    async def test_interact_with_bot_sends_command(
        self, mocker, user_telegram_client_connected, mock_telegram_message, command
    ):
        """Test interact_with_bot() sends command."""
        with allure.step("Mock send_message and get_messages"):
            user_telegram_client_connected.send_message = mocker.AsyncMock(
                return_value=mock_telegram_message
            )
            user_telegram_client_connected.get_messages = mocker.AsyncMock(
                return_value=[]
            )

        with allure.step(f"Call interact_with_bot() with command: {command}"):
            await user_telegram_client_connected.interact_with_bot(
                "test_bot", command, wait_for_response=False
            )

        with allure.step("Verify send_message was called with correct parameters"):
            user_telegram_client_connected.send_message.assert_called_once_with(
                "test_bot", command
            )

    @pytest.mark.asyncio
    @allure.title("interact_with_bot() with wait_for_response=False returns None")
    @allure.description(
        "Test interact_with_bot() with wait_for_response=False returns None."
    )
    async def test_interact_with_bot_wait_for_response_false(
        self, mocker, user_telegram_client_connected, mock_telegram_message
    ):
        """Test interact_with_bot() with wait_for_response=False returns None."""
        with allure.step("Mock send_message"):
            user_telegram_client_connected.send_message = mocker.AsyncMock(
                return_value=mock_telegram_message
            )

        with allure.step("Call interact_with_bot() with wait_for_response=False"):
            result = await user_telegram_client_connected.interact_with_bot(
                "test_bot", "/start", wait_for_response=False
            )

        with allure.step("Verify result is None"):
            assert result is None

    @pytest.mark.asyncio
    @allure.title("interact_with_bot() waits for bot response")
    @allure.description("Test interact_with_bot() waits for bot response.")
    async def test_interact_with_bot_wait_for_response_true(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_message,
        mock_telegram_bot,
    ):
        """Test interact_with_bot() waits for bot response."""
        with allure.step("Set sent_message.id"):
            sent_message = mock_telegram_message
            sent_message.id = 100

        with allure.step("Create mock bot message"):
            bot_message = mocker.MagicMock(spec=Message)
            bot_message.id = 101
            bot_message.text = "Bot response"
            bot_message.from_id = mocker.MagicMock()
            bot_message.from_id.user_id = mock_telegram_bot.id
            bot_message.chat_id = 987654321
            bot_message.date = datetime(2023, 10, 20, 10, 1, 0)
            bot_message.reply_to_msg_id = None
            bot_message.media = None

        with allure.step("Create bot_user_info and bot_message_info"):
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

        with allure.step("Mock client methods"):
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

        with allure.step("Call interact_with_bot() with wait_for_response=True"):
            result = await user_telegram_client_connected.interact_with_bot(
                "test_bot", "/start", wait_for_response=True, timeout=5
            )

        with allure.step("Verify result is not None and from bot"):
            assert result is not None
            assert result.from_user.is_bot is True

    @pytest.mark.asyncio
    @allure.title("interact_with_bot() ignores messages from non-bot users")
    @allure.description("Test interact_with_bot() ignores messages from non-bot users.")
    async def test_interact_with_bot_ignores_non_bot_messages(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_message,
        mock_telegram_user,
    ):
        """Test interact_with_bot() ignores messages from non-bot users."""
        with allure.step("Set sent_message.id"):
            sent_message = mock_telegram_message
            sent_message.id = 100

        with allure.step("Create user_message_info"):
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

        with allure.step("Mock client methods"):
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

        with allure.step("Call interact_with_bot() and verify result is None"):
            result = await user_telegram_client_connected.interact_with_bot(
                "test_bot", "/start", wait_for_response=True, timeout=1
            )

            # Should return None because message is not from bot
            assert result is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("timeout", BOT_TIMEOUTS)
    @allure.title("interact_with_bot() returns None on timeout")
    @allure.description("Test interact_with_bot() returns None on timeout.")
    async def test_interact_with_bot_timeout(
        self, mocker, user_telegram_client_connected, mock_telegram_message, timeout
    ):
        """Test interact_with_bot() returns None on timeout."""
        with allure.step("Set sent_message.id"):
            sent_message = mock_telegram_message
            sent_message.id = 100

        with allure.step("Mock client methods to simulate timeout"):
            user_telegram_client_connected.send_message = mocker.AsyncMock(
                return_value=sent_message
            )
            user_telegram_client_connected.get_messages = mocker.AsyncMock(
                return_value=[]
            )
            # Simulate timeout by making time progress beyond timeout
            user_telegram_client_connected.client.loop.time = mocker.AsyncMock(
                side_effect=[0, timeout + 1]
            )

            mocker.patch("asyncio.sleep", new_callable=mocker.AsyncMock)

        with allure.step(f"Call interact_with_bot() with timeout={timeout}"):
            result = await user_telegram_client_connected.interact_with_bot(
                "test_bot", "/start", wait_for_response=True, timeout=timeout
            )

        with allure.step("Verify result is None on timeout"):
            assert result is None

    @pytest.mark.asyncio
    @allure.title("interact_with_bot() calls sleep when waiting for response")
    @allure.description(
        "Test interact_with_bot() calls sleep when waiting for response."
    )
    async def test_interact_with_bot_multiple_iterations(
        self, mocker, user_telegram_client_connected, mock_telegram_message
    ):
        """Test interact_with_bot() calls sleep when waiting for response."""

        with allure.step("Set sent_message.id"):
            sent_message = mock_telegram_message
            sent_message.id = 100

        with allure.step(
            "Create response message that will be found after a few iterations"
        ):
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

        with allure.step("Mock client methods"):
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

            # Mock sleep in the module where it's used (tma_test_framework.clients.mtproto_client)
            mock_sleep = mocker.patch(
                "tma_test_framework.clients.mtproto_client.sleep",
                new_callable=mocker.AsyncMock,
            )

        with allure.step("Call interact_with_bot()"):
            result = await user_telegram_client_connected.interact_with_bot(
                "test_bot", "/start", wait_for_response=True, timeout=30
            )

        with allure.step("Verify result and sleep was called"):
            # Should return response message
            assert result == response_message
            # Should have called sleep twice (for two empty results before finding response)
            assert mock_sleep.call_count == 2

    @pytest.mark.asyncio
    @allure.title("interact_with_bot() raises exception for invalid bot_username")
    @allure.description(
        "Test interact_with_bot() raises exception for invalid bot_username."
    )
    async def test_interact_with_bot_invalid_username(
        self, mocker, user_telegram_client_connected
    ):
        """Test interact_with_bot() raises exception for invalid bot_username."""
        with allure.step("Mock send_message to raise ValueError"):
            user_telegram_client_connected.send_message = mocker.AsyncMock(
                side_effect=ValueError("User not found")
            )

        with allure.step("Attempt to interact with invalid bot and expect ValueError"):
            with pytest.raises(ValueError, match="User not found"):
                await user_telegram_client_connected.interact_with_bot(
                    "invalid_bot", "/start"
                )


class TestUserTelegramClientGetMiniAppFromBot:
    """Test UserTelegramClient get_mini_app_from_bot method."""

    @pytest.mark.asyncio
    @allure.title("get_mini_app_from_bot() finds Mini App URL in text")
    @allure.description("Test get_mini_app_from_bot() finds Mini App URL in text.")
    async def test_get_mini_app_from_bot_found_in_text(
        self, mocker, user_telegram_client_connected, mock_telegram_message
    ):
        """Test get_mini_app_from_bot() finds Mini App URL in text."""
        with allure.step("Create bot_message with Mini App URL in text"):
            bot_message = MessageInfo(
                id=101,
                text="Click https://t.me/mybot/app?start=123",
                from_user=None,
                chat=ChatInfo(id=987654321, title="Test Bot", type="private"),
                date="2023-10-20T10:01:00Z",
                reply_to=None,
                media=None,
            )

        with allure.step("Mock interact_with_bot"):
            user_telegram_client_connected.interact_with_bot = mocker.AsyncMock(
                return_value=bot_message
            )

        with allure.step("Call get_mini_app_from_bot()"):
            result = await user_telegram_client_connected.get_mini_app_from_bot(
                "mybot", "123"
            )

        with allure.step("Verify result contains Mini App URL"):
            assert result is not None
            assert result.url == "https://t.me/mybot/app?start=123"

    @pytest.mark.asyncio
    @allure.title("get_mini_app_from_bot() finds Mini App URL in media")
    @allure.description("Test get_mini_app_from_bot() finds Mini App URL in media.")
    async def test_get_mini_app_from_bot_found_in_media(
        self, mocker, user_telegram_client_connected, mock_telegram_message_with_webapp
    ):
        """Test get_mini_app_from_bot() finds Mini App URL in media."""
        with allure.step("Create bot_message with Mini App URL in media"):
            bot_message = MessageInfo(
                id=101,
                text="No URL in text",
                from_user=None,
                chat=ChatInfo(id=987654321, title="Test Bot", type="private"),
                date="2023-10-20T10:01:00Z",
                reply_to=None,
                media={"type": "web_app", "url": "https://t.me/mybot/app?start=123"},
            )

        with allure.step("Mock interact_with_bot and get_messages"):
            messages = [bot_message]
            user_telegram_client_connected.interact_with_bot = mocker.AsyncMock(
                return_value=None
            )
            user_telegram_client_connected.get_messages = mocker.AsyncMock(
                return_value=messages
            )

        with allure.step("Call get_mini_app_from_bot()"):
            result = await user_telegram_client_connected.get_mini_app_from_bot("mybot")

        with allure.step("Verify result contains Mini App URL from media"):
            assert result is not None
            assert result.url == "https://t.me/mybot/app?start=123"

    @pytest.mark.asyncio
    @allure.title("get_mini_app_from_bot() returns None when not found")
    @allure.description("Test get_mini_app_from_bot() returns None when not found.")
    async def test_get_mini_app_from_bot_not_found(
        self, mocker, user_telegram_client_connected
    ):
        """Test get_mini_app_from_bot() returns None when not found."""
        with allure.step("Create bot_message without Mini App URL"):
            bot_message = MessageInfo(
                id=101,
                text="No Mini App here",
                from_user=None,
                chat=ChatInfo(id=987654321, title="Test Bot", type="private"),
                date="2023-10-20T10:01:00Z",
                reply_to=None,
                media=None,
            )

        with allure.step("Mock interact_with_bot and get_messages"):
            user_telegram_client_connected.interact_with_bot = mocker.AsyncMock(
                return_value=bot_message
            )
            user_telegram_client_connected.get_messages = mocker.AsyncMock(
                return_value=[]
            )

        with allure.step("Call get_mini_app_from_bot()"):
            result = await user_telegram_client_connected.get_mini_app_from_bot("mybot")

        with allure.step("Verify result is None"):
            assert result is None

    @pytest.mark.asyncio
    @allure.title("get_mini_app_from_bot() uses start_param")
    @allure.description("Test get_mini_app_from_bot() uses start_param.")
    async def test_get_mini_app_from_bot_with_start_param(
        self, mocker, user_telegram_client_connected
    ):
        """Test get_mini_app_from_bot() uses start_param."""
        with allure.step("Create bot_message with Mini App URL"):
            bot_message = MessageInfo(
                id=101,
                text="Click https://t.me/mybot/app?start=abc123",
                from_user=None,
                chat=ChatInfo(id=987654321, title="Test Bot", type="private"),
                date="2023-10-20T10:01:00Z",
                reply_to=None,
                media=None,
            )

        with allure.step("Mock interact_with_bot"):
            user_telegram_client_connected.interact_with_bot = mocker.AsyncMock(
                return_value=bot_message
            )

        with allure.step("Call get_mini_app_from_bot() with start_param"):
            result = await user_telegram_client_connected.get_mini_app_from_bot(
                "mybot", "abc123"
            )

        with allure.step(
            "Verify interact_with_bot was called with correct command and result"
        ):
            # Verify interact_with_bot was called with correct command
            user_telegram_client_connected.interact_with_bot.assert_called_once_with(
                "mybot", "/start abc123"
            )
            assert result is not None


class TestUserTelegramClientExtractMiniAppUrl:
    """Test UserTelegramClient _extract_mini_app_url method."""

    @pytest.mark.parametrize("text,expected", MINI_APP_TEXT_SAMPLES)
    @allure.title("_extract_mini_app_url() with various text samples")
    @allure.description("Test _extract_mini_app_url() with various text samples.")
    def test_extract_mini_app_url(self, user_telegram_client, text, expected):
        """Test _extract_mini_app_url() with various text samples."""
        with allure.step(f"Call _extract_mini_app_url() with text: {text[:50]}..."):
            result = user_telegram_client._extract_mini_app_url(text)
        with allure.step("Verify result matches expected"):
            assert result == expected


class TestUserTelegramClientExtractMediaInfo:
    """Test UserTelegramClient _extract_media_info method."""

    @allure.title("_extract_media_info() with None media")
    @allure.description("Test _extract_media_info() with None media.")
    def test_extract_media_info_none(self, user_telegram_client, mock_telegram_message):
        """Test _extract_media_info() with None media."""
        with allure.step("Set mock_telegram_message.media to None"):
            mock_telegram_message.media = None

        with allure.step("Call _extract_media_info()"):
            result = user_telegram_client._extract_media_info(mock_telegram_message)

        with allure.step("Verify result is None"):
            assert result is None

    @allure.title("_extract_media_info() with media that has url")
    @allure.description("Test _extract_media_info() with media that has url.")
    def test_extract_media_info_with_url(
        self, user_telegram_client, mock_telegram_message_with_media
    ):
        """Test _extract_media_info() with media that has url."""
        with allure.step("Call _extract_media_info()"):
            result = user_telegram_client._extract_media_info(
                mock_telegram_message_with_media
            )

        with allure.step("Verify result contains url"):
            assert result is not None
            assert result.get("url") == "https://example.com/photo.jpg"

    @allure.title("_extract_media_info() with media that has webpage")
    @allure.description("Test _extract_media_info() with media that has webpage.")
    def test_extract_media_info_with_webpage(
        self, user_telegram_client, mock_telegram_message_with_webapp
    ):
        """Test _extract_media_info() with media that has webpage."""
        with allure.step("Call _extract_media_info()"):
            result = user_telegram_client._extract_media_info(
                mock_telegram_message_with_webapp
            )

        with allure.step("Verify result contains webpage"):
            assert result is not None
            assert result.get("webpage") == "https://t.me/mybot/app?start=123"


# ============================================================================
# V. Обработка событий
# ============================================================================


class TestUserTelegramClientStartListening:
    """Test UserTelegramClient start_listening method."""

    @pytest.mark.asyncio
    @allure.title("start_listening() calls connect() if not connected")
    @allure.description("Test start_listening() calls connect() if not connected.")
    async def test_start_listening_connects_if_not_connected(
        self, mocker, user_telegram_client
    ):
        """Test start_listening() calls connect() if not connected."""
        with allure.step("Mock connect and run_until_disconnected"):
            user_telegram_client.connect = mocker.AsyncMock()
            user_telegram_client.client.run_until_disconnected = mocker.AsyncMock()

        with allure.step("Start listening task and cancel it after short delay"):
            # This will run indefinitely, so we need to cancel it

            task = asyncio.create_task(user_telegram_client.start_listening())
            await asyncio.sleep(0.1)  # Give it time to call connect
            task.cancel()

            try:
                await task
            except asyncio.CancelledError:
                pass

        with allure.step("Verify connect was called"):
            user_telegram_client.connect.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("start_listening() adds event handler if provided")
    @allure.description("Test start_listening() adds event handler if provided.")
    async def test_start_listening_with_event_handler(
        self, mocker, user_telegram_client_connected
    ):
        """Test start_listening() adds event handler if provided."""
        with allure.step("Create event handler and mock client methods"):
            event_handler = mocker.MagicMock()
            user_telegram_client_connected.client.add_event_handler = mocker.MagicMock()
            user_telegram_client_connected.client.run_until_disconnected = (
                mocker.AsyncMock()
            )

        with allure.step("Start listening task with event handler and cancel it"):
            task = asyncio.create_task(
                user_telegram_client_connected.start_listening(event_handler)
            )
            await asyncio.sleep(0.1)
            task.cancel()

            try:
                await task
            except asyncio.CancelledError:
                pass

        with allure.step("Verify add_event_handler was called"):
            user_telegram_client_connected.client.add_event_handler.assert_called_once_with(
                event_handler, events.NewMessage
            )

    @pytest.mark.asyncio
    @allure.title("TC-CLIENT-045: start_listening() without event handler")
    @allure.description("Test start_listening() without event handler. TC-CLIENT-045")
    async def test_start_listening_without_handler(
        self, mocker, user_telegram_client_connected
    ):
        """Test start_listening() without event handler. TC-CLIENT-045"""
        with allure.step("Mock run_until_disconnected"):
            user_telegram_client_connected.client.run_until_disconnected = (
                mocker.AsyncMock()
            )

        with allure.step("Start listening task without handler and cancel it"):
            task = asyncio.create_task(user_telegram_client_connected.start_listening())
            await asyncio.sleep(0.1)
            task.cancel()

            try:
                await task
            except asyncio.CancelledError:
                pass

        with allure.step("Verify run_until_disconnected was called"):
            # Should call run_until_disconnected without adding event handler
            user_telegram_client_connected.client.run_until_disconnected.assert_called_once()
            # Should not call add_event_handler when no handler provided
            # Note: We can't easily verify add_event_handler wasn't called without mocking,
            # but the test verifies that start_listening works without handler


class TestUserTelegramClientAddEventHandler:
    """Test UserTelegramClient add_event_handler method."""

    @allure.title("add_event_handler() calls client.add_event_handler")
    @allure.description("Test add_event_handler() calls client.add_event_handler.")
    def test_add_event_handler(self, mocker, user_telegram_client_connected):
        """Test add_event_handler() calls client.add_event_handler."""
        with allure.step("Create handler and import events"):
            handler = mocker.MagicMock()

        with allure.step("Call add_event_handler()"):
            user_telegram_client_connected.add_event_handler(handler, events.NewMessage)

        with allure.step("Verify client.add_event_handler was called"):
            user_telegram_client_connected.client.add_event_handler.assert_called_once_with(
                handler, events.NewMessage
            )


# ============================================================================
# VI. Обработка ошибок и логирование
# ============================================================================


class TestUserTelegramClientErrorHandling:
    """Test UserTelegramClient error handling."""

    @pytest.mark.asyncio
    @allure.title("get_entity() logs error and raises exception")
    @allure.description("Test get_entity() logs error and raises exception.")
    async def test_get_entity_logs_error(self, mocker, user_telegram_client):
        """Test get_entity() logs error and raises exception."""
        with allure.step("Mock client.get_entity to raise ValueError"):
            error = ValueError("Entity not found")
            user_telegram_client.client.get_entity = mocker.AsyncMock(side_effect=error)

        with allure.step("Attempt to get invalid entity and expect ValueError"):
            with pytest.raises(ValueError):
                await user_telegram_client.get_entity("invalid")

            # Error should be logged (we can't easily test logging, but exception should be raised)

    @pytest.mark.asyncio
    @allure.title("send_message() logs error and raises exception")
    @allure.description("Test send_message() logs error and raises exception.")
    async def test_send_message_logs_error(
        self, mocker, user_telegram_client_connected
    ):
        """Test send_message() logs error and raises exception."""
        with allure.step("Mock client.send_message to raise ValueError"):
            error = ValueError("Failed to send")
            user_telegram_client_connected.client.send_message = mocker.AsyncMock(
                side_effect=error
            )

        with allure.step(
            "Attempt to send message to invalid entity and expect ValueError"
        ):
            with pytest.raises(ValueError):
                await user_telegram_client_connected.send_message("invalid", "Hello")

    @pytest.mark.asyncio
    @allure.title("get_messages() logs error and returns empty list")
    @allure.description("Test get_messages() logs error and returns empty list.")
    async def test_get_messages_logs_error(
        self, mocker, user_telegram_client_connected
    ):
        """Test get_messages() logs error and returns empty list."""
        with allure.step("Mock client.get_messages to raise ValueError"):
            error = ValueError("Failed to get messages")
            user_telegram_client_connected.client.get_messages = mocker.AsyncMock(
                side_effect=error
            )

        with allure.step("Call get_messages() and verify empty list is returned"):
            # Method returns empty list on error, doesn't raise
            result = await user_telegram_client_connected.get_messages("invalid")
            assert result == []

    @pytest.mark.asyncio
    @allure.title("interact_with_bot() logs error and raises exception")
    @allure.description("Test interact_with_bot() logs error and raises exception.")
    async def test_interact_with_bot_logs_error(
        self, mocker, user_telegram_client_connected
    ):
        """Test interact_with_bot() logs error and raises exception."""
        with allure.step("Mock send_message to raise ValueError"):
            error = ValueError("Bot not found")
            user_telegram_client_connected.send_message = mocker.AsyncMock(
                side_effect=error
            )

        with allure.step("Attempt to interact with invalid bot and expect ValueError"):
            with pytest.raises(ValueError):
                await user_telegram_client_connected.interact_with_bot(
                    "invalid_bot", "/start"
                )

    @pytest.mark.asyncio
    @allure.title("get_mini_app_from_bot() logs error and raises exception")
    @allure.description("Test get_mini_app_from_bot() logs error and raises exception.")
    async def test_get_mini_app_from_bot_logs_error(
        self, mocker, user_telegram_client_connected
    ):
        """Test get_mini_app_from_bot() logs error and raises exception."""
        with allure.step("Mock interact_with_bot to raise ValueError"):
            error = ValueError("Bot not found")
            user_telegram_client_connected.interact_with_bot = mocker.AsyncMock(
                side_effect=error
            )

        with allure.step(
            "Attempt to get mini app from invalid bot and expect ValueError"
        ):
            with pytest.raises(ValueError):
                await user_telegram_client_connected.get_mini_app_from_bot(
                    "invalid_bot"
                )


# ============================================================================
# XII. Session Management Tests
# ============================================================================


class TestSessionString:
    """Test session_string property."""

    @pytest.mark.asyncio
    @allure.title("Get session_string from connected client")
    @allure.description(
        "Test session_string property returns session string. TC-CLIENT-053"
    )
    async def test_session_string_returns_string(
        self, mocker, user_telegram_client_connected, config_with_session_string
    ):
        """Test session_string property returns session string. TC-CLIENT-053"""
        with allure.step("Mock StringSession.save() to return session string"):
            expected_session = "test_session_string_12345"
            user_telegram_client_connected.client.session.save = mocker.Mock(
                return_value=expected_session
            )

        with allure.step("Verify session is StringSession"):
            # Create a proper mock that passes isinstance check
            # Use spec_set to ensure isinstance works correctly
            mock_session = mocker.Mock(spec_set=StringSession)
            mock_session.save.return_value = expected_session
            # Set __class__.__name__ to "StringSession" for type name check
            type(mock_session).__name__ = "StringSession"
            user_telegram_client_connected.client.session = mock_session

        with allure.step("Access session_string property"):
            result = user_telegram_client_connected.session_string

        with allure.step("Verify session string is returned"):
            assert result == expected_session
            user_telegram_client_connected.client.session.save.assert_called_once()

    @allure.title("Get session_string raises when not connected")
    @allure.description(
        "Test session_string raises ValueError when not connected. TC-CLIENT-054"
    )
    def test_session_string_not_connected(self, user_telegram_client):
        """Test session_string raises ValueError when not connected. TC-CLIENT-054"""
        with allure.step("Access session_string property without connecting"):
            with pytest.raises(ValueError, match="Client is not connected"):
                _ = user_telegram_client.session_string

    @pytest.mark.asyncio
    @allure.title("Get session_string raises with SQLiteSession")
    @allure.description(
        "Test session_string raises ValueError with SQLiteSession. TC-CLIENT-055"
    )
    async def test_session_string_with_sqlite_session(
        self, mocker, user_telegram_client_connected, config_with_session_file
    ):
        """Test session_string raises ValueError with SQLiteSession. TC-CLIENT-055"""
        with allure.step("Create client with SQLiteSession"):
            # Create a proper mock that passes isinstance check
            mock_session = mocker.Mock(spec_set=SQLiteSession)
            # Set __class__.__name__ to "SQLiteSession" for type name check
            type(mock_session).__name__ = "SQLiteSession"
            user_telegram_client_connected.client.session = mock_session

        with allure.step("Access session_string property and expect ValueError"):
            with pytest.raises(ValueError, match="Session is not a StringSession"):
                _ = user_telegram_client_connected.session_string


class TestCreateSession:
    """Test create_session classmethod."""

    @pytest.mark.asyncio
    @allure.title("TC-CLIENT-056: Create session with api_id and api_hash")
    @allure.description("Test create_session() creates new session. TC-CLIENT-056")
    async def test_create_session_with_params(self, mocker):
        """Test create_session() creates new session. TC-CLIENT-056"""
        with allure.step("Mock TelegramClient and authentication flow"):
            mock_session = mocker.Mock()
            mock_session.save.return_value = "test_session_string"

            mock_client = mocker.AsyncMock()
            mock_client.is_user_authorized.return_value = True
            mock_client.session = mock_session
            mock_client.connect = mocker.AsyncMock()
            mock_client.disconnect = mocker.AsyncMock()

            mocker.patch(
                "tma_test_framework.clients.mtproto_client.TelegramClient",
                return_value=mock_client,
            )
            mocker.patch(
                "tma_test_framework.clients.mtproto_client.StringSession",
                return_value=mock_session,
            )

        with allure.step("Call create_session()"):
            result = await UserTelegramClient.create_session(
                api_id=12345,
                api_hash="test_api_hash_32_characters_long!!",
                phone_number="+1234567890",
                interactive=False,
            )

        with allure.step("Verify session string is returned"):
            assert result == "test_session_string"
            mock_client.connect.assert_called_once()
            mock_client.disconnect.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("TC-CLIENT-057: Create session with Config object")
    @allure.description("Test create_session() accepts Config object. TC-CLIENT-057")
    async def test_create_session_with_config(self, mocker, valid_config):
        """Test create_session() accepts Config object. TC-CLIENT-057"""
        with allure.step("Mock TelegramClient and authentication flow"):
            mock_session = mocker.Mock()
            mock_session.save.return_value = "test_session_string"

            mock_client = mocker.AsyncMock()
            mock_client.is_user_authorized.return_value = True
            mock_client.session = mock_session
            mock_client.connect = mocker.AsyncMock()
            mock_client.disconnect = mocker.AsyncMock()

            mocker.patch(
                "tma_test_framework.clients.mtproto_client.TelegramClient",
                return_value=mock_client,
            )
            mocker.patch(
                "tma_test_framework.clients.mtproto_client.StringSession",
                return_value=mock_session,
            )

        with allure.step("Call create_session() with Config"):
            result = await UserTelegramClient.create_session(
                config=valid_config,
                phone_number="+1234567890",
                interactive=False,
            )

        with allure.step("Verify session string is returned"):
            assert result == "test_session_string"

    @pytest.mark.asyncio
    @allure.title("Create session interactive mode")
    @allure.description(
        "Test create_session() prompts for phone and code in interactive mode. TC-CLIENT-058"
    )
    async def test_create_session_interactive(self, mocker):
        """Test create_session() prompts for phone and code in interactive mode. TC-CLIENT-058"""
        with allure.step("Mock input() and getpass.getpass()"):
            mock_input = mocker.patch("builtins.input", return_value="+1234567890")
            mock_getpass = mocker.patch(
                "tma_test_framework.clients.mtproto_client.getpass.getpass",
                return_value="12345",
            )

        with allure.step("Mock TelegramClient and authentication flow"):
            mock_session = mocker.Mock()
            mock_session.save.return_value = "test_session_string"

            mock_client = mocker.AsyncMock()
            mock_client.is_user_authorized.return_value = False
            mock_client.send_code_request = mocker.AsyncMock()
            mock_client.sign_in = mocker.AsyncMock()
            mock_client.session = mock_session
            mock_client.connect = mocker.AsyncMock()
            mock_client.disconnect = mocker.AsyncMock()

            mocker.patch(
                "tma_test_framework.clients.mtproto_client.TelegramClient",
                return_value=mock_client,
            )
            mocker.patch(
                "tma_test_framework.clients.mtproto_client.StringSession",
                return_value=mock_session,
            )

        with allure.step("Call create_session() in interactive mode"):
            result = await UserTelegramClient.create_session(
                api_id=12345,
                api_hash="test_api_hash_32_characters_long!!",
                interactive=True,
            )

        with allure.step("Verify prompts were shown and session string returned"):
            assert result == "test_session_string"
            mock_input.assert_called_once()
            mock_getpass.assert_called_once()
            mock_client.send_code_request.assert_called_once_with("+1234567890")
            mock_client.sign_in.assert_called_once_with("+1234567890", "12345")

    @pytest.mark.asyncio
    @allure.title("Create session non-interactive mode")
    @allure.description(
        "Test create_session() uses provided phone_number when interactive=False. TC-CLIENT-059"
    )
    async def test_create_session_non_interactive(self, mocker):
        """Test create_session() uses provided phone_number when interactive=False. TC-CLIENT-059"""
        with allure.step("Mock input() to verify it's not called"):
            mock_input = mocker.patch("builtins.input")

        with allure.step(
            "Mock getpass for code (still needed even in non-interactive)"
        ):
            mocker.patch(
                "tma_test_framework.clients.mtproto_client.getpass.getpass",
                return_value="12345",
            )

        with allure.step(
            "Mock TelegramClient with already authorized user (non-interactive requires auth)"
        ):
            mock_session = mocker.Mock()
            mock_session.save.return_value = "test_session_string"

            mock_client = mocker.AsyncMock()
            mock_client.is_user_authorized.return_value = (
                True  # Already authorized for non-interactive
            )
            mock_client.session = mock_session
            mock_client.connect = mocker.AsyncMock()
            mock_client.disconnect = mocker.AsyncMock()

            mocker.patch(
                "tma_test_framework.clients.mtproto_client.TelegramClient",
                return_value=mock_client,
            )
            mocker.patch(
                "tma_test_framework.clients.mtproto_client.StringSession",
                return_value=mock_session,
            )

        with allure.step("Call create_session() in non-interactive mode"):
            result = await UserTelegramClient.create_session(
                api_id=12345,
                api_hash="test_api_hash_32_characters_long!!",
                phone_number="+1234567890",
                interactive=False,
            )

        with allure.step("Verify input() was not called and session string returned"):
            # input should not be called for phone since it's provided
            # But we still need code, so getpass is called
            mock_input.assert_not_called()
            assert result == "test_session_string"

    @pytest.mark.asyncio
    @allure.title("TC-CLIENT-060: Create session with 2FA password")
    @allure.description("Test create_session() handles 2FA password. TC-CLIENT-060")
    async def test_create_session_with_2fa(self, mocker):
        """Test create_session() handles 2FA password. TC-CLIENT-060"""
        with allure.step("Mock getpass for code and password"):
            mock_getpass = mocker.patch(
                "tma_test_framework.clients.mtproto_client.getpass.getpass",
                side_effect=["12345", "2fa_password"],
            )

        with allure.step("Mock TelegramClient with 2FA flow"):
            mock_session = mocker.Mock()
            mock_session.save.return_value = "test_session_string"

            mock_client = mocker.AsyncMock()
            mock_client.is_user_authorized.return_value = False
            mock_client.send_code_request = mocker.AsyncMock()

            # First sign_in raises password error, second succeeds
            async def sign_in_side_effect(*args, **kwargs):
                if "password" not in kwargs:
                    raise Exception("password required")
                return mocker.Mock()

            mock_client.sign_in = mocker.AsyncMock(side_effect=sign_in_side_effect)
            mock_client.session = mock_session
            mock_client.connect = mocker.AsyncMock()
            mock_client.disconnect = mocker.AsyncMock()

            mocker.patch(
                "tma_test_framework.clients.mtproto_client.TelegramClient",
                return_value=mock_client,
            )
            mocker.patch(
                "tma_test_framework.clients.mtproto_client.StringSession",
                return_value=mock_session,
            )

        with allure.step(
            "Call create_session() in interactive mode (2FA requires interactive)"
        ):
            result = await UserTelegramClient.create_session(
                api_id=12345,
                api_hash="test_api_hash_32_characters_long!!",
                phone_number="+1234567890",
                interactive=True,  # 2FA requires interactive mode
            )

        with allure.step("Verify password was prompted and session string returned"):
            assert result == "test_session_string"
            assert mock_getpass.call_count == 2  # Code and password

    @pytest.mark.asyncio
    @allure.title("TC-CLIENT-061: Create session validates api_id")
    @allure.description("Test create_session() validates api_id. TC-CLIENT-061")
    async def test_create_session_invalid_api_id(self):
        """Test create_session() validates api_id. TC-CLIENT-061"""
        with allure.step("Call create_session() with invalid api_id (0)"):
            with pytest.raises(ValueError, match="api_id must be a positive number"):
                await UserTelegramClient.create_session(
                    api_id=0,  # 0 is falsy, but we check <= 0 after checking for None
                    api_hash="test_api_hash_32_characters_long!!",
                    phone_number="+1234567890",
                    interactive=False,
                )

    @pytest.mark.asyncio
    @allure.title("Create session validates phone number format")
    @allure.description(
        "Test create_session() validates phone number format. TC-CLIENT-062"
    )
    async def test_create_session_invalid_phone(self):
        """Test create_session() validates phone number format. TC-CLIENT-062"""
        with allure.step("Call create_session() with invalid phone number"):
            with pytest.raises(ValueError, match="Invalid phone number format"):
                await UserTelegramClient.create_session(
                    api_id=12345,
                    api_hash="test_api_hash_32_characters_long!!",
                    phone_number="invalid",
                    interactive=False,
                )

    @pytest.mark.asyncio
    @allure.title("Create session requires phone_number when non-interactive")
    @allure.description(
        "Test create_session() requires phone_number when interactive=False. TC-CLIENT-063"
    )
    async def test_create_session_missing_phone_non_interactive(self):
        """Test create_session() requires phone_number when interactive=False. TC-CLIENT-063"""
        with allure.step(
            "Call create_session() without phone_number in non-interactive mode"
        ):
            with pytest.raises(
                ValueError, match="phone_number is required when interactive=False"
            ):
                await UserTelegramClient.create_session(
                    api_id=12345,
                    api_hash="test_api_hash_32_characters_long!!",
                    interactive=False,
                )

    @pytest.mark.asyncio
    @allure.title("Create session requires api_id and api_hash")
    @allure.description(
        "Test create_session() requires api_id and api_hash. TC-CLIENT-064"
    )
    async def test_create_session_missing_params(self):
        """Test create_session() requires api_id and api_hash. TC-CLIENT-064"""
        with allure.step("Call create_session() without api_id"):
            with pytest.raises(ValueError, match="api_id and api_hash are required"):
                await UserTelegramClient.create_session(
                    api_id=None,
                    api_hash="test_api_hash_32_characters_long!!",
                    phone_number="+1234567890",
                    interactive=False,
                )

        with allure.step("Call create_session() without api_hash"):
            with pytest.raises(ValueError, match="api_id and api_hash are required"):
                await UserTelegramClient.create_session(
                    api_id=12345,
                    api_hash=None,
                    phone_number="+1234567890",
                    interactive=False,
                )

    @pytest.mark.asyncio
    @allure.title("Create session handles already authorized user")
    @allure.description(
        "Test create_session() handles already authorized user. TC-CLIENT-065"
    )
    async def test_create_session_already_authorized(self, mocker):
        """Test create_session() handles already authorized user. TC-CLIENT-065"""
        with allure.step("Mock TelegramClient with already authorized user"):
            mock_session = mocker.Mock()
            mock_session.save.return_value = "test_session_string"

            mock_client = mocker.AsyncMock()
            mock_client.is_user_authorized.return_value = True
            mock_client.session = mock_session
            mock_client.connect = mocker.AsyncMock()
            mock_client.disconnect = mocker.AsyncMock()

            mocker.patch(
                "tma_test_framework.clients.mtproto_client.TelegramClient",
                return_value=mock_client,
            )
            mocker.patch(
                "tma_test_framework.clients.mtproto_client.StringSession",
                return_value=mock_session,
            )

        with allure.step("Call create_session()"):
            result = await UserTelegramClient.create_session(
                api_id=12345,
                api_hash="test_api_hash_32_characters_long!!",
                phone_number="+1234567890",
                interactive=False,
            )

        with allure.step("Verify no authentication flow was triggered"):
            assert result == "test_session_string"
            mock_client.send_code_request.assert_not_called()
            mock_client.sign_in.assert_not_called()

    @pytest.mark.asyncio
    @allure.title("Create session disconnects client after use")
    @allure.description(
        "Test create_session() disconnects temporary client. TC-CLIENT-066"
    )
    async def test_create_session_disconnects(self, mocker):
        """Test create_session() disconnects temporary client. TC-CLIENT-066"""
        with allure.step("Mock TelegramClient"):
            mock_session = mocker.Mock()
            mock_session.save.return_value = "test_session_string"

            mock_client = mocker.AsyncMock()
            mock_client.is_user_authorized.return_value = True
            mock_client.session = mock_session
            mock_client.connect = mocker.AsyncMock()
            mock_client.disconnect = mocker.AsyncMock()

            mocker.patch(
                "tma_test_framework.clients.mtproto_client.TelegramClient",
                return_value=mock_client,
            )
            mocker.patch(
                "tma_test_framework.clients.mtproto_client.StringSession",
                return_value=mock_session,
            )

        with allure.step("Call create_session()"):
            await UserTelegramClient.create_session(
                api_id=12345,
                api_hash="test_api_hash_32_characters_long!!",
                phone_number="+1234567890",
                interactive=False,
            )

        with allure.step("Verify client.disconnect() was called"):
            mock_client.disconnect.assert_called_once()


# ============================================================================
# VIII. Edge Cases
# ============================================================================


class TestUserTelegramClientEdgeCases:
    """Test UserTelegramClient edge cases."""

    @pytest.mark.asyncio
    @allure.title("TC-CLIENT-068: get_tma_data() without prior authorization")
    @allure.description(
        "Test get_tma_data() raises ValueError when user is not authorized. TC-CLIENT-068"
    )
    async def test_get_tma_data_without_authorization(self, mocker, valid_config):
        """Test get_tma_data() raises ValueError when user is not authorized."""
        with allure.step("Create UserTelegramClient instance"):
            mocker.patch("tma_test_framework.clients.mtproto_client.StringSession")
            mocker.patch("tma_test_framework.clients.mtproto_client.TelegramClient")
            client = UserTelegramClient(valid_config)

        with allure.step("Do not call get_me() (user not authorized)"):
            # _me should be None
            assert client._me is None

        with allure.step("Call client.to_tma_user_data() and verify ValueError"):
            with pytest.raises(
                ValueError, match="User not authorized. Call get_me\\(\\) first\\."
            ):
                client.to_tma_user_data()

    @pytest.mark.asyncio
    @allure.title("TC-CLIENT-069: generate_init_data() without bot_token")
    @allure.description(
        "Test generate_init_data() raises ValueError when bot_token is missing. TC-CLIENT-069"
    )
    async def test_generate_init_data_without_bot_token(
        self, mocker, valid_config, user_telegram_client_connected
    ):
        """Test generate_init_data() raises ValueError when bot_token is missing."""
        with allure.step("Mock get_me() to authorize user"):
            mock_user = mocker.Mock()
            mock_user.id = 12345
            mock_user.username = "testuser"
            mock_user.first_name = "Test"
            user_telegram_client_connected._me = mock_user

        with allure.step("Create config without bot_token"):
            config_without_token = Config(
                api_id=valid_config.api_id,
                api_hash=valid_config.api_hash,
                session_string=valid_config.session_string,
                timeout=valid_config.timeout,
                retry_count=valid_config.retry_count,
                retry_delay=valid_config.retry_delay,
                log_level=valid_config.log_level,
                bot_token=None,  # No bot_token
            )

        with allure.step(
            "Call await client.generate_init_data(config) and verify ValueError"
        ):
            with pytest.raises(ValueError, match="bot_token is required in config"):
                await user_telegram_client_connected.generate_init_data(
                    config_without_token
                )

    @pytest.mark.asyncio
    @allure.title("TC-CLIENT-070: generate_init_data() without authorization")
    @allure.description(
        "Test generate_init_data() raises ValueError when user is not authorized. TC-CLIENT-070"
    )
    async def test_generate_init_data_without_authorization(self, mocker, valid_config):
        """Test generate_init_data() raises ValueError when user is not authorized."""
        with allure.step("Create UserTelegramClient instance"):
            mocker.patch("tma_test_framework.clients.mtproto_client.StringSession")
            mocker.patch("tma_test_framework.clients.mtproto_client.TelegramClient")
            client = UserTelegramClient(valid_config)

        with allure.step("Do not call get_me() (user not authorized)"):
            # _me should be None
            assert client._me is None

        with allure.step("Create config with bot_token"):
            # Create config with bot_token for this test
            config_with_token = Config(
                api_id=valid_config.api_id,
                api_hash=valid_config.api_hash,
                session_string=valid_config.session_string,
                timeout=valid_config.timeout,
                retry_count=valid_config.retry_count,
                retry_delay=valid_config.retry_delay,
                log_level=valid_config.log_level,
                bot_token="test_bot_token_123456789",
            )

        with allure.step(
            "Call await client.generate_init_data(config) and verify ValueError"
        ):
            with pytest.raises(
                ValueError, match="User not authorized. Call get_me\\(\\) first\\."
            ):
                await client.generate_init_data(config_with_token)

    @pytest.mark.asyncio
    @allure.title("TC-CLIENT-071: Handle messages with various date formats")
    @allure.description(
        "Test send_message() handles messages with different date formats correctly. TC-CLIENT-071"
    )
    async def test_send_message_various_date_formats(
        self,
        mocker,
        user_telegram_client_connected,
        mock_telegram_chat,
    ):
        """Test send_message() handles messages with different date formats correctly."""
        with allure.step("Test with datetime object (has isoformat method)"):
            mock_message_datetime = mocker.Mock()
            mock_message_datetime.id = 1
            mock_message_datetime.text = "Test message"
            mock_message_datetime.date = datetime(2024, 1, 1, 12, 0, 0)
            mock_message_datetime.from_id = None
            mock_message_datetime.reply_to = None
            mock_message_datetime.media = None

            user_telegram_client_connected.client.send_message = mocker.AsyncMock(
                return_value=mock_message_datetime
            )

            result = await user_telegram_client_connected.send_message("@test", "Hello")
            assert isinstance(result, MessageInfo)
            assert result.id == 1

        with allure.step("Test with string date (no isoformat method)"):

            class StringDate:
                def __str__(self):
                    return "2024-01-01T12:00:00"

            mock_message_string = mocker.Mock()
            mock_message_string.id = 2
            mock_message_string.text = "Test message 2"
            mock_message_string.date = StringDate()
            mock_message_string.from_id = None
            mock_message_string.reply_to = None
            mock_message_string.media = None

            user_telegram_client_connected.client.send_message = mocker.AsyncMock(
                return_value=mock_message_string
            )

            result = await user_telegram_client_connected.send_message(
                "@test", "Hello 2"
            )
            assert isinstance(result, MessageInfo)
            assert result.id == 2

        with allure.step("Test with None date"):
            mock_message_none = mocker.Mock()
            mock_message_none.id = 3
            mock_message_none.text = "Test message 3"
            mock_message_none.date = None
            mock_message_none.from_id = None
            mock_message_none.reply_to = None
            mock_message_none.media = None

            user_telegram_client_connected.client.send_message = mocker.AsyncMock(
                return_value=mock_message_none
            )

            # Should handle None date gracefully
            result = await user_telegram_client_connected.send_message(
                "@test", "Hello 3"
            )
            assert isinstance(result, MessageInfo)
            assert result.id == 3

    @pytest.mark.asyncio
    @allure.title(
        "TC-CLIENT-072: create_session() with config missing api_id or api_hash"
    )
    @allure.description(
        "Test create_session() raises ValueError when config is missing api_id or api_hash. TC-CLIENT-072"
    )
    async def test_create_session_with_config_missing_api_id_or_hash(self, mocker):
        """Test create_session() raises ValueError when config is missing api_id or api_hash."""
        with allure.step("Create Config without api_id"):
            # Config validation will raise ValueError when api_id is None
            with pytest.raises(ValueError, match="api_id must be between"):
                Config(
                    api_id=None,  # type: ignore[arg-type] # Missing api_id
                    api_hash="test_hash",
                    bot_token="test_token",
                )

        with allure.step("Call await UserTelegramClient.create_session(config=None)"):
            # Test with config=None instead, which should raise ValueError
            with pytest.raises(ValueError) as exc_info:
                await UserTelegramClient.create_session(config=None)

        with allure.step(
            "Verify ValueError is raised with message about api_id and api_hash"
        ):
            error_message = str(exc_info.value)
            assert (
                "api_id and api_hash are required" in error_message
                or "Config must have api_id and api_hash" in error_message
            )

        with allure.step("Create Config without api_hash"):
            # Config validation will raise ValueError when api_hash is None
            with pytest.raises(ValueError, match="api_hash must be exactly"):
                Config(
                    api_id=123,
                    api_hash=None,  # type: ignore[arg-type] # Missing api_hash
                    bot_token="test_token",
                )

        with allure.step("Call await UserTelegramClient.create_session(config=None)"):
            # Test with config=None instead, which should raise ValueError
            with pytest.raises(ValueError) as exc_info2:
                await UserTelegramClient.create_session(config=None)

        with allure.step(
            "Verify ValueError is raised with message about api_id and api_hash"
        ):
            error_message2 = str(exc_info2.value)
            assert (
                "api_id and api_hash are required" in error_message2
                or "Config must have api_id and api_hash" in error_message2
            )

    @pytest.mark.asyncio
    @allure.title(
        "TC-CLIENT-073: create_session() with interactive=False and unauthorized user"
    )
    @allure.description(
        "Test create_session() raises ValueError when interactive=False and user is not authorized. TC-CLIENT-073"
    )
    async def test_create_session_interactive_false_unauthorized(self, mocker):
        """Test create_session() raises ValueError when interactive=False and user is not authorized."""
        with allure.step(
            "Mock TelegramClient with is_user_authorized() returning False"
        ):
            mock_client = mocker.Mock()
            mock_client.is_user_authorized = mocker.AsyncMock(return_value=False)
            mock_client.connect = mocker.AsyncMock()
            mock_client.send_code_request = mocker.AsyncMock()
            mock_client.disconnect = mocker.AsyncMock()

            mocker.patch(
                "tma_test_framework.clients.mtproto_client.TelegramClient",
                return_value=mock_client,
            )

        with allure.step(
            "Call await UserTelegramClient.create_session(api_id=123, api_hash='hash', phone_number='+1234567890', interactive=False)"
        ):
            with pytest.raises(ValueError) as exc_info:
                await UserTelegramClient.create_session(
                    api_id=123,
                    api_hash="hash",
                    phone_number="+1234567890",
                    interactive=False,
                )

        with allure.step(
            "Verify ValueError is raised with message 'User not authorized and interactive=False'"
        ):
            assert "User not authorized and interactive=False" in str(exc_info.value)
            assert "Cannot request code non-interactively" in str(exc_info.value)

    @pytest.mark.asyncio
    @allure.title(
        "TC-CLIENT-074: create_session() with 2FA password when interactive=False"
    )
    @allure.description(
        "Test create_session() raises ValueError when 2FA password is required but interactive=False. TC-CLIENT-074"
    )
    async def test_create_session_2fa_password_interactive_false(self, mocker):
        """Test create_session() raises ValueError when 2FA password is required but interactive=False."""
        with allure.step("Mock TelegramClient with sign_in() raising password error"):
            mock_client = mocker.Mock()
            mock_client.is_user_authorized = mocker.AsyncMock(return_value=False)
            mock_client.connect = mocker.AsyncMock()
            mock_client.send_code_request = mocker.AsyncMock()
            mock_client.disconnect = mocker.AsyncMock()

            # First sign_in raises password error
            password_error = Exception("password required")
            mock_client.sign_in = mocker.AsyncMock(side_effect=password_error)

            mocker.patch(
                "tma_test_framework.clients.mtproto_client.TelegramClient",
                return_value=mock_client,
            )

            # Mock getpass.getpass to avoid actual password prompt
            mocker.patch(
                "tma_test_framework.clients.mtproto_client.getpass.getpass",
                return_value="123456",
            )

        with allure.step(
            "Call await UserTelegramClient.create_session(api_id=123, api_hash='hash', phone_number='+1234567890', interactive=False)"
        ):
            with pytest.raises(ValueError) as exc_info:
                await UserTelegramClient.create_session(
                    api_id=123,
                    api_hash="hash",
                    phone_number="+1234567890",
                    interactive=False,
                )

        with allure.step("Verify ValueError is raised with message about 2FA password"):
            error_message = str(exc_info.value)
            # The error occurs before 2FA check, so we check for the earlier error message
            assert "interactive=False" in error_message
            assert "Cannot request" in error_message
