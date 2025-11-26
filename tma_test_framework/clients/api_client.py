"""
Telegram Mini App API client for interacting with HTTP API endpoints.
"""

# Python imports
from hashlib import sha256
from hmac import compare_digest, new
from urllib.parse import parse_qs
from typing import Optional, Dict, Any, TYPE_CHECKING
from http import HTTPStatus
from httpx import AsyncClient, Limits

# Local imports
from .base_client import BaseClient
from .models import ApiResult
from ..config import Config
from ..utils import generate_telegram_init_data, user_info_to_tma_data

if TYPE_CHECKING:
    from .mtproto_client import UserInfo


class ApiClient(BaseClient):
    """
    Telegram Mini App HTTP API client.

    Provides methods for testing HTTP API endpoints of Mini Apps:
    - HTTP request handling (GET, POST, PUT, DELETE, PATCH)
    - Authentication token management
    - initData validation using HMAC-SHA256
    - TMA authentication setup
    - Response analysis and validation
    """

    def __init__(self, url: str, config: Optional[Config] = None) -> None:
        """
        Initialize API client.

        Args:
            url: Mini App URL
            config: Configuration object
        """
        super().__init__(url, config)
        self.client = AsyncClient(
            timeout=self.config.timeout,
            limits=Limits(max_keepalive_connections=5, max_connections=10),
        )
        self._auth_token: Optional[str] = None
        self._auth_token_type: str = "Bearer"

    async def close(self) -> None:
        """Close HTTP client."""
        await self.client.aclose()

    def set_auth_token(self, token: str, token_type: str = "Bearer") -> None:
        """
        Set authentication token for all subsequent requests.

        Args:
            token: Authentication token (JWT, API key, etc.)
            token_type: Token type (default: "Bearer")

        Example:
            >>> client = ApiClient("http://api.example.com", config)
            >>> result = await client.make_request("v1/login/", method="POST", data=credentials)
            >>> token_data = json.loads(result.body)
            >>> client.set_auth_token(token_data["access"])
            >>> # All subsequent requests will automatically include the token
            >>> result = await client.make_request("v1/users/", method="GET")
        """
        self._auth_token = token
        self._auth_token_type = token_type
        self.logger.debug(f"Authentication token set (type: {token_type})")

    def clear_auth_token(self) -> None:
        """Clear authentication token."""
        self._auth_token = None
        self._auth_token_type = "Bearer"
        self.logger.debug("Authentication token cleared")

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
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> ApiResult:
        """
        Make request to Mini App API endpoint.

        Args:
            endpoint: API endpoint to test
            method: HTTP method (GET, POST, PUT, DELETE)
            data: Request data (for POST, PUT, PATCH)
            params: Query parameters (for GET requests)
            headers: Request headers (will be merged with auth token if set)

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

            # Add query params to URL
            if params:
                from urllib.parse import urlencode

                query_string = urlencode(params)
                if query_string:
                    separator = "&" if "?" in url else "?"
                    url = f"{url}{separator}{query_string}"

            # Prepare headers with automatic token addition
            request_headers: Dict[str, str] = {}
            if headers:
                request_headers.update(headers)

            # Automatically add token if set (unless Authorization header is already provided)
            if self._auth_token and "Authorization" not in request_headers:
                auth_header = f"{self._auth_token_type} {self._auth_token}"
                request_headers["Authorization"] = auth_header

            # Set default Content-Type if not specified and data is provided
            if data is not None and "Content-Type" not in request_headers:
                request_headers["Content-Type"] = "application/json"

            self.logger.info(f"Making request: {method} {url}")
            response = await self.client.request(
                method=method, url=url, json=data, headers=request_headers
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

    async def setup_tma_auth(
        self,
        user_info: Optional["UserInfo"] = None,
        config: Optional[Config] = None,
        create_user: bool = True,
        create_user_endpoint: str = "v1/create/tma/",
    ) -> None:
        """
        Setup TMA authentication: create user and set init_data token.

        Args:
            user_info: UserInfo object (if None, will try to get from UserTelegramClient)
            config: Config object (required for generating init_data and for getting user_info if user_info is None)
            create_user: Whether to create user via API (default: True)
            create_user_endpoint: Endpoint for creating user (default: "v1/create/tma/")

        Raises:
            ValueError: If config is None, or if both user_info and config are None
            Exception: If user creation fails (unless user already exists)
        """
        # Validate config early - it's always required for generating init_data
        if config is None:
            raise ValueError("config is required for generating init_data")

        if user_info is None:
            # Import here to avoid circular dependency
            from .mtproto_client import UserTelegramClient

            # Try to get user info from UserTelegramClient
            try:
                async with UserTelegramClient(config) as tg_client:
                    user_info = await tg_client.get_me()
            except Exception as e:
                raise ValueError(f"Failed to get user info from Telegram: {e}") from e

        # Prepare user data
        user_data = user_info_to_tma_data(user_info)

        # Create user if needed
        if create_user:
            result = await self.make_request(
                create_user_endpoint,
                method="POST",
                data=user_data,
            )
            # 400 means user already exists, which is fine
            if result.status_code not in [HTTPStatus.CREATED, HTTPStatus.BAD_REQUEST]:
                result.raise_for_status()

        # Generate init_data

        init_data = generate_telegram_init_data(
            user_id=user_info.id,
            username=user_info.username or "",
            first_name=user_info.first_name or "",
            last_name=user_info.last_name or "",
            bot_token=config.bot_token or "",
            language_code=config.language_code,
            is_premium=user_info.is_premium,
        )

        # Set auth token
        self.set_auth_token(init_data, token_type="tma")
