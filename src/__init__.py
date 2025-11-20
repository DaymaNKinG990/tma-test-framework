# Local imports
from .mtproto_client import UserTelegramClient, UserInfo, ChatInfo, MessageInfo
from .mini_app import (
    MiniAppApi,
    MiniAppUI,
    MiniAppInfo,
    ApiResult,
)
from .config import Config


__version__ = "0.2.0"
__author__ = "DaymaNKinG990 aka Ravil Shakerov"
__all__ = [
    "UserTelegramClient",
    "UserInfo",
    "ChatInfo",
    "MessageInfo",
    "MiniAppApi",
    "MiniAppUI",
    "MiniAppInfo",
    "ApiResult",
    "Config",
]
