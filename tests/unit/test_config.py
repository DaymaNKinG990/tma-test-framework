"""
Unit tests for TMA Framework configuration.
"""

# Python imports
import os
from msgspec import convert, to_builtins
from pytest import mark, raises

# Local imports
from tma_test_framework.config import Config


@mark.unit
def test_valid_config_creation(valid_config_data: dict[str, int | str | float]) -> None:
    """
    Test creating a valid configuration.

    Args:
        valid_config_data: Valid configuration data.
    """
    config = Config(**valid_config_data)  # type: ignore[arg-type]
    assert config.api_id == valid_config_data.get("api_id"), "API ID does not match"
    assert config.api_hash == valid_config_data.get("api_hash"), (
        "API hash does not match"
    )
    assert config.session_string == valid_config_data.get("session_string"), (
        "Session string does not match"
    )
    assert config.timeout == valid_config_data.get("timeout"), "Timeout does not match"
    assert config.retry_count == valid_config_data.get("retry_count"), (
        "Retry count does not match"
    )
    assert config.retry_delay == valid_config_data.get("retry_delay"), (
        "Retry delay does not match"
    )
    assert config.log_level == valid_config_data.get("log_level"), (
        "Log level does not match"
    )


@mark.unit
def test_valid_config_with_file(
    valid_config_with_file_data: dict[str, int | str | float],
) -> None:
    """
    Test creating a valid configuration with session file.

    Args:
        valid_config_with_file_data: Valid configuration data with session file.
    """
    config = Config(**valid_config_with_file_data)  # type: ignore[arg-type]
    assert config.api_id == valid_config_with_file_data.get("api_id"), (
        "API ID does not match"
    )
    assert config.api_hash == valid_config_with_file_data.get("api_hash"), (
        "API hash does not match"
    )
    assert config.session_file == valid_config_with_file_data.get("session_file"), (
        "Session file does not match"
    )
    assert config.session_string is None, "Session string should be None"


@mark.unit
def test_config_default_values(
    config_data_for_default_values: dict[str, int | str],
) -> None:
    """Test configuration default values."""
    config = Config(**config_data_for_default_values)  # type: ignore[arg-type]
    assert config.timeout == config_data_for_default_values.get("timeout"), (
        "Timeout should be default 30"
    )
    assert config.retry_count == config_data_for_default_values.get("retry_count"), (
        "Retry count should be default 3"
    )
    assert config.retry_delay == config_data_for_default_values.get("retry_delay"), (
        "Retry delay should be default 1.0"
    )
    assert config.log_level == config_data_for_default_values.get("log_level"), (
        "Log level should be default INFO"
    )
    assert config.mini_app_url is config_data_for_default_values.get("mini_app_url"), (
        "Mini app URL should be None"
    )
    assert config.mini_app_start_param is config_data_for_default_values.get(
        "mini_app_start_param"
    ), "Mini app start param should be None"


@mark.unit
def test_config_validation_success(
    valid_config_data: dict[str, int | str | float],
) -> None:
    """
    Test successful configuration validation.

    Args:
        valid_config_data: Valid configuration data.
    """
    config = Config(**valid_config_data)  # type: ignore[arg-type]
    assert config.api_id > 0, "API ID should be greater than 0"
    assert config.api_hash, "API hash should be not None"
    assert config.session_string or config.session_file, (
        "Session string or session file should be provided"
    )


@mark.unit
def test_config_validation_missing_api_id(
    invalid_config_data_without_api_id: dict[str, str | int | float],
) -> None:
    """
    Test configuration validation with missing api_id.

    Args:
        invalid_config_data_without_api_id: Invalid configuration data without api_id.
    """
    with raises(TypeError, match="Missing required argument 'api_id'"):
        Config(**invalid_config_data_without_api_id)  # type: ignore[arg-type]


@mark.unit
def test_config_validation_missing_api_hash(
    invalid_config_data_without_api_hash: dict[str, int | str],
) -> None:
    """
    Test configuration validation with missing api_hash.

    Args:
        invalid_config_data_without_api_hash: Invalid configuration data without api_hash.
    """
    with raises(TypeError, match="Missing required argument 'api_hash'"):
        Config(**invalid_config_data_without_api_hash)  # type: ignore[arg-type]


@mark.unit
def test_config_validation_missing_session(
    config_data_for_missing_session: dict[str, int | str],
) -> None:
    """
    Test configuration validation with missing session.

    Args:
        config_data_for_missing_session: Configuration data with missing session.
    """
    with raises(ValueError, match="Session required"):
        Config(**config_data_for_missing_session)  # type: ignore[arg-type]


@mark.unit
def test_config_validation_invalid_log_level(
    config_data_for_invalid_log_level: dict[str, int | str],
) -> None:
    """
    Test configuration validation with invalid log level.

    Args:
        config_data_for_invalid_log_level: Configuration data with invalid log level.
    """
    with raises(ValueError, match="Invalid log level"):
        Config(**config_data_for_invalid_log_level)  # type: ignore[arg-type]


@mark.unit
def test_config_validation_invalid_retry_count(
    config_data_for_invalid_retry_count: dict[str, int | str],
) -> None:
    """
    Test configuration validation with invalid retry count.

    Args:
        config_data_for_invalid_retry_count: Configuration data with invalid retry count.
    """
    with raises(ValueError, match="retry_count must be between 0 and 10"):
        Config(**config_data_for_invalid_retry_count)  # type: ignore[arg-type]


@mark.unit
def test_config_validation_invalid_retry_delay(
    config_data_for_invalid_retry_delay: dict[str, int | str | float],
) -> None:
    """
    Test configuration validation with invalid retry delay.

    Args:
        config_data_for_invalid_retry_delay: Configuration data with invalid retry delay.
    """
    with raises(ValueError, match="retry_delay must be between 0.1 and 10.0"):
        Config(**config_data_for_invalid_retry_delay)  # type: ignore[arg-type]


@mark.unit
def test_config_validation_minimal_values(
    valid_config_data_minimal: dict[str, int | str | float],
) -> None:
    """
    Test configuration validation with minimal values.

    Args:
        valid_config_data_minimal: Valid configuration data minimal.
    """
    config = Config(**valid_config_data_minimal)  # type: ignore[arg-type]
    assert config.api_id == valid_config_data_minimal.get("api_id"), (
        "API ID does not match"
    )
    assert config.api_hash == valid_config_data_minimal.get("api_hash"), (
        "API hash does not match"
    )
    assert config.session_string == valid_config_data_minimal.get("session_string"), (
        "Session string does not match"
    )
    assert config.timeout == valid_config_data_minimal.get("timeout"), (
        "Timeout does not match"
    )
    assert config.retry_count == valid_config_data_minimal.get("retry_count"), (
        "Retry count does not match"
    )
    assert config.retry_delay == valid_config_data_minimal.get("retry_delay"), (
        "Retry delay does not match"
    )


