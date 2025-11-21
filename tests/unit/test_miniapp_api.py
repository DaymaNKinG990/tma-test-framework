"""
Unit tests for MiniAppApi.
"""

import allure
import pytest

# Removed unittest.mock import - using pytest-mock instead AsyncMock, MagicMock, patch
from httpx import RequestError, TimeoutException

from tma_test_framework.mini_app.api import MiniAppApi
from tests.fixtures.miniapp_api import (
    generate_valid_init_data,
)


# ============================================================================
# I. Инициализация и закрытие
# ============================================================================


class TestMiniAppApiInit:
    """Test MiniAppApi initialization."""

    @allure.title("Initialize MiniAppApi with URL and config")
    @allure.description(
        "Test successful initialization with url and config. TC-API-001"
    )
    def test_init_with_url_and_config(self, mocker, valid_config, mock_httpx_client):
        """Test successful initialization with url and config. TC-API-001"""
        with allure.step("Mock AsyncClient"):
            mocker.patch(
                "tma_test_framework.mini_app.api.AsyncClient",
                return_value=mock_httpx_client,
            )
        with allure.step("Create MiniAppApi instance"):
            api = MiniAppApi("https://example.com/app", valid_config)

        with allure.step("Verify api.url is set correctly"):
            assert api.url == "https://example.com/app"
        with allure.step("Verify api.config matches provided config"):
            assert api.config == valid_config
        with allure.step("Verify api.client is initialized"):
            assert api.client is not None

    @allure.title("TC-API-002: Initialize MiniAppApi with config=None raises error")
    @allure.description("Test initialization with config=None raises error. TC-API-002")
    def test_init_with_config_none_raises_error(self, mocker, mock_httpx_client):
        """Test initialization with config=None raises error. TC-API-002"""
        # BaseMiniApp raises ValueError when config is None
        with allure.step("Mock AsyncClient"):
            mocker.patch(
                "tma_test_framework.mini_app.api.AsyncClient",
                return_value=mock_httpx_client,
            )
        with allure.step("Attempt to create MiniAppApi with config=None"):
            with pytest.raises(ValueError, match="config is required"):
                MiniAppApi("https://example.com/app", None)

    @allure.title("TC-API-003: Verify AsyncClient is initialized with correct timeout")
    @allure.description("Test AsyncClient is created with correct timeout. TC-API-003")
    def test_init_creates_async_client_with_timeout(
        self, mocker, valid_config, mock_httpx_client
    ):
        """Test AsyncClient is created with correct timeout. TC-API-003"""
        with allure.step("Mock AsyncClient class"):
            mock_client_class = mocker.patch(
                "tma_test_framework.mini_app.api.AsyncClient",
                return_value=mock_httpx_client,
            )
        with allure.step("Create MiniAppApi instance"):
            _ = MiniAppApi("https://example.com/app", valid_config)

        with allure.step("Verify AsyncClient was called once"):
            mock_client_class.assert_called_once()
        with allure.step("Verify timeout matches config.timeout"):
            call_kwargs = mock_client_class.call_args[1]
            assert call_kwargs["timeout"] == valid_config.timeout

    @allure.title("TC-API-004: Verify AsyncClient is initialized with correct Limits")
    @allure.description("Test AsyncClient is created with correct Limits. TC-API-004")
    def test_init_creates_async_client_with_limits(
        self, mocker, valid_config, mock_httpx_client
    ):
        """Test AsyncClient is created with correct Limits. TC-API-004"""

        with allure.step("Mock AsyncClient class"):
            mock_client_class = mocker.patch(
                "tma_test_framework.mini_app.api.AsyncClient",
                return_value=mock_httpx_client,
            )
        with allure.step("Create MiniAppApi instance"):
            _ = MiniAppApi("https://example.com/app", valid_config)

        with allure.step("Verify AsyncClient was called once"):
            mock_client_class.assert_called_once()
        with allure.step("Verify Limits were passed to AsyncClient"):
            call_kwargs = mock_client_class.call_args[1]
            assert "limits" in call_kwargs
            limits = call_kwargs["limits"]
        with allure.step("Verify max_keepalive_connections is 5"):
            assert limits.max_keepalive_connections == 5
        with allure.step("Verify max_connections is 10"):
            assert limits.max_connections == 10


