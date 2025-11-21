"""
Telegram Mini App API client for interacting with Telegram WebApp API.
"""

# Python imports
from hashlib import sha256
from hmac import compare_digest, new
from urllib.parse import parse_qs
from typing import Optional, Dict, Any
from httpx import AsyncClient, Limits

# Local imports
from .base import BaseMiniApp
from .models import ApiResult
from ..config import Config


class MiniAppApi(BaseMiniApp):
    """
    Telegram Mini App HTTP API client.

    Provides methods for testing HTTP API endpoints of Mini Apps:
    - Testing REST API endpoints
    - Validating initData with HMAC (without browser)
    """

    def __init__(self, url: str, config: Optional[Config] = None) -> None:
        """
        Initialize Mini App API client.

        Args:
            url: Mini App URL
            config: Configuration object
        """
        super().__init__(url, config)
        self.client = AsyncClient(
            timeout=self.config.timeout,
            limits=Limits(max_keepalive_connections=5, max_connections=10),
        )

    async def close(self) -> None:
        """Close HTTP client."""
        await self.client.aclose()

    async def validate_init_data(self, init_data: str, bot_token: str) -> bool:
        """
        Validate Telegram initData using HMAC-SHA256.

        Args:
            init_data: Raw initData string from Telegram
            bot_token: Bot token for validation

        Returns:
            True if initData is valid, False otherwise
        """
        try:
            if not init_data or not bot_token:
                return False
            parsed_data = parse_qs(qs=init_data)
            if "hash" not in parsed_data:
                return False
            received_hash = parsed_data["hash"][0]
            # Remove 'hash' parameter for data_check_string construction
            params_without_hash = {k: v for k, v in parsed_data.items() if k != "hash"}
            # Build data_check_string: sort keys alphabetically, join "key=value" pairs with newlines
            # Use first value for each key (parse_qs returns lists)
            sorted_keys = sorted(params_without_hash.keys())
            data_check_pairs = [
                f"{key}={params_without_hash[key][0]}" for key in sorted_keys
            ]
            data_to_validate = "\n".join(data_check_pairs)
            secret_key = new(
                key="WebAppData".encode(), msg=bot_token.encode(), digestmod=sha256
            ).digest()
            expected_hash = new(
                key=secret_key, msg=data_to_validate.encode(), digestmod=sha256
            ).hexdigest()
            is_valid = compare_digest(received_hash, expected_hash)
            self.logger.info(
                f"InitData validation: {'valid' if is_valid else 'invalid'}"
            )
            return is_valid
        except Exception as e:
            self.logger.error(f"InitData validation failed: {e}")
            return False

    async def make_request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> ApiResult:
        """
        Make request to Mini App API endpoint.

        Args:
            endpoint: API endpoint to test
            method: HTTP method (GET, POST, PUT, DELETE)
            data: Request data
            headers: Request headers

        Returns:
            ApiResult with request result
        """
        try:
            if endpoint.startswith("http"):
                url = endpoint
            else:
                # Assume endpoint is relative to Mini App URL
                base_url = self.url.split("?")[0]  # Remove query params
                url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            self.logger.info(f"Making request: {method} {url}")
            response = await self.client.request(
                method=method, url=url, json=data, headers=headers
            )
            # Extract response data before closing
            # response.content automatically reads the response body
            # This must be done before accessing response.elapsed
            response_body = response.content
            response_headers = dict(response.headers)

            # Redact sensitive headers and normalize to lowercase keys
            sensitive_headers = {
                "authorization",
                "cookie",
                "set-cookie",
                "x-api-key",
                "x-auth-token",
            }
            redacted_headers = {
                k.lower(): ("[REDACTED]" if k.lower() in sensitive_headers else v)
                for k, v in response_headers.items()
            }

            # Get content type (normalize header name)
            content_type = None
            for key, value in response_headers.items():
                if key.lower() == "content-type":
                    content_type = value
                    break

            # Get reason phrase
            reason = getattr(response, "reason_phrase", None)

            # Get response time - elapsed is only available after response is read
            try:
                response_time = response.elapsed.total_seconds()
            except (AttributeError, RuntimeError):
                # If elapsed is not available (e.g., timeout or response not fully read), use 0
                response_time = 0.0

            self.logger.info(
                f"Response got: status_code={response.status_code}, "
                f"elapsed={response_time:.3f}s, "
                f"content_length={len(response_body)}"
            )

            return ApiResult(
                endpoint=endpoint,
                method=method,
                informational=response.is_informational,
                success=response.is_success,
                redirect=response.is_redirect,
                client_error=response.is_client_error,
                server_error=response.is_server_error,
                status_code=response.status_code,
                response_time=response_time,
                headers=redacted_headers,
                body=response_body,
                content_type=content_type,
                reason=reason,
                error_message=None,
            )
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Request failed: {method} {endpoint} - {error_msg}")
            return ApiResult(
                endpoint=endpoint,
                method=method,
                status_code=0,
                response_time=0,
                success=False,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
                headers={},
                body=b"",
                content_type=None,
                reason=None,
                error_message=error_msg,
            )
