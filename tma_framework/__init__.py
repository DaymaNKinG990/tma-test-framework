"""
TMA Framework - Simple Python framework for working with Telegram API and Mini Apps.

This framework provides simple classes for:
- Working with Telegram Bot API
- Interacting with Telegram Mini Apps
- Testing Mini App UI and API

Example usage:
    from tma_framework import TelegramBot, MiniApp
    
    # Initialize bot
    bot = TelegramBot(token="your_bot_token")
    
    # Get Mini App from bot
    mini_app = await bot.get_mini_app()
    
    # Test Mini App
    await mini_app.test_ui()
    await mini_app.test_api()
"""

__version__ = "0.1.0"
__author__ = "TMA Framework Team"

# Main classes
from .bot import TelegramBot, BotInfo, WebViewResult
from .mini_app import (
    MiniAppApi,
    MiniAppUI,
    MiniAppInfo,
    ApiResult,
)
from .config import Config

__all__ = [
    "TelegramBot",
    "BotInfo",
    "WebViewResult",
    "MiniAppApi",
    "MiniAppUI",
    "MiniAppInfo",
    "ApiResult",
    "Config",
]
