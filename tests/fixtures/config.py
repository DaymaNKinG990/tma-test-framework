# Python imports
import os
from os import environ
from pytest import fixture
from yaml import load, SafeLoader  # type: ignore[import-untyped]


@fixture
def valid_config_data() -> dict[str, int | str | float]:
    """
    Valid configuration data.

    Returns:
        dict[str, int | str | float]: Valid configuration data.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session_string_123456789",
        "timeout": 30,
        "retry_count": 3,
        "retry_delay": 1.0,
        "log_level": "DEBUG",
    }


@fixture
def valid_config_data_minimal() -> dict[str, int | str | float]:
    """
    Valid configuration data minimal.

    Returns:
        dict[str, int | str | float]: Valid configuration data minimal.
    """
    return {
        "api_id": 1,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "timeout": 1,
        "retry_count": 0,
        "retry_delay": 0.1,
    }


@fixture
def valid_config_data_maximal() -> dict[str, int | str | float]:
    """
    Valid configuration data maximal.

    Returns:
        dict[str, int | str | float]: Valid configuration data maximal.
    """
    return {
        "api_id": 999999999,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "timeout": 300,
        "retry_count": 10,
        "retry_delay": 10.0,
    }


@fixture
def valid_config_with_file_data() -> dict[str, int | str | float]:
    """
    Valid configuration data with session file.

    Returns:
        dict[str, int | str | float]: Valid configuration data with session file.
    """
    return {
        "api_id": 999999999,
        "api_hash": "DUMMY_TEST_HASH_32_CHARS_LONG!!!",
        "session_file": "test_session.session",
        "timeout": 30,
        "retry_count": 3,
        "retry_delay": 1.0,
        "log_level": "DEBUG",
    }


@fixture
def invalid_config_data() -> dict[str, int | str | float]:
    """
    Invalid configuration data.

    Returns:
        dict[str, int | str | float]: Invalid configuration data.
    """
    return {
        "api_id": 0,
        "api_hash": "",
        "timeout": 0,
        "retry_count": -1,
        "retry_delay": 0.0,
        "log_level": "INVALID",
    }


@fixture
def invalid_config_data_api_id() -> dict[str, int | str | float]:
    """
    Invalid configuration data with api_id 0.

    Returns:
        dict[str, int | str | float]: Invalid configuration data with api_id 0.
    """
    return {
        "api_id": 0,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
    }


@fixture
def invalid_config_data_timeout() -> dict[str, int | str | float]:
    """
    Invalid configuration data with timeout 0.

    Returns:
        dict[str, int | str | float]: Invalid configuration data with timeout 0.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "timeout": 0,
    }


@fixture
def invalid_config_data_minimal_retry_count() -> dict[str, int | str | float]:
    """
    Invalid configuration data with minimal retry count.

    Returns:
        dict[str, int | str | float]: Invalid configuration data with minimal retry count.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "retry_count": -1,
    }


@fixture
def invalid_config_data_maximal_retry_count() -> dict[str, int | str | float]:
    """
    Invalid configuration data with maximal retry count.

    Returns:
        dict[str, int | str | float]: Invalid configuration data with maximal retry count.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "retry_count": 11,
    }


@fixture
def invalid_config_data_minimal_retry_delay() -> dict[str, int | str | float]:
    """
    Invalid configuration data with minimal retry delay.

    Returns:
        dict[str, int | str | float]: Invalid configuration data with minimal retry delay.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "retry_delay": 0.0,
    }


@fixture
def invalid_config_data_maximal_retry_delay() -> dict[str, int | str | float]:
    """
    Invalid configuration data with maximal retry delay.

    Returns:
        dict[str, int | str | float]: Invalid configuration data with maximal retry delay.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "retry_delay": 10.1,
    }


@fixture
def invalid_config_data_timeout_max() -> dict[str, int | str | float]:
    """
    Invalid configuration data with maximal timeout 301.

    Returns:
        dict[str, int | str | float]: Invalid configuration data with maximal timeout.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "timeout": 301,
    }


@fixture
def invalid_config_data_without_api_id() -> dict[str, str]:
    """
    Configuration data without api_id.

    Returns:
        dict[str, str]: Configuration data without api_id.
    """
    return {
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session_string_123456789",
    }


@fixture
def invalid_config_data_without_api_hash() -> dict[str, int | str]:
    """
    Configuration data without api_hash.

    Returns:
        dict[str, int | str]: Configuration data without api_hash.
    """
    return {"api_id": 12345, "session_string": "test_session_string_123456789"}


@fixture
def invalid_config_data_without_session() -> dict[str, int | str]:
    """
    Configuration data without session_string or session_file.

    Returns:
        dict[str, int | str]: Configuration data without session_string or session_file.
    """
    return {"api_id": 12345, "api_hash": "12345678901234567890123456789012"}


@fixture
def config_data_for_default_values() -> dict[str, int | str]:
    """
    Configuration data for testing default values.

    Returns:
        dict[str, int | str]: Configuration data for default values test.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "timeout": 30,
        "retry_count": 3,
        "retry_delay": 1.0,
        "log_level": "INFO",
        "mini_app_url": None,
        "mini_app_start_param": None,
    }


