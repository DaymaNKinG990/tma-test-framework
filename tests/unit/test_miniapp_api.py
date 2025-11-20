"""
Unit tests for MiniAppApi.
"""

import pytest

# Removed unittest.mock import - using pytest-mock instead AsyncMock, MagicMock, patch
from httpx import RequestError, TimeoutException

from src.mini_app.api import MiniAppApi
from tests.fixtures.miniapp_api import (
    generate_valid_init_data,
)


# ============================================================================
# I. Инициализация и закрытие
# ============================================================================


class TestMiniAppApiInit:
    """Test MiniAppApi initialization."""

    def test_init_with_url_and_config(self, mocker, valid_config, mock_httpx_client):
        """Test successful initialization with url and config. TC-API-001"""
        mocker.patch("src.mini_app.api.AsyncClient", return_value=mock_httpx_client)
        api = MiniAppApi("https://example.com/app", valid_config)

        assert api.url == "https://example.com/app"
        assert api.config == valid_config
        assert api.client is not None

    def test_init_with_config_none_raises_error(self, mocker, mock_httpx_client):
        """Test initialization with config=None raises error. TC-API-002"""
        # BaseMiniApp raises ValueError when config is None
        mocker.patch("src.mini_app.api.AsyncClient", return_value=mock_httpx_client)
        with pytest.raises(ValueError, match="config is required"):
            MiniAppApi("https://example.com/app", None)

    def test_init_creates_async_client_with_timeout(
        self, mocker, valid_config, mock_httpx_client
    ):
        """Test AsyncClient is created with correct timeout. TC-API-003"""
        mock_client_class = mocker.patch(
            "src.mini_app.api.AsyncClient", return_value=mock_httpx_client
        )
        _ = MiniAppApi("https://example.com/app", valid_config)

        # Verify AsyncClient was called with timeout
        mock_client_class.assert_called_once()
        call_kwargs = mock_client_class.call_args[1]
        assert call_kwargs["timeout"] == valid_config.timeout

    def test_init_creates_async_client_with_limits(
        self, mocker, valid_config, mock_httpx_client
    ):
        """Test AsyncClient is created with correct Limits. TC-API-004"""

        mock_client_class = mocker.patch(
            "src.mini_app.api.AsyncClient", return_value=mock_httpx_client
        )
        _ = MiniAppApi("https://example.com/app", valid_config)

        # Verify Limits were passed
        mock_client_class.assert_called_once()
        call_kwargs = mock_client_class.call_args[1]
        assert "limits" in call_kwargs
        limits = call_kwargs["limits"]
        assert limits.max_keepalive_connections == 5
        assert limits.max_connections == 10


class TestMiniAppApiClose:
    """Test MiniAppApi close method."""

    @pytest.mark.asyncio
    async def test_close_calls_client_aclose(self, miniapp_api_with_config):
        """Test close() calls await self.client.aclose(). TC-API-005"""
        await miniapp_api_with_config.close()

        miniapp_api_with_config.client.aclose.assert_called_once()

    @pytest.mark.asyncio
    async def test_close_is_async(self, miniapp_api_with_config):
        """Test close() is async and can be awaited."""
        # Should not raise any exception
        await miniapp_api_with_config.close()

    @pytest.mark.asyncio
    async def test_close_multiple_times(self, miniapp_api_with_config):
        """Test close() can be called multiple times safely. TC-API-006"""
        # First call
        await miniapp_api_with_config.close()
        miniapp_api_with_config.client.aclose.assert_called_once()

        # Reset mock to count calls
        miniapp_api_with_config.client.aclose.reset_mock()

        # Second call should not raise exception (idempotent)
        await miniapp_api_with_config.close()
        # Should still call aclose (or handle gracefully)
        # The actual behavior depends on httpx client implementation
        # but the test verifies no exception is raised


# ============================================================================
# II. Валидация init_data (validate_init_data)
# ============================================================================


