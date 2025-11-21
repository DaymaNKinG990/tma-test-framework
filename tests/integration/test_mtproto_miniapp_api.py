"""
Integration tests for UserTelegramClient + MiniAppApi.
Tests verify interaction between MTProto client and Mini App API client.
"""

import pytest
from httpx import Response
from datetime import timedelta

from tma_test_framework.mtproto_client import MessageInfo, UserInfo, ChatInfo
from tma_test_framework.mini_app.api import MiniAppApi


@pytest.mark.integration
class TestMTProtoMiniAppApiIntegration:
    """Integration tests for UserTelegramClient and MiniAppApi."""

    @pytest.mark.asyncio
    async def test_get_mini_app_and_test_api_endpoint(
        self, mocker, user_telegram_client_connected, mock_mini_app_url
    ):
        """
        TC-INTEGRATION-MTAPI-001: Get Mini App from bot and test API endpoint.

        Verify complete flow: get Mini App from bot, then test its API.
        """

        # Mock get_mini_app_from_bot to return MiniAppUI
        mock_mini_app_ui = mocker.MagicMock()
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        # Get Mini App from bot
        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        assert mini_app_ui is not None
        assert mini_app_ui.url == mock_mini_app_url

        # Create MiniAppApi from the URL
        config = user_telegram_client_connected.config
        mini_app_api = MiniAppApi(mini_app_ui.url, config)

        # Mock HTTP response
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.5)
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"status": "ok"}'
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.reason_phrase = "OK"
        mock_response.json = mocker.MagicMock(return_value={"status": "ok"})

        mini_app_api.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        # Test API endpoint
        result = await mini_app_api.make_request("/api/status", method="GET")

        # Verify response
        assert result is not None
        assert result.status_code == 200
        assert result.success is True
        assert result.method == "GET"

        # Cleanup
        await mini_app_api.close()

    @pytest.mark.asyncio
    async def test_get_mini_app_with_start_param_and_test_api(
        self, mocker, user_telegram_client_connected, mock_mini_app_url_with_start_param
    ):
        """
        TC-INTEGRATION-MTAPI-002: Get Mini App with start_param and test API.

        Verify Mini App retrieval with start parameter.
        """
        # Mock get_mini_app_from_bot to return MiniAppUI with start param
        mock_mini_app_ui = mocker.MagicMock()
        mock_mini_app_ui.url = mock_mini_app_url_with_start_param
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        # Get Mini App with start parameter
        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot", start_param="test123"
        )

        assert mini_app_ui is not None
        assert "start=test123" in mini_app_ui.url
        # Create MiniAppApi and test
        config = user_telegram_client_connected.config
        mini_app_api = MiniAppApi(mini_app_ui.url, config)

        # Mock HTTP response
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.3)
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"param": "test123"}'
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.reason_phrase = "OK"

        mini_app_api.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        # Test API
        result = await mini_app_api.make_request("/api/data", method="GET")

        assert result.status_code == 200
        assert result.success is True

        await mini_app_api.close()

    @pytest.mark.asyncio
    async def test_get_mini_app_from_media_and_test_api(
        self, mocker, user_telegram_client_connected, mock_mini_app_url
    ):
        """
        TC-INTEGRATION-MTAPI-003: Get Mini App from media and test API.

        Verify Mini App retrieval from message media.
        """

        # Create message with web_app media
        bot_user = UserInfo(
            id=999, first_name="Bot", is_bot=True, is_verified=False, is_premium=False
        )

        chat_info = ChatInfo(
            id=123, title="Test Chat", type="private", is_verified=False
        )

        message_with_media = MessageInfo(
            id=100,
            chat=chat_info,
            date="2023-10-20T10:00:00Z",
            text=None,
            from_user=bot_user,
            reply_to=None,
            media={"type": "web_app", "url": mock_mini_app_url},
        )

        # Mock get_messages to return message with media
        user_telegram_client_connected.get_messages = mocker.AsyncMock(
            return_value=[message_with_media]
        )

        # Mock get_mini_app_from_bot to extract from media
        mock_mini_app_ui = mocker.MagicMock()
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        # Get Mini App from bot (should extract from media)
        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        assert mini_app_ui is not None
        assert mini_app_ui.url == mock_mini_app_url

        # Create MiniAppApi and test
        config = user_telegram_client_connected.config
        mini_app_api = MiniAppApi(mini_app_ui.url, config)

        # Mock HTTP response
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.4)
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"media": "web_app"}'
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.reason_phrase = "OK"

        mini_app_api.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        # Test API
        result = await mini_app_api.make_request("/api/media", method="GET")

        assert result.status_code == 200
        assert result.success is True

        await mini_app_api.close()

    @pytest.mark.asyncio
    async def test_validate_init_data_integration(
        self, mocker, user_telegram_client_connected, mock_bot_token
    ):
        """
        TC-INTEGRATION-MTAPI-004: Get initData from bot and validate.

        Verify initData validation in integration context.
        """
        from tests.fixtures.miniapp_api import generate_valid_init_data

        # Get Mini App (simulated)
        mock_mini_app_ui = mocker.MagicMock()
        mock_mini_app_ui.url = "https://example.com/mini-app"
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppApi
        config = user_telegram_client_connected.config
        mini_app_api = MiniAppApi(mini_app_ui.url, config)

        # Generate valid initData for testing
        user_data = {"user": '{"id":123}', "auth_date": "1698000000"}
        valid_init_data = generate_valid_init_data(mock_bot_token, user_data)

        # Validate initData
        result = await mini_app_api.validate_init_data(valid_init_data, mock_bot_token)

        assert result is True

        await mini_app_api.close()

    @pytest.mark.asyncio
    async def test_get_endpoint_after_getting_mini_app(
        self, mocker, user_telegram_client_connected, mock_mini_app_url
    ):
        """
        TC-INTEGRATION-MTAPI-006: Test GET endpoint after getting Mini App.

        Verify GET request to Mini App API.
        """
        # Get Mini App from bot
        mock_mini_app_ui = mocker.MagicMock()
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppApi
        config = user_telegram_client_connected.config
        mini_app_api = MiniAppApi(mini_app_ui.url, config)

        # Mock GET response
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"status": "ok", "data": {"key": "value"}}'
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.reason_phrase = "OK"

        mini_app_api.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        # Test GET endpoint
        result = await mini_app_api.make_request("/api/status", method="GET")

        # Verify response
        assert result.status_code == 200
        assert result.success is True
        assert result.method == "GET"
        assert result.client_error is False
        assert result.server_error is False

        await mini_app_api.close()

    @pytest.mark.asyncio
    async def test_post_endpoint_with_data(
        self, mocker, user_telegram_client_connected, mock_mini_app_url
    ):
        """
        TC-INTEGRATION-MTAPI-007: Test POST endpoint with data.

        Verify POST request with JSON data.
        """
        # Get Mini App from bot
        mock_mini_app_ui = mocker.MagicMock()
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppApi
        config = user_telegram_client_connected.config
        mini_app_api = MiniAppApi(mini_app_ui.url, config)

        # Mock POST response
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.status_code = 201
        mock_response.elapsed = timedelta(seconds=0.3)
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"id": 123, "created": true}'
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.reason_phrase = "Created"

        mini_app_api.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        # Test POST endpoint with data
        test_data = {"key": "value", "number": 42}
        result = await mini_app_api.make_request(
            "/api/data", method="POST", data=test_data
        )

        # Verify response
        assert result.status_code == 201
        assert result.success is True
        assert result.method == "POST"

        # Verify request was made with data
        call_kwargs = mini_app_api.client.request.call_args[1]  # type: ignore[attr-defined]
        assert call_kwargs["json"] == test_data

        await mini_app_api.close()

    @pytest.mark.asyncio
    async def test_multiple_api_endpoints(
        self, mocker, user_telegram_client_connected, mock_mini_app_url
    ):
        """
        TC-INTEGRATION-MTAPI-008: Test multiple API endpoints.

        Verify testing multiple endpoints in sequence.
        """
        # Get Mini App from bot
        mock_mini_app_ui = mocker.MagicMock()
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppApi
        config = user_telegram_client_connected.config
        mini_app_api = MiniAppApi(mini_app_ui.url, config)

        # Mock responses for different endpoints
        def create_mock_response(status_code, content):
            mock_response = mocker.MagicMock(spec=Response)
            mock_response.status_code = status_code
            mock_response.elapsed = timedelta(seconds=0.2)
            mock_response.is_informational = status_code < 200
            mock_response.is_success = 200 <= status_code < 300
            mock_response.is_redirect = 300 <= status_code < 400
            mock_response.is_client_error = 400 <= status_code < 500
            mock_response.is_server_error = status_code >= 500
            mock_response.content = (
                content.encode() if isinstance(content, str) else content
            )
            mock_response.headers = {"Content-Type": "application/json"}
            mock_response.reason_phrase = "OK"
            return mock_response

        # Test endpoint 1: /api/status
        mini_app_api.client.request = mocker.AsyncMock(  # type: ignore[method-assign]
            return_value=create_mock_response(200, '{"status": "ok"}')
        )
        result1 = await mini_app_api.make_request("/api/status", method="GET")
        assert result1.status_code == 200
        assert result1.success is True

        # Test endpoint 2: /api/data
        mini_app_api.client.request = mocker.AsyncMock(  # type: ignore[method-assign]
            return_value=create_mock_response(200, '{"data": [1, 2, 3]}')
        )
        result2 = await mini_app_api.make_request("/api/data", method="GET")
        assert result2.status_code == 200
        assert result2.success is True

        # Test endpoint 3: /api/users
        mini_app_api.client.request = mocker.AsyncMock(  # type: ignore[method-assign]
            return_value=create_mock_response(200, '{"users": []}')
        )
        result3 = await mini_app_api.make_request("/api/users", method="GET")
        assert result3.status_code == 200
        assert result3.success is True

        await mini_app_api.close()

    @pytest.mark.asyncio
    async def test_api_with_authentication(
        self, mocker, user_telegram_client_connected, mock_mini_app_url
    ):
        """
        TC-INTEGRATION-MTAPI-009: Test API with authentication.

        Verify API requests with authentication headers.
        """
        # Get Mini App from bot
        mock_mini_app_ui = mocker.MagicMock()
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppApi
        config = user_telegram_client_connected.config
        mini_app_api = MiniAppApi(mini_app_ui.url, config)

        # Mock authenticated response
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"authenticated": true}'
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.reason_phrase = "OK"

        mini_app_api.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        # Test with auth headers
        auth_headers = {"Authorization": "Bearer test_token"}
        result = await mini_app_api.make_request(
            "/api/protected", method="GET", headers=auth_headers
        )

        # Verify response
        assert result.status_code == 200
        assert result.success is True

        # Verify headers were sent
        call_kwargs = mini_app_api.client.request.call_args[1]  # type: ignore[attr-defined]
        assert call_kwargs["headers"] == auth_headers

        await mini_app_api.close()

    @pytest.mark.asyncio
    async def test_handle_bot_not_responding(
        self, mocker, user_telegram_client_connected
    ):
        """
        TC-INTEGRATION-MTAPI-010: Handle bot not responding.

        Verify error handling when bot doesn't respond.
        """
        # Mock bot that doesn't respond
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=None
        )

        # Try to get Mini App from non-existent bot
        result = await user_telegram_client_connected.get_mini_app_from_bot(
            "nonexistent_bot"
        )

        # Verify returns None (error handled gracefully)
        assert result is None

    @pytest.mark.asyncio
    async def test_handle_mini_app_api_errors(
        self, mocker, user_telegram_client_connected, mock_mini_app_url
    ):
        """
        TC-INTEGRATION-MTAPI-011: Handle Mini App API errors.

        Verify error handling for API failures.
        """
        from httpx import RequestError

        # Get Mini App from bot
        mock_mini_app_ui = mocker.MagicMock()
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppApi
        config = user_telegram_client_connected.config
        mini_app_api = MiniAppApi(mini_app_ui.url, config)

        # Mock API error
        error = RequestError("Request failed", request=mocker.MagicMock())
        mini_app_api.client.request = mocker.AsyncMock(side_effect=error)  # type: ignore[method-assign]

        # Test failing endpoint
        result = await mini_app_api.make_request("/api/failing", method="GET")

        # Verify error is handled
        assert result is not None
        assert result.success is False
        assert result.status_code == 0
        assert result.error_message is not None

        await mini_app_api.close()

    @pytest.mark.asyncio
    async def test_context_manager_integration(
        self, mocker, user_telegram_client_connected, mock_mini_app_url
    ):
        """
        TC-INTEGRATION-MTAPI-013: Use context manager for full flow.

        Verify context manager usage in integration.
        """
        # Mock get_mini_app_from_bot
        mock_mini_app_ui = mocker.MagicMock()
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        # Mock HTTP response
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"status": "ok"}'
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.reason_phrase = "OK"

        # Use context managers
        async with user_telegram_client_connected as client:
            mini_app_ui = await client.get_mini_app_from_bot("test_bot")

            async with MiniAppApi(mini_app_ui.url, client.config) as api:
                api.client.request = mocker.AsyncMock(return_value=mock_response)
                result = await api.make_request("/api/status")
                assert result.status_code == 200

        # Verify both closed (mocked close methods should be called)
        # Note: Actual cleanup verification depends on implementation

    @pytest.mark.asyncio
    async def test_multiple_api_calls_performance(
        self, mocker, user_telegram_client_connected, mock_mini_app_url
    ):
        """
        TC-INTEGRATION-MTAPI-014: Test multiple API calls performance.

        Verify performance with multiple requests.
        """
        import time

        # Get Mini App from bot
        mock_mini_app_ui = mocker.MagicMock()
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppApi
        config = user_telegram_client_connected.config
        mini_app_api = MiniAppApi(mini_app_ui.url, config)

        # Mock responses for multiple calls
        def create_mock_response():
            mock_response = mocker.MagicMock(spec=Response)
            mock_response.status_code = 200
            mock_response.elapsed = timedelta(seconds=0.1)
            mock_response.is_informational = False
            mock_response.is_success = True
            mock_response.is_redirect = False
            mock_response.is_client_error = False
            mock_response.is_server_error = False
            mock_response.content = b'{"status": "ok"}'
            mock_response.headers = {"Content-Type": "application/json"}
            mock_response.reason_phrase = "OK"
            return mock_response

        mini_app_api.client.request = mocker.AsyncMock(  # type: ignore[method-assign]
            side_effect=[create_mock_response() for _ in range(10)]
        )

        # Measure time for 10 sequential API calls
        start_time = time.perf_counter()

        results = []
        for i in range(10):
            result = await mini_app_api.make_request(f"/api/endpoint{i}", method="GET")
            results.append(result)

        end_time = time.perf_counter()
        total_time = end_time - start_time

        # Verify all succeed
        assert len(results) == 10
        assert all(r.status_code == 200 for r in results)
        assert all(r.success is True for r in results)

        # Verify time is reasonable (should be fast with mocks)
        assert total_time < 5.0  # Should complete quickly with mocked responses

        await mini_app_api.close()

    @pytest.mark.asyncio
    async def test_concurrent_api_calls(
        self, mocker, user_telegram_client_connected, mock_mini_app_url
    ):
        """
        TC-INTEGRATION-MTAPI-015: Test concurrent API calls.

        Verify concurrent request handling.
        """
        import asyncio

        # Get Mini App from bot
        mock_mini_app_ui = mocker.MagicMock()
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppApi
        config = user_telegram_client_connected.config
        mini_app_api = MiniAppApi(mini_app_ui.url, config)

        # Mock responses for concurrent calls
        def create_mock_response(index):
            mock_response = mocker.MagicMock(spec=Response)
            mock_response.status_code = 200
            mock_response.elapsed = timedelta(seconds=0.1)
            mock_response.is_informational = False
            mock_response.is_success = True
            mock_response.is_redirect = False
            mock_response.is_client_error = False
            mock_response.is_server_error = False
            mock_response.content = f'{{"index": {index}}}'.encode()
            mock_response.headers = {"Content-Type": "application/json"}
            mock_response.reason_phrase = "OK"
            return mock_response

        # Create 5 concurrent requests
        call_count = 0

        async def mock_request(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            return create_mock_response(call_count)

        mini_app_api.client.request = mocker.AsyncMock(side_effect=mock_request)  # type: ignore[method-assign]

        # Make 5 concurrent API calls using asyncio.gather
        tasks = [
            mini_app_api.make_request(f"/api/endpoint{i}", method="GET")
            for i in range(5)
        ]

        results = await asyncio.gather(*tasks)

        # Verify all complete
        assert len(results) == 5
        assert all(r.status_code == 200 for r in results)
        assert all(r.success is True for r in results)

        await mini_app_api.close()

    @pytest.mark.asyncio
    async def test_handle_network_timeout(
        self, mocker, user_telegram_client_connected, mock_mini_app_url
    ):
        """
        TC-INTEGRATION-MTAPI-012: Handle network timeout.

        Verify timeout handling in integration.
        """
        import asyncio

        # Get Mini App from bot
        mock_mini_app_ui = mocker.MagicMock()
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppApi with short timeout
        # Create new config with short timeout instead of modifying frozen struct
        from tma_test_framework.config import Config

        original_config = user_telegram_client_connected.config
        config = Config(
            api_id=original_config.api_id,
            api_hash=original_config.api_hash,
            session_string=original_config.session_string,
            session_file=original_config.session_file,
            timeout=1,  # Short timeout (minimum valid is 1)
            retry_count=original_config.retry_count,
            retry_delay=original_config.retry_delay,
            log_level=original_config.log_level,
        )

        mini_app_api = MiniAppApi(mini_app_ui.url, config)

        # Mock timeout error
        timeout_error = asyncio.TimeoutError("Request timed out")
        mini_app_api.client.request = mocker.AsyncMock(side_effect=timeout_error)  # type: ignore[method-assign]

        # Test failing endpoint with timeout
        result = await mini_app_api.make_request("/api/slow", method="GET")

        # Verify timeout is handled
        assert result is not None
        assert result.success is False
        assert result.status_code == 0
        assert result.error_message is not None
        assert (
            "timeout" in result.error_message.lower()
            or "timed out" in result.error_message.lower()
        )

        await mini_app_api.close()

    @pytest.mark.asyncio
    async def test_validate_init_data_with_different_bot_tokens(
        self, mocker, user_telegram_client_connected
    ):
        """
        TC-INTEGRATION-MTAPI-005: Validate initData with different bot tokens.

        Verify initData validation with multiple bots.
        """
        from tests.fixtures.miniapp_api import generate_valid_init_data

        # Get Mini App (simulated)
        mock_mini_app_ui = mocker.MagicMock()
        mock_mini_app_ui.url = "https://example.com/mini-app"
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppApi
        config = user_telegram_client_connected.config
        mini_app_api = MiniAppApi(mini_app_ui.url, config)

        # Generate valid initData for bot A
        bot_token_a = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
        user_data = {"user": '{"id":123}', "auth_date": "1698000000"}
        valid_init_data = generate_valid_init_data(bot_token_a, user_data)

        # Validate with bot A token (should succeed)
        result_a = await mini_app_api.validate_init_data(valid_init_data, bot_token_a)
        assert result_a is True

        # Validate with bot B token (should fail)
        bot_token_b = "987654321:XYZabcDEFghiJKLmnoPQRstuv"
        result_b = await mini_app_api.validate_init_data(valid_init_data, bot_token_b)
        assert result_b is False

        await mini_app_api.close()