@mark.unit
def test_config_validation_maximal_values(
    valid_config_data_maximal: dict[str, int | str | float],
) -> None:
    """
    Test configuration validation with maximal values.

    Args:
        valid_config_data_maximal: Valid configuration data maximal.
    """
    config = Config(**valid_config_data_maximal)  # type: ignore[arg-type]
    assert config.api_id == valid_config_data_maximal.get("api_id"), (
        "API ID does not match"
    )
    assert config.api_hash == valid_config_data_maximal.get("api_hash"), (
        "API hash does not match"
    )
    assert config.session_string == valid_config_data_maximal.get("session_string"), (
        "Session string does not match"
    )
    assert config.timeout == valid_config_data_maximal.get("timeout"), (
        "Timeout does not match"
    )
    assert config.retry_count == valid_config_data_maximal.get("retry_count"), (
        "Retry count does not match"
    )
    assert config.retry_delay == valid_config_data_maximal.get("retry_delay"), (
        "Retry delay does not match"
    )


@mark.unit
def test_config_validation_invalid_api_id(
    invalid_config_data_api_id: dict[str, int | str | float],
) -> None:
    """
    Test configuration validation with invalid api_id.

    Args:
        invalid_config_data_api_id: Invalid configuration data with invalid api_id.
    """
    with raises(ValueError):
        Config(**invalid_config_data_api_id)  # type: ignore[arg-type]


@mark.unit
def test_config_validation_invalid_minimal_retry_count(
    invalid_config_data_minimal_retry_count: dict[str, int | str | float],
) -> None:
    """
    Test configuration validation with invalid minimal retry count.

    Args:
        invalid_config_data_minimal_retry_count: Invalid configuration data with invalid minimal retry count.
    """
    with raises(ValueError, match="retry_count must be between 0 and 10"):
        Config(**invalid_config_data_minimal_retry_count)  # type: ignore[arg-type]


@mark.unit
def test_config_validation_invalid_minimal_retry_delay(
    invalid_config_data_minimal_retry_delay: dict[str, int | str | float],
) -> None:
    """
    Test configuration validation with invalid minimal retry delay.

    Args:
        invalid_config_data_minimal_retry_delay: Invalid configuration data with invalid minimal retry delay.
    """
    with raises(ValueError, match="retry_delay must be between 0.1 and 10.0"):
        Config(**invalid_config_data_minimal_retry_delay)  # type: ignore[arg-type]


@mark.unit
def test_config_validation_invalid_timeout(
    invalid_config_data_timeout: dict[str, int | str | float],
) -> None:
    """
    Test configuration validation with invalid timeout.

    Args:
        invalid_config_data_timeout: Invalid configuration data with invalid timeout.
    """
    with raises(ValueError, match="timeout must be between 1 and 300 seconds"):
        Config(**invalid_config_data_timeout)  # type: ignore[arg-type]


@mark.unit
def test_config_validation_invalid_maximal_retry_count(
    invalid_config_data_maximal_retry_count,
):
    """
    Test configuration validation with invalid maximal retry count.

    Args:
        invalid_config_data_maximal_retry_count: Invalid configuration data with invalid maximal retry count.
    """
    with raises(ValueError, match="retry_count must be between 0 and 10"):
        Config(**invalid_config_data_maximal_retry_count)


@mark.unit
def test_config_validation_invalid_maximal_retry_delay(
    invalid_config_data_maximal_retry_delay: dict[str, int | str | float],
) -> None:
    """
    Test configuration validation with invalid maximal retry delay.

    Args:
        invalid_config_data_maximal_retry_delay: Invalid configuration data with invalid maximal retry delay.
    """
    with raises(ValueError, match="retry_delay must be between 0.1 and 10.0"):
        Config(**invalid_config_data_maximal_retry_delay)  # type: ignore[arg-type]


@mark.unit
def test_config_serialization(valid_config_data: dict[str, int | str | float]) -> None:
    """
    Test configuration serialization.

    Args:
        valid_config_data: Valid configuration data.
    """
    config = Config(**valid_config_data)  # type: ignore[arg-type]
    config_dict = to_builtins(config)
    assert isinstance(config_dict, dict)
    assert config_dict.get("api_id") == valid_config_data.get("api_id")
    assert config_dict.get("api_hash") == valid_config_data.get("api_hash")


@mark.unit
def test_config_deserialization(
    valid_config_data: dict[str, int | str | float],
) -> None:
    """
    Test configuration deserialization.

    Args:
        valid_config_data: Valid configuration data.
    """
    config_dict = valid_config_data.copy()
    config = convert(config_dict, Config)
    assert isinstance(config, Config)
    assert config.api_id == valid_config_data.get("api_id")
    assert config.api_hash == valid_config_data.get("api_hash")


@mark.unit
def test_config_equality(valid_config_data: dict[str, int | str | float]) -> None:
    """
    Test configuration equality with same data.

    Args:
        valid_config_data: Valid configuration data.
    """
    config1 = Config(**valid_config_data)  # type: ignore[arg-type]
    config2 = Config(**valid_config_data)  # type: ignore[arg-type]
    assert config1 == config2, "Configuration should be equal"


@mark.unit
def test_config_inequality(
    valid_config_data: dict[str, int | str | float],
    valid_config_with_file_data: dict[str, int | str | float],
) -> None:
    """
    Test configuration inequality with different data.

    Args:
        valid_config_data: Valid configuration data.
        valid_config_with_file_data: Valid configuration data with file.
    """
    config1 = Config(**valid_config_data)  # type: ignore[arg-type]
    config2 = Config(**valid_config_with_file_data)  # type: ignore[arg-type]
    assert config1 != config2, "Configuration should be different"


@mark.unit
def test_config_hash_equality(valid_config_data: dict[str, int | str | float]) -> None:
    """
    Test configuration hash equality with same data.

    Args:
        valid_config_data: Valid configuration data.
    """
    config1 = Config(**valid_config_data)  # type: ignore[arg-type]
    config2 = Config(**valid_config_data)  # type: ignore[arg-type]
    assert hash(config1) == hash(config2), "Configuration hashes should be equal"


@mark.unit
def test_config_hash_inequality(
    valid_config_data: dict[str, int | str | float],
    valid_config_with_file_data: dict[str, int | str | float],
) -> None:
    """
    Test configuration hash inequality with different data.

    Args:
        valid_config_data: Valid configuration data.
        valid_config_with_file_data: Valid configuration data with file.
    """
    config1 = Config(**valid_config_data)  # type: ignore[arg-type]
    config2 = Config(**valid_config_with_file_data)  # type: ignore[arg-type]
    assert hash(config1) != hash(config2), "Configuration hashes should be different"


@mark.unit
def test_config_repr(valid_config_data: dict[str, int | str | float]) -> None:
    """
    Test configuration string representation.

    Args:
        valid_config_data: Valid configuration data.
    """
    config = Config(**valid_config_data)  # type: ignore[arg-type]
    repr_str = repr(config)
    assert "Config" in repr_str
    assert f"api_id={valid_config_data.get('api_id')}" in repr_str
    assert f"api_hash='{valid_config_data.get('api_hash')}'" in repr_str