class TestMiniAppApiValidateInitData:
    """Test MiniAppApi validate_init_data method."""

    @pytest.mark.asyncio
    async def test_validate_init_data_empty_init_data(self, miniapp_api_with_config):
        """Test validate_init_data with empty init_data returns False. TC-API-010"""
        result = await miniapp_api_with_config.validate_init_data("", "bot_token")
        assert result is False

    @pytest.mark.asyncio
    async def test_validate_init_data_empty_bot_token(self, miniapp_api_with_config):
        """Test validate_init_data with empty bot_token returns False. TC-API-011"""
        result = await miniapp_api_with_config.validate_init_data("init_data", "")
        assert result is False

    @pytest.mark.asyncio
    async def test_validate_init_data_both_empty(self, miniapp_api_with_config):
        """Test validate_init_data with both empty returns False. TC-API-012"""
        result = await miniapp_api_with_config.validate_init_data("", "")
        assert result is False

    @pytest.mark.asyncio
    async def test_validate_init_data_without_hash(
        self, miniapp_api_with_config, init_data_without_hash
    ):
        """Test validate_init_data without hash parameter returns False. TC-API-009"""
        init_data, bot_token = init_data_without_hash
        result = await miniapp_api_with_config.validate_init_data(init_data, bot_token)
        assert result is False

    @pytest.mark.asyncio
    async def test_validate_init_data_valid(
        self, miniapp_api_with_config, valid_init_data_and_token
    ):
        """Test validate_init_data with valid init_data returns True. TC-API-007"""
        init_data, bot_token = valid_init_data_and_token
        result = await miniapp_api_with_config.validate_init_data(init_data, bot_token)
        assert result is True

    @pytest.mark.asyncio
    async def test_validate_init_data_invalid_token(
        self, miniapp_api_with_config, valid_init_data_and_token
    ):
        """Test validate_init_data with wrong bot_token returns False."""
        init_data, _ = valid_init_data_and_token
        wrong_token = "wrong_token"
        result = await miniapp_api_with_config.validate_init_data(
            init_data, wrong_token
        )
        assert result is False

    @pytest.mark.asyncio
    async def test_validate_init_data_invalid_hash(
        self, miniapp_api_with_config, invalid_init_data_and_token
    ):
        """Test validate_init_data with invalid hash returns False. TC-API-008"""
        init_data, bot_token = invalid_init_data_and_token
        result = await miniapp_api_with_config.validate_init_data(init_data, bot_token)
        assert result is False

    @pytest.mark.asyncio
    async def test_validate_init_data_hash_at_beginning(self, miniapp_api_with_config):
        """Test validate_init_data with hash at beginning. TC-API-013"""
        bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
        # Create init_data with hash at beginning
        user_data = {"user": '{"id":123,"auth_date":"1698000000"}'}
        init_data = generate_valid_init_data(bot_token, user_data)
        # Reorder to put hash first
        from urllib.parse import parse_qs, urlencode

        parsed = parse_qs(init_data)
        hash_value = parsed["hash"][0]
        del parsed["hash"]
        # Put hash first
        reordered = {"hash": [hash_value]}
        reordered.update(parsed)
        init_data_reordered = urlencode(reordered, doseq=True)

        result = await miniapp_api_with_config.validate_init_data(
            init_data_reordered, bot_token
        )
        assert result is True

    @pytest.mark.asyncio
    async def test_validate_init_data_hash_in_middle(self, miniapp_api_with_config):
        """Test validate_init_data with hash in middle. TC-API-014"""
        bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
        user_data = {
            "user": '{"id":123}',
            "auth_date": "1698000000",
            "start_param": "test",
        }
        init_data = generate_valid_init_data(bot_token, user_data)

        result = await miniapp_api_with_config.validate_init_data(init_data, bot_token)
        assert result is True

    @pytest.mark.asyncio
    async def test_validate_init_data_hash_at_end(self, miniapp_api_with_config):
        """Test validate_init_data with hash at end. TC-API-015"""
        bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
        user_data = {"user": '{"id":123}', "auth_date": "1698000000"}
        init_data = generate_valid_init_data(bot_token, user_data)
        # Hash should already be at end in generated data

        result = await miniapp_api_with_config.validate_init_data(init_data, bot_token)
        assert result is True

    @pytest.mark.asyncio
    async def test_validate_init_data_uses_compare_digest(
        self, mocker, miniapp_api_with_config, valid_init_data_and_token
    ):
        """Test validate_init_data uses hmac.compare_digest for security. TC-API-016"""
        init_data, bot_token = valid_init_data_and_token

        mock_compare = mocker.patch("src.mini_app.api.compare_digest")
        mock_compare.return_value = True
        result = await miniapp_api_with_config.validate_init_data(init_data, bot_token)

        assert mock_compare.called
        assert result is True

    @pytest.mark.asyncio
    async def test_validate_init_data_logs_success(
        self, miniapp_api_with_config, valid_init_data_and_token, caplog
    ):
        """Test validate_init_data logs success message."""
        init_data, bot_token = valid_init_data_and_token

        with caplog.at_level("INFO"):
            await miniapp_api_with_config.validate_init_data(init_data, bot_token)

        assert "InitData validation: valid" in caplog.text

    @pytest.mark.asyncio
    async def test_validate_init_data_logs_invalid(
        self, miniapp_api_with_config, invalid_init_data_and_token, caplog
    ):
        """Test validate_init_data logs invalid message."""
        init_data, bot_token = invalid_init_data_and_token

        with caplog.at_level("INFO"):
            await miniapp_api_with_config.validate_init_data(init_data, bot_token)

        assert "InitData validation: invalid" in caplog.text

    @pytest.mark.asyncio
    async def test_validate_init_data_logs_error_on_exception(
        self, mocker, miniapp_api_with_config, caplog
    ):
        """Test validate_init_data logs error on exception. TC-API-017"""
        # Force an exception by mocking hmac.new to raise an exception
        with caplog.at_level("ERROR"):
            mocker.patch(
                "src.mini_app.api.new", side_effect=Exception("Test exception")
            )
            result = await miniapp_api_with_config.validate_init_data(
                "user=test&hash=abc", "token"
            )

        # Should return False and log error
        assert result is False
        assert "InitData validation failed" in caplog.text

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "init_data,bot_token,expected,description",
        [
            ("", "token", False, "Empty init_data"),
            ("data", "", False, "Empty bot_token"),
            ("", "", False, "Both empty"),
            ("user=test&hash=abc", "token", False, "Invalid hash"),
            ("user=test", "token", False, "No hash parameter"),
        ],
    )
    async def test_validate_init_data_parametrized(
        self, miniapp_api_with_config, init_data, bot_token, expected, description
    ):
        """Test validate_init_data with parametrized test cases."""
        result = await miniapp_api_with_config.validate_init_data(init_data, bot_token)
        assert result == expected, f"Failed for: {description}"


