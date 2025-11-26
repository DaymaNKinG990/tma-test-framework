"""
Fixtures for ApiClient testing.
"""

from pytest import fixture
from httpx import Response
from datetime import timedelta

from tma_test_framework.clients.api_client import ApiClient
from tma_test_framework.config import Config
from tests.fixtures.base_miniapp import _get_base_config_data


@fixture
def valid_config() -> Config:
    """Create a valid Config instance."""
    return Config(**_get_base_config_data())


@fixture
def mock_httpx_response_200(mocker):
    """Create a mock httpx.Response with status 200."""
    response = mocker.MagicMock(spec=Response)
    response.status_code = 200
    response.elapsed = timedelta(seconds=0.5)
    response.is_informational = False
    response.is_success = True
    response.is_redirect = False
    response.is_client_error = False
    response.is_server_error = False
    response.content = b'{"test": "data"}'
    response.headers = {"Content-Type": "application/json", "Content-Length": "15"}
    response.reason_phrase = "OK"
    return response


@fixture
def mock_httpx_response_301(mocker):
    """Create a mock httpx.Response with status 301."""
    response = mocker.MagicMock(spec=Response)
    response.status_code = 301
    response.elapsed = timedelta(seconds=0.1)
    response.is_informational = False
    response.is_success = False
    response.is_redirect = True
    response.is_client_error = False
    response.is_server_error = False
    response.content = b"Redirect"
    response.headers = {"Location": "https://example.com/new"}
    response.reason_phrase = "Moved Permanently"
    return response


@fixture
def mock_httpx_response_404(mocker):
    """Create a mock httpx.Response with status 404."""
    response = mocker.MagicMock(spec=Response)
    response.status_code = 404
    response.elapsed = timedelta(seconds=0.2)
    response.is_informational = False
    response.is_success = False
    response.is_redirect = False
    response.is_client_error = True
    response.is_server_error = False
    response.content = b"Not Found"
    response.headers = {"Content-Type": "text/plain"}
    response.reason_phrase = "Not Found"
    return response


@fixture
def mock_httpx_response_500(mocker):
    """Create a mock httpx.Response with status 500."""
    response = mocker.MagicMock(spec=Response)
    response.status_code = 500
    response.elapsed = timedelta(seconds=1.0)
    response.is_informational = False
    response.is_success = False
    response.is_redirect = False
    response.is_client_error = False
    response.is_server_error = True
    response.content = b"Internal Server Error"
    response.headers = {"Content-Type": "text/plain"}
    response.reason_phrase = "Internal Server Error"
    return response


@fixture
def mock_httpx_response_101(mocker):
    """Create a mock httpx.Response with status 101."""
    response = mocker.MagicMock(spec=Response)
    response.status_code = 101
    response.elapsed = timedelta(seconds=0.05)
    response.is_informational = True
    response.is_success = False
    response.is_redirect = False
    response.is_client_error = False
    response.is_server_error = False
    response.content = b"Switching Protocols"
    response.headers = {"Upgrade": "websocket"}
    response.reason_phrase = "Switching Protocols"
    return response


@fixture
def mock_httpx_response_201(mocker):
    """Create a mock httpx.Response with status 201 (CREATED)."""
    response = mocker.MagicMock(spec=Response)
    response.status_code = 201
    response.elapsed = timedelta(seconds=0.3)
    response.is_informational = False
    response.is_success = True
    response.is_redirect = False
    response.is_client_error = False
    response.is_server_error = False
    response.content = b'{"id": 1, "status": "created"}'
    response.headers = {"Content-Type": "application/json", "Content-Length": "30"}
    response.reason_phrase = "Created"
    return response


@fixture
def mock_httpx_response_400(mocker):
    """Create a mock httpx.Response with status 400 (BAD_REQUEST)."""
    response = mocker.MagicMock(spec=Response)
    response.status_code = 400
    response.elapsed = timedelta(seconds=0.2)
    response.is_informational = False
    response.is_success = False
    response.is_redirect = False
    response.is_client_error = True
    response.is_server_error = False
    response.content = b'{"error": "Bad Request"}'
    response.headers = {"Content-Type": "application/json"}
    response.reason_phrase = "Bad Request"
    return response


