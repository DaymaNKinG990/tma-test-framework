"""
Utility functions for API testing.
"""

import hashlib
import hmac
import json
import time
from typing import Dict, Any, List, TYPE_CHECKING
from urllib.parse import urlencode

if TYPE_CHECKING:
    from .mtproto_client import UserInfo


def parse_json(body: bytes) -> Dict[str, Any]:
    """
    Parse JSON from response body.

    Args:
        body: Response body as bytes

    Returns:
        Parsed JSON data
    """
    try:
        result: Dict[str, Any] = json.loads(body.decode("utf-8"))
        return result
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
        return {}


def validate_response_structure(
    data: Dict[str, Any], expected_fields: List[str]
) -> bool:
    """
    Validate that response contains expected fields.

    Args:
        data: Response data dictionary
        expected_fields: List of expected field names

    Returns:
        True if all fields present, False otherwise
    """
    return all(field in data for field in expected_fields)


def extract_pagination_info(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract pagination information from response.

    Args:
        data: Response data dictionary

    Returns:
        Dictionary with pagination info
    """
    return {
        "count": data.get("count"),
        "next": data.get("next"),
        "previous": data.get("previous"),
        "results": data.get("results", []),
    }


def get_error_detail(data: Dict[str, Any]) -> str:
    """
    Extract error detail from response data.

    Args:
        data: Response data dictionary

    Returns:
        Error detail string
    """
    detail = data.get("detail")
    if detail:
        return str(detail)
    error = data.get("error")
    if error:
        return str(error)
    return str(data)


def user_info_to_tma_data(user_info: "UserInfo") -> Dict[str, Any]:
    """
    Convert UserInfo to TMA user data format for API.

    Args:
        user_info: UserInfo object from UserTelegramClient

    Returns:
        Dictionary with user data in format expected by /v1/create/tma/ endpoint
    """
    return {
        "telegram_id": str(user_info.id),
        "telegram_username": user_info.username or "",
        "first_name": user_info.first_name or "",
        "last_name": user_info.last_name or "",
    }


def generate_telegram_init_data(
    user_id: int = 123456789,
    username: str = "test_user",
    first_name: str = "Test",
    last_name: str = "User",
    bot_token: str = "test_bot_token",
    language_code: str = "ru",
    is_premium: bool = False,
) -> str:
    """
    Generate valid Telegram init data for testing.

    Args:
        user_id: Telegram user ID
        username: Telegram username
        first_name: User first name
        last_name: User last name
        bot_token: Bot token for signature generation
        language_code: User language code
        is_premium: Whether user has premium

    Returns:
        Valid Telegram init data string
    """
    auth_date = int(time.time())
    user_data = {
        "id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "language_code": language_code,
        "is_premium": is_premium,
        "allows_write_to_pm": True,
    }

    data = {
        "user": json.dumps(user_data),
        "auth_date": str(auth_date),
    }

    # Generate hash
    check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
    secret = hmac.new(
        "WebAppData".encode(), bot_token.encode(), hashlib.sha256
    ).digest()
    signature = hmac.new(secret, check_string.encode(), hashlib.sha256).hexdigest()

    data["hash"] = signature
    return urlencode(data)
