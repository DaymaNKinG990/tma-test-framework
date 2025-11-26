"""
Data models for Telegram Mini App testing framework.
"""

from typing import Optional, Dict, Any
import msgspec


class MiniAppInfo(msgspec.Struct, frozen=True):
    """
    Mini App information.

    Contains all information needed to identify and launch a Mini App.
    """

    url: str
    start_param: Optional[str] = None
    theme_params: Optional[Dict[str, Any]] = None
    platform: str = "web"


class ApiResult(msgspec.Struct, frozen=True):
    """
    API request result.

    Contains complete information about an HTTP API request and response,
    including status, headers, body, and timing information.
    """

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

    def json(self) -> Dict[str, Any]:
        """
        Parse JSON from response body.

        Returns:
            Parsed JSON data as dictionary

        Raises:
            ValueError: If body is not valid JSON
        """
        import json

        try:
            return json.loads(self.body.decode("utf-8"))
        except (json.JSONDecodeError, ValueError, UnicodeDecodeError) as e:
            raise ValueError(f"Failed to parse JSON: {e}") from e

    def text(self) -> str:
        """
        Get response body as text.

        Returns:
            Response body decoded as UTF-8 string
        """
        return self.body.decode("utf-8", errors="replace")

    def raise_for_status(self) -> None:
        """
        Raise exception if status code indicates error.

        Raises:
            Exception: If status code is 4xx or 5xx
        """
        if 400 <= self.status_code < 600:
            error_msg = self.error_message or self.text()
            raise Exception(f"HTTP {self.status_code}: {error_msg}")

    def assert_status_code(self, expected_code: int) -> None:
        """
        Assert that status code matches expected value.

        Args:
            expected_code: Expected HTTP status code

        Raises:
            AssertionError: If status code doesn't match
        """
        assert self.status_code == expected_code, (
            f"Expected status code {expected_code}, got {self.status_code}. "
            f"Response: {self.text()}"
        )

    def assert_success(self) -> None:
        """Assert that request was successful (2xx status)."""
        assert self.success, (
            f"Request failed with status {self.status_code}. Response: {self.text()}"
        )

    def assert_has_fields(self, *fields: str) -> None:
        """
        Assert that JSON response contains specified fields.

        Args:
            *fields: Field names that must be present in response

        Raises:
            AssertionError: If any field is missing
        """
        data = self.json()
        missing = [field for field in fields if field not in data]
        if missing:
            raise AssertionError(
                f"Missing required fields: {', '.join(missing)}. Response: {data}"
            )