@mark.unit
def test_from_env_valid_variables(mock_environment: dict[str, str]) -> None:
    """
    Test creating config from valid environment variables.

    Args:
        mock_environment: Mock environment variables (already patched by fixture).
    """
    # Environment is already patched by mock_environment fixture
    config = Config.from_env()
    assert config.api_id == int(mock_environment.get("TMA_API_ID") or "0"), (
        "API ID does not match"
    )
    assert config.api_hash == mock_environment.get("TMA_API_HASH"), (
        "API hash does not match"
    )
    assert config.session_string == mock_environment.get("TMA_SESSION_STRING"), (
        "Session string does not match"
    )
    assert config.mini_app_url == mock_environment.get("TMA_MINI_APP_URL"), (
        "Mini app URL does not match"
    )
    assert config.mini_app_start_param == mock_environment.get(
        "TMA_MINI_APP_START_PARAM"
    ), "Mini app start param does not match"
    assert config.timeout == int(mock_environment.get("TMA_TIMEOUT") or "30"), (
        "Timeout does not match"
    )
    assert config.retry_count == int(mock_environment.get("TMA_RETRY_COUNT") or "3"), (
        "Retry count does not match"
    )
    assert config.retry_delay == float(
        mock_environment.get("TMA_RETRY_DELAY") or "1.0"
    ), "Retry delay does not match"
    assert config.log_level == mock_environment.get("TMA_LOG_LEVEL"), (
        "Log level does not match"
    )


@mark.unit
def test_from_env_missing_required_variables(
    mock_empty_environment: dict[str, str],
) -> None:
    """
    Test creating config with missing required environment variables.

    Args:
        mock_empty_environment: Mock empty environment variables (already patched by fixture).
    """
    # Environment is already patched by mock_empty_environment fixture
    # api_id is checked first, then api_hash
    with raises(ValueError, match="TMA_API_ID environment variable is required"):
        Config.from_env()


@mark.unit
def test_from_env_missing_api_id(
    mock_environment_missing_api_id: dict[str, str],
) -> None:
    """
    Test creating config with missing TMA_API_ID.

    Args:
        mock_environment_missing_api_id: Mock environment variables missing TMA_API_ID (already patched by fixture).
    """
    # Environment is already patched by mock_environment_missing_api_id fixture
    with raises(ValueError, match="TMA_API_ID environment variable is required"):
        Config.from_env()


@mark.unit
def test_from_env_missing_api_hash(
    mock_environment_missing_api_hash: dict[str, str],
) -> None:
    """
    Test creating config with missing TMA_API_HASH.

    Args:
        mock_environment_missing_api_hash: Mock environment variables missing TMA_API_HASH (already patched by fixture).
    """
    # Environment is already patched by mock_environment_missing_api_hash fixture
    with raises(ValueError, match="TMA_API_HASH environment variable is required"):
        Config.from_env()


@mark.unit
def test_from_env_invalid_api_id(
    mock_environment_invalid_api_id: dict[str, str],
) -> None:
    """
    Test creating config with invalid TMA_API_ID.

    Args:
        mock_environment_invalid_api_id: Mock environment variables with invalid TMA_API_ID (already patched by fixture).
    """
    # Environment is already patched by mock_environment_invalid_api_id fixture
    with raises(ValueError):
        Config.from_env()


@mark.unit
def test_from_env_default_values(
    mock_environment_default_values: dict[str, str],
) -> None:
    """
    Test creating config with default values from environment.

    Args:
        mock_environment_default_values: Mock environment variables with default values (already patched by fixture).
    """
    # Environment is already patched by mock_environment_default_values fixture
    config = Config.from_env()
    assert config.timeout == int(
        mock_environment_default_values.get("TMA_TIMEOUT") or "30"
    ), "Timeout should be default 30"
    assert config.retry_count == int(
        mock_environment_default_values.get("TMA_RETRY_COUNT") or "3"
    ), "Retry count should be default 3"
    assert config.retry_delay == float(
        mock_environment_default_values.get("TMA_RETRY_DELAY") or "1.0"
    ), "Retry delay should be default 1.0"
    assert config.log_level == mock_environment_default_values.get("TMA_LOG_LEVEL"), (
        "Log level should be default INFO"
    )


@mark.unit
def test_from_env_override_defaults(
    mock_environment_override_defaults: dict[str, str],
) -> None:
    """
    Test creating config with overridden default values.

    Args:
        mock_environment_override_defaults: Mock environment variables with overridden defaults (already patched by fixture).
    """
    # Environment is already patched by mock_environment_override_defaults fixture
    config = Config.from_env()
    assert config.timeout == int(
        mock_environment_override_defaults.get("TMA_TIMEOUT") or "60"
    ), "Timeout should be overridden to 60"
    assert config.retry_count == int(
        mock_environment_override_defaults.get("TMA_RETRY_COUNT") or "5"
    ), "Retry count should be overridden to 5"
    assert config.retry_delay == float(
        mock_environment_override_defaults.get("TMA_RETRY_DELAY") or "2.0"
    ), "Retry delay should be overridden to 2.0"
    assert config.log_level == mock_environment_override_defaults.get(
        "TMA_LOG_LEVEL"
    ), "Log level should be overridden to WARNING"


@mark.unit
def test_from_env_optional_variables(
    mock_environment_optional_variables: dict[str, str],
) -> None:
    """
    Test creating config with optional environment variables.
    Both session_string and session_file are set, which should raise ValueError.

    Args:
        mock_environment_optional_variables: Mock environment variables with optional variables (already patched by fixture).
    """
    # Environment is already patched by mock_environment_optional_variables fixture
    # Both TMA_SESSION_STRING and TMA_SESSION_FILE are set, which should raise ValueError
    with raises(
        ValueError, match="Cannot provide both session_string and session_file"
    ):
        Config.from_env()


@mark.unit
def test_from_env_type_conversion(
    mock_environment_type_conversion: dict[str, str],
) -> None:
    """
    Test type conversion in from_env method.

    Args:
        mock_environment_type_conversion: Mock environment variables for type conversion testing (already patched by fixture).
    """
    # Environment is already patched by mock_environment_type_conversion fixture
    config = Config.from_env()
    assert isinstance(config.api_id, int), "API ID should be int"
    assert isinstance(config.timeout, int), "Timeout should be int"
    assert isinstance(config.retry_count, int), "Retry count should be int"
    assert isinstance(config.retry_delay, float), "Retry delay should be float"


@mark.unit
def test_from_env_invalid_type_conversion(
    mock_environment_invalid_type_conversion: dict[str, str],
) -> None:
    """
    Test invalid type conversion in from_env method.

    Args:
        mock_environment_invalid_type_conversion: Mock environment variables with invalid type conversion.
    """
    # Environment is already set by fixture
    with raises(ValueError):
        Config.from_env()


@mark.unit
def test_from_env_with_empty_strings(
    monkeypatch, mock_environment_missing_session_string: dict[str, str]
) -> None:
    """
    Test from_env method with missing session string.

    Args:
        mock_environment_missing_session_string: Mock environment variables missing TMA_SESSION_STRING.
    """
    # Environment is already set by fixture
    import re

    pattern = re.escape(
        "Session required. Provide one of: session_string (for saved session) or session_file (for file session). You need to authenticate manually first to get a session."
    )
    with raises(ValueError, match=pattern):
        Config.from_env()


