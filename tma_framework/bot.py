"""
Telegram Bot API client for TMA Framework.
"""
# Python imports
from asyncio import sleep
from typing import Optional, Dict, Any, List
from msgspec import Struct
from httpx import AsyncClient, HTTPError, Limits
from loguru import logger
# Local imports
from .config import Config
from .mini_app import MiniAppUI


class BotInfo(Struct):
    """Bot information."""
    id: int
    username: str
    first_name: str
    can_join_groups: bool = False
    can_read_all_group_messages: bool = False
    supports_inline_queries: bool = False


class WebViewResult(Struct):
    """WebView result from Bot API."""
    url: str
    fullsize: bool = False
    fullscreen: bool = False


class TelegramBot:
    """
    Simple Telegram Bot API client.
    
    This class provides methods to interact with Telegram Bot API
    and get Mini Apps from bots.
    """
    
    def __init__(self, token: str, config: Optional[Config] = None) -> None:
        """
        Initialize Telegram Bot client.
        
        Args:
            token: Bot API token
            config: Configuration object
        """
        self.token = token
        self.config = config or Config(bot_token=token)
        # Configuration is validated in __post_init__   
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.logger = logger.bind(name="TelegramBot")
        self.client = AsyncClient(
            timeout=self.config.timeout,
            limits=Limits(max_keepalive_connections=5, max_connections=10)
        )
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def close(self) -> None:
        """Close HTTP client."""
        await self.client.aclose()
    
    async def get_me(self) -> BotInfo:
        """
        Get bot information.
        
        Returns:
            BotInfo object with bot details
            
        Raises:
            httpx.HTTPError: If API request fails
        """
        response = await self._make_request("getMe")
        return BotInfo(
            id=response["id"],
            username=response["username"],
            first_name=response["first_name"],
            can_join_groups=response.get("can_join_groups", False),
            can_read_all_group_messages=response.get("can_read_all_group_messages", False),
            supports_inline_queries=response.get("supports_inline_queries", False)
        )
    
    async def request_simple_webview(
        self,
        user_id: int,
        url: Optional[str] = None,
        start_param: Optional[str] = None,
        theme_params: Optional[Dict[str, Any]] = None,
        platform: str = "web",
        compact: bool = False,
        fullscreen: bool = False
    ) -> WebViewResult:
        """
        Request simple webview (Mini App) from bot.
        
        Args:
            user_id: User ID to send Mini App to
            url: Mini App URL (optional)
            start_param: Start parameter for Mini App
            theme_params: Theme parameters
            platform: Platform (web, ios, android)
            compact: Compact mode
            fullscreen: Fullscreen mode
            
        Returns:
            WebViewResult with Mini App URL
            
        Raises:
            httpx.HTTPError: If API request fails
        """
        data = {
            "user_id": user_id,
            "platform": platform,
            "compact": compact,
            "fullscreen": fullscreen
        }
        if url:
            data["url"] = url
        if start_param:
            data["start_param"] = start_param
        if theme_params:
            data["theme_params"] = theme_params
        response = await self._make_request("requestSimpleWebView", data)
        return WebViewResult(
            url=response["url"],
            fullsize=response.get("fullsize", False),
            fullscreen=response.get("fullscreen", False)
        )
    
    async def get_mini_app(
        self,
        user_id: int,
        url: Optional[str] = None,
        start_param: Optional[str] = None
    ) -> MiniAppUI:
        """
        Get Mini App from bot.
        
        Args:
            user_id: User ID to get Mini App for
            url: Mini App URL (optional)
            start_param: Start parameter for Mini App
            
        Returns:
            MiniAppUI object ready for testing
        """
        webview_result = await self.request_simple_webview(
            user_id=user_id,
            url=url,
            start_param=start_param
        )
        return MiniAppUI(
            url=webview_result.url,
            config=self.config
        )
    
    async def send_message(
        self,
        chat_id: int,
        text: str,
        parse_mode: Optional[str] = None,
        reply_markup: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send message to chat.
        
        Args:
            chat_id: Chat ID
            text: Message text
            parse_mode: Parse mode (HTML, Markdown)
            reply_markup: Reply markup (keyboard, inline keyboard)
            
        Returns:
            API response
        """
        data = {
            "chat_id": chat_id,
            "text": text
        }
        if parse_mode:
            data["parse_mode"] = parse_mode
        if reply_markup:
            data["reply_markup"] = reply_markup
        return await self._make_request("sendMessage", data)
    
    async def _make_request(
        self,
        method: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make request to Bot API.
        
        Args:
            method: API method name
            data: Request data
            
        Returns:
            API response
            
        Raises:
            httpx.HTTPError: If request fails
        """
        url = f"{self.base_url}/{method}"
        for attempt in range(self.config.retry_count + 1):
            try:
                self.logger.debug(f"Making request to {method}")
                if data:
                    response = await self.client.post(url, json=data)
                else:
                    response = await self.client.get(url)
                response.raise_for_status()
                result = response.json()
                if not result.get("ok"):
                    raise HTTPError(f"API error: {result.get('description', 'Unknown error')}")
                return result["result"]
            except HTTPError as e:
                if attempt == self.config.retry_count:
                    self.logger.error(f"Request failed after {self.config.retry_count + 1} attempts: {e}")
                    raise
                self.logger.warning(f"Request failed, retrying in {self.config.retry_delay}s: {e}")
                await sleep(self.config.retry_delay)
    
    async def get_updates(
        self,
        offset: Optional[int] = None,
        limit: int = 100,
        timeout: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get updates from bot.
        
        Args:
            offset: Offset for pagination
            limit: Maximum number of updates
            timeout: Timeout in seconds
            
        Returns:
            List of updates
        """
        data = {
            "limit": limit,
            "timeout": timeout
        }
        if offset:
            data["offset"] = offset
        return await self._make_request("getUpdates", data)