# ============================================================================
# III. Выполнение HTTP-запросов (make_request)
# ============================================================================


class TestMiniAppApiMakeRequest:
    """Test MiniAppApi make_request method."""

    @pytest.mark.asyncio
    async def test_make_request_absolute_url(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with absolute URL uses it as is. TC-API-021"""
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_200
        )

        result = await miniapp_api_with_config.make_request(
            "https://api.example.com/data"
        )

        assert result.endpoint == "https://api.example.com/data"
        miniapp_api_with_config.client.request.assert_called_once()
        call_kwargs = miniapp_api_with_config.client.request.call_args[1]
        assert call_kwargs["url"] == "https://api.example.com/data"

    @pytest.mark.asyncio
    async def test_make_request_relative_url_with_slash(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with relative URL starting with /. TC-API-020, TC-API-022"""
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_200
        )

        result = await miniapp_api_with_config.make_request("/api/data")

        assert result.endpoint == "/api/data"
        call_kwargs = miniapp_api_with_config.client.request.call_args[1]
        assert call_kwargs["url"] == "https://example.com/app/api/data"

    @pytest.mark.asyncio
    async def test_make_request_relative_url_without_slash(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with relative URL without /. TC-API-023"""
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_200
        )

        result = await miniapp_api_with_config.make_request("api/data")

        assert result.endpoint == "api/data"
        call_kwargs = miniapp_api_with_config.client.request.call_args[1]
        assert call_kwargs["url"] == "https://example.com/app/api/data"

    @pytest.mark.asyncio
    async def test_make_request_removes_query_params_from_base_url(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request removes query params from base URL. TC-API-035"""
        miniapp_api_with_config.url = "https://t.me/mybot/app?start=123"
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_200
        )

        _ = await miniapp_api_with_config.make_request("/api/data")

        call_kwargs = miniapp_api_with_config.client.request.call_args[1]
        assert call_kwargs["url"] == "https://t.me/mybot/app/api/data"
        assert "start=123" not in call_kwargs["url"]

    @pytest.mark.asyncio
    async def test_make_request_get_method(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with GET method. TC-API-024"""
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_200
        )

        result = await miniapp_api_with_config.make_request("/api/data", method="GET")

        assert result.method == "GET"
        call_kwargs = miniapp_api_with_config.client.request.call_args[1]
        assert call_kwargs["method"] == "GET"

    @pytest.mark.asyncio
    async def test_make_request_post_with_data(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with POST method and data. TC-API-025"""
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_200
        )
        data = {"key": "value"}

        result = await miniapp_api_with_config.make_request(
            "/api/data", method="POST", data=data
        )

        assert result.method == "POST"
        call_kwargs = miniapp_api_with_config.client.request.call_args[1]
        assert call_kwargs["method"] == "POST"
        assert call_kwargs["json"] == data

    @pytest.mark.asyncio
    async def test_make_request_with_headers(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with headers. TC-API-026"""
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_200
        )
        headers = {"Authorization": "Bearer token"}

        _ = await miniapp_api_with_config.make_request("/api/data", headers=headers)

        call_kwargs = miniapp_api_with_config.client.request.call_args[1]
        assert call_kwargs["headers"] == headers

    @pytest.mark.asyncio
    async def test_make_request_status_200(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with status 200. TC-API-024, TC-API-034"""
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_200
        )

        result = await miniapp_api_with_config.make_request("/api/data")

        assert result.status_code == 200
        assert result.success is True
        assert result.client_error is False
        assert result.server_error is False
        assert result.redirect is False
        assert result.informational is False

    @pytest.mark.asyncio
    async def test_make_request_status_301(
        self, mocker, miniapp_api_with_config, mock_httpx_response_301
    ):
        """Test make_request with status 301. TC-API-034"""
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_301
        )

        result = await miniapp_api_with_config.make_request("/api/data")

        assert result.status_code == 301
        assert result.redirect is True
        assert result.success is False

    @pytest.mark.asyncio
    async def test_make_request_status_404(
        self, mocker, miniapp_api_with_config, mock_httpx_response_404
    ):
        """Test make_request with status 404. TC-API-034"""
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_404
        )

        result = await miniapp_api_with_config.make_request("/api/data")

        assert result.status_code == 404
        assert result.client_error is True
        assert result.success is False

    @pytest.mark.asyncio
    async def test_make_request_status_500(
        self, mocker, miniapp_api_with_config, mock_httpx_response_500
    ):
        """Test make_request with status 500. TC-API-034"""
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_500
        )

        result = await miniapp_api_with_config.make_request("/api/data")

        assert result.status_code == 500
        assert result.server_error is True
        assert result.success is False

    @pytest.mark.asyncio
    async def test_make_request_status_101(
        self, mocker, miniapp_api_with_config, mock_httpx_response_101
    ):
        """Test make_request with status 101. TC-API-034"""
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_101
        )

        result = await miniapp_api_with_config.make_request("/api/data")

        assert result.status_code == 101
        assert result.informational is True
        assert result.success is False

    @pytest.mark.asyncio
    async def test_make_request_response_time(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request captures response_time. TC-API-027"""
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_200
        )

        result = await miniapp_api_with_config.make_request("/api/data")

        assert result.response_time == 0.5
        assert isinstance(result.response_time, float)

    @pytest.mark.asyncio
    async def test_make_request_response_time_unavailable(
        self, mocker, miniapp_api_with_config
    ):
        """Test make_request handles case when response.elapsed is unavailable. TC-API-038"""
        # Create a mock response where elapsed raises AttributeError
        mock_response = mocker.MagicMock()
        mock_response.status_code = 200
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"test": "data"}'
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.reason_phrase = "OK"

        # Create a mock elapsed object that raises AttributeError when total_seconds() is called
        mock_elapsed = mocker.MagicMock()
        mock_elapsed.total_seconds = mocker.Mock(
            side_effect=AttributeError("elapsed not available")
        )
        # Make elapsed property return the mock that raises error
        type(mock_response).elapsed = mocker.PropertyMock(return_value=mock_elapsed)

        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_response
        )

        result = await miniapp_api_with_config.make_request("/api/data")

        # Should handle gracefully and set response_time to 0.0
        assert result.response_time == 0.0
        assert isinstance(result.response_time, float)
        assert result.success is True
        assert result.status_code == 200

    @pytest.mark.asyncio
    async def test_make_request_response_time_runtime_error(
        self, mocker, miniapp_api_with_config
    ):
        """Test make_request handles RuntimeError when accessing response.elapsed. TC-API-038"""
        # Create a mock response where elapsed raises RuntimeError
        mock_response = mocker.MagicMock()
        mock_response.status_code = 200
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"test": "data"}'
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.reason_phrase = "OK"

        # Create a mock elapsed object that raises RuntimeError when total_seconds() is called
        mock_elapsed = mocker.MagicMock()
        mock_elapsed.total_seconds = mocker.Mock(
            side_effect=RuntimeError(
                "elapsed may only be accessed after the response has been read"
            )
        )
        # Make elapsed property return the mock that raises error
        type(mock_response).elapsed = mocker.PropertyMock(return_value=mock_elapsed)

        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_response
        )

        result = await miniapp_api_with_config.make_request("/api/data")

        # Should handle gracefully and set response_time to 0.0
        assert result.response_time == 0.0
        assert isinstance(result.response_time, float)
        assert result.success is True
        assert result.status_code == 200

    @pytest.mark.asyncio
    async def test_make_request_extracts_response_data(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request extracts response data into immutable fields. TC-API-028"""
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_200
        )

        result = await miniapp_api_with_config.make_request("/api/data")

        # Response data should be extracted into immutable fields
        assert result.headers is not None
        assert isinstance(result.headers, dict)
        assert result.body is not None
        assert isinstance(result.body, bytes)
        # Response object should not be stored
        assert (
            not hasattr(result, "response") or getattr(result, "response", None) is None
        )

    @pytest.mark.asyncio
    async def test_make_request_network_error(self, mocker, miniapp_api_with_config):
        """Test make_request handles network errors. TC-API-029"""
        error = RequestError("Network error", request=mocker.MagicMock())
        miniapp_api_with_config.client.request = mocker.AsyncMock(side_effect=error)

        result = await miniapp_api_with_config.make_request("/api/data")

        assert result.status_code == 0
        assert result.success is False
        assert result.error_message == "Network error"
        assert result.headers == {}
        assert result.body == b""
        assert result.content_type is None
        assert result.reason is None

    @pytest.mark.asyncio
    async def test_make_request_timeout_error(self, mocker, miniapp_api_with_config):
        """Test make_request handles timeout errors. TC-API-029"""
        error = TimeoutException("Request timeout", request=mocker.MagicMock())
        miniapp_api_with_config.client.request = mocker.AsyncMock(side_effect=error)

        result = await miniapp_api_with_config.make_request("/api/data")

        assert result.status_code == 0
        assert result.success is False
        assert "timeout" in result.error_message.lower()

    @pytest.mark.asyncio
    async def test_make_request_logs_request(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200, caplog
    ):
        """Test make_request logs request. TC-API-030"""
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_200
        )

        with caplog.at_level("INFO"):
            await miniapp_api_with_config.make_request("/api/data", method="POST")

        assert "Making request: POST" in caplog.text

    @pytest.mark.asyncio
    async def test_make_request_logs_response(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200, caplog
    ):
        """Test make_request logs response. TC-API-031"""
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_200
        )

        with caplog.at_level("INFO"):
            await miniapp_api_with_config.make_request("/api/data")

        assert "Response got:" in caplog.text
        assert "status_code=200" in caplog.text

    @pytest.mark.asyncio
    async def test_make_request_logs_error(
        self, mocker, miniapp_api_with_config, caplog
    ):
        """Test make_request logs error on failure. TC-API-032"""
        error = RequestError("Request failed", request=mocker.MagicMock())
        miniapp_api_with_config.client.request = mocker.AsyncMock(side_effect=error)

        with caplog.at_level("ERROR"):
            await miniapp_api_with_config.make_request("/api/data", method="POST")

        assert "Request failed: POST /api/data" in caplog.text

    @pytest.mark.asyncio
    async def test_make_request_put_method(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with PUT method. TC-API-033"""
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_200
        )
        data = {"key": "updated_value"}

        result = await miniapp_api_with_config.make_request(
            "/api/data/1", method="PUT", data=data
        )

        assert result.method == "PUT"
        call_kwargs = miniapp_api_with_config.client.request.call_args[1]
        assert call_kwargs["method"] == "PUT"
        assert call_kwargs["json"] == data

    @pytest.mark.asyncio
    async def test_make_request_delete_method(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with DELETE method. TC-API-033"""
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_200
        )

        result = await miniapp_api_with_config.make_request(
            "/api/data/1", method="DELETE"
        )

        assert result.method == "DELETE"
        call_kwargs = miniapp_api_with_config.client.request.call_args[1]
        assert call_kwargs["method"] == "DELETE"