@fixture
def config_data_for_missing_session() -> dict[str, int | str]:
    """
    Configuration data for testing missing session validation.

    Returns:
        dict[str, int | str]: Configuration data without session.
    """
    return {"api_id": 12345, "api_hash": "12345678901234567890123456789012"}


@fixture
def config_data_for_invalid_log_level() -> dict[str, int | str]:
    """
    Configuration data for testing invalid log level validation.

    Returns:
        dict[str, int | str]: Configuration data with invalid log level.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "log_level": "INVALID",
    }


@fixture
def config_data_for_invalid_retry_count() -> dict[str, int | str]:
    """
    Configuration data for testing invalid retry count validation.

    Returns:
        dict[str, int | str]: Configuration data with invalid retry count.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "retry_count": -1,
    }


@fixture
def config_data_for_invalid_retry_delay() -> dict[str, int | str | float]:
    """
    Configuration data for testing invalid retry delay validation.

    Returns:
        dict[str, int | str | float]: Configuration data with invalid retry delay.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "retry_delay": 0.05,
    }


@fixture
def config_data_for_empty_strings() -> dict[str, int | str]:
    """
    Configuration data for testing empty strings validation.

    Returns:
        dict[str, int | str]: Configuration data with empty strings.
    """
    return {"api_id": 12345, "api_hash": "", "session_string": "test_session"}


@fixture
def config_data_for_whitespace_strings() -> dict[str, int | str]:
    """
    Configuration data for testing whitespace strings validation.

    Returns:
        dict[str, int | str]: Configuration data with whitespace strings.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "   ",
    }


@fixture
def config_data_for_very_long_strings() -> dict[str, int | str]:
    """
    Configuration data for testing very long strings.

    Returns:
        dict[str, int | str]: Configuration data with very long strings.
    """
    long_string = "a" * 10000
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": long_string,
    }


@fixture
def config_data_for_special_characters() -> dict[str, int | str]:
    """
    Configuration data for testing special characters.

    Returns:
        dict[str, int | str]: Configuration data with special characters.
    """
    special_string = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": special_string,
    }


@fixture
def config_data_for_unicode_characters() -> dict[str, int | str]:
    """
    Configuration data for testing unicode characters.

    Returns:
        dict[str, int | str]: Configuration data with unicode characters.
    """
    unicode_string = "тест_用户_テスト"
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": unicode_string,
    }


@fixture
def config_data_for_none_values() -> dict[str, int | str | None]:
    """
    Configuration data for testing None values.

    Returns:
        dict[str, int | str | None]: Configuration data with None values.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "mini_app_url": None,
        "mini_app_start_param": None,
    }


@fixture
def config_data_for_both_session_methods() -> dict[str, int | str]:
    """
    Configuration data for testing both session methods.

    Returns:
        dict[str, int | str]: Configuration data with both session_string and session_file.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "session_file": "test.session",
    }


@fixture
def config_data_for_log_level_debug() -> dict[str, int | str]:
    """
    Configuration data for testing log level debug.

    Returns:
        dict[str, int | str]: Configuration data for log level debug testing.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "log_level": "DEBUG",
    }


@fixture
def config_data_for_log_level_info() -> dict[str, int | str]:
    """
    Configuration data for testing log level info.

    Returns:
        dict[str, int | str]: Configuration data for log level info testing.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "log_level": "INFO",
    }


@fixture
def config_data_for_log_level_warning() -> dict[str, int | str]:
    """
    Configuration data for testing log level warning.

    Returns:
        dict[str, int | str]: Configuration data for log level warning testing.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "log_level": "WARNING",
    }


@fixture
def config_data_for_log_level_error() -> dict[str, int | str]:
    """
    Configuration data for testing log level error.

    Returns:
        dict[str, int | str]: Configuration data for log level error testing.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "log_level": "ERROR",
    }


