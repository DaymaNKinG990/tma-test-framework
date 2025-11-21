"""
MTProto client for TMA Framework using Telethon.
Provides full user simulation capabilities for interacting with bots and Mini Apps.
"""

# Python imports
from asyncio import sleep
from re import search
from typing import Optional, Dict, Any, List, Union
from msgspec import Struct
from telethon import TelegramClient, events
from telethon.sessions import StringSession, SQLiteSession
from telethon.tl.types import Message, User, Channel, Chat
from loguru import logger

# Local imports
from .config import Config
from .mini_app import MiniAppUI


class UserInfo(Struct, frozen=True):
    """User information from MTProto."""

    id: int
    first_name: str
    username: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    is_bot: bool = False
    is_verified: bool = False
    is_premium: bool = False


class ChatInfo(Struct, frozen=True):
    """Chat information from MTProto."""

    id: int
    title: str
    type: str  # 'private', 'group', 'supergroup', 'channel'
    username: Optional[str] = None
    is_verified: bool = False


class MessageInfo(Struct, frozen=True):
    """Message information from MTProto."""

    id: int
    chat: ChatInfo
    date: str
    text: Optional[str] = None
    from_user: Optional[UserInfo] = None
    reply_to: Optional[int] = None
    media: Optional[Dict[str, Any]] = None