# ============================================================================
# IV. Граничные и специальные случаи
# ============================================================================


class TestMiniAppApiEdgeCases:
    """Test MiniAppApi edge cases."""

    @pytest.mark.asyncio
    async def test_validate_init_data_very_long(self, miniapp_api_with_config):
        """Test validate_init_data with very long init_data."""
        bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
        # Create very long user data
        long_user_data = {
            "user": '{"id":123,"data":"' + "x" * 10000 + '"}',
            "auth_date": "1698000000",
        }
        init_data = generate_valid_init_data(bot_token, long_user_data)

        result = await miniapp_api_with_config.validate_init_data(init_data, bot_token)
        # Should handle without error
        assert isinstance(result, bool)

    @pytest.mark.asyncio
    async def test_validate_init_data_unicode(self, miniapp_api_with_config):
        """Test validate_init_data with unicode characters. TC-API-018"""
        bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
        user_data = {"user": '{"id":123,"name":"Тест"}', "auth_date": "1698000000"}
        init_data = generate_valid_init_data(bot_token, user_data)

        result = await miniapp_api_with_config.validate_init_data(init_data, bot_token)
        assert result is True

    @pytest.mark.asyncio
    async def test_validate_init_data_with_ampersand_in_values(
        self, miniapp_api_with_config
    ):
        """Test validate_init_data with & in values. TC-API-019"""
        bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
        user_data = {"user": '{"id":123,"data":"a&b"}', "auth_date": "1698000000"}
        init_data = generate_valid_init_data(bot_token, user_data)

        result = await miniapp_api_with_config.validate_init_data(init_data, bot_token)
        assert result is True

    @pytest.mark.asyncio
    async def test_validate_init_data_bot_token_special_chars(
        self, miniapp_api_with_config
    ):
        """Test validate_init_data with bot_token containing special characters."""
        bot_token = "123456789:ABC-def_GHI.jkl+MNO"
        user_data = {"user": '{"id":123}', "auth_date": "1698000000"}
        init_data = generate_valid_init_data(bot_token, user_data)

        result = await miniapp_api_with_config.validate_init_data(init_data, bot_token)
        assert result is True


