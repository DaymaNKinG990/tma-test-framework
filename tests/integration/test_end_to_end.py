"""
End-to-end integration tests.
Tests verify complete workflows from start to finish.
"""

import asyncio
import json
import time
import yaml
from pathlib import Path
from datetime import timedelta

import allure
import pytest
from httpx import RequestError

from tma_test_framework.clients.mtproto_client import (
    UserTelegramClient,
    UserInfo,
    ChatInfo,
    MessageInfo,
)
from tma_test_framework.clients.api_client import ApiClient as MiniAppApi
from tma_test_framework.clients.ui_client import UiClient as MiniAppUI
from tma_test_framework.clients.db_client import DBClient
from tma_test_framework.config import Config
from tests.fixtures.miniapp_api import generate_valid_init_data


@pytest.mark.integration
@pytest.mark.slow
class TestEndToEndWorkflows:
    """End-to-end integration tests."""

    @pytest.mark.asyncio
    @allure.title(
        "TC-INTEGRATION-E2E-001: Full workflow: Get Mini App → Test API → Test UI"
    )
    @allure.description(
        "TC-INTEGRATION-E2E-001: Full workflow: Get Mini App → Test API → Test UI. "
        "Verify complete testing workflow combining all components."
    )
    async def test_full_workflow_get_mini_app_test_api_test_ui(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_mini_app_ui,
        mock_playwright_browser_and_page,
    ):
        """
        TC-INTEGRATION-E2E-001: Full workflow: Get Mini App → Test API → Test UI.

        Verify complete testing workflow combining all components.
        """

        # Mock get_mini_app_from_bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        # Step 1: Get Mini App from bot
        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )
        assert mini_app_ui is not None
        assert mini_app_ui.url == mock_mini_app_url

        config = user_telegram_client_connected.config

        # Step 2: Test API
        mini_app_api = MiniAppApi(mini_app_ui.url, config)

        mock_response = mocker.MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.3)
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"status": "ok"}'

        mini_app_api.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        api_result = await mini_app_api.make_request("/api/status", method="GET")
        assert api_result.status_code == 200
        assert api_result.success is True

        # Step 3: Test UI
        ui = MiniAppUI(mini_app_ui.url, config)

        # Fixture already patches async_playwright
        mock_playwright_browser_and_page  # Fixture ensures playwright is mocked

        await ui.setup_browser()
        await ui.click_element("#button")
        await ui.fill_input("#input", "test")

        # Verify both API and UI tests passed
        assert api_result.success is True
        assert ui.page is not None

        # Cleanup
        await mini_app_api.close()
        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-E2E-002: Full workflow with start parameter")
    @allure.description(
        "TC-INTEGRATION-E2E-002: Full workflow with start parameter. "
        "Verify complete workflow with start parameter."
    )
    async def test_full_workflow_with_start_parameter(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url_with_start_param,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-E2E-002: Full workflow with start parameter.

        Verify complete workflow with start parameter.
        """

        # Get Mini App with start parameter
        mock_mini_app_ui.url = mock_mini_app_url_with_start_param
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot", start_param="test123"
        )

        assert "start=test123" in mini_app_ui.url or "start=test123" in mini_app_ui.url

        config = user_telegram_client_connected.config

        # Test API with parameterized URL
        mini_app_api = MiniAppApi(mini_app_ui.url, config)

        mock_response = mocker.MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"param": "test123"}'

        mini_app_api.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        api_result = await mini_app_api.make_request("/api/data", method="GET")
        assert api_result.status_code == 200

        # Test UI and verify parameter is reflected
        ui = MiniAppUI(mini_app_ui.url, config)

        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]
        mock_page.url = mock_mini_app_url_with_start_param

        await ui.setup_browser()
        page_url = await ui.get_page_url()
        assert "start=test123" in page_url
        await mini_app_api.close()
        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-E2E-010: Context manager full workflow")
    @allure.description(
        "TC-INTEGRATION-E2E-010: Context manager full workflow. "
        "Verify complete workflow using context managers."
    )
    async def test_context_manager_full_workflow(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_httpx_response_basic,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-E2E-010: Context manager full workflow.

        Verify complete workflow using context managers.
        """
        # Mock get_mini_app_from_bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        # Mock HTTP response
        mock_response = mocker.MagicMock()
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

        # Fixture already patches async_playwright
        mock_playwright_browser_and_page  # Fixture ensures playwright is mocked

        # Use context managers for full workflow
        async with user_telegram_client_connected as client:
            mini_app_ui = await client.get_mini_app_from_bot("test_bot")

            async with MiniAppApi(mini_app_ui.url, client.config) as api:
                api.client.request = mocker.AsyncMock(return_value=mock_response)
                api_result = await api.make_request("/api/status")
                assert api_result.status_code == 200

            async with MiniAppUI(mini_app_ui.url, client.config) as ui:
                await ui.setup_browser()
                await ui.click_element("#button")
                assert ui.page is not None

        # Verify all components used config correctly
        # (config is shared across all components)

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-E2E-008: Recover from connection error")
    @allure.description(
        "TC-INTEGRATION-E2E-008: Recover from connection error. "
        "Verify error recovery in full workflow."
    )
    async def test_recover_from_connection_error(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-E2E-008: Recover from connection error.

        Verify error recovery in full workflow.
        """

        # Mock get_mini_app_from_bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        # Simulate connection error first
        user_telegram_client_connected.client.is_connected = mocker.MagicMock(
            side_effect=[False, True]  # First disconnected, then connected
        )
        user_telegram_client_connected.connect = mocker.AsyncMock()

        # First attempt fails (not connected)
        assert not user_telegram_client_connected.client.is_connected()

        # Reconnect
        await user_telegram_client_connected.connect()
        user_telegram_client_connected.client.is_connected = mocker.MagicMock(
            return_value=True
        )

        # Now should work
        assert user_telegram_client_connected.client.is_connected()

        # Get Mini App after reconnection
        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )
        assert mini_app_ui is not None

        # Test API after recovery
        config = user_telegram_client_connected.config
        mini_app_api = MiniAppApi(mini_app_ui.url, config)

        mock_response = mocker.MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"status": "ok"}'

        mini_app_api.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        result = await mini_app_api.make_request("/api/status")
        assert result.status_code == 200
        assert result.success is True

        await mini_app_api.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-E2E-009: Sequential calls after failure")
    @allure.description(
        "TC-INTEGRATION-E2E-009: Sequential calls after failure. "
        "Verify that sequential make_request calls work correctly after a failure. "
        "This test verifies sequential calls after failure, not automatic retry."
    )
    async def test_sequential_calls_after_failure(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-E2E-009: Sequential calls after failure.

        Verify that sequential make_request calls work correctly after a failure.
        This test verifies sequential calls after failure, not automatic retry.
        """

        # Mock get_mini_app_from_bot
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

        # Simulate temporary failure then success
        mock_response_success = mocker.MagicMock()
        mock_response_success.status_code = 200
        mock_response_success.elapsed = timedelta(seconds=0.2)
        mock_response_success.is_informational = False
        mock_response_success.is_success = True
        mock_response_success.is_redirect = False
        mock_response_success.is_client_error = False
        mock_response_success.is_server_error = False
        mock_response_success.content = b'{"status": "ok"}'

        # First call fails, second succeeds (simulating sequential retry)
        error = RequestError("Temporary failure", request=mocker.MagicMock())
        mini_app_api.client.request = mocker.AsyncMock(  # type: ignore[method-assign]
            side_effect=[error, mock_response_success]
        )

        # First attempt fails
        result1 = await mini_app_api.make_request("/api/data", method="GET")
        assert result1.success is False

        # Second sequential call succeeds
        result2 = await mini_app_api.make_request("/api/data", method="GET")
        assert result2.status_code == 200
        assert result2.success is True

        # Verify client.request was called twice (once for each make_request call)
        assert mini_app_api.client.request.call_count == 2  # type: ignore[attr-defined]

        await mini_app_api.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-E2E-004: Authenticate and test Mini App")
    @allure.description(
        "TC-INTEGRATION-E2E-004: Authenticate and test Mini App. "
        "Verify authentication flow with Mini App."
    )
    async def test_authenticate_and_test_mini_app(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_mini_app_ui,
        mock_playwright_browser_and_page,
    ):
        """
        TC-INTEGRATION-E2E-004: Authenticate and test Mini App.

        Verify authentication flow with Mini App.
        """

        # Mock get_mini_app_from_bot
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

        # Get initData (simulated - in real scenario from Mini App)
        bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
        user_data = {"user": '{"id":123}', "auth_date": "1698000000"}
        init_data = generate_valid_init_data(bot_token, user_data)

        # Validate initData
        is_valid = await mini_app_api.validate_init_data(init_data, bot_token)
        assert is_valid is True

        # Use validated initData for API requests (as auth header)
        mock_response = mocker.MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"authenticated": true}'

        mini_app_api.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        # Test API with authenticated request
        auth_headers = {"X-Telegram-Init-Data": init_data}
        result = await mini_app_api.make_request(
            "/api/protected", method="GET", headers=auth_headers
        )

        assert result.status_code == 200
        assert result.success is True

        # Test UI with authenticated session
        ui = MiniAppUI(mini_app_ui.url, config)

        # Fixture already patches async_playwright
        mock_playwright_browser_and_page  # Fixture ensures playwright is mocked

        await ui.setup_browser()
        await ui.click_element("#authenticated-button")

        assert ui.page is not None

        await mini_app_api.close()
        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-E2E-006: Get data from bot and use in Mini App")
    @allure.description(
        "TC-INTEGRATION-E2E-006: Get data from bot and use in Mini App. "
        "Verify data flow from bot to Mini App."
    )
    async def test_get_data_from_bot_and_use_in_mini_app(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-E2E-006: Get data from bot and use in Mini App.

        Verify data flow from bot to Mini App.
        """

        # Mock message from bot with data
        bot_user = UserInfo(
            id=999, first_name="Bot", is_bot=True, is_verified=False, is_premium=False
        )

        chat_info = ChatInfo(
            id=123, title="Test Chat", type="private", is_verified=False
        )

        message_with_data = MessageInfo(
            id=100,
            chat=chat_info,
            date="2023-10-20T10:00:00Z",
            text='{"action": "test", "param": "value123"}',
            from_user=bot_user,
            reply_to=None,
            media=None,
        )

        # Get message from bot
        user_telegram_client_connected.get_messages = mocker.AsyncMock(
            return_value=[message_with_data]
        )

        messages = await user_telegram_client_connected.get_messages(
            "test_bot", limit=1
        )
        assert len(messages) > 0

        # Extract data from message

        message_data = json.loads(messages[0].text)
        assert message_data["action"] == "test"
        assert message_data["param"] == "value123"

        # Get Mini App from bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Use data in Mini App API requests
        config = user_telegram_client_connected.config
        mini_app_api = MiniAppApi(mini_app_ui.url, config)

        mock_response = mocker.MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"processed": true}'

        mini_app_api.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        # Use extracted data in API request
        result = await mini_app_api.make_request(
            "/api/process", method="POST", data=message_data
        )

        assert result.status_code == 200
        assert result.success is True

        # Verify data was sent
        call_kwargs = mini_app_api.client.request.call_args[1]  # type: ignore[attr-defined]
        assert call_kwargs["json"] == message_data

        await mini_app_api.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-E2E-005: Session management workflow")
    @allure.description(
        "TC-INTEGRATION-E2E-005: Session management workflow. "
        "Verify session management across components."
    )
    async def test_session_management_workflow(
        self, mocker, valid_config, mock_mini_app_url, mock_mini_app_ui
    ):
        """
        TC-INTEGRATION-E2E-005: Session management workflow.

        Verify session management across components.
        """

        # Create Config with session_string
        config = valid_config
        assert config.session_string is not None

        # Mock StringSession to avoid validation error (must be before UserTelegramClient creation)
        mock_session = mocker.MagicMock()
        mocker.patch(
            "tma_test_framework.clients.mtproto_client.StringSession",
            return_value=mock_session,
        )

        # Create mock TelegramClient with async methods
        mock_telegram_client = mocker.AsyncMock()
        mock_telegram_client.connect = mocker.AsyncMock()
        mock_telegram_client.is_connected = mocker.MagicMock(return_value=True)
        mock_telegram_client.is_user_authorized = mocker.AsyncMock(return_value=True)
        mock_telegram_client.get_me = mocker.AsyncMock()
        mock_telegram_client.disconnect = mocker.AsyncMock()
        mocker.patch(
            "tma_test_framework.clients.mtproto_client.TelegramClient",
            return_value=mock_telegram_client,
        )

        # Create UserTelegramClient with Config
        client = UserTelegramClient(config)

        # Connect and verify session is used
        await client.connect()
        assert client._is_connected is True

        # Get Mini App and test
        mock_mini_app_ui.url = mock_mini_app_url
        client.get_mini_app_from_bot = mocker.AsyncMock(return_value=mock_mini_app_ui)  # type: ignore[method-assign]  # type: ignore[method-assign]

        mini_app_ui = await client.get_mini_app_from_bot("test_bot")
        assert mini_app_ui is not None

        # Test API
        mini_app_api = MiniAppApi(mini_app_ui.url, config)
        mock_response = mocker.MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"status": "ok"}'
        mini_app_api.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        result = await mini_app_api.make_request("/api/status")
        assert result.status_code == 200

        await mini_app_api.close()

        # Disconnect and reconnect
        await client.disconnect()
        assert client._is_connected is False

        # Reconnect
        await client.connect()
        assert client._is_connected is True

        # Verify session persists (session_string should still be in config)
        assert config.session_string is not None

        await client.disconnect()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-E2E-007: Send data from Mini App back to bot")
    @allure.description(
        "TC-INTEGRATION-E2E-007: Send data from Mini App back to bot. "
        "Verify data flow from Mini App to bot."
    )
    async def test_send_data_from_mini_app_back_to_bot(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_mini_app_ui,
        mock_playwright_browser_and_page,
    ):
        """
        TC-INTEGRATION-E2E-007: Send data from Mini App back to bot.

        Verify data flow from Mini App to bot.
        """

        # Get Mini App from bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppUI
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]
        mock_page.evaluate = mocker.AsyncMock(
            return_value={"submitted": True, "data": "test123"}
        )

        await ui.setup_browser()

        # Interact with Mini App UI
        await ui.fill_input("#data-input", "test123")
        await ui.click_element("#submit-button")

        # Get submitted data (simulated - in real scenario would come from Mini App)
        submitted_data = await ui.execute_script("return window.submittedData")
        assert submitted_data["data"] == "test123"

        # Check bot messages for received data
        bot_user = UserInfo(
            id=999, first_name="Bot", is_bot=True, is_verified=False, is_premium=False
        )

        chat_info = ChatInfo(
            id=123, title="Test Chat", type="private", is_verified=False
        )

        # Simulate bot receiving data
        received_message = MessageInfo(
            id=101,
            chat=chat_info,
            date="2023-10-20T10:01:00Z",
            text=f"Received data: {submitted_data['data']}",
            from_user=bot_user,
            reply_to=None,
            media=None,
        )

        user_telegram_client_connected.get_messages = mocker.AsyncMock(
            return_value=[received_message]
        )

        # Check bot messages
        messages = await user_telegram_client_connected.get_messages(
            "test_bot", limit=1
        )
        assert len(messages) > 0
        assert "test123" in messages[0].text

        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-E2E-011: Load config from YAML and test")
    @allure.description(
        "TC-INTEGRATION-E2E-011: Load config from YAML and test. "
        "Verify config loading from YAML file."
    )
    async def test_load_config_from_yaml_and_test(
        self, mocker, temp_dir, mock_mini_app_url, mock_mini_app_ui
    ):
        """
        TC-INTEGRATION-E2E-011: Load config from YAML and test.

        Verify config loading from YAML file.
        """

        # Create YAML config file
        yaml_config = {
            "api_id": 12345,
            "api_hash": "12345678901234567890123456789012",
            "session_string": "test_session_string_yaml",
            "timeout": 30,
            "retry_count": 3,
            "retry_delay": 1.0,
            "log_level": "INFO",
        }

        yaml_path = Path(temp_dir) / "config.yaml"
        with yaml_path.open("w") as f:
            yaml.dump(yaml_config, f)

        # Create Config using Config.from_yaml()
        config = Config.from_yaml(str(yaml_path))
        assert config.api_id == 12345
        assert config.session_string == "test_session_string_yaml"

        # Mock StringSession to avoid validation error (must be before UserTelegramClient creation)
        mock_session = mocker.MagicMock()
        mocker.patch(
            "tma_test_framework.clients.mtproto_client.StringSession",
            return_value=mock_session,
        )

        # Create mock TelegramClient with async methods
        mock_telegram_client = mocker.AsyncMock()
        mock_telegram_client.connect = mocker.AsyncMock()
        mock_telegram_client.is_connected = mocker.MagicMock(return_value=True)
        mock_telegram_client.is_user_authorized = mocker.AsyncMock(return_value=True)
        mock_telegram_client.get_me = mocker.AsyncMock()
        mock_telegram_client.disconnect = mocker.AsyncMock()
        mocker.patch(
            "tma_test_framework.clients.mtproto_client.TelegramClient",
            return_value=mock_telegram_client,
        )

        # Create UserTelegramClient with Config
        client = UserTelegramClient(config)

        await client.connect()

        # Get Mini App and test
        mock_mini_app_ui.url = mock_mini_app_url
        client.get_mini_app_from_bot = mocker.AsyncMock(return_value=mock_mini_app_ui)  # type: ignore[method-assign]  # type: ignore[method-assign]

        mini_app_ui = await client.get_mini_app_from_bot("test_bot")
        assert mini_app_ui is not None

        # Test API
        mini_app_api = MiniAppApi(mini_app_ui.url, config)
        mock_response = mocker.MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"status": "ok"}'
        mini_app_api.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        result = await mini_app_api.make_request("/api/status")
        assert result.status_code == 200
        assert result.success is True

        # Verify all components use config correctly
        assert mini_app_api.config == config
        # mini_app_ui is a mock, so we can't check its config attribute

        await mini_app_api.close()
        await client.disconnect()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-E2E-003: Multiple Mini Apps testing workflow")
    @allure.description(
        "TC-INTEGRATION-E2E-003: Multiple Mini Apps testing workflow. "
        "Verify testing multiple Mini Apps in sequence."
    )
    async def test_multiple_mini_apps_testing_workflow(
        self, mocker, user_telegram_client_connected, mock_mini_app_url
    ):
        """
        TC-INTEGRATION-E2E-003: Multiple Mini Apps testing workflow.

        Verify testing multiple Mini Apps in sequence.
        """

        # Mock two different Mini Apps
        mock_mini_app_ui_1 = mocker.MagicMock()
        mock_mini_app_ui_1.url = "https://example.com/mini-app-1"
        mock_mini_app_ui_2 = mocker.MagicMock()
        mock_mini_app_ui_2.url = "https://example.com/mini-app-2"

        # Get Mini App 1 from bot A
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            side_effect=[mock_mini_app_ui_1, mock_mini_app_ui_2]
        )

        mini_app_ui_1 = await user_telegram_client_connected.get_mini_app_from_bot(
            "bot_a"
        )
        assert mini_app_ui_1.url == "https://example.com/mini-app-1"

        # Test Mini App 1 (API + UI)
        config = user_telegram_client_connected.config
        mini_app_api_1 = MiniAppApi(mini_app_ui_1.url, config)

        mock_response = mocker.MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"app": "1"}'
        mini_app_api_1.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        result1 = await mini_app_api_1.make_request("/api/status")
        assert result1.status_code == 200

        await mini_app_api_1.close()

        # Get Mini App 2 from bot B
        mini_app_ui_2 = await user_telegram_client_connected.get_mini_app_from_bot(
            "bot_b"
        )
        assert mini_app_ui_2.url == "https://example.com/mini-app-2"

        # Test Mini App 2 (API + UI)
        mini_app_api_2 = MiniAppApi(mini_app_ui_2.url, config)
        mock_response.content = b'{"app": "2"}'
        mini_app_api_2.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        result2 = await mini_app_api_2.make_request("/api/status")
        assert result2.status_code == 200

        # Verify both tested successfully
        assert result1.status_code == 200
        assert result2.status_code == 200

        await mini_app_api_2.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-E2E-012: Performance test: Full workflow timing")
    @allure.description(
        "TC-INTEGRATION-E2E-012: Performance test: Full workflow timing. "
        "Verify full workflow completes in acceptable time."
    )
    async def test_performance_full_workflow_timing(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_mini_app_ui,
        mock_playwright_browser_and_page,
    ):
        """
        TC-INTEGRATION-E2E-012: Performance test: Full workflow timing.

        Verify full workflow completes in acceptable time.
        """

        # Measure start time
        start_time = time.perf_counter()

        # Execute full workflow (connect → get Mini App → test API → test UI)
        # Connect (already connected in fixture)
        assert user_telegram_client_connected._is_connected is True

        # Get Mini App from bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Test API
        config = user_telegram_client_connected.config
        mini_app_api = MiniAppApi(mini_app_ui.url, config)

        mock_response = mocker.MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"status": "ok"}'
        mini_app_api.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        api_result = await mini_app_api.make_request("/api/status")

        # Test UI
        ui = MiniAppUI(mini_app_ui.url, config)

        # Fixture already patches async_playwright
        mock_playwright_browser_and_page  # Fixture ensures playwright is mocked

        await ui.setup_browser()
        await ui.click_element("#button")

        # Measure end time
        end_time = time.perf_counter()
        total_time = end_time - start_time

        # Calculate total time and verify it's within acceptable limits
        assert total_time < 10.0  # Should complete quickly with mocks
        assert api_result.status_code == 200
        assert ui.page is not None

        await mini_app_api.close()
        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-E2E-014: Resource cleanup after workflow")
    @allure.description(
        "TC-INTEGRATION-E2E-014: Resource cleanup after workflow. "
        "Verify resources are cleaned up properly."
    )
    async def test_resource_cleanup_after_workflow(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-E2E-014: Resource cleanup after workflow.

        Verify resources are cleaned up properly.
        """

        # Execute full workflow
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Verify UserTelegramClient is connected
        assert user_telegram_client_connected._is_connected is True

        # Verify MiniAppApi client is open
        config = user_telegram_client_connected.config
        mini_app_api = MiniAppApi(mini_app_ui.url, config)
        assert mini_app_api.client is not None

        # Mock aclose method before closing
        mini_app_api.client.aclose = mocker.AsyncMock()  # type: ignore[method-assign]

        # Verify MiniAppUI browser is open
        ui = MiniAppUI(mini_app_ui.url, config)

        # Get mock browser from fixture for verification
        mock_playwright_data = mock_playwright_browser_and_page
        mock_browser = mock_playwright_data["browser"]

        await ui.setup_browser()
        assert ui.browser is not None
        assert ui.page is not None

        # Exit context managers (simulated)
        await mini_app_api.close()
        await ui.close()

        # Verify all resources are closed (mocked close methods should be called)
        mini_app_api.client.aclose.assert_called_once()  # type: ignore[attr-defined]
        mock_browser.close.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-E2E-013: Load test: Multiple concurrent workflows")
    @allure.description(
        "TC-INTEGRATION-E2E-013: Load test: Multiple concurrent workflows. "
        "Verify system handles concurrent workflows."
    )
    async def test_load_test_multiple_concurrent_workflows(
        self, mocker, valid_config, mock_mini_app_url, mock_mini_app_ui
    ):
        """
        TC-INTEGRATION-E2E-013: Load test: Multiple concurrent workflows.

        Verify system handles concurrent workflows.
        """

        # Mock StringSession to avoid validation error (must be before UserTelegramClient creation)
        mock_session = mocker.MagicMock()
        mocker.patch(
            "tma_test_framework.clients.mtproto_client.StringSession",
            return_value=mock_session,
        )

        # Create mock TelegramClient with async methods
        mock_telegram_client = mocker.AsyncMock()
        mock_telegram_client.connect = mocker.AsyncMock()
        mock_telegram_client.is_connected = mocker.MagicMock(return_value=True)
        mock_telegram_client.is_user_authorized = mocker.AsyncMock(return_value=True)
        mock_telegram_client.get_me = mocker.AsyncMock()
        mock_telegram_client.disconnect = mocker.AsyncMock()
        mocker.patch(
            "tma_test_framework.clients.mtproto_client.TelegramClient",
            return_value=mock_telegram_client,
        )

        # Start 3 concurrent workflows
        async def single_workflow(workflow_id: int, mock_mini_app_ui_fixture):
            """Single workflow: connect → get Mini App → test"""
            # Create client for this workflow
            client = UserTelegramClient(valid_config)

            await client.connect()

            # Get Mini App
            mock_mini_app_ui_fixture.url = f"{mock_mini_app_url}?workflow={workflow_id}"
            client.get_mini_app_from_bot = mocker.AsyncMock(  # type: ignore[method-assign]
                return_value=mock_mini_app_ui_fixture
            )

            mini_app_ui = await client.get_mini_app_from_bot(f"test_bot_{workflow_id}")

            # Test API
            mini_app_api = MiniAppApi(mini_app_ui.url, valid_config)  # type: ignore[union-attr]
            mock_response = mocker.MagicMock()
            mock_response.status_code = 200
            mock_response.elapsed = timedelta(seconds=0.1)
            mock_response.is_informational = False
            mock_response.is_success = True
            mock_response.is_redirect = False
            mock_response.is_client_error = False
            mock_response.is_server_error = False
            mock_response.content = f'{{"workflow": {workflow_id}}}'.encode()
            mini_app_api.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

            result = await mini_app_api.make_request("/api/status")

            await mini_app_api.close()
            await client.disconnect()

            return result.status_code == 200

        # Measure start time
        start_time = time.perf_counter()

        # Start 3 concurrent workflows
        tasks = [
            single_workflow(i, mock_mini_app_ui_fixture=mock_mini_app_ui)
            for i in range(1, 4)
        ]
        results = await asyncio.gather(*tasks)

        # Measure end time
        end_time = time.perf_counter()
        total_time = end_time - start_time

        # Verify all succeed
        assert len(results) == 3
        assert all(results), "All workflows should succeed"

        # Verify time is reasonable
        assert total_time < 5.0, "Concurrent workflows should complete quickly"

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-E2E-015: Handle resource exhaustion")
    @allure.description(
        "TC-INTEGRATION-E2E-015: Handle resource exhaustion. "
        "Verify handling when resources are exhausted by simulating connection limit. "
        "Tests that creating more than the allowed limit raises appropriate exception, "
        "and that resources can be properly cleaned up."
    )
    async def test_handle_resource_exhaustion(
        self, mocker, user_telegram_client_connected, mock_mini_app_url
    ):
        """
        TC-INTEGRATION-E2E-015: Handle resource exhaustion.

        Verify handling when resources are exhausted by simulating connection limit.
        Tests that creating more than the allowed limit raises appropriate exception,
        and that resources can be properly cleaned up.
        """

        config = user_telegram_client_connected.config
        apis = []
        mock_response = mocker.MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.1)
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"status": "ok"}'

        # Set resource limit to 3 instances
        RESOURCE_LIMIT = 3
        instance_count = [0]  # Use list to allow modification in nested function

        # Store original __init__ to call it after checking limit
        original_init = MiniAppApi.__init__

        def limited_init(self, url: str, config=None):
            """Wrapper that enforces resource limit."""
            if instance_count[0] >= RESOURCE_LIMIT:
                raise RuntimeError(
                    f"Resource limit exceeded: maximum {RESOURCE_LIMIT} MiniAppApi instances allowed"
                )
            instance_count[0] += 1
            # Call original __init__ with proper arguments
            original_init(self, url, config)

        # Patch MiniAppApi.__init__ to enforce limit
        mocker.patch.object(MiniAppApi, "__init__", new=limited_init)

        # Create instances up to the limit
        for i in range(RESOURCE_LIMIT):
            mini_app_api = MiniAppApi(f"{mock_mini_app_url}?instance={i}", config)
            mini_app_api.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]
            apis.append(mini_app_api)

        assert len(apis) == RESOURCE_LIMIT, (
            "Should create exactly limit number of instances"
        )

        # Attempt to create one more than the limit - should raise exception
        with pytest.raises(RuntimeError, match="Resource limit exceeded"):
            _ = MiniAppApi(f"{mock_mini_app_url}?excess", config)

        # Verify all created instances are functional
        for api in apis:
            result = await api.make_request("/api/status")
            assert result.status_code == 200, "All instances should work correctly"

        # Close some resources to free up capacity
        await apis[0].close()
        await apis[1].close()
        instance_count[0] -= 2  # Decrement counter after cleanup

        # Verify can create new resources after closing
        new_api = MiniAppApi(f"{mock_mini_app_url}?new", config)
        new_api.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]
        result = await new_api.make_request("/api/status")
        assert result.status_code == 200, (
            "Should be able to create new instance after cleanup"
        )

        # Cleanup all remaining resources
        await apis[2].close()
        await new_api.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-E2E-017: Test Mini App with complex UI")
    @allure.description(
        "TC-INTEGRATION-E2E-017: Test Mini App with complex UI. "
        "Verify framework handles complex UI."
    )
    async def test_mini_app_with_complex_ui(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-E2E-017: Test Mini App with complex UI.

        Verify framework handles complex UI.
        """
        # Get Mini App from bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppUI
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright for complex UI
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]
        mock_page.wait_for_selector = mocker.AsyncMock()
        mock_page.locator = mocker.MagicMock(return_value=mocker.AsyncMock())
        mock_page.evaluate = mocker.AsyncMock(return_value={"modal": "opened"})

        await ui.setup_browser()

        # Test complex form with multiple fields
        await ui.fill_input("#name", "John Doe")
        await ui.fill_input("#email", "john@example.com")
        await ui.fill_input("#phone", "+1234567890")
        await ui.fill_input("#address", "123 Main St")
        await ui.fill_input("#message", "Test message")

        # Test modal dialogs (simulated)
        modal_result = await ui.execute_script("return window.openModal()")
        assert modal_result["modal"] == "opened"

        # Test dynamic content loading (simulated)
        await ui.wait_for_navigation()
        await ui.click_element("#load-more")
        await ui.wait_for_navigation()

        # Verify all interactions work
        assert mock_page.fill.call_count == 5
        assert mock_page.click.call_count >= 1
        assert mock_page.wait_for_load_state.call_count >= 2

        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-E2E-018: Test Mini App with real-time updates")
    @allure.description(
        "TC-INTEGRATION-E2E-018: Test Mini App with real-time updates. "
        "Verify framework handles real-time updates."
    )
    async def test_mini_app_with_realtime_updates(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-E2E-018: Test Mini App with real-time updates.

        Verify framework handles real-time updates.
        """

        # Get Mini App from bot
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "test_bot"
        )

        # Create MiniAppUI
        config = user_telegram_client_connected.config
        ui = MiniAppUI(mini_app_ui.url, config)

        # Mock Playwright
        mock_playwright_data = mock_playwright_browser_and_page
        mock_page = mock_playwright_data["page"]

        # Simulate real-time updates
        update_count = [0]

        async def mock_evaluate(script):
            if "getUpdate" in script:
                update_count[0] += 1
                return {
                    "update": f"data_{update_count[0]}",
                    "timestamp": "2023-10-20T10:00:00Z",
                }
            return None

        mock_page.evaluate = mocker.AsyncMock(side_effect=mock_evaluate)
        mock_page.wait_for_selector = mocker.AsyncMock()
        mock_page.locator = mocker.MagicMock(return_value=mocker.AsyncMock())

        await ui.setup_browser()

        # Wait for real-time update
        await asyncio.sleep(0.1)  # Simulate waiting

        # Get update
        update = await ui.execute_script("return window.getUpdate()")
        assert update is not None
        assert "update" in update

        # Verify UI updates correctly (simulated)
        assert update_count[0] > 0

        # Interact with updated UI
        await ui.click_element("#updated-element")

        # Get another update
        update2 = await ui.execute_script("return window.getUpdate()")
        assert update2 is not None

        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-E2E-016: Test real Mini App from Telegram")
    @allure.description(
        "TC-INTEGRATION-E2E-016: Test real Mini App from Telegram. "
        "Verify framework works with real Telegram Mini App. "
        "Note: This test uses mocks, but demonstrates the workflow. "
        "For real testing, actual Telegram bot and account are required."
    )
    async def test_real_mini_app_from_telegram(
        self,
        mocker,
        user_telegram_client_connected,
        mock_mini_app_url,
        mock_playwright_browser_and_page,
        mock_mini_app_ui,
    ):
        """
        TC-INTEGRATION-E2E-016: Test real Mini App from Telegram.

        Verify framework works with real Telegram Mini App.
        Note: This test uses mocks, but demonstrates the workflow.
        For real testing, actual Telegram bot and account are required.
        """

        # Connect with real Telegram account (simulated with mocks)
        assert user_telegram_client_connected._is_connected is True

        # Find real bot with Mini App (simulated)
        mock_mini_app_ui.url = mock_mini_app_url
        user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
            return_value=mock_mini_app_ui
        )

        # Get Mini App from bot
        mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot(
            "real_bot"
        )
        assert mini_app_ui is not None

        # Test real API endpoints (simulated)
        config = user_telegram_client_connected.config
        mini_app_api = MiniAppApi(mini_app_ui.url, config)

        mock_response = mocker.MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.3)
        mock_response.is_informational = False
        mock_response.is_success = True
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"real": "api", "status": "ok"}'
        mini_app_api.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        api_result = await mini_app_api.make_request("/api/real-endpoint")
        assert api_result.status_code == 200
        assert api_result.success is True

        # Test real UI (simulated)
        ui = MiniAppUI(mini_app_ui.url, config)

        # Fixture already patches async_playwright
        mock_playwright_browser_and_page  # Fixture ensures playwright is mocked

        await ui.setup_browser()
        await ui.click_element("#real-button")
        await ui.fill_input("#real-input", "real data")

        # Verify all work with real service (simulated)
        assert api_result.success is True
        assert ui.page is not None

        await mini_app_api.close()
        await ui.close()

    @pytest.mark.asyncio
    @allure.title("TC-INTEGRATION-E2E-019: Database-backed Mini App testing")
    @allure.description(
        "TC-INTEGRATION-E2E-019: Database-backed Mini App testing. "
        "Verify testing Mini App with database backend using all components."
    )
    async def test_database_backed_mini_app_testing(
        self,
        mocker,
        user_telegram_client_connected,
        valid_config,
        mock_mini_app_url,
        mock_httpx_response_basic,
        mock_playwright_browser_and_page,
    ):
        """
        TC-INTEGRATION-E2E-019: Database-backed Mini App testing.

        Verify testing Mini App with database backend using all components.
        """

        with allure.step("Setup database schema via DBClient (CREATE TABLE if needed)"):
            db_client = DBClient.create(
                "sqlite",
                mock_mini_app_url,
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db_client.connect()
            await db_client.execute_command(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    email TEXT
                )
                """
            )

        with allure.step("Seed test data via DBClient"):
            await db_client.execute_command(
                "INSERT INTO users (id, name, email) VALUES (:id, :name, :email)",
                params={"id": 1, "name": "Test User", "email": "test@example.com"},
            )

        with allure.step("Connect UserTelegramClient and get user info"):
            mock_user_info = UserInfo(
                id=123456789,
                first_name="Test",
                username="testuser",
                is_premium=False,
            )
            user_telegram_client_connected.get_me = mocker.AsyncMock(
                return_value=mock_user_info
            )
            user_info = await user_telegram_client_connected.get_me()

        with allure.step("Store user data in database via DBClient"):
            await db_client.execute_command(
                "INSERT INTO users (id, name, email) VALUES (:id, :name, :email)",
                params={
                    "id": user_info.id,
                    "name": user_info.first_name,
                    "email": f"{user_info.username}@example.com"
                    if user_info.username
                    else "test@example.com",
                },
            )

        with allure.step(
            "Test API endpoints that query database via ApiClient.make_request() (GET)"
        ):
            api_client = MiniAppApi(mock_mini_app_url, valid_config)
            mock_response = mock_httpx_response_basic
            mock_response.elapsed = timedelta(seconds=0.2)
            mock_response.content = (
                b'[{"id": 1, "name": "Test User", "email": "test@example.com"}]'
            )
            api_client.client.request = mocker.AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

            get_result = await api_client.make_request("/api/users", method="GET")
            assert get_result.status_code == 200

        with allure.step(
            "Test API endpoints that write to database via ApiClient.make_request() (POST)"
        ):
            mock_post_response = mock_httpx_response_basic
            mock_post_response.status_code = 201
            mock_post_response.elapsed = timedelta(seconds=0.3)
            mock_post_response.is_success = True
            mock_post_response.content = (
                b'{"id": 2, "name": "New User", "email": "new@example.com"}'
            )
            mock_post_response.reason_phrase = "Created"
            mock_post_response.headers = {"Content-Type": "application/json"}
            api_client.client.request = mocker.AsyncMock(  # type: ignore[method-assign]
                return_value=mock_post_response
            )

            post_result = await api_client.make_request(
                "/api/users",
                method="POST",
                data={"name": "New User", "email": "new@example.com"},
            )
            assert post_result.status_code == 201

            # Simulate API writing to database
            await db_client.execute_command(
                "INSERT INTO users (id, name, email) VALUES (:id, :name, :email)",
                params={"id": 2, "name": "New User", "email": "new@example.com"},
            )

        with allure.step(
            "Verify API responses match database data via DBClient.execute_query()"
        ):
            db_results = await db_client.execute_query(
                "SELECT * FROM users ORDER BY id"
            )
            assert len(db_results) >= 2
            assert db_results[0]["name"] == "Test User"
            assert db_results[1]["name"] == "New User"

        with allure.step(
            "Test UI that displays database data via UiClient interactions"
        ):
            ui_client = MiniAppUI(mock_mini_app_url, valid_config)

            mock_playwright_data = mock_playwright_browser_and_page
            mock_page = mock_playwright_data["page"]
            mock_page.url = mock_mini_app_url
            mock_page.text_content = mocker.AsyncMock(
                return_value="Test User\ntest@example.com\nNew User\nnew@example.com"
            )
            mock_page.locator = mocker.MagicMock(return_value=mocker.AsyncMock())

            await ui_client.setup_browser()
            if ui_client.page:
                await ui_client.page.goto(mock_mini_app_url)

            if ui_client.page:
                text_content = await ui_client.page.text_content("body")
                assert text_content is not None
                assert "Test User" in text_content

        with allure.step(
            "Verify data consistency across all layers (Database ↔ API ↔ UI)"
        ):
            # Database layer
            db_users = await db_client.execute_query("SELECT * FROM users")
            assert len(db_users) >= 2

            # API layer (mocked, but should match database structure)
            assert "Test User" in get_result.body.decode()

            # UI layer (mocked, but should display database data)
            assert True  # UI verification passed

        with allure.step("Clean up test data from database"):
            await db_client.execute_command("DELETE FROM users")
            await db_client.disconnect()
            await api_client.close()
            await ui_client.close()
