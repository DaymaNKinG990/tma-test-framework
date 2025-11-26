# Local imports
from .clients.mtproto_client import UserTelegramClient, UserInfo, ChatInfo, MessageInfo
from .clients.api_client import ApiClient as MiniAppApi
from .clients.ui_client import UiClient as MiniAppUI
from .clients.models import MiniAppInfo, ApiResult
from .config import Config
from .utils import (
    parse_json,
    validate_response_structure,
    extract_pagination_info,
    get_error_detail,
    generate_telegram_init_data,
    user_info_to_tma_data,
)


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
    "parse_json",
    "validate_response_structure",
    "extract_pagination_info",
    "get_error_detail",
    "generate_telegram_init_data",
    "user_info_to_tma_data",
]