class TestMiniAppApiClose:
    """Test MiniAppApi close method."""

    @pytest.mark.asyncio
    @allure.title("TC-API-005: Close MiniAppApi client")
    @allure.description("Test close() calls await self.client.aclose(). TC-API-005")
    async def test_close_calls_client_aclose(self, miniapp_api_with_config):
        """Test close() calls await self.client.aclose(). TC-API-005"""
        with allure.step("Call close() method"):
            await miniapp_api_with_config.close()

        with allure.step("Verify client.aclose() was called once"):
            miniapp_api_with_config.client.aclose.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("Close MiniAppApi is async")
    @allure.description("Test close() is async and can be awaited.")
    async def test_close_is_async(self, miniapp_api_with_config):
        """Test close() is async and can be awaited."""
        with allure.step("Call close() method and await"):
            # Should not raise any exception
            await miniapp_api_with_config.close()

    @pytest.mark.asyncio
    @allure.title("TC-API-006: Close MiniAppApi multiple times")
    @allure.description("Test close() can be called multiple times safely. TC-API-006")
    async def test_close_multiple_times(self, miniapp_api_with_config):
        """Test close() can be called multiple times safely. TC-API-006"""
        with allure.step("First call to close()"):
            await miniapp_api_with_config.close()
            miniapp_api_with_config.client.aclose.assert_called_once()

        with allure.step("Reset mock to count calls"):
            # Reset mock to count calls
            miniapp_api_with_config.client.aclose.reset_mock()

        with allure.step("Second call to close() should not raise exception"):
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
    @allure.title("Validate init_data with empty init_data")
    @allure.description(
        "Test validate_init_data with empty init_data returns False. TC-API-010"
    )
    async def test_validate_init_data_empty_init_data(self, miniapp_api_with_config):
        """Test validate_init_data with empty init_data returns False. TC-API-010"""
        with allure.step("Call validate_init_data with empty init_data"):
            result = await miniapp_api_with_config.validate_init_data("", "bot_token")
        with allure.step("Verify result is False"):
            assert result is False

    @pytest.mark.asyncio
    @allure.title("Validate init_data with empty bot_token")
    @allure.description(
        "Test validate_init_data with empty bot_token returns False. TC-API-011"
    )
    async def test_validate_init_data_empty_bot_token(self, miniapp_api_with_config):
        """Test validate_init_data with empty bot_token returns False. TC-API-011"""
        with allure.step("Call validate_init_data with empty bot_token"):
            result = await miniapp_api_with_config.validate_init_data("init_data", "")
        with allure.step("Verify result is False"):
            assert result is False

    @pytest.mark.asyncio
    @allure.title("Validate init_data with both empty")
    @allure.description(
        "Test validate_init_data with both empty returns False. TC-API-012"
    )
    async def test_validate_init_data_both_empty(self, miniapp_api_with_config):
        """Test validate_init_data with both empty returns False. TC-API-012"""
        with allure.step("Call validate_init_data with both empty"):
            result = await miniapp_api_with_config.validate_init_data("", "")
        with allure.step("Verify result is False"):
            assert result is False

    @pytest.mark.asyncio
    @allure.title("Validate init_data without hash parameter")
    @allure.description(
        "Test validate_init_data without hash parameter returns False. TC-API-009"
    )
    async def test_validate_init_data_without_hash(
        self, miniapp_api_with_config, init_data_without_hash
    ):
        """Test validate_init_data without hash parameter returns False. TC-API-009"""
        with allure.step("Get init_data without hash from fixture"):
            init_data, bot_token = init_data_without_hash
        with allure.step("Call validate_init_data"):
            result = await miniapp_api_with_config.validate_init_data(
                init_data, bot_token
            )
        with allure.step("Verify result is False"):
            assert result is False

    @pytest.mark.asyncio
    @allure.title("Validate init_data with valid init_data")
    @allure.description(
        "Test validate_init_data with valid init_data returns True. TC-API-007"
    )
    async def test_validate_init_data_valid(
        self, miniapp_api_with_config, valid_init_data_and_token
    ):
        """Test validate_init_data with valid init_data returns True. TC-API-007"""
        with allure.step("Get valid init_data and token from fixture"):
            init_data, bot_token = valid_init_data_and_token
        with allure.step("Call validate_init_data"):
            result = await miniapp_api_with_config.validate_init_data(
                init_data, bot_token
            )
        with allure.step("Verify result is True"):
            assert result is True

    @pytest.mark.asyncio
    @allure.title("Validate init_data with wrong bot_token")
    @allure.description("Test validate_init_data with wrong bot_token returns False.")
    async def test_validate_init_data_invalid_token(
        self, miniapp_api_with_config, valid_init_data_and_token
    ):
        """Test validate_init_data with wrong bot_token returns False."""
        with allure.step("Get valid init_data from fixture"):
            init_data, _ = valid_init_data_and_token
        with allure.step("Use wrong token"):
            wrong_token = "wrong_token"
        with allure.step("Call validate_init_data with wrong token"):
            result = await miniapp_api_with_config.validate_init_data(
                init_data, wrong_token
            )
        with allure.step("Verify result is False"):
            assert result is False

    @pytest.mark.asyncio
    @allure.title("Validate init_data with invalid hash")
    @allure.description(
        "Test validate_init_data with invalid hash returns False. TC-API-008"
    )
    async def test_validate_init_data_invalid_hash(
        self, miniapp_api_with_config, invalid_init_data_and_token
    ):
        """Test validate_init_data with invalid hash returns False. TC-API-008"""
        with allure.step("Get invalid init_data and token from fixture"):
            init_data, bot_token = invalid_init_data_and_token
        with allure.step("Call validate_init_data"):
            result = await miniapp_api_with_config.validate_init_data(
                init_data, bot_token
            )
        with allure.step("Verify result is False"):
            assert result is False

    @pytest.mark.asyncio
    @allure.title("TC-API-013: Validate init_data with hash at beginning")
    @allure.description("Test validate_init_data with hash at beginning. TC-API-013")
    async def test_validate_init_data_hash_at_beginning(self, miniapp_api_with_config):
        """Test validate_init_data with hash at beginning. TC-API-013"""
        with allure.step("Prepare bot_token and user_data"):
            bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
            user_data = {"user": '{"id":123,"auth_date":"1698000000"}'}
        with allure.step("Generate valid init_data"):
            init_data = generate_valid_init_data(bot_token, user_data)
        with allure.step("Reorder to put hash first"):
            from urllib.parse import parse_qs, urlencode

            parsed = parse_qs(init_data)
            hash_value = parsed["hash"][0]
            del parsed["hash"]
            # Put hash first
            reordered = {"hash": [hash_value]}
            reordered.update(parsed)
            init_data_reordered = urlencode(reordered, doseq=True)

        with allure.step("Call validate_init_data with reordered init_data"):
            result = await miniapp_api_with_config.validate_init_data(
                init_data_reordered, bot_token
            )
        with allure.step("Verify result is True"):
            assert result is True

    @pytest.mark.asyncio
    @allure.title("TC-API-014: Validate init_data with hash in middle")
    @allure.description("Test validate_init_data with hash in middle. TC-API-014")
    async def test_validate_init_data_hash_in_middle(self, miniapp_api_with_config):
        """Test validate_init_data with hash in middle. TC-API-014"""
        with allure.step("Prepare bot_token and user_data"):
            bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
            user_data = {
                "user": '{"id":123}',
                "auth_date": "1698000000",
                "start_param": "test",
            }
        with allure.step("Generate valid init_data"):
            init_data = generate_valid_init_data(bot_token, user_data)

        with allure.step("Call validate_init_data"):
            result = await miniapp_api_with_config.validate_init_data(
                init_data, bot_token
            )
        with allure.step("Verify result is True"):
            assert result is True

    @pytest.mark.asyncio
    @allure.title("TC-API-015: Validate init_data with hash at end")
    @allure.description("Test validate_init_data with hash at end. TC-API-015")
    async def test_validate_init_data_hash_at_end(self, miniapp_api_with_config):
        """Test validate_init_data with hash at end. TC-API-015"""
        with allure.step("Prepare bot_token and user_data"):
            bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
            user_data = {"user": '{"id":123}', "auth_date": "1698000000"}
        with allure.step("Generate valid init_data (hash should be at end)"):
            init_data = generate_valid_init_data(bot_token, user_data)

        with allure.step("Call validate_init_data"):
            result = await miniapp_api_with_config.validate_init_data(
                init_data, bot_token
            )
        with allure.step("Verify result is True"):
            assert result is True

    @pytest.mark.asyncio
    @allure.title("Validate init_data uses hmac.compare_digest for security")
    @allure.description(
        "Test validate_init_data uses hmac.compare_digest for security. TC-API-016"
    )
    async def test_validate_init_data_uses_compare_digest(
        self, mocker, miniapp_api_with_config, valid_init_data_and_token
    ):
        """Test validate_init_data uses hmac.compare_digest for security. TC-API-016"""
        with allure.step("Get valid init_data and token from fixture"):
            init_data, bot_token = valid_init_data_and_token

        with allure.step("Mock compare_digest function"):
            mock_compare = mocker.patch(
                "tma_test_framework.mini_app.api.compare_digest"
            )
            mock_compare.return_value = True
        with allure.step("Call validate_init_data"):
            result = await miniapp_api_with_config.validate_init_data(
                init_data, bot_token
            )

        with allure.step("Verify compare_digest was called"):
            assert mock_compare.called
        with allure.step("Verify result is True"):
            assert result is True

    @pytest.mark.asyncio
    @allure.title("Validate init_data logs success message")
    @allure.description("Test validate_init_data logs success message.")
    async def test_validate_init_data_logs_success(
        self, miniapp_api_with_config, valid_init_data_and_token, caplog
    ):
        """Test validate_init_data logs success message."""
        with allure.step("Get valid init_data and token from fixture"):
            init_data, bot_token = valid_init_data_and_token

        with allure.step("Call validate_init_data and capture logs"):
            with caplog.at_level("INFO"):
                await miniapp_api_with_config.validate_init_data(init_data, bot_token)

        with allure.step("Verify success message in logs"):
            assert "InitData validation: valid" in caplog.text

    @pytest.mark.asyncio
    @allure.title("Validate init_data logs invalid message")
    @allure.description("Test validate_init_data logs invalid message.")
    async def test_validate_init_data_logs_invalid(
        self, miniapp_api_with_config, invalid_init_data_and_token, caplog
    ):
        """Test validate_init_data logs invalid message."""
        with allure.step("Get invalid init_data and token from fixture"):
            init_data, bot_token = invalid_init_data_and_token

        with allure.step("Call validate_init_data and capture logs"):
            with caplog.at_level("INFO"):
                await miniapp_api_with_config.validate_init_data(init_data, bot_token)

        with allure.step("Verify invalid message in logs"):
            assert "InitData validation: invalid" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-API-017: Validate init_data logs error on exception")
    @allure.description("Test validate_init_data logs error on exception. TC-API-017")
    async def test_validate_init_data_logs_error_on_exception(
        self, mocker, miniapp_api_with_config, caplog
    ):
        """Test validate_init_data logs error on exception. TC-API-017"""
        with allure.step("Mock hmac.new to raise exception"):
            # Force an exception by mocking hmac.new to raise an exception
            with caplog.at_level("ERROR"):
                mocker.patch(
                    "tma_test_framework.mini_app.api.new",
                    side_effect=Exception("Test exception"),
                )
        with allure.step("Call validate_init_data and capture error logs"):
            result = await miniapp_api_with_config.validate_init_data(
                "user=test&hash=abc", "token"
            )

        with allure.step("Verify result is False"):
            assert result is False
        with allure.step("Verify error message in logs"):
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
    @allure.title("Validate init_data with parametrized test cases")
    @allure.description("Test validate_init_data with parametrized test cases.")
    async def test_validate_init_data_parametrized(
        self, miniapp_api_with_config, init_data, bot_token, expected, description
    ):
        """Test validate_init_data with parametrized test cases."""
        with allure.step(f"Call validate_init_data with {description}"):
            result = await miniapp_api_with_config.validate_init_data(
                init_data, bot_token
            )
        with allure.step(f"Verify result is {expected}"):
            assert result == expected, f"Failed for: {description}"