@mark.unit
def test_from_env_with_invalid_api_id(
    monkeypatch, mock_environment_invalid_api_id: dict[str, str]
) -> None:
    """
    Test from_env method with invalid TMA_API_ID.

    Args:
        mock_environment_invalid_api_id: Mock environment variables with invalid TMA_API_ID.
    """
    # Environment is already set by fixture
    # Invalid string "invalid" will cause ValueError when converting to int
    with raises(ValueError, match="Invalid int value for TMA_API_ID: 'invalid'"):
        Config.from_env()


@mark.unit
def test_from_env_with_invalid_api_hash_length(
    monkeypatch, mock_environment_invalid_api_hash_length: dict[str, str]
) -> None:
    """
    Test from_env method with invalid TMA_API_HASH length.

    Args:
        mock_environment_invalid_api_hash_length: Mock environment variables with invalid TMA_API_HASH length.
    """
    # Environment is already set by fixture
    with raises(ValueError, match="api_hash must be exactly 32 characters long, got"):
        Config.from_env()


@mark.unit
def test_config_with_empty_strings(
    config_data_for_empty_strings: dict[str, int | str],
) -> None:
    """
    Test configuration with empty strings.

    Args:
        config_data_for_empty_strings: Configuration data with empty strings.
    """
    with raises(ValueError, match="api_hash must be exactly 32 characters long"):
        Config(**config_data_for_empty_strings)  # type: ignore[arg-type]


@mark.unit
def test_config_with_whitespace_strings(
    config_data_for_whitespace_strings: dict[str, int | str],
) -> None:
    """
    Test configuration with whitespace strings.

    Args:
        config_data_for_whitespace_strings: Configuration data with whitespace strings.
    """
    with raises(
        ValueError, match="session_string cannot be empty or contain only whitespace"
    ):
        Config(**config_data_for_whitespace_strings)  # type: ignore[arg-type]


@mark.unit
def test_config_with_very_long_strings(
    config_data_for_very_long_strings: dict[str, int | str],
) -> None:
    """
    Test configuration with very long strings.

    Args:
        config_data_for_very_long_strings: Configuration data with very long strings.
    """
    config = Config(**config_data_for_very_long_strings)  # type: ignore[arg-type]
    assert config.session_string == config_data_for_very_long_strings["session_string"]


@mark.unit
def test_config_with_special_characters(
    config_data_for_special_characters: dict[str, int | str],
) -> None:
    """
    Test configuration with special characters.

    Args:
        config_data_for_special_characters: Configuration data with special characters.
    """
    config = Config(**config_data_for_special_characters)  # type: ignore[arg-type]
    assert config.session_string == config_data_for_special_characters.get(
        "session_string"
    ), "Session string should match"


@mark.unit
def test_config_with_unicode_characters(
    config_data_for_unicode_characters: dict[str, int | str],
) -> None:
    """
    Test configuration with unicode characters.

    Args:
        config_data_for_unicode_characters: Configuration data with unicode characters.
    """
    config = Config(**config_data_for_unicode_characters)  # type: ignore[arg-type]
    assert config.session_string == config_data_for_unicode_characters.get(
        "session_string"
    ), "Session string should match"


@mark.unit
def test_config_with_none_values(
    config_data_for_none_values: dict[str, int | str | None],
) -> None:
    """
    Test configuration with None values.

    Args:
        config_data_for_none_values: Configuration data with None values.
    """
    config = Config(**config_data_for_none_values)  # type: ignore[arg-type]
    assert config.mini_app_url is None, "Mini app URL should be None"
    assert config.mini_app_start_param is None, "Mini app start param should be None"


@mark.unit
def test_config_with_both_session_methods(
    config_data_for_both_session_methods: dict[str, int | str],
) -> None:
    """
    Test configuration with both session_string and session_file should raise ValueError.

    Args:
        config_data_for_both_session_methods: Configuration data with both session_string and session_file.
    """
    with raises(
        ValueError, match="Cannot provide both session_string and session_file"
    ):
        Config(**config_data_for_both_session_methods)  # type: ignore[arg-type]


@mark.unit
def test_config_mini_app_url_with_whitespace() -> None:
    """
    Test that mini_app_url with whitespace at beginning/end is preserved as-is (no strip).

    This test verifies that optional fields like mini_app_url preserve whitespace
    and are not automatically stripped, as per specification requirement.
    """
    url_with_whitespace = "  https://example.com/mini-app  "
    config = Config(
        api_id=12345,
        api_hash="12345678901234567890123456789012",
        session_string="test_session",
        mini_app_url=url_with_whitespace,
    )
    assert config.mini_app_url == url_with_whitespace, (
        "mini_app_url should preserve whitespace without strip"
    )


@mark.unit
def test_config_log_level_debug(
    config_data_for_log_level_debug: dict[str, int | str],
) -> None:
    """
    Test configuration log level debug.

    Args:
        config_data_for_log_level_debug: Configuration data with log level debug.
    """
    config = Config(**config_data_for_log_level_debug)  # type: ignore[arg-type]
    assert config.log_level == config_data_for_log_level_debug.get("log_level"), (
        "Log level should match"
    )


@mark.unit
def test_config_log_level_info(
    config_data_for_log_level_info: dict[str, int | str],
) -> None:
    """
    Test configuration log level info.

    Args:
        config_data_for_log_level_info: Configuration data with log level info.
    """
    config = Config(**config_data_for_log_level_info)  # type: ignore[arg-type]
    assert config.log_level == config_data_for_log_level_info.get("log_level"), (
        "Log level should match"
    )


@mark.unit
def test_config_log_level_warning(
    config_data_for_log_level_warning: dict[str, int | str],
) -> None:
    """
    Test configuration log level warning.

    Args:
        config_data_for_log_level_warning: Configuration data with log level warning.
    """
    config = Config(**config_data_for_log_level_warning)  # type: ignore[arg-type]
    assert config.log_level == config_data_for_log_level_warning.get("log_level"), (
        "Log level should match"
    )


@mark.unit
def test_config_log_level_error(
    config_data_for_log_level_error: dict[str, int | str],
) -> None:
    """
    Test configuration log level error.

    Args:
        config_data_for_log_level_error: Configuration data with log level error.
    """
    config = Config(**config_data_for_log_level_error)  # type: ignore[arg-type]
    assert config.log_level == config_data_for_log_level_error.get("log_level"), (
        "Log level should match"
    )


@mark.unit
def test_config_log_level_critical(
    config_data_for_log_level_critical: dict[str, int | str],
) -> None:
    """
    Test configuration log level critical.

    Args:
        config_data_for_log_level_critical: Configuration data with log level critical.
    """
    config = Config(**config_data_for_log_level_critical)  # type: ignore[arg-type]
    assert config.log_level == config_data_for_log_level_critical.get("log_level"), (
        "Log level should match"
    )


@mark.unit
def test_config_log_level_case_sensitivity(
    config_data_for_log_level_case_sensitivity: dict[str, int | str],
) -> None:
    """
    Test log level case sensitivity.

    Args:
        config_data_for_log_level_case_sensitivity: Configuration data with log level case sensitivity.
    """
    with raises(ValueError, match="Invalid log level"):
        Config(**config_data_for_log_level_case_sensitivity)  # type: ignore[arg-type]