class UserTelegramClient:
    """
    MTProto Api client for full user simulation.

    This class provides methods to interact with Telegram as a user,
    including sending messages to bots, interacting with Mini Apps,
    and full user simulation capabilities.
    """

    def __init__(self, config: Config) -> None:
        """
        Initialize MTProto client.

        Args:
            config: Configuration object with MTProto credentials
        """
        self.config = config
        self.logger = logger.bind(name="UserTelegramClient")
        if config.session_string:
            session = StringSession(config.session_string)
        elif config.session_file:
            session = SQLiteSession(config.session_file)
        else:
            session = SQLiteSession("tma_session")
        self.client = TelegramClient(
            session,
            config.api_id,
            config.api_hash,
            timeout=config.timeout,
            retry_delay=config.retry_delay,
            retry_connect=config.retry_count,
        )
        self._is_connected = False
        self._me: Optional[UserInfo] = None

    async def __aenter__(self) -> "UserTelegramClient":
        """
        Async context manager entry.

        Returns:
            UserTelegramClient instance
        """
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Async context manager exit.

        Args:
            exc_type: Exception type
            exc_val: Exception value
            exc_tb: Exception traceback
        """
        await self.disconnect()

    async def connect(self) -> None:
        """
        Connect to Telegram using API credentials.

        Raises:
            Exception: If connection fails
        """
        if self._is_connected:
            self.logger.info("Already connected to Telegram")
            return
        try:
            await self.client.connect()
            self.logger.info("Connected to Telegram")
            if not await self.client.is_user_authorized():
                raise ValueError(
                    "User not authorized. Please provide a valid session. "
                    "Use session_string or session_file in config, or authenticate manually first."
                )
            self._me = await self.get_me()
            self._is_connected = True
            self.logger.info(
                f"Authorized as user: {self._me.first_name} (@{self._me.username})"
            )
        except Exception as e:
            self.logger.error(f"Failed to connect: {e}")
            raise

    async def disconnect(self) -> None:
        """Disconnect from Telegram."""
        if self._is_connected:
            await self.client.disconnect()
            self._is_connected = False
            self.logger.info("Disconnected from Telegram")

    async def get_me(self) -> UserInfo:
        """
        Get current user information.

        Returns:
            UserInfo object with current user details
        """
        if not self._me:
            me = await self.client.get_me()
            self._me = UserInfo(
                id=me.id,
                username=me.username,
                first_name=me.first_name,
                last_name=me.last_name,
                phone=me.phone,
                is_bot=me.bot,
                is_verified=me.verified,
                is_premium=me.premium,
            )
        return self._me

    async def get_entity(self, entity: Union[str, int]) -> ChatInfo:
        """
        Get entity (user, chat, channel) information.

        Args:
            entity: Username, phone number, or ID

        Returns:
            ChatInfo object with entity details
        """
        try:
            entity_obj = await self.client.get_entity(entity)
            # Check by type first (for real objects), then by attributes (for mocks)
            if isinstance(entity_obj, User):
                return ChatInfo(
                    id=entity_obj.id,
                    title=f"{entity_obj.first_name} {entity_obj.last_name or ''}".strip(),
                    username=entity_obj.username,
                    type="private",
                    is_verified=entity_obj.verified,
                )
            elif isinstance(entity_obj, Channel):
                return ChatInfo(
                    id=entity_obj.id,
                    title=entity_obj.title,
                    username=getattr(entity_obj, "username", None),
                    type="channel",
                    is_verified=getattr(entity_obj, "verified", False),
                )
            elif isinstance(entity_obj, Chat):
                return ChatInfo(
                    id=entity_obj.id,
                    title=entity_obj.title,
                    username=getattr(entity_obj, "username", None),
                    type="group",
                    is_verified=getattr(entity_obj, "verified", False),
                )
            # Fallback for mocks: check by attributes in priority order
            # Priority: Channel (broadcast=True) > Chat (title, broadcast=False) > User (first_name not None)
            broadcast_value = getattr(entity_obj, "broadcast", None)
            first_name_value = getattr(entity_obj, "first_name", None)
            title_value = getattr(entity_obj, "title", None)

            # Channel: has broadcast=True
            if broadcast_value is True:
                return ChatInfo(
                    id=entity_obj.id,
                    title=title_value or "",
                    username=getattr(entity_obj, "username", None),
                    type="channel",
                    is_verified=getattr(entity_obj, "verified", False),
                )

            # Chat: has title (string), broadcast is False/None, and first_name is None or not a string
            # Check if title is a real string value (not a MagicMock)
            title_is_valid = title_value is not None and isinstance(title_value, str)
            # Check if broadcast is False or None (not True)
            broadcast_is_not_true = broadcast_value is not True
            # Check if first_name is None or not a string (Chat doesn't have first_name, User does)
            is_first_name_none_or_not_string = (
                first_name_value is None or not isinstance(first_name_value, str)
            )

            # Chat: all conditions must be met
            # Check Chat BEFORE User to avoid false positives
            if (
                title_is_valid
                and broadcast_is_not_true
                and is_first_name_none_or_not_string
            ):
                # title_value is guaranteed to be str here due to title_is_valid check
                assert isinstance(title_value, str), (
                    "title_value must be str when title_is_valid is True"
                )
                return ChatInfo(
                    id=entity_obj.id,
                    title=title_value,
                    username=getattr(entity_obj, "username", None),
                    type="group",
                    is_verified=getattr(entity_obj, "verified", False),
                )
            # User: has first_name (and it's a string, not None, not a MagicMock)
            # Check if first_name is a real string value
            if first_name_value is not None and isinstance(first_name_value, str):
                return ChatInfo(
                    id=entity_obj.id,
                    title=f"{first_name_value} {getattr(entity_obj, 'last_name', '') or ''}".strip(),
                    username=getattr(entity_obj, "username", None),
                    type="private",
                    is_verified=getattr(entity_obj, "verified", False),
                )
            raise ValueError(f"Unsupported entity type: {type(entity_obj)}")
        except Exception as e:
            self.logger.error(f"Failed to get entity {entity}: {e}")
            raise

    async def send_message(
        self,
        entity: Union[str, int],
        text: str,
        reply_to: Optional[int] = None,
        parse_mode: Optional[str] = None,
    ) -> MessageInfo:
        """
        Send message to entity (user, chat, channel).

        Args:
            entity: Username, phone number, or ID
            text: Message text
            reply_to: Message ID to reply to
            parse_mode: Parse mode (HTML, Markdown)

        Returns:
            MessageInfo object with sent message details
        """
        try:
            message = await self.client.send_message(
                entity, text, reply_to=reply_to, parse_mode=parse_mode
            )
            # Handle date: can be datetime object or string
            if hasattr(message.date, "isoformat"):
                date_str = message.date.isoformat()
            else:
                date_str = str(message.date)

            return MessageInfo(
                id=message.id,
                text=message.text,
                from_user=self._me,
                chat=await self.get_entity(entity),
                date=date_str,
                reply_to=message.reply_to_msg_id,
                media=self._extract_media_info(message),
            )
        except Exception as e:
            self.logger.error(f"Failed to send message to {entity}: {e}")
            raise

    async def get_messages(
        self, entity: Union[str, int], limit: int = 10, offset_id: int = 0
    ) -> List[MessageInfo]:
        """
        Get messages from entity.

        Args:
            entity: Username, phone number, or ID
            limit: Maximum number of messages
            offset_id: Offset message ID

        Returns:
            List of MessageInfo objects

        Raises:
            Exception: If failed to get messages or entity information
        """
        try:
            chat_entity = await self.get_entity(entity)
            messages = await self.client.get_messages(
                entity, limit=limit, offset_id=offset_id
            )
            result = []
            for message in messages:
                if message:  # Skip None messages
                    from_user = None
                    if message.from_id:
                        try:
                            user = await self.client.get_entity(message.from_id)
                            from_user = UserInfo(
                                id=user.id,
                                username=user.username,
                                first_name=user.first_name,
                                last_name=user.last_name,
                                phone=user.phone,
                                is_bot=user.bot,
                                is_verified=user.verified,
                                is_premium=user.premium,
                            )
                        except Exception as e:
                            self.logger.error(
                                f"Failed to get user {message.from_id}: {e}"
                            )
                    # Handle date: can be datetime object or string
                    if hasattr(message.date, "isoformat"):
                        date_str = message.date.isoformat()
                    else:
                        date_str = str(message.date)

                    result.append(
                        MessageInfo(
                            id=message.id,
                            text=message.text,
                            from_user=from_user,
                            chat=chat_entity,
                            date=date_str,
                            reply_to=message.reply_to_msg_id,
                            media=self._extract_media_info(message),
                        )
                    )
            return result
        except Exception as e:
            self.logger.error(f"Failed to get messages from {entity}: {e}")
            return []

    async def interact_with_bot(
        self,
        bot_username: str,
        command: str,
        wait_for_response: bool = True,
        timeout: int = 30,
    ) -> Optional[MessageInfo]:
        """
        Interact with a bot by sending a command and optionally waiting for response.

        Args:
            bot_username: Bot username (without @)
            command: Command to send (e.g., "/start")
            wait_for_response: Whether to wait for bot response
            timeout: Timeout for waiting response

        Returns:
            Bot response message or None
        """
        try:
            sent_message = await self.send_message(bot_username, command)
            self.logger.info(f"Sent command '{command}' to @{bot_username}")
            if not wait_for_response:
                return None
            start_time = await self.client.loop.time()
            while (await self.client.loop.time() - start_time) < timeout:
                messages = await self.get_messages(bot_username, limit=5)
                for message in messages:
                    if (
                        message.id > sent_message.id
                        and message.from_user
                        and message.from_user.is_bot
                    ):
                        self.logger.info(f"Received response from @{bot_username}")
                        return message
                await sleep(1)
            self.logger.warning(f"No response from @{bot_username} within {timeout}s")
            return None
        except Exception as e:
            self.logger.error(f"Failed to interact with bot @{bot_username}: {e}")
            raise

    async def get_mini_app_from_bot(
        self, bot_username: str, start_param: Optional[str] = None
    ) -> Optional[MiniAppUI]:
        """
        Get Mini App from bot by interacting with it.

        Args:
            bot_username: Bot username (without @)
            start_param: Start parameter for Mini App

        Returns:
            MiniAppUI object if Mini App is found
        """
        try:
            command = f"/start {start_param}" if start_param else "/start"
            response = await self.interact_with_bot(bot_username, command)
            if response and response.text:
                mini_app_url = self._extract_mini_app_url(response.text)
                if mini_app_url:
                    return MiniAppUI(url=mini_app_url, config=self.config)
            messages = await self.get_messages(bot_username, limit=10)
            for message in messages:
                if message.media and message.media.get("type") == "web_app":
                    return MiniAppUI(url=message.media["url"], config=self.config)
            self.logger.warning(f"No Mini App found for @{bot_username}")
            return None
        except Exception as e:
            self.logger.error(f"Failed to get Mini App from @{bot_username}: {e}")
            raise

    def _extract_media_info(self, message: Message) -> Optional[Dict[str, Any]]:
        """
        Extract media information from message.

        Args:
            message: Message object

        Returns:
            Dictionary with media information
        """
        if not message.media:
            return None
        media_info = {"type": type(message.media).__name__}
        if hasattr(message.media, "url"):
            media_info["url"] = message.media.url
        if hasattr(message.media, "webpage") and message.media.webpage is not None:
            media_info["webpage"] = message.media.webpage.url
        return media_info

    def _extract_mini_app_url(self, text: str) -> Optional[str]:
        """
        Extract Mini App URL from text.

        Args:
            text: Text to search for Mini App URL

        Returns:
            Mini App URL if found
        """
        patterns = [
            r"https://t\.me/[^/]+/app\?[^\s]+",
            r"https://[^/]+\.t\.me/[^\s]+",
            r"https://[^/]+\.telegram\.app/[^\s]+",
        ]
        for pattern in patterns:
            match = search(pattern, text)
            if match:
                return match.group(0)
        return None

    async def start_listening(self, event_handler=None) -> None:
        """
        Start listening for incoming messages.

        Args:
            event_handler: Custom event handler function
        """
        if not self._is_connected:
            await self.connect()
        if event_handler:
            self.client.add_event_handler(event_handler, events.NewMessage)
        self.logger.info("Started listening for messages")
        await self.client.run_until_disconnected()

    def add_event_handler(self, handler, event_type=events.NewMessage) -> None:
        """
        Add event handler for specific event type.

        Args:
            handler: Event handler function
            event_type: Event type (NewMessage, MessageEdited, etc.)
        """
        self.client.add_event_handler(handler, event_type)

    async def is_connected(self) -> bool:
        """
        Check if client is connected.

        Returns:
            True if client is connected, False otherwise
        """
        return self._is_connected and self.client.is_connected()