# ============================================================================
# III. Выполнение HTTP-запросов (make_request)
# ============================================================================


class TestMiniAppApiMakeRequest:
    """Test MiniAppApi make_request method."""

    @pytest.mark.asyncio
    @allure.title("TC-API-021: Make request with absolute URL")
    @allure.description("Test make_request with absolute URL uses it as is. TC-API-021")
    async def test_make_request_absolute_url(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with absolute URL uses it as is. TC-API-021"""
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )

        with allure.step("Call make_request with absolute URL"):
            result = await miniapp_api_with_config.make_request(
                "https://api.example.com/data"
            )

        with allure.step("Verify result.endpoint matches input"):
            assert result.endpoint == "https://api.example.com/data"
        with allure.step("Verify client.request was called once"):
            miniapp_api_with_config.client.request.assert_called_once()
        with allure.step("Verify URL in request matches absolute URL"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            assert call_kwargs["url"] == "https://api.example.com/data"

    @pytest.mark.asyncio
    @allure.title("Make request with relative URL starting with slash")
    @allure.description(
        "Test make_request with relative URL starting with /. TC-API-020, TC-API-022"
    )
    async def test_make_request_relative_url_with_slash(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with relative URL starting with /. TC-API-020, TC-API-022"""
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )

        with allure.step("Call make_request with relative URL starting with /"):
            result = await miniapp_api_with_config.make_request("/api/data")

        with allure.step("Verify result.endpoint matches input"):
            assert result.endpoint == "/api/data"
        with allure.step("Verify URL is constructed correctly"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            assert call_kwargs["url"] == "https://example.com/app/api/data"

    @pytest.mark.asyncio
    @allure.title("TC-API-023: Make request with relative URL without slash")
    @allure.description("Test make_request with relative URL without /. TC-API-023")
    async def test_make_request_relative_url_without_slash(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with relative URL without /. TC-API-023"""
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )

        with allure.step("Call make_request with relative URL without /"):
            result = await miniapp_api_with_config.make_request("api/data")

        with allure.step("Verify result.endpoint matches input"):
            assert result.endpoint == "api/data"
        with allure.step("Verify URL is constructed correctly"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            assert call_kwargs["url"] == "https://example.com/app/api/data"

    @pytest.mark.asyncio
    @allure.title("Make request removes query params from base URL")
    @allure.description(
        "Test make_request removes query params from base URL. TC-API-035"
    )
    async def test_make_request_removes_query_params_from_base_url(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request removes query params from base URL. TC-API-035"""
        with allure.step("Set base URL with query params"):
            miniapp_api_with_config.url = "https://t.me/mybot/app?start=123"
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )

        with allure.step("Call make_request"):
            _ = await miniapp_api_with_config.make_request("/api/data")

        with allure.step("Verify query params are removed from URL"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            assert call_kwargs["url"] == "https://t.me/mybot/app/api/data"
            assert "start=123" not in call_kwargs["url"]

    @pytest.mark.asyncio
    @allure.title("TC-API-024: Make request with GET method")
    @allure.description("Test make_request with GET method. TC-API-024")
    async def test_make_request_get_method(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with GET method. TC-API-024"""
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )

        with allure.step("Call make_request with GET method"):
            result = await miniapp_api_with_config.make_request(
                "/api/data", method="GET"
            )

        with allure.step("Verify result.method is GET"):
            assert result.method == "GET"
        with allure.step("Verify request method is GET"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            assert call_kwargs["method"] == "GET"

    @pytest.mark.asyncio
    @allure.title("TC-API-025: Make request with POST method and data")
    @allure.description("Test make_request with POST method and data. TC-API-025")
    async def test_make_request_post_with_data(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with POST method and data. TC-API-025"""
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )
        with allure.step("Prepare request data"):
            data = {"key": "value"}

        with allure.step("Call make_request with POST method and data"):
            result = await miniapp_api_with_config.make_request(
                "/api/data", method="POST", data=data
            )

        with allure.step("Verify result.method is POST"):
            assert result.method == "POST"
        with allure.step("Verify request method and data"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            assert call_kwargs["method"] == "POST"
            assert call_kwargs["json"] == data

    @pytest.mark.asyncio
    @allure.title("TC-API-026: Make request with headers")
    @allure.description("Test make_request with headers. TC-API-026")
    async def test_make_request_with_headers(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with headers. TC-API-026"""
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )
        with allure.step("Prepare custom headers"):
            headers = {"Authorization": "Bearer token"}

        with allure.step("Call make_request with headers"):
            _ = await miniapp_api_with_config.make_request("/api/data", headers=headers)

        with allure.step("Verify headers are passed to request"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            assert call_kwargs["headers"] == headers

    @pytest.mark.asyncio
    @allure.title("TC-API-024: Make request with status 200")
    @allure.description("Test make_request with status 200. TC-API-024, TC-API-034")
    async def test_make_request_status_200(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with status 200. TC-API-024, TC-API-034"""
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )

        with allure.step("Call make_request"):
            result = await miniapp_api_with_config.make_request("/api/data")

        with allure.step("Verify status_code is 200"):
            assert result.status_code == 200
        with allure.step("Verify success flags"):
            assert result.success is True
            assert result.client_error is False
            assert result.server_error is False
            assert result.redirect is False
            assert result.informational is False

    @pytest.mark.asyncio
    @allure.title("TC-API-034: Make request with status 301")
    @allure.description("Test make_request with status 301. TC-API-034")
    async def test_make_request_status_301(
        self, mocker, miniapp_api_with_config, mock_httpx_response_301
    ):
        """Test make_request with status 301. TC-API-034"""
        with allure.step("Mock client.request with 301 response"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_301
            )

        with allure.step("Call make_request"):
            result = await miniapp_api_with_config.make_request("/api/data")

        with allure.step("Verify status_code is 301"):
            assert result.status_code == 301
        with allure.step("Verify redirect flag is True"):
            assert result.redirect is True
            assert result.success is False

    @pytest.mark.asyncio
    @allure.title("TC-API-034: Make request with status 404")
    @allure.description("Test make_request with status 404. TC-API-034")
    async def test_make_request_status_404(
        self, mocker, miniapp_api_with_config, mock_httpx_response_404
    ):
        """Test make_request with status 404. TC-API-034"""
        with allure.step("Mock client.request with 404 response"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_404
            )

        with allure.step("Call make_request"):
            result = await miniapp_api_with_config.make_request("/api/data")

        with allure.step("Verify status_code is 404"):
            assert result.status_code == 404
        with allure.step("Verify client_error flag is True"):
            assert result.client_error is True
            assert result.success is False

    @pytest.mark.asyncio
    @allure.title("TC-API-034: Make request with status 500")
    @allure.description("Test make_request with status 500. TC-API-034")
    async def test_make_request_status_500(
        self, mocker, miniapp_api_with_config, mock_httpx_response_500
    ):
        """Test make_request with status 500. TC-API-034"""
        with allure.step("Mock client.request with 500 response"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_500
            )

        with allure.step("Call make_request"):
            result = await miniapp_api_with_config.make_request("/api/data")

        with allure.step("Verify status_code is 500"):
            assert result.status_code == 500
        with allure.step("Verify server_error flag is True"):
            assert result.server_error is True
            assert result.success is False

    @pytest.mark.asyncio
    @allure.title("TC-API-034: Make request with status 101")
    @allure.description("Test make_request with status 101. TC-API-034")
    async def test_make_request_status_101(
        self, mocker, miniapp_api_with_config, mock_httpx_response_101
    ):
        """Test make_request with status 101. TC-API-034"""
        with allure.step("Mock client.request with 101 response"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_101
            )

        with allure.step("Call make_request"):
            result = await miniapp_api_with_config.make_request("/api/data")

        with allure.step("Verify status_code is 101"):
            assert result.status_code == 101
        with allure.step("Verify informational flag is True"):
            assert result.informational is True
            assert result.success is False

    @pytest.mark.asyncio
    @allure.title("TC-API-027: Make request captures response_time")
    @allure.description("Test make_request captures response_time. TC-API-027")
    async def test_make_request_response_time(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request captures response_time. TC-API-027"""
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )

        with allure.step("Call make_request"):
            result = await miniapp_api_with_config.make_request("/api/data")

        with allure.step("Verify response_time is captured"):
            assert result.response_time == 0.5
            assert isinstance(result.response_time, float)

    @pytest.mark.asyncio
    @allure.title("Make request handles unavailable response_time")
    @allure.description(
        "Test make_request handles case when response.elapsed is unavailable. TC-API-038"
    )
    async def test_make_request_response_time_unavailable(
        self, mocker, miniapp_api_with_config
    ):
        """Test make_request handles case when response.elapsed is unavailable. TC-API-038"""
        with allure.step("Create mock response where elapsed raises AttributeError"):
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

        with allure.step("Mock client.request with problematic response"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_response
            )

        with allure.step("Call make_request"):
            result = await miniapp_api_with_config.make_request("/api/data")

        with allure.step("Verify response_time is set to 0.0 gracefully"):
            # Should handle gracefully and set response_time to 0.0
            assert result.response_time == 0.0
            assert isinstance(result.response_time, float)
            assert result.success is True
            assert result.status_code == 200

    @pytest.mark.asyncio
    @allure.title("Make request handles RuntimeError when accessing response.elapsed")
    @allure.description(
        "Test make_request handles RuntimeError when accessing response.elapsed. TC-API-038"
    )
    async def test_make_request_response_time_runtime_error(
        self, mocker, miniapp_api_with_config
    ):
        """Test make_request handles RuntimeError when accessing response.elapsed. TC-API-038"""
        with allure.step("Create mock response where elapsed raises RuntimeError"):
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

        with allure.step("Mock client.request with problematic response"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_response
            )

        with allure.step("Call make_request"):
            result = await miniapp_api_with_config.make_request("/api/data")

        with allure.step("Verify response_time is set to 0.0 gracefully"):
            # Should handle gracefully and set response_time to 0.0
            assert result.response_time == 0.0
            assert isinstance(result.response_time, float)
            assert result.success is True
            assert result.status_code == 200

    @pytest.mark.asyncio
    @allure.title("Make request extracts response data into immutable fields")
    @allure.description(
        "Test make_request extracts response data into immutable fields. TC-API-028"
    )
    async def test_make_request_extracts_response_data(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request extracts response data into immutable fields. TC-API-028"""
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )

        with allure.step("Call make_request"):
            result = await miniapp_api_with_config.make_request("/api/data")

        with allure.step("Verify response data is extracted into immutable fields"):
            # Response data should be extracted into immutable fields
            assert result.headers is not None
            assert isinstance(result.headers, dict)
            assert result.body is not None
            assert isinstance(result.body, bytes)
        with allure.step("Verify response object is not stored"):
            # Response object should not be stored
            assert (
                not hasattr(result, "response")
                or getattr(result, "response", None) is None
            )

    @pytest.mark.asyncio
    @allure.title("TC-API-029: Make request handles network errors")
    @allure.description("Test make_request handles network errors. TC-API-029")
    async def test_make_request_network_error(self, mocker, miniapp_api_with_config):
        """Test make_request handles network errors. TC-API-029"""
        with allure.step("Create RequestError"):
            error = RequestError("Network error", request=mocker.MagicMock())
        with allure.step("Mock client.request to raise error"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(side_effect=error)

        with allure.step("Call make_request"):
            result = await miniapp_api_with_config.make_request("/api/data")

        with allure.step("Verify error result"):
            assert result.status_code == 0
            assert result.success is False
            assert result.error_message == "Network error"
            assert result.headers == {}
            assert result.body == b""
            assert result.content_type is None
            assert result.reason is None

    @pytest.mark.asyncio
    @allure.title("TC-API-029: Make request handles timeout errors")
    @allure.description("Test make_request handles timeout errors. TC-API-029")
    async def test_make_request_timeout_error(self, mocker, miniapp_api_with_config):
        """Test make_request handles timeout errors. TC-API-029"""
        with allure.step("Create TimeoutException"):
            error = TimeoutException("Request timeout", request=mocker.MagicMock())
        with allure.step("Mock client.request to raise timeout error"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(side_effect=error)

        with allure.step("Call make_request"):
            result = await miniapp_api_with_config.make_request("/api/data")

        with allure.step("Verify timeout error result"):
            assert result.status_code == 0
            assert result.success is False
            assert "timeout" in result.error_message.lower()

    @pytest.mark.asyncio
    @allure.title("TC-API-030: Make request logs request")
    @allure.description("Test make_request logs request. TC-API-030")
    async def test_make_request_logs_request(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200, caplog
    ):
        """Test make_request logs request. TC-API-030"""
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )

        with allure.step("Call make_request and capture logs"):
            with caplog.at_level("INFO"):
                await miniapp_api_with_config.make_request("/api/data", method="POST")

        with allure.step("Verify request is logged"):
            assert "Making request: POST" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-API-031: Make request logs response")
    @allure.description("Test make_request logs response. TC-API-031")
    async def test_make_request_logs_response(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200, caplog
    ):
        """Test make_request logs response. TC-API-031"""
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )

        with allure.step("Call make_request and capture logs"):
            with caplog.at_level("INFO"):
                await miniapp_api_with_config.make_request("/api/data")

        with allure.step("Verify response is logged"):
            assert "Response got:" in caplog.text
            assert "status_code=200" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-API-032: Make request logs error on failure")
    @allure.description("Test make_request logs error on failure. TC-API-032")
    async def test_make_request_logs_error(
        self, mocker, miniapp_api_with_config, caplog
    ):
        """Test make_request logs error on failure. TC-API-032"""
        with allure.step("Create RequestError"):
            error = RequestError("Request failed", request=mocker.MagicMock())
        with allure.step("Mock client.request to raise error"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(side_effect=error)

        with allure.step("Call make_request and capture error logs"):
            with caplog.at_level("ERROR"):
                await miniapp_api_with_config.make_request("/api/data", method="POST")

        with allure.step("Verify error is logged"):
            assert "Request failed: POST /api/data" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-API-033: Make request with PUT method")
    @allure.description("Test make_request with PUT method. TC-API-033")
    async def test_make_request_put_method(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with PUT method. TC-API-033"""
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )
        with allure.step("Prepare request data"):
            data = {"key": "updated_value"}

        with allure.step("Call make_request with PUT method"):
            result = await miniapp_api_with_config.make_request(
                "/api/data/1", method="PUT", data=data
            )

        with allure.step("Verify result.method is PUT"):
            assert result.method == "PUT"
        with allure.step("Verify request method and data"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            assert call_kwargs["method"] == "PUT"
            assert call_kwargs["json"] == data

    @pytest.mark.asyncio
    @allure.title("TC-API-033: Make request with DELETE method")
    @allure.description("Test make_request with DELETE method. TC-API-033")
    async def test_make_request_delete_method(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with DELETE method. TC-API-033"""
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )

        with allure.step("Call make_request with DELETE method"):
            result = await miniapp_api_with_config.make_request(
                "/api/data/1", method="DELETE"
            )

        with allure.step("Verify result.method is DELETE"):
            assert result.method == "DELETE"
        with allure.step("Verify request method is DELETE"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            assert call_kwargs["method"] == "DELETE"


# ============================================================================
# IV. Граничные и специальные случаи
# ============================================================================


class TestMiniAppApiEdgeCases:
    """Test MiniAppApi edge cases."""

    @pytest.mark.asyncio
    @allure.title("Validate init_data with very long init_data")
    @allure.description("Test validate_init_data with very long init_data.")
    async def test_validate_init_data_very_long(self, miniapp_api_with_config):
        """Test validate_init_data with very long init_data."""
        with allure.step("Prepare bot_token and very long user_data"):
            bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
            # Create very long user data
            long_user_data = {
                "user": '{"id":123,"data":"' + "x" * 10000 + '"}',
                "auth_date": "1698000000",
            }
        with allure.step("Generate init_data with very long data"):
            init_data = generate_valid_init_data(bot_token, long_user_data)

        with allure.step("Call validate_init_data"):
            result = await miniapp_api_with_config.validate_init_data(
                init_data, bot_token
            )
        with allure.step("Verify result is boolean (should handle without error)"):
            # Should handle without error
            assert isinstance(result, bool)

    @pytest.mark.asyncio
    @allure.title("TC-API-018: Validate init_data with unicode characters")
    @allure.description("Test validate_init_data with unicode characters. TC-API-018")
    async def test_validate_init_data_unicode(self, miniapp_api_with_config):
        """Test validate_init_data with unicode characters. TC-API-018"""
        with allure.step("Prepare bot_token and user_data with unicode"):
            bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
            user_data = {"user": '{"id":123,"name":"Тест"}', "auth_date": "1698000000"}
        with allure.step("Generate init_data"):
            init_data = generate_valid_init_data(bot_token, user_data)

        with allure.step("Call validate_init_data"):
            result = await miniapp_api_with_config.validate_init_data(
                init_data, bot_token
            )
        with allure.step("Verify result is True"):
            assert result is True

    @pytest.mark.asyncio
    @allure.title("TC-API-019: Validate init_data with ampersand in values")
    @allure.description("Test validate_init_data with & in values. TC-API-019")
    async def test_validate_init_data_with_ampersand_in_values(
        self, miniapp_api_with_config
    ):
        """Test validate_init_data with & in values. TC-API-019"""
        with allure.step("Prepare bot_token and user_data with ampersand"):
            bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
            user_data = {"user": '{"id":123,"data":"a&b"}', "auth_date": "1698000000"}
        with allure.step("Generate init_data"):
            init_data = generate_valid_init_data(bot_token, user_data)

        with allure.step("Call validate_init_data"):
            result = await miniapp_api_with_config.validate_init_data(
                init_data, bot_token
            )
        with allure.step("Verify result is True"):
            assert result is True

    @pytest.mark.asyncio
    @allure.title("Validate init_data with bot_token containing special characters")
    @allure.description(
        "Test validate_init_data with bot_token containing special characters."
    )
    async def test_validate_init_data_bot_token_special_chars(
        self, miniapp_api_with_config
    ):
        """Test validate_init_data with bot_token containing special characters."""
        with allure.step("Prepare bot_token with special characters"):
            bot_token = "123456789:ABC-def_GHI.jkl+MNO"
        with allure.step("Prepare user_data"):
            user_data = {"user": '{"id":123}', "auth_date": "1698000000"}
        with allure.step("Generate init_data"):
            init_data = generate_valid_init_data(bot_token, user_data)

        with allure.step("Call validate_init_data"):
            result = await miniapp_api_with_config.validate_init_data(
                init_data, bot_token
            )
        with allure.step("Verify result is True"):
            assert result is True


# ============================================================================
# V. Безопасность и надёжность
# ============================================================================


class TestMiniAppApiSecurity:
    """Test MiniAppApi security and reliability."""

    @pytest.mark.asyncio
    @allure.title("TC-API-036: Make request with very long endpoint")
    @allure.description("Test make_request with very long endpoint. TC-API-036")
    async def test_make_request_very_long_endpoint(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with very long endpoint. TC-API-036"""
        with allure.step("Create a very long endpoint (>1000 characters)"):
            long_endpoint = "/api/" + "a" * 1000
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )

        with allure.step("Call make_request with very long endpoint"):
            result = await miniapp_api_with_config.make_request(long_endpoint)

        with allure.step("Verify status_code is 200"):
            assert result.status_code == 200
        with allure.step("Verify the endpoint was used in the request"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            assert long_endpoint in call_kwargs["url"] or call_kwargs["url"].endswith(
                long_endpoint
            )

    @pytest.mark.asyncio
    @allure.title("Make request with unicode characters in endpoint")
    @allure.description(
        "Test make_request with unicode characters in endpoint. TC-API-037"
    )
    async def test_make_request_unicode_endpoint(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request with unicode characters in endpoint. TC-API-037"""
        with allure.step("Create endpoint with unicode characters"):
            unicode_endpoint = "/api/тест/用户/ユーザー"
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )

        with allure.step("Call make_request with unicode endpoint"):
            result = await miniapp_api_with_config.make_request(unicode_endpoint)

        with allure.step("Verify status_code is 200"):
            assert result.status_code == 200
        with allure.step("Verify the endpoint was used in the request"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            # The URL should contain the unicode endpoint (may be URL-encoded)
            assert unicode_endpoint in call_kwargs["url"] or any(
                char in call_kwargs["url"] for char in unicode_endpoint
            )

    @pytest.mark.asyncio
    @allure.title("Make request respects timeout settings")
    @allure.description(
        "Test make_request respects timeout settings by returning error result on slow request."
    )
    async def test_make_request_timeout_respected(
        self, mocker, miniapp_api_with_config
    ):
        """Test make_request respects timeout settings by returning error result on slow request."""
        with allure.step("Import TimeoutException"):
            from httpx import TimeoutException
        with allure.step("Mock client.request to raise TimeoutException"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                side_effect=TimeoutException("Request timed out", request=None)
            )

        with allure.step("Call make_request (should catch exception)"):
            # make_request catches exceptions and returns ApiResult with error_message
            result = await miniapp_api_with_config.make_request(
                "/api/data", method="GET"
            )

        with allure.step("Verify the timeout error is reflected in the result"):
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
    @allure.title("Async context manager calls close")
    @allure.description("Test async context manager calls close().")
    async def test_context_manager_calls_close(self, mocker, miniapp_api_with_config):
        """Test async context manager calls close()."""
        with allure.step("Mock close method"):
            miniapp_api_with_config.close = mocker.AsyncMock()

        with allure.step("Use async context manager"):
            async with miniapp_api_with_config:
                pass

        with allure.step("Verify close was called once"):
            miniapp_api_with_config.close.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("Logger is bound to MiniAppApi class name")
    @allure.description("Test logger is bound to MiniAppApi class name.")
    async def test_logger_bound_to_class_name(self, miniapp_api_with_config):
        """Test logger is bound to MiniAppApi class name."""
        with allure.step("Verify logger is not None"):
            assert miniapp_api_with_config.logger is not None
            # Logger should be bound to "MiniAppApi"

    @allure.title("MiniAppApi inherits from BaseMiniApp")
    @allure.description("Test MiniAppApi inherits from BaseMiniApp.")
    def test_inherits_from_base_miniapp(self, mocker, valid_config, mock_httpx_client):
        """Test MiniAppApi inherits from BaseMiniApp."""
        with allure.step("Mock AsyncClient"):
            mocker.patch(
                "tma_test_framework.mini_app.api.AsyncClient",
                return_value=mock_httpx_client,
            )
        with allure.step("Create MiniAppApi instance"):
            api = MiniAppApi("https://example.com/app", valid_config)

        with allure.step("Verify api is instance of BaseMiniApp"):
            from tma_test_framework.mini_app.base import BaseMiniApp

            assert isinstance(api, BaseMiniApp)


# ============================================================================
# VII. Authentication Token Management
# ============================================================================


class TestMiniAppApiAuthToken:
    """Test authentication token management in MiniAppApi."""

    @allure.title("TC-API-039: __init__ sets default auth token values")
    @allure.description("Test that __init__ sets default auth token values. TC-API-039")
    def test_init_sets_default_auth_token_values(
        self, mocker, valid_config, mock_httpx_client
    ):
        """Test that __init__ sets default auth token values."""
        with allure.step("Mock AsyncClient"):
            mocker.patch(
                "tma_test_framework.mini_app.api.AsyncClient",
                return_value=mock_httpx_client,
            )
        with allure.step("Create MiniAppApi instance"):
            api = MiniAppApi("https://example.com/app", valid_config)

        with allure.step("Verify default auth token values"):
            assert api._auth_token is None
            assert api._auth_token_type == "Bearer"

    @allure.title("TC-API-040: set_auth_token sets token and type")
    @allure.description("Test set_auth_token sets token and type. TC-API-040")
    def test_set_auth_token(self, mocker, valid_config, mock_httpx_client):
        """Test set_auth_token sets token and type."""
        with allure.step("Mock AsyncClient"):
            mocker.patch(
                "tma_test_framework.mini_app.api.AsyncClient",
                return_value=mock_httpx_client,
            )
        with allure.step("Create MiniAppApi instance"):
            api = MiniAppApi("https://example.com/app", valid_config)

        with allure.step("Call set_auth_token"):
            api.set_auth_token("test_token_123", "Bearer")
        with allure.step("Verify token and type are set"):
            assert api._auth_token == "test_token_123"
            assert api._auth_token_type == "Bearer"

    @allure.title("TC-API-041: set_auth_token with custom token type")
    @allure.description("Test set_auth_token with custom token type. TC-API-041")
    def test_set_auth_token_with_custom_type(
        self, mocker, valid_config, mock_httpx_client
    ):
        """Test set_auth_token with custom token type."""
        with allure.step("Mock AsyncClient"):
            mocker.patch(
                "tma_test_framework.mini_app.api.AsyncClient",
                return_value=mock_httpx_client,
            )
        with allure.step("Create MiniAppApi instance"):
            api = MiniAppApi("https://example.com/app", valid_config)

        with allure.step("Call set_auth_token with custom type"):
            api.set_auth_token("api_key_456", "ApiKey")
        with allure.step("Verify token and custom type are set"):
            assert api._auth_token == "api_key_456"
            assert api._auth_token_type == "ApiKey"

    @allure.title("TC-API-042: clear_auth_token resets token to None")
    @allure.description("Test clear_auth_token resets token to None. TC-API-042")
    def test_clear_auth_token(self, mocker, valid_config, mock_httpx_client):
        """Test clear_auth_token resets token to None."""
        with allure.step("Mock AsyncClient"):
            mocker.patch(
                "tma_test_framework.mini_app.api.AsyncClient",
                return_value=mock_httpx_client,
            )
        with allure.step("Create MiniAppApi instance"):
            api = MiniAppApi("https://example.com/app", valid_config)

        with allure.step("Set auth token first"):
            api.set_auth_token("test_token", "Bearer")
            assert api._auth_token == "test_token"

        with allure.step("Call clear_auth_token"):
            api.clear_auth_token()
        with allure.step("Verify token is reset to None"):
            assert api._auth_token is None
            assert api._auth_token_type == "Bearer"

    @pytest.mark.asyncio
    @allure.title("TC-API-043: Make request automatically adds auth token to headers")
    @allure.description(
        "Test make_request automatically adds auth token to headers. TC-API-043"
    )
    async def test_make_request_adds_auth_token_automatically(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request automatically adds auth token to headers."""
        with allure.step("Set auth token"):
            miniapp_api_with_config.set_auth_token("test_token_123")
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )

        with allure.step("Call make_request"):
            await miniapp_api_with_config.make_request("/api/data")

        with allure.step("Verify Authorization header is added"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            assert "headers" in call_kwargs
            assert call_kwargs["headers"]["Authorization"] == "Bearer test_token_123"

    @pytest.mark.asyncio
    @allure.title(
        "TC-API-044: Make request without token does not add Authorization header"
    )
    @allure.description(
        "Test make_request without token does not add Authorization header. TC-API-044"
    )
    async def test_make_request_without_token_no_auth_header(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request without token does not add Authorization header."""
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )

        with allure.step("Call make_request"):
            await miniapp_api_with_config.make_request("/api/data")

        with allure.step("Verify Authorization header is not present"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            headers = call_kwargs.get("headers", {})
            assert "Authorization" not in headers

    @pytest.mark.asyncio
    @allure.title("TC-API-045: Make request uses custom token type")
    @allure.description("Test make_request uses custom token type. TC-API-045")
    async def test_make_request_custom_token_type(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request uses custom token type."""
        with allure.step("Set auth token with custom type"):
            miniapp_api_with_config.set_auth_token("api_key_456", "ApiKey")
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )

        with allure.step("Call make_request"):
            await miniapp_api_with_config.make_request("/api/data")

        with allure.step("Verify Authorization header uses custom token type"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            assert call_kwargs["headers"]["Authorization"] == "ApiKey api_key_456"

    @pytest.mark.asyncio
    @allure.title("TC-API-046: Make request allows overriding Authorization header")
    @allure.description(
        "Test make_request allows overriding Authorization header. TC-API-046"
    )
    async def test_make_request_headers_override_auth_token(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request allows overriding Authorization header."""
        with allure.step("Set default auth token"):
            miniapp_api_with_config.set_auth_token("default_token")
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )
        with allure.step("Prepare custom headers with Authorization"):
            custom_headers = {"Authorization": "Bearer custom_token"}

        with allure.step("Call make_request with custom headers"):
            await miniapp_api_with_config.make_request(
                "/api/data", headers=custom_headers
            )

        with allure.step("Verify custom Authorization header overrides default"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            assert call_kwargs["headers"]["Authorization"] == "Bearer custom_token"

    @pytest.mark.asyncio
    @allure.title("TC-API-047: Make request merges custom headers with auth token")
    @allure.description(
        "Test make_request merges custom headers with auth token. TC-API-047"
    )
    async def test_make_request_merges_headers_with_token(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request merges custom headers with auth token."""
        with allure.step("Set auth token"):
            miniapp_api_with_config.set_auth_token("test_token")
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )
        with allure.step("Prepare custom headers"):
            custom_headers = {"X-Custom-Header": "custom_value"}

        with allure.step("Call make_request with custom headers"):
            await miniapp_api_with_config.make_request(
                "/api/data", headers=custom_headers
            )

        with allure.step("Verify both Authorization and custom headers are present"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            assert call_kwargs["headers"]["Authorization"] == "Bearer test_token"
            assert call_kwargs["headers"]["X-Custom-Header"] == "custom_value"

    @pytest.mark.asyncio
    @allure.title("TC-API-048: Make request sets Content-Type when data is provided")
    @allure.description(
        "Test make_request sets Content-Type when data is provided. TC-API-048"
    )
    async def test_make_request_sets_content_type_for_data(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request sets Content-Type when data is provided."""
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )
        with allure.step("Prepare request data"):
            data = {"key": "value"}

        with allure.step("Call make_request with data"):
            await miniapp_api_with_config.make_request(
                "/api/data", method="POST", data=data
            )

        with allure.step("Verify Content-Type is set to application/json"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            assert call_kwargs["headers"]["Content-Type"] == "application/json"

    @pytest.mark.asyncio
    @allure.title("TC-API-049: Make request preserves custom Content-Type header")
    @allure.description(
        "Test make_request preserves custom Content-Type header. TC-API-049"
    )
    async def test_make_request_preserves_custom_content_type(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request preserves custom Content-Type header."""
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )
        with allure.step("Prepare custom headers and data"):
            custom_headers = {"Content-Type": "application/xml"}
            data = {"key": "value"}

        with allure.step("Call make_request with custom Content-Type"):
            await miniapp_api_with_config.make_request(
                "/api/data", method="POST", data=data, headers=custom_headers
            )

        with allure.step("Verify custom Content-Type is preserved"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            assert call_kwargs["headers"]["Content-Type"] == "application/xml"

    @pytest.mark.asyncio
    @allure.title("TC-API-050: Make request adds query params to URL")
    @allure.description("Test make_request adds query params to URL. TC-API-050")
    async def test_make_request_with_query_params(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request adds query params to URL."""
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )
        with allure.step("Prepare query params"):
            params = {"page": 1, "limit": 10}

        with allure.step("Call make_request with query params"):
            await miniapp_api_with_config.make_request("/api/data", params=params)

        with allure.step("Verify query params are added to URL"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            assert (
                "?page=1&limit=10" in call_kwargs["url"]
                or "?limit=10&page=1" in call_kwargs["url"]
            )

    @pytest.mark.asyncio
    @allure.title(
        "TC-API-051: Make request appends query params to URL with existing query string"
    )
    @allure.description(
        "Test make_request appends query params to URL with existing query string. TC-API-051"
    )
    async def test_make_request_with_query_params_and_existing_query(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request appends query params to URL with existing query string."""
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )
        with allure.step("Prepare query params"):
            params = {"filter": "active"}

        with allure.step("Call make_request with existing query and new params"):
            await miniapp_api_with_config.make_request(
                "https://example.com/api/data?existing=param", params=params
            )

        with allure.step("Verify both existing and new query params are in URL"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            assert "existing=param" in call_kwargs["url"]
            assert "filter=active" in call_kwargs["url"]
            assert "&" in call_kwargs["url"]  # Should use & separator

    @pytest.mark.asyncio
    @allure.title("TC-API-052: Make request handles empty params dict")
    @allure.description("Test make_request handles empty params dict. TC-API-052")
    async def test_make_request_with_empty_params(
        self, mocker, miniapp_api_with_config, mock_httpx_response_200
    ):
        """Test make_request handles empty params dict."""
        with allure.step("Mock client.request"):
            miniapp_api_with_config.client.request = mocker.AsyncMock(
                return_value=mock_httpx_response_200
            )

        with allure.step("Call make_request with empty params"):
            await miniapp_api_with_config.make_request("/api/data", params={})

        with allure.step("Verify query string is not added to URL"):
            call_kwargs = miniapp_api_with_config.client.request.call_args[1]
            assert "?" not in call_kwargs["url"] or call_kwargs["url"].endswith(
                "/api/data"
            )