@mark.unit
def test_config_float_precision(
    config_data_for_float_precision: dict[str, int | str | float],
) -> None:
    """
    Test float precision in retry_delay.

    Args:
        config_data_for_float_precision: Configuration data with float precision.
    """
    config = Config(**config_data_for_float_precision)  # type: ignore[arg-type]
    assert config.retry_delay == config_data_for_float_precision.get("retry_delay"), (
        "Retry delay should match"
    )


@mark.unit
def test_config_large_numbers(
    config_data_for_large_numbers: dict[str, int | str | float],
) -> None:
    """
    Test configuration with large numbers.

    Args:
        config_data_for_large_numbers: Configuration data with large numbers.
    """
    config = Config(**config_data_for_large_numbers)  # type: ignore[arg-type]
    assert config.api_id == config_data_for_large_numbers.get("api_id"), (
        "API ID should match"
    )
    assert config.timeout == config_data_for_large_numbers.get("timeout"), (
        "Timeout should match"
    )
    assert config.retry_count == config_data_for_large_numbers.get("retry_count"), (
        "Retry count should match"
    )
    assert config.retry_delay == config_data_for_large_numbers.get("retry_delay"), (
        "Retry delay should match"
    )


@mark.unit
def test_from_yaml_valid_file(
    yaml_config_file_valid: str, yaml_config_data_valid: dict
) -> None:
    """
    Test creating config from valid YAML file.

    Args:
        yaml_config_file_valid: Path to valid YAML config file.
        yaml_config_data_valid: Parsed YAML config data.
    """
    config = Config.from_yaml(yaml_config_file_valid)
    assert config.api_id == yaml_config_data_valid.get("api_id"), "API ID should match"
    assert config.api_hash == yaml_config_data_valid.get("api_hash"), (
        "API hash should match"
    )
    assert config.session_string == yaml_config_data_valid.get("session_string"), (
        "Session string should match"
    )
    assert config.timeout == yaml_config_data_valid.get("timeout"), (
        "Timeout should match"
    )
    assert config.retry_count == yaml_config_data_valid.get("retry_count"), (
        "Retry count should match"
    )
    assert config.retry_delay == yaml_config_data_valid.get("retry_delay"), (
        "Retry delay should match"
    )
    assert config.log_level == yaml_config_data_valid.get("log_level"), (
        "Log level should match"
    )


@mark.unit
def test_from_yaml_minimal_file(
    yaml_config_file_minimal: str, yaml_config_data_minimal: dict
) -> None:
    """
    Test creating config from minimal YAML file.

    Args:
        yaml_config_file_minimal: Path to minimal YAML config file.
        yaml_config_data_minimal: Parsed YAML config data.
    """
    config = Config.from_yaml(yaml_config_file_minimal)
    assert config.api_id == yaml_config_data_minimal.get("api_id"), (
        "API ID should match"
    )
    assert config.api_hash == yaml_config_data_minimal.get("api_hash"), (
        "API hash should match"
    )
    assert config.session_string == yaml_config_data_minimal.get("session_string"), (
        "Session string should match"
    )
    assert config.timeout == yaml_config_data_minimal.get("timeout"), (
        "Timeout should match"
    )
    assert config.retry_count == yaml_config_data_minimal.get("retry_count"), (
        "Retry count should match"
    )
    assert config.retry_delay == yaml_config_data_minimal.get("retry_delay"), (
        "Retry delay should match"
    )
    assert config.log_level == yaml_config_data_minimal.get("log_level", "INFO"), (
        "Log level should be default INFO"
    )


@mark.unit
def test_from_yaml_with_file_session(
    yaml_config_file_with_file_session: str, yaml_config_data_with_file_session: dict
) -> None:
    """
    Test creating config from YAML file with session_file.

    Args:
        yaml_config_file_with_file_session: Path to YAML config file with session_file.
        yaml_config_data_with_file_session: Parsed YAML config data.
    """
    config = Config.from_yaml(yaml_config_file_with_file_session)
    assert config.api_id == yaml_config_data_with_file_session.get("api_id"), (
        "API ID should match"
    )
    assert config.api_hash == yaml_config_data_with_file_session.get("api_hash"), (
        "API hash should match"
    )
    assert config.session_file == yaml_config_data_with_file_session.get(
        "session_file"
    ), "Session file should match"
    assert config.session_string == yaml_config_data_with_file_session.get(
        "session_string"
    ), "Session string should be None"
    assert config.timeout == yaml_config_data_with_file_session.get("timeout"), (
        "Timeout should match"
    )
    assert config.retry_count == yaml_config_data_with_file_session.get(
        "retry_count"
    ), "Retry count should match"
    assert config.retry_delay == yaml_config_data_with_file_session.get(
        "retry_delay"
    ), "Retry delay should match"
    assert config.log_level == yaml_config_data_with_file_session.get("log_level"), (
        "Log level should match"
    )


@mark.unit
def test_from_yaml_with_mini_app(
    yaml_config_file_with_mini_app: str, yaml_config_data_with_mini_app: dict
) -> None:
    """
    Test creating config from YAML file with mini app settings.

    Args:
        yaml_config_file_with_mini_app: Path to YAML config file with mini app settings.
        yaml_config_data_with_mini_app: Parsed YAML config data.
    """
    config = Config.from_yaml(yaml_config_file_with_mini_app)
    assert config.api_id == yaml_config_data_with_mini_app.get("api_id"), (
        "API ID should match"
    )
    assert config.api_hash == yaml_config_data_with_mini_app.get("api_hash"), (
        "API hash should match"
    )
    assert config.session_string == yaml_config_data_with_mini_app.get(
        "session_string"
    ), "Session string should match"
    assert config.mini_app_url == yaml_config_data_with_mini_app.get("mini_app_url"), (
        "Mini app URL should match"
    )
    assert config.mini_app_start_param == yaml_config_data_with_mini_app.get(
        "mini_app_start_param"
    ), "Mini app start param should match"
    assert config.timeout == yaml_config_data_with_mini_app.get("timeout"), (
        "Timeout should match"
    )
    assert config.retry_count == yaml_config_data_with_mini_app.get("retry_count"), (
        "Retry count should match"
    )
    assert config.retry_delay == yaml_config_data_with_mini_app.get("retry_delay"), (
        "Retry delay should match"
    )
    assert config.log_level == yaml_config_data_with_mini_app.get("log_level"), (
        "Log level should match"
    )


@mark.unit
def test_from_yaml_invalid_file(yaml_config_file_invalid: str) -> None:
    """
    Test creating config from invalid YAML file.

    Args:
        yaml_config_file_invalid: Path to invalid YAML config file.
    """
    with raises(ValueError):
        Config.from_yaml(yaml_config_file_invalid)


@mark.unit
def test_from_yaml_missing_session(yaml_config_file_missing_session: str) -> None:
    """
    Test creating config from YAML file missing session.

    Args:
        yaml_config_file_missing_session: Path to YAML config file missing session.
    """
    with raises(ValueError, match="Session required"):
        Config.from_yaml(yaml_config_file_missing_session)