@fixture
def config_data_for_log_level_critical() -> dict[str, int | str]:
    """
    Configuration data for testing log level critical.

    Returns:
        dict[str, int | str]: Configuration data for log level critical testing.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "log_level": "CRITICAL",
    }


@fixture
def config_data_for_log_level_case_sensitivity() -> dict[str, int | str]:
    """
    Configuration data for testing log level case sensitivity.

    Returns:
        dict[str, int | str]: Configuration data with lowercase log level.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "log_level": "debug",
    }


@fixture
def config_data_for_float_precision() -> dict[str, int | str | float]:
    """
    Configuration data for testing float precision.

    Returns:
        dict[str, int | str | float]: Configuration data with precise float.
    """
    return {
        "api_id": 12345,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "retry_delay": 0.123456789,
    }


@fixture
def config_data_for_large_numbers() -> dict[str, int | str | float]:
    """
    Configuration data for testing large numbers.

    Returns:
        dict[str, int | str | float]: Configuration data with large numbers.
    """
    return {
        "api_id": 999999999,
        "api_hash": "12345678901234567890123456789012",
        "session_string": "test_session",
        "timeout": 300,
        "retry_count": 10,
        "retry_delay": 10.0,
    }


@fixture
def mock_environment(mocker) -> dict[str, str]:
    """
    Mock environment variables for testing.

    Returns:
        dict[str, str]: Environment variables.
    """
    env_vars = {
        "TMA_API_ID": "12345",
        "TMA_API_HASH": "12345678901234567890123456789012",
        "TMA_SESSION_STRING": "test_session_string_123456789",
        "TMA_MINI_APP_URL": "https://example.com/mini-app",
        "TMA_MINI_APP_START_PARAM": "test_param",
        "TMA_TIMEOUT": "30",
        "TMA_RETRY_COUNT": "3",
        "TMA_RETRY_DELAY": "1.0",
        "TMA_LOG_LEVEL": "DEBUG",
    }
    # Use mocker.patch.dict with os.environ object (not string)
    # pytest-mock will automatically undo the patch after fixture completes
    mocker.patch.dict(os.environ, env_vars, clear=True)
    yield env_vars


@fixture
def mock_empty_environment(mocker) -> dict[str, str]:
    """
    Mock empty environment variables for testing.

    Returns:
        dict[str, str]: Empty environment variables.
    """
    env_vars = {}
    # Use mocker.patch.dict with os.environ object (not string)
    # pytest-mock will automatically undo the patch after fixture completes
    mocker.patch.dict(os.environ, env_vars, clear=True)
    yield env_vars


@fixture
def mock_environment_missing_api_id(mocker) -> dict[str, str]:
    """
    Mock environment variables missing TMA_API_ID for testing.

    Returns:
        dict[str, str]: Environment variables missing TMA_API_ID.
    """
    env_vars = {"TMA_API_HASH": "12345678901234567890123456789012"}
    # Use mocker.patch.dict with os.environ object (not string)
    # pytest-mock will automatically undo the patch after fixture completes
    mocker.patch.dict(os.environ, env_vars, clear=True)
    yield env_vars


@fixture
def mock_environment_missing_api_hash(mocker) -> dict[str, str]:
    """
    Mock environment variables missing TMA_API_HASH for testing.

    Returns:
        dict[str, str]: Environment variables missing TMA_API_HASH.
    """
    env_vars = {"TMA_API_ID": "12345"}
    # Use mocker.patch.dict with os.environ object (not string)
    # pytest-mock will automatically undo the patch after fixture completes
    mocker.patch.dict(os.environ, env_vars, clear=True)
    yield env_vars


@fixture
def mock_environment_invalid_api_id(mocker) -> dict[str, str]:
    """
    Mock environment variables with invalid TMA_API_ID for testing.

    Returns:
        dict[str, str]: Environment variables with invalid TMA_API_ID.
    """
    env_vars = {
        "TMA_API_ID": "invalid",
        "TMA_API_HASH": "12345678901234567890123456789012",
    }
    # Use mocker.patch.dict with os.environ object (not string)
    # pytest-mock will automatically undo the patch after fixture completes
    mocker.patch.dict(os.environ, env_vars, clear=True)
    yield env_vars


@fixture
def mock_environment_default_values(mocker) -> dict[str, str]:
    """
    Mock environment variables with default values for testing.

    Returns:
        dict[str, str]: Environment variables with default values.
    """
    env_vars = {
        "TMA_API_ID": "12345",
        "TMA_API_HASH": "12345678901234567890123456789012",
        "TMA_SESSION_STRING": "test_session",
        "TMA_TIMEOUT": "30",
        "TMA_RETRY_COUNT": "3",
        "TMA_RETRY_DELAY": "1.0",
        "TMA_LOG_LEVEL": "INFO",
    }
    # Use mocker.patch.dict with os.environ object (not string)
    # pytest-mock will automatically undo the patch after fixture completes
    mocker.patch.dict(os.environ, env_vars, clear=True)
    yield env_vars