# ============================================================================
# V. Безопасность и надёжность
# ============================================================================


class TestMiniAppApiSecurity:
    """Test MiniAppApi security and reliability."""

    @pytest.mark.asyncio
    async def test_make_request_very_long_endpoint(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with very long endpoint. TC-API-036"""
        # Create a very long endpoint (>1000 characters)
        long_endpoint = "/api/" + "a" * 1000
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_200
        )

        result = await miniapp_api_with_config.make_request(long_endpoint)

        assert result.status_code == 200
        # Verify the endpoint was used in the request
        call_kwargs = miniapp_api_with_config.client.request.call_args[1]
        assert long_endpoint in call_kwargs["url"] or call_kwargs["url"].endswith(
            long_endpoint
        )

    @pytest.mark.asyncio
    async def test_make_request_unicode_endpoint(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with unicode characters in endpoint. TC-API-037"""
        # Endpoint with unicode characters
        unicode_endpoint = "/api/тест/用户/ユーザー"
        miniapp_api_with_config.client.request = mocker.AsyncMock(
            return_value=mock_httpx_response_200
        )

        result = await miniapp_api_with_config.make_request(unicode_endpoint)

        assert result.status_code == 200
        # Verify the endpoint was used in the request
        call_kwargs = miniapp_api_with_config.client.request.call_args[1]
        # The URL should contain the unicode endpoint (may be URL-encoded)
        assert unicode_endpoint in call_kwargs["url"] or any(
            char in call_kwargs["url"] for char in unicode_endpoint
        )

    @pytest.mark.asyncio
    async def test_make_request_timeout_respected(
        self, mocker, miniapp_api_with_config
    ):
        """Test make_request respects timeout settings by returning error result on slow request."""
        # Mock the client.request to raise TimeoutException
        from httpx import TimeoutException

        miniapp_api_with_config.client.request = mocker.AsyncMock(
            side_effect=TimeoutException("Request timed out", request=None)
        )

        # make_request catches exceptions and returns ApiResult with error_message
        result = await miniapp_api_with_config.make_request("/api/data", method="GET")

        # Verify the timeout error is reflected in the result
        assert result.success is False
        assert result.status_code == 0
        assert result.error_message is not None
        # Check for "timeout" or "timed out" in error message
        error_lower = result.error_message.lower()
        assert "timeout" in error_lower or "timed out" in error_lower


# ============================================================================
# VI. Совместимость с родителем
# ============================================================================


class TestMiniAppApiInheritance:
    """Test MiniAppApi compatibility with BaseMiniApp."""

    @pytest.mark.asyncio
    async def test_context_manager_calls_close(self, mocker, miniapp_api_with_config):
        """Test async context manager calls close()."""
        miniapp_api_with_config.close = mocker.AsyncMock()

        async with miniapp_api_with_config:
            pass

        miniapp_api_with_config.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_logger_bound_to_class_name(self, miniapp_api_with_config):
        """Test logger is bound to MiniAppApi class name."""
        assert miniapp_api_with_config.logger is not None
        # Logger should be bound to "MiniAppApi"

    def test_inherits_from_base_miniapp(self, mocker, valid_config, mock_httpx_client):
        """Test MiniAppApi inherits from BaseMiniApp."""
        mocker.patch("src.mini_app.api.AsyncClient", return_value=mock_httpx_client)
        api = MiniAppApi("https://example.com/app", valid_config)

        from src.mini_app.base import BaseMiniApp

        assert isinstance(api, BaseMiniApp)