@fixture
def mock_httpx_client(mocker):
    """Create a mock httpx.AsyncClient instance."""
    client = mocker.AsyncMock()
    client.aclose = mocker.AsyncMock()
    client.request = mocker.AsyncMock()
    return client


@fixture
def miniapp_api_with_config(mocker, valid_config, mock_httpx_client):
    """Create ApiClient with valid config and mocked httpx client."""
    mocker.patch(
        "tma_test_framework.clients.api_client.AsyncClient",
        return_value=mock_httpx_client,
    )
    api = ApiClient("https://example.com/app", valid_config)
    api.client = mock_httpx_client
    return api


# Test data for validate_init_data
# Note: These are example values - in real tests, you'd generate valid init_data
# using actual Telegram bot token and user data


def generate_valid_init_data(bot_token: str, user_data: dict) -> str:
    """
    Generate valid init_data for testing using official Telegram Mini App algorithm.

    This is a helper function to create test data.
    In real scenarios, init_data comes from Telegram.

    Algorithm:
    1. Exclude 'hash' key from parameters
    2. Sort remaining keys alphabetically
    3. Build verification string by joining "key=value" pairs with newline characters (\\n)
    4. Compute secret key: HMAC-SHA256("WebAppData", bot_token)
    5. Compute hash: HMAC-SHA256(secret_key, verification_string)
    6. Attach hash back into parameters
    7. Return final init_data as URL-encoded query string
    """
    from hashlib import sha256
    from hmac import new
    from urllib.parse import urlencode

    # Exclude 'hash' key from parameters
    params_without_hash = {k: v for k, v in user_data.items() if k != "hash"}

    # Sort keys alphabetically
    sorted_keys = sorted(params_without_hash.keys())

    # Build verification string by joining "key=value" pairs with newline characters
    data_check_pairs = [f"{key}={params_without_hash[key]}" for key in sorted_keys]
    data_to_validate = "\n".join(data_check_pairs)

    # Compute secret key: HMAC-SHA256("WebAppData", bot_token)
    secret_key = new(
        key="WebAppData".encode(), msg=bot_token.encode(), digestmod=sha256
    ).digest()

    # Compute hash: HMAC-SHA256(secret_key, verification_string)
    expected_hash = new(
        key=secret_key, msg=data_to_validate.encode(), digestmod=sha256
    ).hexdigest()

    # Attach hash back into parameters
    params_without_hash["hash"] = expected_hash

    # Return final init_data as URL-encoded query string
    init_data = urlencode(params_without_hash)

    return init_data


@fixture
def valid_init_data_and_token():
    """Create valid init_data and bot_token pair."""
    bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
    user_data = {
        "user": '{"id":123456789,"first_name":"Test","last_name":"User"}',
        "auth_date": "1698000000",
        "start_param": "test_param",
    }

    # Generate valid init_data
    init_data = generate_valid_init_data(bot_token, user_data)
    return init_data, bot_token


@fixture
def invalid_init_data_and_token():
    """Create invalid init_data and bot_token pair."""
    bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
    # Invalid init_data with wrong hash
    init_data = "user=%7B%22id%22%3A123456789%7D&auth_date=1698000000&hash=invalid_hash"
    return init_data, bot_token


@fixture
def init_data_without_hash():
    """Create init_data without hash parameter."""
    return (
        "user=%7B%22id%22%3A123456789%7D&auth_date=1698000000",
        "123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
    )


@fixture
def init_data_test_cases():
    """Various test cases for init_data validation."""
    return [
        # (init_data, bot_token, expected_result, description)
        ("", "token", False, "Empty init_data"),
        ("data", "", False, "Empty bot_token"),
        ("", "", False, "Both empty"),
        ("user=test&hash=abc", "token", False, "Invalid hash"),
        ("user=test", "token", False, "No hash parameter"),
    ]
