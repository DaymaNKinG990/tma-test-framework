"""
Telegram Mini App testing framework.

This package provides classes for testing Telegram Mini Apps:
- MiniAppApi: HTTP API testing (REST endpoints)
- MiniAppUI: UI testing with Playwright
"""

from .models import (
    MiniAppInfo,
    ApiResult,
)
from .api import MiniAppApi
from .ui import MiniAppUI

__all__ = [
    "MiniAppInfo",
    "ApiResult",
    "MiniAppApi",
    "MiniAppUI",
]
