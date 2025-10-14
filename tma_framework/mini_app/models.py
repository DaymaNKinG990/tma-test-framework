"""
Data models for Telegram Mini App testing framework.
"""

from typing import Optional, Dict, Any
from httpx import Response
import msgspec


class MiniAppInfo(msgspec.Struct):
    """Mini App information."""
    url: str
    start_param: Optional[str] = None
    theme_params: Optional[Dict[str, Any]] = None
    platform: str = "web"


class ApiResult(msgspec.Struct):
    """Api request result."""
    endpoint: str
    method: str
    status_code: int
    response_time: float
    success: bool
    redirect: bool
    client_error: bool
    server_error: bool
    informational: bool
    response: Optional[Response] = None
    error_message: Optional[str] = None
