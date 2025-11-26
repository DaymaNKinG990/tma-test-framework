"""
Telegram Mini App testing framework clients.

This package provides classes for testing Telegram Mini Apps:
- ApiClient: HTTP API testing (REST endpoints)
- UiClient: UI testing with Playwright
- UserTelegramClient: MTProto client for user simulation
- DBClient: Database client with support for multiple backends
"""

from .models import (
    MiniAppInfo,
    ApiResult,
)
from .api_client import ApiClient
from .ui_client import UiClient
from .mtproto_client import UserTelegramClient, UserInfo, ChatInfo, MessageInfo
from .db_client import DBClient

__all__ = [
    "MiniAppInfo",
    "ApiResult",
    "ApiClient",
    "UiClient",
    "UserTelegramClient",
    "UserInfo",
    "ChatInfo",
    "MessageInfo",
    "DBClient",
]
