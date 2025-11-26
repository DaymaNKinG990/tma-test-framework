"""
Integration tests for ApiClient.setup_tma_auth() with UserTelegramClient.
Tests verify integration between ApiClient.setup_tma_auth() and UserTelegramClient.
"""

import allure
import pytest
from httpx import Response
from datetime import timedelta
from http import HTTPStatus

from tma_test_framework.clients.mtproto_client import UserInfo
from tma_test_framework.clients.api_client import ApiClient as MiniAppApi


@pytest.mark.integration
class TestMTProtoApiAuthIntegration:
    """Integration tests for ApiClient.setup_tma_auth() with UserTelegramClient."""

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-AUTH-001: setup_tma_auth with UserTelegramClient")
    @allure.description(
        "TC-INTEGRATION-AUTH-001: setup_tma_auth with UserTelegramClient. "
        "Verify setup_tma_auth integrates with UserTelegramClient to automatically get user info."
    )
    async def test_setup_tma_auth_with_user_telegram_client(
        self,
        mocker,
        user_telegram_client_connected,
        valid_config,
        mock_mini_app_url,
        mock_httpx_response_basic,
    ):
        """
        TC-INTEGRATION-AUTH-001: setup_tma_auth with UserTelegramClient.

        Verify setup_tma_auth integrates with UserTelegramClient to automatically get user info.
        """
        with allure.step("Create ApiClient with Mini App URL"):
            api_client = MiniAppApi(mock_mini_app_url, valid_config)

        with allure.step("Mock UserTelegramClient.get_me() to return user info"):
            mock_user_info = UserInfo(
                id=123456789,
                first_name="Test",
                username="testuser",
                is_premium=False,
            )
            user_telegram_client_connected.get_me = mocker.AsyncMock(
                return_value=mock_user_info
            )

        with allure.step("Mock UserTelegramClient context manager"):
            mock_tg_client_context = mocker.AsyncMock()
            mock_tg_client_context.__aenter__ = mocker.AsyncMock(
                return_value=user_telegram_client_connected
            )
            mock_tg_client_context.__aexit__ = mocker.AsyncMock(return_value=None)
            mocker.patch(
                "tma_test_framework.clients.mtproto_client.UserTelegramClient",
                return_value=mock_tg_client_context,
            )

        with allure.step("Mock HTTP response for user creation (201 CREATED)"):
            mock_response = mock_httpx_response_basic
            mock_response.status_code = HTTPStatus.CREATED
            mock_response.elapsed = timedelta(seconds=0.3)
            mock_response.is_success = True
            mock_response.content = b'{"id": 1, "status": "created"}'
            mock_response.reason_phrase = "Created"
            mock_response.raise_for_status = mocker.MagicMock()

            api_client.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        with allure.step("Call setup_tma_auth() without user_info"):
            await api_client.setup_tma_auth(config=valid_config)

        with allure.step("Verify UserTelegramClient.get_me() was called"):
            user_telegram_client_connected.get_me.assert_called_once()

        with allure.step("Verify user creation API was called"):
            api_client.client.request.assert_called_once()  # type: ignore[attr-defined]
            call_args = api_client.client.request.call_args  # type: ignore[attr-defined]
            assert call_args[1]["method"] == "POST"
            assert "v1/create/tma/" in str(call_args[1]["url"])

        with allure.step("Verify init_data token was set"):
            assert api_client._auth_token is not None
            assert api_client._auth_token_type == "tma"

        with allure.step("Verify authenticated API requests work"):
            mock_get_response = mocker.MagicMock(spec=Response)
            mock_get_response.status_code = 200
            mock_get_response.elapsed = timedelta(seconds=0.2)
            mock_get_response.content = b'{"data": "test"}'
            mock_get_response.headers = {"Content-Type": "application/json"}
            mock_get_response.reason_phrase = "OK"
            api_client.client.request = mocker.AsyncMock(return_value=mock_get_response)  # type: ignore[method-assign]

            result = await api_client.make_request("/api/test", method="GET")
            assert result.status_code == 200
            # Verify token was included in headers
            call_args = api_client.client.request.call_args  # type: ignore[attr-defined]
            headers = call_args[1].get("headers", {})
            assert "tma" in headers.get(
                "Authorization", ""
            ).lower() or api_client._auth_token in str(headers)

        await api_client.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-AUTH-002: setup_tma_auth with existing user")
    @allure.description(
        "TC-INTEGRATION-AUTH-002: setup_tma_auth with existing user. "
        "Verify setup_tma_auth handles existing user gracefully (400 response)."
    )
    async def test_setup_tma_auth_with_existing_user(
        self,
        mocker,
        user_telegram_client_connected,
        valid_config,
        mock_mini_app_url,
        mock_httpx_response_basic,
    ):
        """
        TC-INTEGRATION-AUTH-002: setup_tma_auth with existing user.

        Verify setup_tma_auth handles existing user gracefully (400 response).
        """
        with allure.step("Create ApiClient"):
            api_client = MiniAppApi(mock_mini_app_url, valid_config)

        with allure.step("Mock UserTelegramClient.get_me()"):
            mock_user_info = UserInfo(
                id=123456789,
                first_name="Test",
                username="testuser",
                is_premium=False,
            )
            user_telegram_client_connected.get_me = mocker.AsyncMock(
                return_value=mock_user_info
            )

        with allure.step("Mock UserTelegramClient context manager"):
            mock_tg_client_context = mocker.AsyncMock()
            mock_tg_client_context.__aenter__ = mocker.AsyncMock(
                return_value=user_telegram_client_connected
            )
            mock_tg_client_context.__aexit__ = mocker.AsyncMock(return_value=None)
            mocker.patch(
                "tma_test_framework.clients.mtproto_client.UserTelegramClient",
                return_value=mock_tg_client_context,
            )

        with allure.step("Mock HTTP response for existing user (400 BAD_REQUEST)"):
            mock_response = mock_httpx_response_basic
            mock_response.status_code = HTTPStatus.BAD_REQUEST
            mock_response.elapsed = timedelta(seconds=0.2)
            mock_response.is_success = False
            mock_response.is_client_error = True
            mock_response.content = b'{"error": "User already exists"}'
            mock_response.reason_phrase = "Bad Request"
            mock_response.raise_for_status = mocker.MagicMock()

            api_client.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        with allure.step("Call setup_tma_auth() (user already exists)"):
            # Should not raise exception
            await api_client.setup_tma_auth(config=valid_config)

        with allure.step("Verify 400 response was handled gracefully"):
            # No exception should be raised
            assert True

        with allure.step("Verify init_data token was still set"):
            assert api_client._auth_token is not None
            assert api_client._auth_token_type == "tma"

        with allure.step("Verify authenticated API requests work"):
            mock_get_response = mocker.MagicMock(spec=Response)
            mock_get_response.status_code = 200
            mock_get_response.elapsed = timedelta(seconds=0.2)
            mock_get_response.content = b'{"data": "test"}'
            mock_get_response.headers = {"Content-Type": "application/json"}
            api_client.client.request = mocker.AsyncMock(return_value=mock_get_response)  # type: ignore[method-assign]

            result = await api_client.make_request("/api/test", method="GET")
            assert result.status_code == 200

        await api_client.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-AUTH-003: setup_tma_auth with provided user_info")
    @allure.description(
        "TC-INTEGRATION-AUTH-003: setup_tma_auth with provided user_info. "
        "Verify setup_tma_auth works with explicitly provided user_info parameter."
    )
    async def test_setup_tma_auth_with_provided_user_info(
        self, mocker, valid_config, mock_mini_app_url, mock_httpx_response_basic
    ):
        """
        TC-INTEGRATION-AUTH-003: setup_tma_auth with provided user_info.

        Verify setup_tma_auth works with explicitly provided user_info parameter.
        """
        with allure.step("Create ApiClient"):
            api_client = MiniAppApi(mock_mini_app_url, valid_config)

        with allure.step("Create UserInfo object"):
            user_info = UserInfo(
                id=123456789,
                first_name="Test",
                username="testuser",
                is_premium=False,
            )

        with allure.step("Mock HTTP response for user creation"):
            mock_response = mock_httpx_response_basic
            mock_response.status_code = HTTPStatus.CREATED
            mock_response.elapsed = timedelta(seconds=0.3)
            mock_response.is_success = True
            mock_response.content = b'{"id": 1, "status": "created"}'
            mock_response.reason_phrase = "Created"
            mock_response.raise_for_status = mocker.MagicMock()

            api_client.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        with allure.step("Call setup_tma_auth(user_info=user_info)"):
            await api_client.setup_tma_auth(user_info=user_info, config=valid_config)

        with allure.step("Verify user creation API was called"):
            api_client.client.request.assert_called_once()  # type: ignore[attr-defined]

        with allure.step("Verify init_data token was set"):
            assert api_client._auth_token is not None
            assert api_client._auth_token_type == "tma"

        await api_client.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-AUTH-004: setup_tma_auth without creating user")
    @allure.description(
        "TC-INTEGRATION-AUTH-004: setup_tma_auth without creating user. "
        "Verify setup_tma_auth can skip user creation and only set auth token."
    )
    async def test_setup_tma_auth_without_creating_user(
        self, mocker, user_telegram_client_connected, valid_config, mock_mini_app_url
    ):
        """
        TC-INTEGRATION-AUTH-004: setup_tma_auth without creating user.

        Verify setup_tma_auth can skip user creation and only set auth token.
        """
        with allure.step("Create ApiClient"):
            api_client = MiniAppApi(mock_mini_app_url, valid_config)

        with allure.step("Mock UserTelegramClient.get_me()"):
            mock_user_info = UserInfo(
                id=123456789,
                first_name="Test",
                username="testuser",
                is_premium=False,
            )
            user_telegram_client_connected.get_me = mocker.AsyncMock(
                return_value=mock_user_info
            )

        with allure.step("Mock UserTelegramClient context manager"):
            mock_tg_client_context = mocker.AsyncMock()
            mock_tg_client_context.__aenter__ = mocker.AsyncMock(
                return_value=user_telegram_client_connected
            )
            mock_tg_client_context.__aexit__ = mocker.AsyncMock(return_value=None)
            mocker.patch(
                "tma_test_framework.clients.mtproto_client.UserTelegramClient",
                return_value=mock_tg_client_context,
            )

        with allure.step("Mock client.request to verify it's not called"):
            api_client.client.request = mocker.AsyncMock()  # type: ignore[method-assign]

        with allure.step("Call setup_tma_auth(create_user=False)"):
            await api_client.setup_tma_auth(config=valid_config, create_user=False)

        with allure.step("Verify user creation API was NOT called"):
            # Since create_user=False, client.request should not be called
            api_client.client.request.assert_not_called()  # type: ignore[attr-defined]

        with allure.step("Verify init_data token was still set"):
            assert api_client._auth_token is not None
            assert api_client._auth_token_type == "tma"

        await api_client.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-AUTH-005: setup_tma_auth with custom endpoint")
    @allure.description(
        "TC-INTEGRATION-AUTH-005: setup_tma_auth with custom endpoint. "
        "Verify setup_tma_auth works with custom user creation endpoint."
    )
    async def test_setup_tma_auth_with_custom_endpoint(
        self,
        mocker,
        user_telegram_client_connected,
        valid_config,
        mock_mini_app_url,
        mock_httpx_response_basic,
    ):
        """
        TC-INTEGRATION-AUTH-005: setup_tma_auth with custom endpoint.

        Verify setup_tma_auth works with custom user creation endpoint.
        """
        with allure.step("Create ApiClient"):
            api_client = MiniAppApi(mock_mini_app_url, valid_config)

        with allure.step("Mock UserTelegramClient.get_me()"):
            mock_user_info = UserInfo(
                id=123456789,
                first_name="Test",
                username="testuser",
                is_premium=False,
            )
            user_telegram_client_connected.get_me = mocker.AsyncMock(
                return_value=mock_user_info
            )

        with allure.step("Mock UserTelegramClient context manager"):
            mock_tg_client_context = mocker.AsyncMock()
            mock_tg_client_context.__aenter__ = mocker.AsyncMock(
                return_value=user_telegram_client_connected
            )
            mock_tg_client_context.__aexit__ = mocker.AsyncMock(return_value=None)
            mocker.patch(
                "tma_test_framework.clients.mtproto_client.UserTelegramClient",
                return_value=mock_tg_client_context,
            )

        with allure.step("Mock HTTP response for custom endpoint"):
            mock_response = mock_httpx_response_basic
            mock_response.status_code = HTTPStatus.CREATED
            mock_response.elapsed = timedelta(seconds=0.3)
            mock_response.is_success = True
            mock_response.content = b'{"id": 1, "status": "created"}'
            mock_response.reason_phrase = "Created"
            mock_response.raise_for_status = mocker.MagicMock()

            api_client.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        custom_endpoint = "/api/users/create"

        with allure.step("Call setup_tma_auth(create_user_endpoint=custom_endpoint)"):
            await api_client.setup_tma_auth(
                config=valid_config, create_user_endpoint=custom_endpoint
            )

        with allure.step("Verify user creation API was called with custom endpoint"):
            api_client.client.request.assert_called_once()  # type: ignore[attr-defined]
            call_args = api_client.client.request.call_args  # type: ignore[attr-defined]
            assert custom_endpoint in str(call_args[1]["url"])

        with allure.step("Verify init_data token was set"):
            assert api_client._auth_token is not None
            assert api_client._auth_token_type == "tma"

        await api_client.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-AUTH-006: setup_tma_auth error handling")
    @allure.description(
        "TC-INTEGRATION-AUTH-006: setup_tma_auth error handling. "
        "Verify setup_tma_auth handles various error conditions correctly."
    )
    async def test_setup_tma_auth_error_handling(
        self,
        mocker,
        user_telegram_client_connected,
        valid_config,
        mock_mini_app_url,
        mock_httpx_response_basic,
    ):
        """
        TC-INTEGRATION-AUTH-006: setup_tma_auth error handling.

        Verify setup_tma_auth handles various error conditions correctly.
        """
        with allure.step("Test with config=None (should raise ValueError)"):
            api_client = MiniAppApi(mock_mini_app_url, valid_config)
            with pytest.raises(ValueError, match="config is required"):
                await api_client.setup_tma_auth(config=None)
            await api_client.close()

        with allure.step("Test with UserTelegramClient connection failure"):
            api_client = MiniAppApi(mock_mini_app_url, valid_config)

            # Mock UserTelegramClient to raise exception
            mock_tg_client_context = mocker.AsyncMock()
            mock_tg_client_context.__aenter__ = mocker.AsyncMock(
                side_effect=Exception("Connection failed")
            )
            mocker.patch(
                "tma_test_framework.clients.mtproto_client.UserTelegramClient",
                return_value=mock_tg_client_context,
            )

            with pytest.raises(
                ValueError, match="Failed to get user info from Telegram"
            ):
                await api_client.setup_tma_auth(config=valid_config)
            await api_client.close()

        with allure.step("Test with API endpoint failure (non-400/201 status)"):
            api_client = MiniAppApi(mock_mini_app_url, valid_config)

            mock_user_info = UserInfo(
                id=123456789,
                first_name="Test",
                username="testuser",
                is_premium=False,
            )
            user_telegram_client_connected.get_me = mocker.AsyncMock(
                return_value=mock_user_info
            )

            mock_tg_client_context = mocker.AsyncMock()
            mock_tg_client_context.__aenter__ = mocker.AsyncMock(
                return_value=user_telegram_client_connected
            )
            mock_tg_client_context.__aexit__ = mocker.AsyncMock(return_value=None)
            mocker.patch(
                "tma_test_framework.clients.mtproto_client.UserTelegramClient",
                return_value=mock_tg_client_context,
            )

            # Mock 500 error response
            mock_response = mock_httpx_response_basic
            mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            mock_response.elapsed = timedelta(seconds=0.2)
            mock_response.is_success = False
            mock_response.is_server_error = True
            mock_response.content = b'{"error": "Internal Server Error"}'
            mock_response.reason_phrase = "Internal Server Error"
            mock_response.raise_for_status = mocker.MagicMock(
                side_effect=Exception("500 Internal Server Error")
            )

            api_client.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

            with pytest.raises(Exception, match="500"):
                await api_client.setup_tma_auth(config=valid_config)
            await api_client.close()

    @pytest.mark.asyncio
    @allure.title(
        "TC-INTEGRATION-AUTH-007: Full authentication workflow with setup_tma_auth"
    )
    @allure.description(
        "TC-INTEGRATION-AUTH-007: Full authentication workflow with setup_tma_auth. "
        "Verify complete authentication workflow using setup_tma_auth in real scenario."
    )
    async def test_full_authentication_workflow_with_setup_tma_auth(
        self,
        mocker,
        user_telegram_client_connected,
        valid_config,
        mock_mini_app_url,
        mock_httpx_response_basic,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-AUTH-007: Full authentication workflow with setup_tma_auth.

        Verify complete authentication workflow using setup_tma_auth in real scenario.
        """
        with allure.step("Get Mini App from bot"):
            mock_mini_app_ui.url = mock_mini_app_url
            user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
                return_value=mock_mini_app_ui
            )

            mini_app = await user_telegram_client_connected.get_mini_app_from_bot(
                "test_bot"
            )
            assert mini_app is not None

        with allure.step("Create ApiClient with Mini App URL"):
            api_client = MiniAppApi(mini_app.url, valid_config)

        with allure.step("Mock UserTelegramClient.get_me()"):
            mock_user_info = UserInfo(
                id=123456789,
                first_name="Test",
                username="testuser",
                is_premium=False,
            )
            user_telegram_client_connected.get_me = mocker.AsyncMock(
                return_value=mock_user_info
            )

        with allure.step("Mock UserTelegramClient context manager"):
            mock_tg_client_context = mocker.AsyncMock()
            mock_tg_client_context.__aenter__ = mocker.AsyncMock(
                return_value=user_telegram_client_connected
            )
            mock_tg_client_context.__aexit__ = mocker.AsyncMock(return_value=None)
            mocker.patch(
                "tma_test_framework.clients.mtproto_client.UserTelegramClient",
                return_value=mock_tg_client_context,
            )

        with allure.step("Mock HTTP response for user creation"):
            # Create separate mock response for POST request (user creation)
            mock_post_response = mocker.MagicMock(spec=Response)
            mock_post_response.status_code = HTTPStatus.CREATED
            mock_post_response.elapsed = timedelta(seconds=0.3)
            mock_post_response.is_informational = False
            mock_post_response.is_success = True
            mock_post_response.is_redirect = False
            mock_post_response.is_client_error = False
            mock_post_response.is_server_error = False
            mock_post_response.content = b'{"id": 1, "status": "created"}'
            mock_post_response.headers = {"Content-Type": "application/json"}
            mock_post_response.reason_phrase = "Created"
            mock_post_response.raise_for_status = mocker.MagicMock()

            api_client.client.request = mocker.AsyncMock(  # type: ignore[method-assign]
                return_value=mock_post_response
            )

        with allure.step("Call setup_tma_auth() to authenticate"):
            await api_client.setup_tma_auth(config=valid_config)

        with allure.step("Test authenticated API endpoints"):
            # Create separate mock response for GET request (protected endpoint)
            mock_get_response = mocker.MagicMock(spec=Response)
            mock_get_response.status_code = HTTPStatus.OK
            mock_get_response.elapsed = timedelta(seconds=0.2)
            mock_get_response.is_informational = False
            mock_get_response.is_success = True
            mock_get_response.is_redirect = False
            mock_get_response.is_client_error = False
            mock_get_response.is_server_error = False
            mock_get_response.content = b'{"data": "authenticated"}'
            mock_get_response.headers = {"Content-Type": "application/json"}
            mock_get_response.reason_phrase = "OK"
            mock_get_response.raise_for_status = mocker.MagicMock()

            api_client.client.request = mocker.AsyncMock(return_value=mock_get_response)  # type: ignore[method-assign]

            result = await api_client.make_request("/api/protected", method="GET")
            assert result.status_code == 200
            assert api_client._auth_token is not None

        with allure.step("Verify complete authentication workflow works"):
            assert api_client._auth_token is not None
            assert api_client._auth_token_type == "tma"

        await api_client.close()