@fixture
def mock_environment_override_defaults(mocker) -> dict[str, str]:
    """
    Mock environment variables with overridden default values for testing.

    Returns:
        dict[str, str]: Environment variables with overridden defaults.
    """
    env_vars = {
        "TMA_API_ID": "12345",
        "TMA_API_HASH": "12345678901234567890123456789012",
        "TMA_SESSION_STRING": "test_session",
        "TMA_TIMEOUT": "60",
        "TMA_RETRY_COUNT": "5",
        "TMA_RETRY_DELAY": "2.0",
        "TMA_LOG_LEVEL": "WARNING",
    }
    # Use mocker.patch.dict with os.environ object (not string)
    # pytest-mock will automatically undo the patch after fixture completes
    mocker.patch.dict(os.environ, env_vars, clear=True)
    yield env_vars


@fixture
def mock_environment_optional_variables(mocker) -> dict[str, str]:
    """
    Mock environment variables with optional variables for testing.

    Returns:
        dict[str, str]: Environment variables with optional variables.
    """
    env_vars = {
        "TMA_API_ID": "12345",
        "TMA_API_HASH": "12345678901234567890123456789012",
        "TMA_SESSION_STRING": "test_session",
        "TMA_SESSION_FILE": "test.session",
        "TMA_MINI_APP_URL": "https://example.com/app",
        "TMA_MINI_APP_START_PARAM": "start_param",
    }
    # Use mocker.patch.dict with os.environ object (not string)
    # pytest-mock will automatically undo the patch after fixture completes
    mocker.patch.dict(os.environ, env_vars, clear=True)
    yield env_vars


@fixture
def mock_environment_type_conversion(mocker) -> dict[str, str]:
    """
    Mock environment variables for testing type conversion.

    Returns:
        dict[str, str]: Environment variables for type conversion testing.
    """
    env_vars = {
        "TMA_API_ID": "12345",
        "TMA_API_HASH": "12345678901234567890123456789012",
        "TMA_SESSION_STRING": "test_session",
        "TMA_TIMEOUT": "30",
        "TMA_RETRY_COUNT": "3",
        "TMA_RETRY_DELAY": "1.0",
    }
    # Use mocker.patch.dict with os.environ object (not string)
    # pytest-mock will automatically undo the patch after fixture completes
    mocker.patch.dict(os.environ, env_vars, clear=True)
    yield env_vars


@fixture
def mock_environment_invalid_type_conversion(mocker) -> dict[str, str]:
    """
    Mock environment variables with invalid type conversion for testing.

    Returns:
        dict[str, str]: Environment variables with invalid type conversion.
    """
    env_vars = {
        "TMA_API_ID": "12345",
        "TMA_API_HASH": "12345678901234567890123456789012",
        "TMA_TIMEOUT": "invalid",
    }
    # Use mocker.patch.dict with os.environ object (not string)
    # pytest-mock will automatically undo the patch after fixture completes
    mocker.patch.dict(os.environ, env_vars, clear=True)
    yield env_vars


@fixture
def mock_environment_missing_session_string(mocker) -> dict[str, str]:
    """
    Mock environment variables missing TMA_SESSION_STRING for testing.

    Returns:
        dict[str, str]: Environment variables missing TMA_SESSION_STRING.
    """
    env_vars = {
        "TMA_API_ID": "12345",
        "TMA_API_HASH": "12345678901234567890123456789012",
    }
    # Use mocker.patch.dict with os.environ object (not string)
    # pytest-mock will automatically undo the patch after fixture completes
    mocker.patch.dict(os.environ, env_vars, clear=True)
    yield env_vars


@fixture
def mock_environment_invalid_api_hash_length(mocker) -> dict[str, str]:
    """
    Mock environment variables with invalid TMA_API_HASH length for testing.

    Returns:
        dict[str, str]: Environment variables with invalid TMA_API_HASH length.
    """
    env_vars = {
        "TMA_API_ID": "12345",
        "TMA_API_HASH": "short",  # Invalid length (should be 32 chars)
    }
    # Use mocker.patch.dict with os.environ object (not string)
    # pytest-mock will automatically undo the patch after fixture completes
    mocker.patch.dict(os.environ, env_vars, clear=True)
    yield env_vars