@mark.unit
def test_from_yaml_nonexistent_file() -> None:
    """
    Test creating config from nonexistent YAML file.
    """
    with raises(ValueError, match="Configuration file not found"):
        Config.from_yaml("nonexistent_config.yaml")


@mark.unit
def test_from_yaml_invalid_yaml_format(yaml_config_file_invalid_format: str) -> None:
    """
    Test creating config from YAML file with invalid format.

    Args:
        yaml_config_file_invalid_format: Path to invalid YAML config file format.
    """
    with raises(ValueError, match="Failed to load configuration"):
        Config.from_yaml(yaml_config_file_invalid_format)


@mark.unit
def test_from_yaml_empty_file(yaml_config_file_empty: str) -> None:
    """
    Test creating config from empty YAML file.

    Args:
        yaml_config_file_empty: Path to empty YAML config file.
    """
    with raises(ValueError, match="Failed to load configuration"):
        Config.from_yaml(yaml_config_file_empty)


@mark.unit
@mark.parametrize("api_id", [1, 999_999_999])
def test_config_valid_api_id(api_id: int) -> None:
    """Test valid api_id values."""
    config = Config(
        api_id=api_id,
        api_hash="12345678901234567890123456789012",
        session_string="test_session",
    )
    assert config.api_id == api_id


@mark.unit
@mark.parametrize("api_id", [0, -1, 1_000_000_000])
def test_config_invalid_api_id(api_id: int) -> None:
    """Test invalid api_id values."""
    with raises(ValueError, match="api_id must be between 1 and 999999999"):
        Config(
            api_id=api_id,
            api_hash="12345678901234567890123456789012",
            session_string="test_session",
        )


@mark.unit
@mark.parametrize("api_hash_length", [32])
def test_config_valid_api_hash_length(api_hash_length: int) -> None:
    """Test valid api_hash length."""
    api_hash = "a" * api_hash_length
    config = Config(api_id=12345, api_hash=api_hash, session_string="test_session")
    assert len(config.api_hash) == api_hash_length


@mark.unit
@mark.parametrize("api_hash_length", [0, 31, 33])
def test_config_invalid_api_hash_length(api_hash_length: int) -> None:
    """Test invalid api_hash length."""
    api_hash = "a" * api_hash_length if api_hash_length > 0 else ""
    with raises(ValueError, match="api_hash must be exactly 32 characters long"):
        Config(api_id=12345, api_hash=api_hash, session_string="test_session")


@mark.unit
def test_config_api_hash_none() -> None:
    """Test api_hash with None value."""
    with raises(ValueError, match="api_hash must be exactly 32 characters long"):
        Config(
            api_id=12345,
            api_hash=None,  # type: ignore
            session_string="test_session",
        )


@mark.unit
@mark.parametrize("timeout", [1, 300])
def test_config_valid_timeout(timeout: int) -> None:
    """Test valid timeout values."""
    config = Config(
        api_id=12345,
        api_hash="12345678901234567890123456789012",
        session_string="test_session",
        timeout=timeout,
    )
    assert config.timeout == timeout


@mark.unit
@mark.parametrize("timeout", [0, 301, -5])
def test_config_invalid_timeout(timeout: int) -> None:
    """Test invalid timeout values."""
    with raises(ValueError, match="timeout must be between 1 and 300 seconds"):
        Config(
            api_id=12345,
            api_hash="12345678901234567890123456789012",
            session_string="test_session",
            timeout=timeout,
        )


@mark.unit
@mark.parametrize("retry_count", [0, 10])
def test_config_valid_retry_count(retry_count: int) -> None:
    """Test valid retry_count values."""
    config = Config(
        api_id=12345,
        api_hash="12345678901234567890123456789012",
        session_string="test_session",
        retry_count=retry_count,
    )
    assert config.retry_count == retry_count


@mark.unit
@mark.parametrize("retry_count", [-1, 11])
def test_config_invalid_retry_count(retry_count: int) -> None:
    """Test invalid retry_count values."""
    with raises(ValueError, match="retry_count must be between 0 and 10"):
        Config(
            api_id=12345,
            api_hash="12345678901234567890123456789012",
            session_string="test_session",
            retry_count=retry_count,
        )


@mark.unit
@mark.parametrize("retry_delay", [0.1, 10.0])
def test_config_valid_retry_delay(retry_delay: float) -> None:
    """Test valid retry_delay values."""
    config = Config(
        api_id=12345,
        api_hash="12345678901234567890123456789012",
        session_string="test_session",
        retry_delay=retry_delay,
    )
    assert config.retry_delay == retry_delay


@mark.unit
@mark.parametrize("retry_delay", [0.09, 10.01])
def test_config_invalid_retry_delay(retry_delay: float) -> None:
    """Test invalid retry_delay values."""
    with raises(ValueError, match="retry_delay must be between 0.1 and 10.0 seconds"):
        Config(
            api_id=12345,
            api_hash="12345678901234567890123456789012",
            session_string="test_session",
            retry_delay=retry_delay,
        )


