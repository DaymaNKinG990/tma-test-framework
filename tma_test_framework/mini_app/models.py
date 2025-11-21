"""
Data models for Telegram Mini App testing framework.
"""

from typing import Optional, Dict, Any
import msgspec


class MiniAppInfo(msgspec.Struct, frozen=True):
    """Mini App information."""

    url: str
    start_param: Optional[str] = None
    theme_params: Optional[Dict[str, Any]] = None
    platform: str = "web"


class ApiResult(msgspec.Struct, frozen=True):
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
    headers: Dict[str, str] = msgspec.field(default_factory=dict)
    body: bytes = b""
    content_type: Optional[str] = None
    reason: Optional[str] = None
    error_message: Optional[str] = None