@fixture
def yaml_config_file_valid() -> str:
    """
    Return path to valid YAML config file for testing.

    Returns:
        str: Path to the YAML file.
    """
    import os

    return os.path.join(os.path.dirname(__file__), "..", "data", "valid_yaml.yaml")


@fixture
def yaml_config_file_minimal() -> str:
    """
    Return path to minimal YAML config file for testing.

    Returns:
        str: Path to the YAML file.
    """
    import os

    return os.path.join(os.path.dirname(__file__), "..", "data", "minimal_config.yaml")


@fixture
def yaml_config_file_with_file_session() -> str:
    """
    Return path to YAML config file with session_file for testing.

    Returns:
        str: Path to the YAML file.
    """
    import os

    return os.path.join(
        os.path.dirname(__file__), "..", "data", "config_with_file.yaml"
    )


@fixture
def yaml_config_file_invalid() -> str:
    """
    Return path to invalid YAML config file for testing.

    Returns:
        str: Path to the YAML file.
    """
    import os

    return os.path.join(os.path.dirname(__file__), "..", "data", "invalid_config.yaml")


@fixture
def yaml_config_file_missing_session() -> str:
    """
    Return path to YAML config file missing session for testing.

    Returns:
        str: Path to the YAML file.
    """
    import os

    return os.path.join(
        os.path.dirname(__file__), "..", "data", "missing_session_config.yaml"
    )


@fixture
def yaml_config_file_with_mini_app() -> str:
    """
    Return path to YAML config file with mini app settings for testing.

    Returns:
        str: Path to the YAML file.
    """
    import os

    return os.path.join(os.path.dirname(__file__), "..", "data", "mini_app_config.yaml")


@fixture
def yaml_config_file_empty() -> str:
    """
    Return path to empty YAML config file for testing.

    Returns:
        str: Path to the YAML file.
    """
    import os

    return os.path.join(os.path.dirname(__file__), "..", "data", "empty_config.yaml")


@fixture
def yaml_config_file_invalid_format() -> str:
    """
    Return path to YAML config file with invalid format for testing.

    Returns:
        str: Path to the YAML file.
    """
    import os

    return os.path.join(
        os.path.dirname(__file__), "..", "data", "invalid_format_config.yaml"
    )


# ============================================================================
# YAML config data fixtures (parsed YAML data)
# ============================================================================


def _load_yaml_data(file_name: str) -> dict:
    """
    Helper function to load YAML data from file.

    Sensitive fields (api_hash, session_string, session_file) are overridden
    by environment variables if they are set:
    - TMA_API_HASH overrides api_hash
    - TMA_SESSION_STRING overrides session_string
    - TMA_SESSION_FILE overrides session_file

    Args:
        file_name: Name of the YAML file in tests/data/.

    Returns:
        dict: Parsed YAML data with optional env var overrides.
    """
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", file_name)
    with open(file_path, "r") as f:
        config_data = load(f, Loader=SafeLoader)

    # Override sensitive fields with environment variables if present
    if environ.get("TMA_API_HASH"):
        config_data["api_hash"] = environ.get("TMA_API_HASH")
    if environ.get("TMA_SESSION_STRING"):
        config_data["session_string"] = environ.get("TMA_SESSION_STRING")
        # Remove session_file if session_string is provided via env
        config_data.pop("session_file", None)
    elif environ.get("TMA_SESSION_FILE"):
        config_data["session_file"] = environ.get("TMA_SESSION_FILE")
        # Remove session_string if session_file is provided via env
        config_data.pop("session_string", None)

    return config_data


@fixture
def yaml_config_data_valid() -> dict:
    """
    Return parsed YAML config data for valid config.

    Returns:
        dict: Parsed YAML config data.
    """
    return _load_yaml_data("valid_yaml.yaml")


@fixture
def yaml_config_data_minimal() -> dict:
    """
    Return parsed YAML config data for minimal config.

    Returns:
        dict: Parsed YAML config data.
    """
    return _load_yaml_data("minimal_config.yaml")


@fixture
def yaml_config_data_with_file_session() -> dict:
    """
    Return parsed YAML config data with session_file.

    Returns:
        dict: Parsed YAML config data.
    """
    return _load_yaml_data("config_with_file.yaml")


@fixture
def yaml_config_data_with_mini_app() -> dict:
    """
    Return parsed YAML config data with mini app settings.

    Returns:
        dict: Parsed YAML config data.
    """
    return _load_yaml_data("mini_app_config.yaml")