@mark.unit
@mark.parametrize("log_level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
def test_config_valid_log_level(log_level: str) -> None:
    """Test valid log_level values."""
    config = Config(
        api_id=12345,
        api_hash="12345678901234567890123456789012",
        session_string="test_session",
        log_level=log_level,
    )
    assert config.log_level == log_level


@mark.unit
@mark.parametrize("log_level", ["debug", "Info", "TRACE", "INVALID", ""])
def test_config_invalid_log_level(log_level: str) -> None:
    """Test invalid log_level values."""
    with raises(ValueError, match="Invalid log level"):
        Config(
            api_id=12345,
            api_hash="12345678901234567890123456789012",
            session_string="test_session",
            log_level=log_level,
        )


@mark.unit
@mark.parametrize("session_string", [" ", "\t\n", ""])
def test_config_empty_whitespace_session_string(session_string: str) -> None:
    """Test empty or whitespace-only session_string."""
    with raises(
        ValueError, match="session_string cannot be empty or contain only whitespace"
    ):
        Config(
            api_id=12345,
            api_hash="12345678901234567890123456789012",
            session_string=session_string,
        )


@mark.unit
@mark.parametrize("session_file", [" ", "\t\n", ""])
def test_config_empty_whitespace_session_file(session_file: str) -> None:
    """Test empty or whitespace-only session_file."""
    with raises(
        ValueError, match="session_file cannot be empty or contain only whitespace"
    ):
        Config(
            api_id=12345,
            api_hash="12345678901234567890123456789012",
            session_file=session_file,
        )


@mark.unit
def test_config_frozen_attribute_error() -> None:
    """Test that frozen config raises AttributeError on attribute modification."""
    config = Config(
        api_id=12345,
        api_hash="12345678901234567890123456789012",
        session_string="test_session",
    )
    with raises(AttributeError):
        config.api_id = 99999  # type: ignore


# ============================================================================
# II. Покрытие Config.from_env()
# ============================================================================


@mark.unit
def test_from_env_missing_api_id_only(monkeypatch) -> None:
    """Test from_env with missing TMA_API_ID only."""
    # Clear all TMA_ env vars
    for key in list(os.environ.keys()):
        if key.startswith("TMA_"):
            monkeypatch.delenv(key, raising=False)
    # Set only required vars (without TMA_API_ID)
    monkeypatch.setenv("TMA_API_HASH", "12345678901234567890123456789012")
    monkeypatch.setenv("TMA_SESSION_STRING", "test_session")

    with raises(ValueError, match="TMA_API_ID environment variable is required"):
        Config.from_env()


@mark.unit
def test_from_env_missing_api_hash_only(monkeypatch) -> None:
    """Test from_env with missing TMA_API_HASH only."""
    # Clear all TMA_ env vars
    for key in list(os.environ.keys()):
        if key.startswith("TMA_"):
            monkeypatch.delenv(key, raising=False)
    # Set only required vars (without TMA_API_HASH)
    monkeypatch.setenv("TMA_API_ID", "12345")
    monkeypatch.setenv("TMA_SESSION_STRING", "test_session")

    with raises(ValueError, match="TMA_API_HASH environment variable is required"):
        Config.from_env()


@mark.unit
def test_from_env_invalid_api_id_empty_string(monkeypatch) -> None:
    """Test from_env with empty TMA_API_ID."""
    # Clear all TMA_ env vars
    for key in list(os.environ.keys()):
        if key.startswith("TMA_"):
            monkeypatch.delenv(key, raising=False)
    # Set env vars with empty TMA_API_ID
    monkeypatch.setenv("TMA_API_ID", "")
    monkeypatch.setenv("TMA_API_HASH", "12345678901234567890123456789012")
    monkeypatch.setenv("TMA_SESSION_STRING", "test_session")

    with raises(ValueError):
        Config.from_env()


@mark.unit
def test_from_env_invalid_api_id_non_numeric(monkeypatch) -> None:
    """Test from_env with non-numeric TMA_API_ID."""
    # Clear all TMA_ env vars
    for key in list(os.environ.keys()):
        if key.startswith("TMA_"):
            monkeypatch.delenv(key, raising=False)
    # Set env vars with non-numeric TMA_API_ID
    monkeypatch.setenv("TMA_API_ID", "abc")
    monkeypatch.setenv("TMA_API_HASH", "12345678901234567890123456789012")
    monkeypatch.setenv("TMA_SESSION_STRING", "test_session")

    with raises(ValueError):
        Config.from_env()


@mark.unit
def test_from_env_invalid_timeout_non_numeric(monkeypatch) -> None:
    """Test from_env with non-numeric TMA_TIMEOUT."""
    # Clear all TMA_ env vars
    for key in list(os.environ.keys()):
        if key.startswith("TMA_"):
            monkeypatch.delenv(key, raising=False)
    # Set env vars with non-numeric TMA_TIMEOUT
    monkeypatch.setenv("TMA_API_ID", "12345")
    monkeypatch.setenv("TMA_API_HASH", "12345678901234567890123456789012")
    monkeypatch.setenv("TMA_SESSION_STRING", "test_session")
    monkeypatch.setenv("TMA_TIMEOUT", "abc")

    with raises(ValueError):
        Config.from_env()


@mark.unit
def test_from_env_invalid_retry_delay_non_numeric(monkeypatch) -> None:
    """Test from_env with non-numeric TMA_RETRY_DELAY."""
    # Clear all TMA_ env vars
    for key in list(os.environ.keys()):
        if key.startswith("TMA_"):
            monkeypatch.delenv(key, raising=False)
    # Set env vars with non-numeric TMA_RETRY_DELAY
    monkeypatch.setenv("TMA_API_ID", "12345")
    monkeypatch.setenv("TMA_API_HASH", "12345678901234567890123456789012")
    monkeypatch.setenv("TMA_SESSION_STRING", "test_session")
    monkeypatch.setenv("TMA_RETRY_DELAY", "xyz")

    with raises(ValueError):
        Config.from_env()


@mark.unit
def test_from_env_empty_session_string_whitespace(monkeypatch) -> None:
    """Test from_env with whitespace-only TMA_SESSION_STRING."""
    # Clear all TMA_ env vars
    for key in list(os.environ.keys()):
        if key.startswith("TMA_"):
            monkeypatch.delenv(key, raising=False)
    # Set env vars with whitespace-only TMA_SESSION_STRING
    monkeypatch.setenv("TMA_API_ID", "12345")
    monkeypatch.setenv("TMA_API_HASH", "12345678901234567890123456789012")
    monkeypatch.setenv("TMA_SESSION_STRING", " ")

    with raises(
        ValueError, match="session_string cannot be empty or contain only whitespace"
    ):
        Config.from_env()


@mark.unit
def test_from_env_default_values_when_missing(monkeypatch) -> None:
    """Test from_env uses default values when optional env vars are missing."""
    # Clear all TMA_ env vars
    for key in list(os.environ.keys()):
        if key.startswith("TMA_"):
            monkeypatch.delenv(key, raising=False)
    # Set only required vars (missing optional ones)
    monkeypatch.setenv("TMA_API_ID", "12345")
    monkeypatch.setenv("TMA_API_HASH", "12345678901234567890123456789012")
    monkeypatch.setenv("TMA_SESSION_STRING", "test_session")

    config = Config.from_env()
    assert config.timeout == 30, "Default timeout should be 30"
    assert config.retry_count == 3, "Default retry_count should be 3"
    assert config.retry_delay == 1.0, "Default retry_delay should be 1.0"
    assert config.log_level == "INFO", "Default log_level should be INFO"


@mark.unit
def test_from_env_both_session_methods(monkeypatch) -> None:
    """Test from_env with both TMA_SESSION_STRING and TMA_SESSION_FILE should raise ValueError."""
    # Clear all TMA_ env vars
    for key in list(os.environ.keys()):
        if key.startswith("TMA_"):
            monkeypatch.delenv(key, raising=False)
    # Set env vars with both session methods
    monkeypatch.setenv("TMA_API_ID", "12345")
    monkeypatch.setenv("TMA_API_HASH", "12345678901234567890123456789012")
    monkeypatch.setenv("TMA_SESSION_STRING", "test_session")
    monkeypatch.setenv("TMA_SESSION_FILE", "test.session")

    with raises(
        ValueError, match="Cannot provide both session_string and session_file"
    ):
        Config.from_env()


@mark.unit
def test_from_env_empty_session_file_whitespace(monkeypatch) -> None:
    """Test from_env with whitespace-only TMA_SESSION_FILE."""
    # Clear all TMA_ env vars
    for key in list(os.environ.keys()):
        if key.startswith("TMA_"):
            monkeypatch.delenv(key, raising=False)
    # Set env vars with whitespace-only TMA_SESSION_FILE
    monkeypatch.setenv("TMA_API_ID", "12345")
    monkeypatch.setenv("TMA_API_HASH", "12345678901234567890123456789012")
    monkeypatch.setenv("TMA_SESSION_FILE", " ")

    with raises(
        ValueError, match="session_file cannot be empty or contain only whitespace"
    ):
        Config.from_env()


# ============================================================================
# III. Покрытие Config.from_yaml(path)
# ============================================================================


@mark.unit
def test_from_yaml_with_null_optional_fields(yaml_config_file_valid: str) -> None:
    """Test from_yaml with null optional fields in YAML."""
    # This test verifies that None values in YAML are handled correctly
    config = Config.from_yaml(yaml_config_file_valid)
    # If mini_app_url is not in YAML, it should be None
    assert config.mini_app_url is None or isinstance(config.mini_app_url, str)


@mark.unit
def test_from_yaml_boundary_values_min() -> None:
    """Test from_yaml with minimum boundary values."""
    import tempfile
    import os

    yaml_content = """api_id: 1
api_hash: "12345678901234567890123456789012"
session_string: "test"
timeout: 1
retry_count: 0
retry_delay: 0.1
log_level: "DEBUG"
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name

    try:
        config = Config.from_yaml(temp_path)
        assert config.api_id == 1
        assert config.timeout == 1
        assert config.retry_count == 0
        assert config.retry_delay == 0.1
    finally:
        os.unlink(temp_path)


@mark.unit
def test_from_yaml_boundary_values_max() -> None:
    """Test from_yaml with maximum boundary values."""
    import tempfile
    import os

    yaml_content = """api_id: 999999999
api_hash: "12345678901234567890123456789012"
session_string: "test"
timeout: 300
retry_count: 10
retry_delay: 10.0
log_level: "CRITICAL"
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name

    try:
        config = Config.from_yaml(temp_path)
        assert config.api_id == 999999999
        assert config.timeout == 300
        assert config.retry_count == 10
        assert config.retry_delay == 10.0
    finally:
        os.unlink(temp_path)


@mark.unit
def test_from_yaml_missing_api_id() -> None:
    """Test from_yaml with missing api_id in YAML."""
    import tempfile
    import os

    yaml_content = """api_hash: "12345678901234567890123456789012"
session_string: "test"
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name

    try:
        with raises(ValueError, match="Failed to load configuration"):
            Config.from_yaml(temp_path)
    finally:
        os.unlink(temp_path)


@mark.unit
def test_from_yaml_invalid_api_id_zero() -> None:
    """Test from_yaml with api_id = 0 in YAML."""
    import tempfile
    import os

    yaml_content = """api_id: 0
api_hash: "12345678901234567890123456789012"
session_string: "test"
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name

    try:
        with raises(ValueError, match="api_id must be between 1 and 999999999"):
            Config.from_yaml(temp_path)
    finally:
        os.unlink(temp_path)


@mark.unit
def test_from_yaml_invalid_log_level_lowercase() -> None:
    """Test from_yaml with lowercase log_level in YAML."""
    import tempfile
    import os

    yaml_content = """api_id: 12345
api_hash: "12345678901234567890123456789012"
session_string: "test"
log_level: "debug"
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name

    try:
        with raises(ValueError, match="Invalid log level"):
            Config.from_yaml(temp_path)
    finally:
        os.unlink(temp_path)


@mark.unit
def test_from_yaml_override_api_hash_from_env(monkeypatch) -> None:
    """Test from_yaml overrides api_hash with TMA_API_HASH env variable. TC-CONFIG-044"""
    import tempfile
    import os

    yaml_content = """api_id: 12345
api_hash: "old_hash_32_characters_long!!!!!"
session_string: "test_session"
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name

    try:
        # Set environment variable
        monkeypatch.setenv("TMA_API_HASH", "new_hash_32_characters_long!!!!!")

        config = Config.from_yaml(temp_path)

        # Verify api_hash is from environment variable, not YAML
        assert config.api_hash == "new_hash_32_characters_long!!!!!"
        assert config.api_hash != "old_hash_32_characters_long!!!!!"
    finally:
        os.unlink(temp_path)


@mark.unit
def test_from_yaml_override_session_string_from_env(monkeypatch) -> None:
    """Test from_yaml overrides session_string with TMA_SESSION_STRING env variable. TC-CONFIG-045"""
    import tempfile
    import os

    yaml_content = """api_id: 12345
api_hash: "12345678901234567890123456789012"
session_string: "old_session"
session_file: "old_session.session"
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name

    try:
        # Set environment variable
        monkeypatch.setenv("TMA_SESSION_STRING", "new_session_from_env")

        config = Config.from_yaml(temp_path)

        # Verify session_string is from environment variable, not YAML
        assert config.session_string == "new_session_from_env"
        assert config.session_string != "old_session"
        # Verify session_file is removed when session_string is provided via env
        assert (
            config.session_file is None or config.session_file != "old_session.session"
        )
    finally:
        os.unlink(temp_path)


@mark.unit
def test_from_yaml_override_session_file_from_env(monkeypatch) -> None:
    """Test from_yaml overrides session_file with TMA_SESSION_FILE env variable. TC-CONFIG-046"""
    import tempfile
    import os

    yaml_content = """api_id: 12345
api_hash: "12345678901234567890123456789012"
session_string: "old_session"
session_file: "old_session.session"
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name

    try:
        # Set environment variable
        monkeypatch.setenv("TMA_SESSION_FILE", "new_session.session")

        config = Config.from_yaml(temp_path)

        # Verify session_file is from environment variable, not YAML
        assert config.session_file == "new_session.session"
        assert config.session_file != "old_session.session"
        # Verify session_string is removed when session_file is provided via env
        assert config.session_string is None or config.session_string != "old_session"
    finally:
        os.unlink(temp_path)


# ============================================================================
# IV. Дополнительные свойства класса
# ============================================================================


@mark.unit
def test_config_serialization_to_builtins(
    valid_config_data: dict[str, int | str | float],
) -> None:
    """Test serialization using msgspec.to_builtins."""
    config = Config(**valid_config_data)  # type: ignore[arg-type]
    config_dict = to_builtins(config)
    assert isinstance(config_dict, dict)
    assert config_dict.get("api_id") == valid_config_data.get("api_id")
    assert config_dict.get("api_hash") == valid_config_data.get("api_hash")
    assert config_dict.get("session_string") == valid_config_data.get("session_string")
    assert config_dict.get("timeout") == valid_config_data.get("timeout")
    assert config_dict.get("retry_count") == valid_config_data.get("retry_count")
    assert config_dict.get("retry_delay") == valid_config_data.get("retry_delay")
    assert config_dict.get("log_level") == valid_config_data.get("log_level")


@mark.unit
def test_config_deserialization_from_dict(
    valid_config_data: dict[str, int | str | float],
) -> None:
    """Test deserialization using msgspec.convert."""
    config = convert(valid_config_data, Config)
    assert isinstance(config, Config)
    assert config.api_id == valid_config_data.get("api_id")
    assert config.api_hash == valid_config_data.get("api_hash")
    assert config.session_string == valid_config_data.get("session_string")
    assert config.timeout == valid_config_data.get("timeout")
    assert config.retry_count == valid_config_data.get("retry_count")
    assert config.retry_delay == valid_config_data.get("retry_delay")
    assert config.log_level == valid_config_data.get("log_level")


@mark.unit
def test_config_repr_contains_class_name(
    valid_config_data: dict[str, int | str | float],
) -> None:
    """Test that repr(config) contains class name."""
    config = Config(**valid_config_data)  # type: ignore[arg-type]
    repr_str = repr(config)
    assert "Config" in repr_str
