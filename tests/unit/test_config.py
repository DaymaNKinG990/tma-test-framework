"""
Unit tests for TMA Framework configuration.
"""

import os
import re
import tempfile

import allure
from msgspec import convert, to_builtins
from pytest import mark, raises

# Local imports
from tma_test_framework.config import Config


# ============================================================================
# I. Инициализация и валидация
# ============================================================================


class TestConfigInit:
    """Test Config initialization and validation."""

    @mark.unit
    @allure.title("TC-CONFIG-001: Create valid configuration")
    @allure.description("TC-CONFIG-001: Test creating a valid configuration.")
    def test_valid_config_creation(
        self, valid_config_data: dict[str, int | str | float]
    ) -> None:
        """
        Test creating a valid configuration.

        Args:
            valid_config_data: Valid configuration data.
        """
        with allure.step("Create Config from valid data"):
            config = Config(**valid_config_data)  # type: ignore[arg-type]
        with allure.step("Verify api_id matches"):
            assert config.api_id == valid_config_data.get("api_id"), (
                "API ID does not match"
            )
        with allure.step("Verify api_hash matches"):
            assert config.api_hash == valid_config_data.get("api_hash"), (
                "API hash does not match"
            )
        with allure.step("Verify session_string matches"):
            assert config.session_string == valid_config_data.get("session_string"), (
                "Session string does not match"
            )
        with allure.step("Verify timeout matches"):
            assert config.timeout == valid_config_data.get("timeout"), (
                "Timeout does not match"
            )
        with allure.step("Verify retry_count matches"):
            assert config.retry_count == valid_config_data.get("retry_count"), (
                "Retry count does not match"
            )
        with allure.step("Verify retry_delay matches"):
            assert config.retry_delay == valid_config_data.get("retry_delay"), (
                "Retry delay does not match"
            )
        with allure.step("Verify log_level matches"):
            assert config.log_level == valid_config_data.get("log_level"), (
                "Log level does not match"
            )

    @mark.unit
    @allure.title("TC-CONFIG-004: Create valid configuration with session file")
    @allure.description(
        "TC-CONFIG-004: Test creating a valid configuration with session file."
    )
    def test_valid_config_with_file(
        self,
        valid_config_with_file_data: dict[str, int | str | float],
    ) -> None:
        """
        Test creating a valid configuration with session file.

        Args:
            valid_config_with_file_data: Valid configuration data with session file.
        """
        with allure.step("Create Config with session file"):
            config = Config(**valid_config_with_file_data)  # type: ignore[arg-type]
        with allure.step("Verify api_id matches"):
            assert config.api_id == valid_config_with_file_data.get("api_id"), (
                "API ID does not match"
            )
        with allure.step("Verify api_hash matches"):
            assert config.api_hash == valid_config_with_file_data.get("api_hash"), (
                "API hash does not match"
            )
        with allure.step("Verify session_file matches"):
            assert config.session_file == valid_config_with_file_data.get(
                "session_file"
            ), "Session file does not match"
        with allure.step("Verify session_string is None"):
            assert config.session_string is None, "Session string should be None"

    @mark.unit
    @allure.title("TC-CONFIG-002: Configuration default values")
    @allure.description("TC-CONFIG-002: Test configuration default values.")
    def test_config_default_values(
        self,
        config_data_for_default_values: dict[str, int | str],
    ) -> None:
        """Test configuration default values."""
        with allure.step("Create Config with default values"):
            config = Config(**config_data_for_default_values)  # type: ignore[arg-type]
        with allure.step("Verify timeout default value"):
            assert config.timeout == config_data_for_default_values.get("timeout"), (
                "Timeout should be default 30"
            )
        with allure.step("Verify retry_count default value"):
            assert config.retry_count == config_data_for_default_values.get(
                "retry_count"
            ), "Retry count should be default 3"
        with allure.step("Verify retry_delay default value"):
            assert config.retry_delay == config_data_for_default_values.get(
                "retry_delay"
            ), "Retry delay should be default 1.0"
        with allure.step("Verify log_level default value"):
            assert config.log_level == config_data_for_default_values.get(
                "log_level"
            ), "Log level should be default INFO"
        with allure.step("Verify mini_app_url default value"):
            assert config.mini_app_url is config_data_for_default_values.get(
                "mini_app_url"
            ), "Mini app URL should be None"
        with allure.step("Verify mini_app_start_param default value"):
            assert config.mini_app_start_param is config_data_for_default_values.get(
                "mini_app_start_param"
            ), "Mini app start param should be None"

    @mark.unit
    @allure.title("TC-CONFIG-001: Configuration validation success")
    @allure.description("TC-CONFIG-001: Test successful configuration validation.")
    def test_config_validation_success(
        self,
        valid_config_data: dict[str, int | str | float],
    ) -> None:
        """
        Test successful configuration validation.

        Args:
            valid_config_data: Valid configuration data.
        """
        with allure.step("Create Config from valid data"):
            config = Config(**valid_config_data)  # type: ignore[arg-type]
        with allure.step("Verify validation passes"):
            assert config.api_id > 0, "API ID should be greater than 0"
            assert config.api_hash, "API hash should be not None"
            assert config.session_string or config.session_file, (
                "Session string or session file should be provided"
            )

    @mark.unit
    @allure.title("TC-CONFIG-006: Configuration validation with missing api_id")
    @allure.description(
        "TC-CONFIG-006: Test configuration validation with missing api_id."
    )
    def test_config_validation_missing_api_id(
        self,
        invalid_config_data_without_api_id: dict[str, str | int | float],
    ) -> None:
        """
        Test configuration validation with missing api_id.

        Args:
            invalid_config_data_without_api_id: Invalid configuration data without api_id.
        """
        with allure.step("Attempt to create Config without api_id"):
            with raises(TypeError, match="Missing required argument 'api_id'"):
                Config(**invalid_config_data_without_api_id)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-009: Configuration validation with missing api_hash")
    @allure.description(
        "TC-CONFIG-009: Test configuration validation with missing api_hash."
    )
    def test_config_validation_missing_api_hash(
        self,
        invalid_config_data_without_api_hash: dict[str, int | str],
    ) -> None:
        """
        Test configuration validation with missing api_hash.

        Args:
            invalid_config_data_without_api_hash: Invalid configuration data without api_hash.
        """
        with allure.step("Attempt to create Config without api_hash"):
            with raises(TypeError, match="Missing required argument 'api_hash'"):
                Config(**invalid_config_data_without_api_hash)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-021: Configuration validation with missing session")
    @allure.description(
        "TC-CONFIG-021: Test configuration validation with missing session."
    )
    def test_config_validation_missing_session(
        self,
        config_data_for_missing_session: dict[str, int | str],
    ) -> None:
        """
        Test configuration validation with missing session.

        Args:
            config_data_for_missing_session: Configuration data with missing session.
        """
        with allure.step("Attempt to create Config without session"):
            with raises(ValueError, match="Session required"):
                Config(**config_data_for_missing_session)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-023: Configuration validation with invalid log level")
    @allure.description(
        "TC-CONFIG-023: Test configuration validation with invalid log level."
    )
    def test_config_validation_invalid_log_level(
        self,
        config_data_for_invalid_log_level: dict[str, int | str],
    ) -> None:
        """
        Test configuration validation with invalid log level.

        Args:
            config_data_for_invalid_log_level: Configuration data with invalid log level.
        """
        with allure.step("Attempt to create Config with invalid log level"):
            with raises(ValueError, match="Invalid log level"):
                Config(**config_data_for_invalid_log_level)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-015: Configuration validation with invalid retry count")
    @allure.description(
        "TC-CONFIG-015: Test configuration validation with invalid retry count."
    )
    def test_config_validation_invalid_retry_count(
        self,
        config_data_for_invalid_retry_count: dict[str, int | str],
    ) -> None:
        """
        Test configuration validation with invalid retry count.

        Args:
            config_data_for_invalid_retry_count: Configuration data with invalid retry count.
        """
        with allure.step("Attempt to create Config with invalid retry_count"):
            with raises(ValueError, match="retry_count must be between 0 and 10"):
                Config(**config_data_for_invalid_retry_count)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-018: Configuration validation with invalid retry delay")
    @allure.description(
        "TC-CONFIG-018: Test configuration validation with invalid retry delay."
    )
    def test_config_validation_invalid_retry_delay(
        self,
        config_data_for_invalid_retry_delay: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration validation with invalid retry delay.

        Args:
            config_data_for_invalid_retry_delay: Configuration data with invalid retry delay.
        """
        with allure.step("Attempt to create Config with invalid retry_delay"):
            with raises(ValueError, match="retry_delay must be between 0.1 and 10.0"):
                Config(**config_data_for_invalid_retry_delay)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-002: Configuration validation with minimal values")
    @allure.description(
        "TC-CONFIG-002: Test configuration validation with minimal values."
    )
    def test_config_validation_minimal_values(
        self,
        valid_config_data_minimal: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration validation with minimal values.

        Args:
            valid_config_data_minimal: Valid configuration data minimal.
        """
        with allure.step("Create Config with minimal values"):
            config = Config(**valid_config_data_minimal)  # type: ignore[arg-type]
        with allure.step("Verify all minimal values are set correctly"):
            assert config.api_id == valid_config_data_minimal.get("api_id"), (
                "API ID does not match"
            )
            assert config.api_hash == valid_config_data_minimal.get("api_hash"), (
                "API hash does not match"
            )
            assert config.session_string == valid_config_data_minimal.get(
                "session_string"
            ), "Session string does not match"
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
    @allure.title("TC-CONFIG-002: Configuration validation with maximal values")
    @allure.description(
        "TC-CONFIG-002: Test configuration validation with maximal values."
    )
    def test_config_validation_maximal_values(
        self,
        valid_config_data_maximal: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration validation with maximal values.

        Args:
            valid_config_data_maximal: Valid configuration data maximal.
        """
        with allure.step("Create Config with maximal values"):
            config = Config(**valid_config_data_maximal)  # type: ignore[arg-type]
        with allure.step("Verify all maximal values are set correctly"):
            assert config.api_id == valid_config_data_maximal.get("api_id"), (
                "API ID does not match"
            )
            assert config.api_hash == valid_config_data_maximal.get("api_hash"), (
                "API hash does not match"
            )
            assert config.session_string == valid_config_data_maximal.get(
                "session_string"
            ), "Session string does not match"
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
    @allure.title("TC-CONFIG-006: Configuration validation with invalid api_id")
    @allure.description(
        "TC-CONFIG-006: Test configuration validation with invalid api_id."
    )
    def test_config_validation_invalid_api_id(
        self,
        invalid_config_data_api_id: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration validation with invalid api_id.

        Args:
            invalid_config_data_api_id: Invalid configuration data with invalid api_id.
        """
        with allure.step("Attempt to create Config with invalid api_id"):
            with raises(ValueError):
                Config(**invalid_config_data_api_id)  # type: ignore[arg-type]

    @mark.unit
    @allure.title(
        "TC-CONFIG-015: Configuration validation with invalid minimal retry count"
    )
    @allure.description(
        "TC-CONFIG-015: Test configuration validation with invalid minimal retry count."
    )
    def test_config_validation_invalid_minimal_retry_count(
        self,
        invalid_config_data_minimal_retry_count: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration validation with invalid minimal retry count.

        Args:
            invalid_config_data_minimal_retry_count: Invalid configuration data with invalid minimal retry count.
        """
        with allure.step("Attempt to create Config with invalid minimal retry_count"):
            with raises(ValueError, match="retry_count must be between 0 and 10"):
                Config(**invalid_config_data_minimal_retry_count)  # type: ignore[arg-type]

    @mark.unit
    @allure.title(
        "TC-CONFIG-018: Configuration validation with invalid minimal retry delay"
    )
    @allure.description(
        "TC-CONFIG-018: Test configuration validation with invalid minimal retry delay."
    )
    def test_config_validation_invalid_minimal_retry_delay(
        self,
        invalid_config_data_minimal_retry_delay: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration validation with invalid minimal retry delay.

        Args:
            invalid_config_data_minimal_retry_delay: Invalid configuration data with invalid minimal retry delay.
        """
        with allure.step("Attempt to create Config with invalid minimal retry_delay"):
            with raises(ValueError, match="retry_delay must be between 0.1 and 10.0"):
                Config(**invalid_config_data_minimal_retry_delay)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-012: Configuration validation with invalid timeout")
    @allure.description(
        "TC-CONFIG-012: Test configuration validation with invalid timeout."
    )
    def test_config_validation_invalid_timeout(
        self,
        invalid_config_data_timeout: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration validation with invalid timeout.

        Args:
            invalid_config_data_timeout: Invalid configuration data with invalid timeout.
        """
        with allure.step("Attempt to create Config with invalid timeout"):
            with raises(ValueError, match="timeout must be between 1 and 300 seconds"):
                Config(**invalid_config_data_timeout)  # type: ignore[arg-type]

    @mark.unit
    @allure.title(
        "TC-CONFIG-016: Configuration validation with invalid maximal retry count"
    )
    @allure.description(
        "TC-CONFIG-016: Test configuration validation with invalid maximal retry count."
    )
    def test_config_validation_invalid_maximal_retry_count(
        self,
        invalid_config_data_maximal_retry_count,
    ):
        """
        Test configuration validation with invalid maximal retry count.

        Args:
            invalid_config_data_maximal_retry_count: Invalid configuration data with invalid maximal retry count.
        """
        with allure.step("Attempt to create Config with invalid maximal retry_count"):
            with raises(ValueError, match="retry_count must be between 0 and 10"):
                Config(**invalid_config_data_maximal_retry_count)

    @mark.unit
    @allure.title(
        "TC-CONFIG-019: Configuration validation with invalid maximal retry delay"
    )
    @allure.description(
        "TC-CONFIG-019: Test configuration validation with invalid maximal retry delay."
    )
    def test_config_validation_invalid_maximal_retry_delay(
        self,
        invalid_config_data_maximal_retry_delay: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration validation with invalid maximal retry delay.

        Args:
            invalid_config_data_maximal_retry_delay: Invalid configuration data with invalid maximal retry delay.
        """
        with allure.step("Attempt to create Config with invalid maximal retry_delay"):
            with raises(ValueError, match="retry_delay must be between 0.1 and 10.0"):
                Config(**invalid_config_data_maximal_retry_delay)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-001: Configuration serialization")
    @allure.description("TC-CONFIG-001: Test configuration serialization.")
    def test_config_serialization(
        self, valid_config_data: dict[str, int | str | float]
    ) -> None:
        """
        Test configuration serialization.

        Args:
            valid_config_data: Valid configuration data.
        """
        with allure.step("Create Config from valid data"):
            config = Config(**valid_config_data)  # type: ignore[arg-type]
        with allure.step("Serialize Config to dict"):
            config_dict = to_builtins(config)
        with allure.step("Verify serialized dict"):
            assert isinstance(config_dict, dict)
            assert config_dict.get("api_id") == valid_config_data.get("api_id")
            assert config_dict.get("api_hash") == valid_config_data.get("api_hash")

    @mark.unit
    @allure.title("TC-CONFIG-001: Configuration deserialization")
    @allure.description("TC-CONFIG-001: Test configuration deserialization.")
    def test_config_deserialization(
        self,
        valid_config_data: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration deserialization.

        Args:
            valid_config_data: Valid configuration data.
        """
        with allure.step("Prepare config dict"):
            config_dict = valid_config_data.copy()
        with allure.step("Deserialize dict to Config"):
            config = convert(config_dict, Config)
        with allure.step("Verify deserialized Config"):
            assert isinstance(config, Config)
            assert config.api_id == valid_config_data.get("api_id")
            assert config.api_hash == valid_config_data.get("api_hash")

    @mark.unit
    @allure.title("TC-CONFIG-001: Configuration equality with same data")
    @allure.description("TC-CONFIG-001: Test configuration equality with same data.")
    def test_config_equality(
        self, valid_config_data: dict[str, int | str | float]
    ) -> None:
        """
        Test configuration equality with same data.

        Args:
            valid_config_data: Valid configuration data.
        """
        with allure.step("Create two Config instances with same data"):
            config1 = Config(**valid_config_data)  # type: ignore[arg-type]
            config2 = Config(**valid_config_data)  # type: ignore[arg-type]
        with allure.step("Verify configurations are equal"):
            assert config1 == config2, "Configuration should be equal"

    @mark.unit
    @allure.title("TC-CONFIG-001: Configuration inequality with different data")
    @allure.description(
        "TC-CONFIG-001: Test configuration inequality with different data."
    )
    def test_config_inequality(
        self,
        valid_config_data: dict[str, int | str | float],
        valid_config_with_file_data: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration inequality with different data.

        Args:
            valid_config_data: Valid configuration data.
            valid_config_with_file_data: Valid configuration data with file.
        """
        with allure.step("Create two Config instances with different data"):
            config1 = Config(**valid_config_data)  # type: ignore[arg-type]
            config2 = Config(**valid_config_with_file_data)  # type: ignore[arg-type]
        with allure.step("Verify configurations are not equal"):
            assert config1 != config2, "Configuration should be different"

    @mark.unit
    @allure.title("TC-CONFIG-039: Configuration hash equality with same data")
    @allure.description(
        "TC-CONFIG-039: Test configuration hash equality with same data."
    )
    def test_config_hash_equality(
        self, valid_config_data: dict[str, int | str | float]
    ) -> None:
        """
        Test configuration hash equality with same data.

        Args:
            valid_config_data: Valid configuration data.
        """
        with allure.step("Create two Config instances with same data"):
            config1 = Config(**valid_config_data)  # type: ignore[arg-type]
            config2 = Config(**valid_config_data)  # type: ignore[arg-type]
        with allure.step("Verify configuration hashes are equal"):
            assert hash(config1) == hash(config2), (
                "Configuration hashes should be equal"
            )

    @mark.unit
    @allure.title("TC-CONFIG-039: Configuration hash inequality with different data")
    @allure.description(
        "TC-CONFIG-039: Test configuration hash inequality with different data."
    )
    def test_config_hash_inequality(
        self,
        valid_config_data: dict[str, int | str | float],
        valid_config_with_file_data: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration hash inequality with different data.

        Args:
            valid_config_data: Valid configuration data.
            valid_config_with_file_data: Valid configuration data with file.
        """
        with allure.step("Create two Config instances with different data"):
            config1 = Config(**valid_config_data)  # type: ignore[arg-type]
            config2 = Config(**valid_config_with_file_data)  # type: ignore[arg-type]
        with allure.step("Verify configuration hashes are not equal"):
            assert hash(config1) != hash(config2), (
                "Configuration hashes should be different"
            )

    @mark.unit
    @allure.title("TC-CONFIG-001: Configuration string representation")
    @allure.description("TC-CONFIG-001: Test configuration string representation.")
    def test_config_repr(self, valid_config_data: dict[str, int | str | float]) -> None:
        """
        Test configuration string representation.

        Args:
            valid_config_data: Valid configuration data.
        """
        with allure.step("Create Config instance"):
            config = Config(**valid_config_data)  # type: ignore[arg-type]
        with allure.step("Get string representation"):
            repr_str = repr(config)
        with allure.step("Verify repr contains expected information"):
            assert "Config" in repr_str
            assert f"api_id={valid_config_data.get('api_id')}" in repr_str
            assert f"api_hash='{valid_config_data.get('api_hash')}'" in repr_str


# ============================================================================
# II. Config.from_env()
# ============================================================================


class TestConfigFromEnv:
    """Test Config.from_env() method."""

    @mark.unit
    @allure.title("TC-CONFIG-025: Create config from valid environment variables")
    @allure.description(
        "TC-CONFIG-025: Test creating config from valid environment variables."
    )
    def test_from_env_valid_variables(self, mock_environment: dict[str, str]) -> None:
        """
        Test creating config from valid environment variables.

        Args:
            mock_environment: Mock environment variables (already patched by fixture).
        """
        # Environment is already patched by mock_environment fixture
        with allure.step("Create Config from environment variables"):
            config = Config.from_env()
        with allure.step("Verify all environment variables are loaded correctly"):
            assert config.api_id == int(mock_environment.get("TMA_API_ID") or "0"), (
                "API ID does not match"
            )
            assert config.api_hash == mock_environment.get("TMA_API_HASH"), (
                "API hash does not match"
            )
            assert config.session_string == mock_environment.get(
                "TMA_SESSION_STRING"
            ), "Session string does not match"
            assert config.mini_app_url == mock_environment.get("TMA_MINI_APP_URL"), (
                "Mini app URL does not match"
            )
            assert config.mini_app_start_param == mock_environment.get(
                "TMA_MINI_APP_START_PARAM"
            ), "Mini app start param does not match"
            assert config.timeout == int(mock_environment.get("TMA_TIMEOUT") or "30"), (
                "Timeout does not match"
            )
            assert config.retry_count == int(
                mock_environment.get("TMA_RETRY_COUNT") or "3"
            ), "Retry count does not match"
            assert config.retry_delay == float(
                mock_environment.get("TMA_RETRY_DELAY") or "1.0"
            ), "Retry delay does not match"
            assert config.log_level == mock_environment.get("TMA_LOG_LEVEL"), (
                "Log level does not match"
            )

    @mark.unit
    @allure.title(
        "TC-CONFIG-028: Create config with missing required environment variables"
    )
    @allure.description(
        "TC-CONFIG-028: Test creating config with missing required environment variables."
    )
    def test_from_env_missing_required_variables(
        self,
        mock_empty_environment: dict[str, str],
    ) -> None:
        """
        Test creating config with missing required environment variables.

        Args:
            mock_empty_environment: Mock empty environment variables (already patched by fixture).
        """
        # Environment is already patched by mock_empty_environment fixture
        # api_id is checked first, then api_hash
        with allure.step("Attempt to create Config from empty environment"):
            with raises(
                ValueError, match="TMA_API_ID environment variable is required"
            ):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-028: Create config with missing TMA_API_ID")
    @allure.description("TC-CONFIG-028: Test creating config with missing TMA_API_ID.")
    def test_from_env_missing_api_id(
        self,
        mock_environment_missing_api_id: dict[str, str],
    ) -> None:
        """
        Test creating config with missing TMA_API_ID.

        Args:
            mock_environment_missing_api_id: Mock environment variables missing TMA_API_ID (already patched by fixture).
        """
        # Environment is already patched by mock_environment_missing_api_id fixture
        with allure.step("Attempt to create Config without TMA_API_ID"):
            with raises(
                ValueError, match="TMA_API_ID environment variable is required"
            ):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-029: Create config with missing TMA_API_HASH")
    @allure.description(
        "TC-CONFIG-029: Test creating config with missing TMA_API_HASH."
    )
    def test_from_env_missing_api_hash(
        self,
        mock_environment_missing_api_hash: dict[str, str],
    ) -> None:
        """
        Test creating config with missing TMA_API_HASH.

        Args:
            mock_environment_missing_api_hash: Mock environment variables missing TMA_API_HASH (already patched by fixture).
        """
        # Environment is already patched by mock_environment_missing_api_hash fixture
        with allure.step("Attempt to create Config without TMA_API_HASH"):
            with raises(
                ValueError, match="TMA_API_HASH environment variable is required"
            ):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-030: Create config with invalid TMA_API_ID")
    @allure.description("TC-CONFIG-030: Test creating config with invalid TMA_API_ID.")
    def test_from_env_invalid_api_id(
        self,
        mock_environment_invalid_api_id: dict[str, str],
    ) -> None:
        """
        Test creating config with invalid TMA_API_ID.

        Args:
            mock_environment_invalid_api_id: Mock environment variables with invalid TMA_API_ID (already patched by fixture).
        """
        # Environment is already patched by mock_environment_invalid_api_id fixture
        with allure.step("Attempt to create Config with invalid TMA_API_ID"):
            with raises(ValueError):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-027: Create config with default values from environment")
    @allure.description(
        "TC-CONFIG-027: Test creating config with default values from environment."
    )
    def test_from_env_default_values(
        self,
        mock_environment_default_values: dict[str, str],
    ) -> None:
        """
        Test creating config with default values from environment.

        Args:
            mock_environment_default_values: Mock environment variables with default values (already patched by fixture).
        """
        # Environment is already patched by mock_environment_default_values fixture
        with allure.step("Create Config from environment with default values"):
            config = Config.from_env()
        with allure.step("Verify default values are set correctly"):
            assert config.timeout == int(
                mock_environment_default_values.get("TMA_TIMEOUT") or "30"
            ), "Timeout should be default 30"
            assert config.retry_count == int(
                mock_environment_default_values.get("TMA_RETRY_COUNT") or "3"
            ), "Retry count should be default 3"
            assert config.retry_delay == float(
                mock_environment_default_values.get("TMA_RETRY_DELAY") or "1.0"
            ), "Retry delay should be default 1.0"
            assert config.log_level == mock_environment_default_values.get(
                "TMA_LOG_LEVEL"
            ), "Log level should be default INFO"

    @mark.unit
    @allure.title("TC-CONFIG-026: Create config with overridden default values")
    @allure.description(
        "TC-CONFIG-026: Test creating config with overridden default values."
    )
    def test_from_env_override_defaults(
        self,
        mock_environment_override_defaults: dict[str, str],
    ) -> None:
        """
        Test creating config with overridden default values.

        Args:
            mock_environment_override_defaults: Mock environment variables with overridden defaults (already patched by fixture).
        """
        # Environment is already patched by mock_environment_override_defaults fixture
        with allure.step("Create Config from environment with overridden defaults"):
            config = Config.from_env()
        with allure.step("Verify overridden values are set correctly"):
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
    @allure.title("TC-CONFIG-005: Create config with optional environment variables")
    @allure.description(
        "TC-CONFIG-005: Test creating config with optional environment variables. Both session_string and session_file are set, which should raise ValueError."
    )
    def test_from_env_optional_variables(
        self,
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
        with allure.step(
            "Attempt to create Config with both session_string and session_file"
        ):
            with raises(
                ValueError, match="Cannot provide both session_string and session_file"
            ):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-025: Type conversion in from_env method")
    @allure.description("TC-CONFIG-025: Test type conversion in from_env method.")
    def test_from_env_type_conversion(
        self,
        mock_environment_type_conversion: dict[str, str],
    ) -> None:
        """
        Test type conversion in from_env method.

        Args:
            mock_environment_type_conversion: Mock environment variables for type conversion testing (already patched by fixture).
        """
        # Environment is already patched by mock_environment_type_conversion fixture
        with allure.step("Create Config from environment"):
            config = Config.from_env()
        with allure.step("Verify type conversions"):
            assert isinstance(config.api_id, int), "API ID should be int"
            assert isinstance(config.timeout, int), "Timeout should be int"
            assert isinstance(config.retry_count, int), "Retry count should be int"
            assert isinstance(config.retry_delay, float), "Retry delay should be float"

    @mark.unit
    @allure.title("TC-CONFIG-030: Invalid type conversion in from_env method")
    @allure.description(
        "TC-CONFIG-030: Test invalid type conversion in from_env method."
    )
    def test_from_env_invalid_type_conversion(
        self,
        mock_environment_invalid_type_conversion: dict[str, str],
    ) -> None:
        """
        Test invalid type conversion in from_env method.

        Args:
            mock_environment_invalid_type_conversion: Mock environment variables with invalid type conversion.
        """
        # Environment is already set by fixture
        with allure.step("Attempt to create Config with invalid type conversion"):
            with raises(ValueError):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-031: from_env method with missing session string")
    @allure.description(
        "TC-CONFIG-031: Test from_env method with missing session string."
    )
    def test_from_env_with_empty_strings(
        self, monkeypatch, mock_environment_missing_session_string: dict[str, str]
    ) -> None:
        """
        Test from_env method with missing session string.

        Args:
            mock_environment_missing_session_string: Mock environment variables missing TMA_SESSION_STRING.
        """
        # Environment is already set by fixture

        pattern = re.escape(
            "Session required. Provide one of: session_string (for saved session) or session_file (for file session). You need to authenticate manually first to get a session."
        )
        with allure.step("Attempt to create Config without session"):
            with raises(ValueError, match=pattern):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-030: from_env method with invalid TMA_API_ID")
    @allure.description("TC-CONFIG-030: Test from_env method with invalid TMA_API_ID.")
    def test_from_env_with_invalid_api_id(
        self, monkeypatch, mock_environment_invalid_api_id: dict[str, str]
    ) -> None:
        """
        Test from_env method with invalid TMA_API_ID.

        Args:
            mock_environment_invalid_api_id: Mock environment variables with invalid TMA_API_ID.
        """
        # Environment is already set by fixture
        # Invalid string "invalid" will cause ValueError when converting to int
        with allure.step("Attempt to create Config with invalid TMA_API_ID"):
            with raises(
                ValueError, match="Invalid int value for TMA_API_ID: 'invalid'"
            ):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-009: from_env method with invalid TMA_API_HASH length")
    @allure.description(
        "TC-CONFIG-009: Test from_env method with invalid TMA_API_HASH length."
    )
    def test_from_env_with_invalid_api_hash_length(
        self, monkeypatch, mock_environment_invalid_api_hash_length: dict[str, str]
    ) -> None:
        """
        Test from_env method with invalid TMA_API_HASH length.

        Args:
            mock_environment_invalid_api_hash_length: Mock environment variables with invalid TMA_API_HASH length.
        """
        # Environment is already set by fixture
        with allure.step("Attempt to create Config with invalid TMA_API_HASH length"):
            with raises(
                ValueError, match="api_hash must be exactly 32 characters long, got"
            ):
                Config.from_env()


# ============================================================================
# III. Граничные случаи и дополнительные тесты инициализации
# ============================================================================


class TestConfigInitEdgeCases:
    """Test Config initialization edge cases."""

    @mark.unit
    @allure.title("TC-CONFIG-009: Configuration with empty strings")
    @allure.description("TC-CONFIG-009: Test configuration with empty strings.")
    def test_config_with_empty_strings(
        self,
        config_data_for_empty_strings: dict[str, int | str],
    ) -> None:
        """
        Test configuration with empty strings.

        Args:
            config_data_for_empty_strings: Configuration data with empty strings.
        """
        with allure.step("Attempt to create Config with empty strings"):
            with raises(
                ValueError, match="api_hash must be exactly 32 characters long"
            ):
                Config(**config_data_for_empty_strings)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-022: Configuration with whitespace strings")
    @allure.description("TC-CONFIG-022: Test configuration with whitespace strings.")
    def test_config_with_whitespace_strings(
        self,
        config_data_for_whitespace_strings: dict[str, int | str],
    ) -> None:
        """
        Test configuration with whitespace strings.

        Args:
            config_data_for_whitespace_strings: Configuration data with whitespace strings.
        """
        with allure.step("Attempt to create Config with whitespace strings"):
            with raises(
                ValueError,
                match="session_string cannot be empty or contain only whitespace",
            ):
                Config(**config_data_for_whitespace_strings)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-041: Configuration with very long strings")
    @allure.description("TC-CONFIG-041: Test configuration with very long strings.")
    def test_config_with_very_long_strings(
        self,
        config_data_for_very_long_strings: dict[str, int | str],
    ) -> None:
        """
        Test configuration with very long strings.

        Args:
            config_data_for_very_long_strings: Configuration data with very long strings.
        """
        with allure.step("Create Config with very long strings"):
            config = Config(**config_data_for_very_long_strings)  # type: ignore[arg-type]
        with allure.step("Verify very long session_string is handled"):
            assert (
                config.session_string
                == config_data_for_very_long_strings["session_string"]
            )

    @mark.unit
    @allure.title("TC-CONFIG-042: Configuration with special characters")
    @allure.description("TC-CONFIG-042: Test configuration with special characters.")
    def test_config_with_special_characters(
        self,
        config_data_for_special_characters: dict[str, int | str],
    ) -> None:
        """
        Test configuration with special characters.

        Args:
            config_data_for_special_characters: Configuration data with special characters.
        """
        with allure.step("Create Config with special characters"):
            config = Config(**config_data_for_special_characters)  # type: ignore[arg-type]
        with allure.step("Verify special characters are handled correctly"):
            assert config.session_string == config_data_for_special_characters.get(
                "session_string"
            ), "Session string should match"

    @mark.unit
    @allure.title("TC-CONFIG-042: Configuration with unicode characters")
    @allure.description("TC-CONFIG-042: Test configuration with unicode characters.")
    def test_config_with_unicode_characters(
        self,
        config_data_for_unicode_characters: dict[str, int | str],
    ) -> None:
        """
        Test configuration with unicode characters.

        Args:
            config_data_for_unicode_characters: Configuration data with unicode characters.
        """
        with allure.step("Create Config with unicode characters"):
            config = Config(**config_data_for_unicode_characters)  # type: ignore[arg-type]
        with allure.step("Verify unicode characters are handled correctly"):
            assert config.session_string == config_data_for_unicode_characters.get(
                "session_string"
            ), "Session string should match"

    @mark.unit
    @allure.title("TC-CONFIG-043: Configuration with None values")
    @allure.description("TC-CONFIG-043: Test configuration with None values.")
    def test_config_with_none_values(
        self,
        config_data_for_none_values: dict[str, int | str | None],
    ) -> None:
        """
        Test configuration with None values.

        Args:
            config_data_for_none_values: Configuration data with None values.
        """
        with allure.step("Create Config with None values"):
            config = Config(**config_data_for_none_values)  # type: ignore[arg-type]
        with allure.step("Verify None values are handled correctly"):
            assert config.mini_app_url is None, "Mini app URL should be None"
            assert config.mini_app_start_param is None, (
                "Mini app start param should be None"
            )

    @mark.unit
    @allure.title(
        "TC-CONFIG-005: Configuration with both session_string and session_file"
    )
    @allure.description(
        "TC-CONFIG-005: Test configuration with both session_string and session_file should raise ValueError."
    )
    def test_config_with_both_session_methods(
        self,
        config_data_for_both_session_methods: dict[str, int | str],
    ) -> None:
        """
        Test configuration with both session_string and session_file should raise ValueError.

        Args:
            config_data_for_both_session_methods: Configuration data with both session_string and session_file.
        """
        with allure.step("Attempt to create Config with both session methods"):
            with raises(
                ValueError, match="Cannot provide both session_string and session_file"
            ):
                Config(**config_data_for_both_session_methods)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-043: Configuration mini_app_url with whitespace")
    @allure.description(
        "TC-CONFIG-043: Test that mini_app_url with whitespace at beginning/end is preserved as-is (no strip)."
    )
    def test_config_mini_app_url_with_whitespace(self) -> None:
        """
        Test that mini_app_url with whitespace at beginning/end is preserved as-is (no strip).

        This test verifies that optional fields like mini_app_url preserve whitespace
        and are not automatically stripped, as per specification requirement.
        """
        with allure.step("Prepare URL with whitespace"):
            url_with_whitespace = "  https://example.com/mini-app  "
        with allure.step("Create Config with URL containing whitespace"):
            config = Config(
                api_id=12345,
                api_hash="12345678901234567890123456789012",
                session_string="test_session",
                mini_app_url=url_with_whitespace,
            )
        with allure.step("Verify whitespace is preserved"):
            assert config.mini_app_url == url_with_whitespace, (
                "mini_app_url should preserve whitespace without strip"
            )

    @mark.unit
    @allure.title("TC-CONFIG-024: Configuration log level debug")
    @allure.description("TC-CONFIG-024: Test configuration log level debug.")
    def test_config_log_level_debug(
        self,
        config_data_for_log_level_debug: dict[str, int | str],
    ) -> None:
        """
        Test configuration log level debug.

        Args:
            config_data_for_log_level_debug: Configuration data with log level debug.
        """
        with allure.step("Create Config with DEBUG log level"):
            config = Config(**config_data_for_log_level_debug)  # type: ignore[arg-type]
        with allure.step("Verify log level is DEBUG"):
            assert config.log_level == config_data_for_log_level_debug.get(
                "log_level"
            ), "Log level should match"

    @mark.unit
    @allure.title("TC-CONFIG-024: Configuration log level info")
    @allure.description("TC-CONFIG-024: Test configuration log level info.")
    def test_config_log_level_info(
        self,
        config_data_for_log_level_info: dict[str, int | str],
    ) -> None:
        """
        Test configuration log level info.

        Args:
            config_data_for_log_level_info: Configuration data with log level info.
        """
        with allure.step("Create Config with INFO log level"):
            config = Config(**config_data_for_log_level_info)  # type: ignore[arg-type]
        with allure.step("Verify log level is INFO"):
            assert config.log_level == config_data_for_log_level_info.get(
                "log_level"
            ), "Log level should match"

    @mark.unit
    @allure.title("TC-CONFIG-024: Configuration log level warning")
    @allure.description("TC-CONFIG-024: Test configuration log level warning.")
    def test_config_log_level_warning(
        self,
        config_data_for_log_level_warning: dict[str, int | str],
    ) -> None:
        """
        Test configuration log level warning.

        Args:
            config_data_for_log_level_warning: Configuration data with log level warning.
        """
        with allure.step("Create Config with WARNING log level"):
            config = Config(**config_data_for_log_level_warning)  # type: ignore[arg-type]
        with allure.step("Verify log level is WARNING"):
            assert config.log_level == config_data_for_log_level_warning.get(
                "log_level"
            ), "Log level should match"

    @mark.unit
    @allure.title("TC-CONFIG-024: Configuration log level error")
    @allure.description("TC-CONFIG-024: Test configuration log level error.")
    def test_config_log_level_error(
        self,
        config_data_for_log_level_error: dict[str, int | str],
    ) -> None:
        """
        Test configuration log level error.

        Args:
            config_data_for_log_level_error: Configuration data with log level error.
        """
        with allure.step("Create Config with ERROR log level"):
            config = Config(**config_data_for_log_level_error)  # type: ignore[arg-type]
        with allure.step("Verify log level is ERROR"):
            assert config.log_level == config_data_for_log_level_error.get(
                "log_level"
            ), "Log level should match"

    @mark.unit
    @allure.title("TC-CONFIG-024: Configuration log level critical")
    @allure.description("TC-CONFIG-024: Test configuration log level critical.")
    def test_config_log_level_critical(
        self,
        config_data_for_log_level_critical: dict[str, int | str],
    ) -> None:
        """
        Test configuration log level critical.

        Args:
            config_data_for_log_level_critical: Configuration data with log level critical.
        """
        with allure.step("Create Config with CRITICAL log level"):
            config = Config(**config_data_for_log_level_critical)  # type: ignore[arg-type]
        with allure.step("Verify log level is CRITICAL"):
            assert config.log_level == config_data_for_log_level_critical.get(
                "log_level"
            ), "Log level should match"

    @mark.unit
    @allure.title("TC-CONFIG-023: Log level case sensitivity")
    @allure.description("TC-CONFIG-023: Test log level case sensitivity.")
    def test_config_log_level_case_sensitivity(
        self,
        config_data_for_log_level_case_sensitivity: dict[str, int | str],
    ) -> None:
        """
        Test log level case sensitivity.

        Args:
            config_data_for_log_level_case_sensitivity: Configuration data with log level case sensitivity.
        """
        with allure.step("Attempt to create Config with invalid case log level"):
            with raises(ValueError, match="Invalid log level"):
                Config(**config_data_for_log_level_case_sensitivity)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-020: Float precision in retry_delay")
    @allure.description("TC-CONFIG-020: Test float precision in retry_delay.")
    def test_config_float_precision(
        self,
        config_data_for_float_precision: dict[str, int | str | float],
    ) -> None:
        """
        Test float precision in retry_delay.

        Args:
            config_data_for_float_precision: Configuration data with float precision.
        """
        with allure.step("Create Config with float precision"):
            config = Config(**config_data_for_float_precision)  # type: ignore[arg-type]
        with allure.step("Verify float precision is preserved"):
            assert config.retry_delay == config_data_for_float_precision.get(
                "retry_delay"
            ), "Retry delay should match"

    @mark.unit
    @allure.title("TC-CONFIG-040: Configuration with large numbers")
    @allure.description("TC-CONFIG-040: Test configuration with large numbers.")
    def test_config_large_numbers(
        self,
        config_data_for_large_numbers: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration with large numbers.

        Args:
            config_data_for_large_numbers: Configuration data with large numbers.
        """
        with allure.step("Create Config with large numbers"):
            config = Config(**config_data_for_large_numbers)  # type: ignore[arg-type]
        with allure.step("Verify large numbers are handled correctly"):
            assert config.api_id == config_data_for_large_numbers.get("api_id"), (
                "API ID should match"
            )
            assert config.timeout == config_data_for_large_numbers.get("timeout"), (
                "Timeout should match"
            )
            assert config.retry_count == config_data_for_large_numbers.get(
                "retry_count"
            ), "Retry count should match"
            assert config.retry_delay == config_data_for_large_numbers.get(
                "retry_delay"
            ), "Retry delay should match"


# ============================================================================
# IV. Config.from_yaml()
# ============================================================================


class TestConfigFromYaml:
    """Test Config.from_yaml() method."""

    @mark.unit
    @allure.title("TC-CONFIG-032: Create config from valid YAML file")
    @allure.description("TC-CONFIG-032: Test creating config from valid YAML file.")
    def test_from_yaml_valid_file(
        self, yaml_config_file_valid: str, yaml_config_data_valid: dict
    ) -> None:
        """
        Test creating config from valid YAML file.

        Args:
            yaml_config_file_valid: Path to valid YAML config file.
            yaml_config_data_valid: Parsed YAML config data.
        """
        with allure.step("Load Config from valid YAML file"):
            config = Config.from_yaml(yaml_config_file_valid)
        with allure.step("Verify all values from YAML are loaded correctly"):
            assert config.api_id == yaml_config_data_valid.get("api_id"), (
                "API ID should match"
            )
            assert config.api_hash == yaml_config_data_valid.get("api_hash"), (
                "API hash should match"
            )
            assert config.session_string == yaml_config_data_valid.get(
                "session_string"
            ), "Session string should match"
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
    @allure.title("TC-CONFIG-034: Create config from minimal YAML file")
    @allure.description("TC-CONFIG-034: Test creating config from minimal YAML file.")
    def test_from_yaml_minimal_file(
        self, yaml_config_file_minimal: str, yaml_config_data_minimal: dict
    ) -> None:
        """
        Test creating config from minimal YAML file.

        Args:
            yaml_config_file_minimal: Path to minimal YAML config file.
            yaml_config_data_minimal: Parsed YAML config data.
        """
        with allure.step("Load Config from minimal YAML file"):
            config = Config.from_yaml(yaml_config_file_minimal)
        with allure.step("Verify all values from minimal YAML are loaded correctly"):
            assert config.api_id == yaml_config_data_minimal.get("api_id"), (
                "API ID should match"
            )
            assert config.api_hash == yaml_config_data_minimal.get("api_hash"), (
                "API hash should match"
            )
            assert config.session_string == yaml_config_data_minimal.get(
                "session_string"
            ), "Session string should match"
            assert config.timeout == yaml_config_data_minimal.get("timeout"), (
                "Timeout should match"
            )
            assert config.retry_count == yaml_config_data_minimal.get("retry_count"), (
                "Retry count should match"
            )
            assert config.retry_delay == yaml_config_data_minimal.get("retry_delay"), (
                "Retry delay should match"
            )
            assert config.log_level == yaml_config_data_minimal.get(
                "log_level", "INFO"
            ), "Log level should be default INFO"

    @mark.unit
    @allure.title("TC-CONFIG-004: Create config from YAML file with session_file")
    @allure.description(
        "TC-CONFIG-004: Test creating config from YAML file with session_file."
    )
    def test_from_yaml_with_file_session(
        self,
        yaml_config_file_with_file_session: str,
        yaml_config_data_with_file_session: dict,
    ) -> None:
        """
        Test creating config from YAML file with session_file.

        Args:
            yaml_config_file_with_file_session: Path to YAML config file with session_file.
            yaml_config_data_with_file_session: Parsed YAML config data.
        """
        with allure.step("Load Config from YAML file with session_file"):
            config = Config.from_yaml(yaml_config_file_with_file_session)
        with allure.step("Verify session_file is set correctly"):
            assert config.api_id == yaml_config_data_with_file_session.get("api_id"), (
                "API ID should match"
            )
            assert config.api_hash == yaml_config_data_with_file_session.get(
                "api_hash"
            ), "API hash should match"
            assert config.session_file == yaml_config_data_with_file_session.get(
                "session_file"
            ), "Session file should match"
            assert config.session_string == yaml_config_data_with_file_session.get(
                "session_string"
            ), "Session string should be None"
        with allure.step("Verify other values are loaded correctly"):
            assert config.timeout == yaml_config_data_with_file_session.get(
                "timeout"
            ), "Timeout should match"
            assert config.retry_count == yaml_config_data_with_file_session.get(
                "retry_count"
            ), "Retry count should match"
            assert config.retry_delay == yaml_config_data_with_file_session.get(
                "retry_delay"
            ), "Retry delay should match"
            assert config.log_level == yaml_config_data_with_file_session.get(
                "log_level"
            ), "Log level should match"

    @mark.unit
    @allure.title("TC-CONFIG-033: Create config from YAML file with mini app settings")
    @allure.description(
        "TC-CONFIG-033: Test creating config from YAML file with mini app settings."
    )
    def test_from_yaml_with_mini_app(
        self, yaml_config_file_with_mini_app: str, yaml_config_data_with_mini_app: dict
    ) -> None:
        """
        Test creating config from YAML file with mini app settings.

        Args:
            yaml_config_file_with_mini_app: Path to YAML config file with mini app settings.
            yaml_config_data_with_mini_app: Parsed YAML config data.
        """
        with allure.step("Load Config from YAML file with mini app settings"):
            config = Config.from_yaml(yaml_config_file_with_mini_app)
        with allure.step(
            "Verify all values from YAML with mini app are loaded correctly"
        ):
            assert config.api_id == yaml_config_data_with_mini_app.get("api_id"), (
                "API ID should match"
            )
            assert config.api_hash == yaml_config_data_with_mini_app.get("api_hash"), (
                "API hash should match"
            )
            assert config.session_string == yaml_config_data_with_mini_app.get(
                "session_string"
            ), "Session string should match"
            assert config.mini_app_url == yaml_config_data_with_mini_app.get(
                "mini_app_url"
            ), "Mini app URL should match"
            assert config.mini_app_start_param == yaml_config_data_with_mini_app.get(
                "mini_app_start_param"
            ), "Mini app start param should match"
            assert config.timeout == yaml_config_data_with_mini_app.get("timeout"), (
                "Timeout should match"
            )
            assert config.retry_count == yaml_config_data_with_mini_app.get(
                "retry_count"
            ), "Retry count should match"
            assert config.retry_delay == yaml_config_data_with_mini_app.get(
                "retry_delay"
            ), "Retry delay should match"
            assert config.log_level == yaml_config_data_with_mini_app.get(
                "log_level"
            ), "Log level should match"

    @mark.unit
    @allure.title("TC-CONFIG-037: Create config from invalid YAML file")
    @allure.description("TC-CONFIG-037: Test creating config from invalid YAML file.")
    @mark.unit
    @allure.title("TC-CONFIG-037: Create config from invalid YAML file")
    @allure.description("TC-CONFIG-037: Test creating config from invalid YAML file.")
    def test_from_yaml_invalid_file(self, yaml_config_file_invalid: str) -> None:
        """
        Test creating config from invalid YAML file.

        Args:
            yaml_config_file_invalid: Path to invalid YAML config file.
        """
        with allure.step("Attempt to load Config from invalid YAML file"):
            with raises(ValueError):
                Config.from_yaml(yaml_config_file_invalid)

    @mark.unit
    @allure.title("TC-CONFIG-031: Create config from YAML file missing session")
    @allure.description(
        "TC-CONFIG-031: Test creating config from YAML file missing session."
    )
    def test_from_yaml_missing_session(
        self, yaml_config_file_missing_session: str
    ) -> None:
        """
        Test creating config from YAML file missing session.

        Args:
            yaml_config_file_missing_session: Path to YAML config file missing session.
        """
        with allure.step("Attempt to load Config from YAML file without session"):
            with raises(ValueError, match="Session required"):
                Config.from_yaml(yaml_config_file_missing_session)

    @mark.unit
    @allure.title("TC-CONFIG-035: Create config from nonexistent YAML file")
    @allure.description(
        "TC-CONFIG-035: Test creating config from nonexistent YAML file."
    )
    def test_from_yaml_nonexistent_file(self) -> None:
        """
        Test creating config from nonexistent YAML file.
        """
        with allure.step("Attempt to load Config from nonexistent file"):
            with raises(ValueError, match="Configuration file not found"):
                Config.from_yaml("nonexistent_config.yaml")

    @mark.unit
    @allure.title("TC-CONFIG-036: Create config from YAML file with invalid format")
    @allure.description(
        "TC-CONFIG-036: Test creating config from YAML file with invalid format."
    )
    def test_from_yaml_invalid_yaml_format(
        self, yaml_config_file_invalid_format: str
    ) -> None:
        """
        Test creating config from YAML file with invalid format.

        Args:
            yaml_config_file_invalid_format: Path to invalid YAML config file format.
        """
        with allure.step("Attempt to load Config from invalid YAML format"):
            with raises(ValueError, match="Failed to load configuration"):
                Config.from_yaml(yaml_config_file_invalid_format)

    @mark.unit
    @allure.title("TC-CONFIG-036: Create config from empty YAML file")
    @allure.description("TC-CONFIG-036: Test creating config from empty YAML file.")
    def test_from_yaml_empty_file(self, yaml_config_file_empty: str) -> None:
        """
        Test creating config from empty YAML file.

        Args:
            yaml_config_file_empty: Path to empty YAML config file.
        """
        with allure.step("Attempt to load Config from empty YAML file"):
            with raises(ValueError, match="Failed to load configuration"):
                Config.from_yaml(yaml_config_file_empty)


# ============================================================================
# V. Параметризованные тесты валидации
# ============================================================================


class TestConfigValidationParametrized:
    """Test Config validation with parametrized tests."""

    @mark.unit
    @mark.parametrize("api_id", [1, 999_999_999])
    @allure.title("TC-CONFIG-040: Valid api_id values")
    @allure.description("TC-CONFIG-040: Test valid api_id values.")
    def test_config_valid_api_id(self, api_id: int) -> None:
        """Test valid api_id values."""
        with allure.step(f"Create Config with api_id={api_id}"):
            config = Config(
                api_id=api_id,
                api_hash="12345678901234567890123456789012",
                session_string="test_session",
            )
        with allure.step("Verify api_id is set correctly"):
            assert config.api_id == api_id

    @mark.unit
    @mark.parametrize("api_id", [0, -1, 1_000_000_000])
    @allure.title("TC-CONFIG-006: Invalid api_id values")
    @allure.description("TC-CONFIG-006: Test invalid api_id values.")
    def test_config_invalid_api_id(self, api_id: int) -> None:
        """Test invalid api_id values."""
        with allure.step(f"Attempt to create Config with invalid api_id={api_id}"):
            with raises(ValueError, match="api_id must be between 1 and 999999999"):
                Config(
                    api_id=api_id,
                    api_hash="12345678901234567890123456789012",
                    session_string="test_session",
                )

    @mark.unit
    @mark.parametrize("api_hash_length", [32])
    @allure.title("TC-CONFIG-009: Valid api_hash length")
    @allure.description("TC-CONFIG-009: Test valid api_hash length.")
    def test_config_valid_api_hash_length(self, api_hash_length: int) -> None:
        """Test valid api_hash length."""
        with allure.step(f"Create api_hash with length={api_hash_length}"):
            api_hash = "a" * api_hash_length
        with allure.step("Create Config with valid api_hash length"):
            config = Config(
                api_id=12345, api_hash=api_hash, session_string="test_session"
            )
        with allure.step("Verify api_hash length is correct"):
            assert len(config.api_hash) == api_hash_length

    @mark.unit
    @mark.parametrize("api_hash_length", [0, 31, 33])
    @allure.title("TC-CONFIG-009: Invalid api_hash length")
    @allure.description("TC-CONFIG-009: Test invalid api_hash length.")
    def test_config_invalid_api_hash_length(self, api_hash_length: int) -> None:
        """Test invalid api_hash length."""
        with allure.step(f"Create api_hash with invalid length={api_hash_length}"):
            api_hash = "a" * api_hash_length if api_hash_length > 0 else ""
        with allure.step("Attempt to create Config with invalid api_hash length"):
            with raises(
                ValueError, match="api_hash must be exactly 32 characters long"
            ):
                Config(api_id=12345, api_hash=api_hash, session_string="test_session")

    @mark.unit
    @allure.title("TC-CONFIG-011: api_hash with None value")
    @allure.description("TC-CONFIG-011: Test api_hash with None value.")
    def test_config_api_hash_none(self) -> None:
        """Test api_hash with None value."""
        with allure.step("Attempt to create Config with api_hash=None"):
            with raises(
                ValueError, match="api_hash must be exactly 32 characters long"
            ):
                Config(
                    api_id=12345,
                    api_hash=None,  # type: ignore
                    session_string="test_session",
                )

    @mark.unit
    @mark.parametrize("timeout", [1, 300])
    @allure.title("TC-CONFIG-014: Valid timeout values")
    @allure.description("TC-CONFIG-014: Test valid timeout values.")
    def test_config_valid_timeout(self, timeout: int) -> None:
        """Test valid timeout values."""
        with allure.step(f"Create Config with timeout={timeout}"):
            config = Config(
                api_id=12345,
                api_hash="12345678901234567890123456789012",
                session_string="test_session",
                timeout=timeout,
            )
        with allure.step("Verify timeout is set correctly"):
            assert config.timeout == timeout

    @mark.unit
    @mark.parametrize("timeout", [0, 301, -5])
    @allure.title("TC-CONFIG-012: Invalid timeout values")
    @allure.description("TC-CONFIG-012: Test invalid timeout values.")
    def test_config_invalid_timeout(self, timeout: int) -> None:
        """Test invalid timeout values."""
        with allure.step(f"Attempt to create Config with invalid timeout={timeout}"):
            with raises(ValueError, match="timeout must be between 1 and 300 seconds"):
                Config(
                    api_id=12345,
                    api_hash="12345678901234567890123456789012",
                    session_string="test_session",
                    timeout=timeout,
                )

    @mark.unit
    @mark.parametrize("retry_count", [0, 10])
    @allure.title("TC-CONFIG-017: Valid retry_count values")
    @allure.description("TC-CONFIG-017: Test valid retry_count values.")
    def test_config_valid_retry_count(self, retry_count: int) -> None:
        """Test valid retry_count values."""
        with allure.step(f"Create Config with retry_count={retry_count}"):
            config = Config(
                api_id=12345,
                api_hash="12345678901234567890123456789012",
                session_string="test_session",
                retry_count=retry_count,
            )
        with allure.step("Verify retry_count is set correctly"):
            assert config.retry_count == retry_count

    @mark.unit
    @mark.parametrize("retry_count", [-1, 11])
    @allure.title("TC-CONFIG-015: Invalid retry_count values")
    @allure.description("TC-CONFIG-015: Test invalid retry_count values.")
    def test_config_invalid_retry_count(self, retry_count: int) -> None:
        """Test invalid retry_count values."""
        with allure.step(
            f"Attempt to create Config with invalid retry_count={retry_count}"
        ):
            with raises(ValueError, match="retry_count must be between 0 and 10"):
                Config(
                    api_id=12345,
                    api_hash="12345678901234567890123456789012",
                    session_string="test_session",
                    retry_count=retry_count,
                )

    @mark.unit
    @mark.parametrize("retry_delay", [0.1, 10.0])
    @allure.title("TC-CONFIG-020: Valid retry_delay values")
    @allure.description("TC-CONFIG-020: Test valid retry_delay values.")
    def test_config_valid_retry_delay(self, retry_delay: float) -> None:
        """Test valid retry_delay values."""
        with allure.step(f"Create Config with retry_delay={retry_delay}"):
            config = Config(
                api_id=12345,
                api_hash="12345678901234567890123456789012",
                session_string="test_session",
                retry_delay=retry_delay,
            )
        with allure.step("Verify retry_delay is set correctly"):
            assert config.retry_delay == retry_delay

    @mark.unit
    @mark.parametrize("retry_delay", [0.09, 10.01])
    @allure.title("TC-CONFIG-018: Invalid retry_delay values")
    @allure.description("TC-CONFIG-018: Test invalid retry_delay values.")
    def test_config_invalid_retry_delay(self, retry_delay: float) -> None:
        """Test invalid retry_delay values."""
        with allure.step(
            f"Attempt to create Config with invalid retry_delay={retry_delay}"
        ):
            with raises(
                ValueError, match="retry_delay must be between 0.1 and 10.0 seconds"
            ):
                Config(
                    api_id=12345,
                    api_hash="12345678901234567890123456789012",
                    session_string="test_session",
                    retry_delay=retry_delay,
                )

    @mark.unit
    @mark.parametrize("log_level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    @allure.title("TC-CONFIG-024: Valid log_level values")
    @allure.description("TC-CONFIG-024: Test valid log_level values.")
    def test_config_valid_log_level(self, log_level: str) -> None:
        """Test valid log_level values."""
        with allure.step(f"Create Config with log_level={log_level}"):
            config = Config(
                api_id=12345,
                api_hash="12345678901234567890123456789012",
                session_string="test_session",
                log_level=log_level,
            )
        with allure.step("Verify log_level is set correctly"):
            assert config.log_level == log_level

    @mark.unit
    @mark.parametrize("log_level", ["debug", "Info", "TRACE", "INVALID", ""])
    @allure.title("TC-CONFIG-023: Invalid log_level values")
    @allure.description("TC-CONFIG-023: Test invalid log_level values.")
    def test_config_invalid_log_level(self, log_level: str) -> None:
        """Test invalid log_level values."""
        with allure.step(
            f"Attempt to create Config with invalid log_level={log_level}"
        ):
            with raises(ValueError, match="Invalid log level"):
                Config(
                    api_id=12345,
                    api_hash="12345678901234567890123456789012",
                    session_string="test_session",
                    log_level=log_level,
                )

    @mark.unit
    @mark.parametrize("session_string", [" ", "\t\n", ""])
    @allure.title("TC-CONFIG-022: Empty or whitespace-only session_string")
    @allure.description("TC-CONFIG-022: Test empty or whitespace-only session_string.")
    def test_config_empty_whitespace_session_string(self, session_string: str) -> None:
        """Test empty or whitespace-only session_string."""
        with allure.step(
            "Attempt to create Config with empty/whitespace session_string"
        ):
            with raises(
                ValueError,
                match="session_string cannot be empty or contain only whitespace",
            ):
                Config(
                    api_id=12345,
                    api_hash="12345678901234567890123456789012",
                    session_string=session_string,
                )

    @mark.unit
    @mark.parametrize("session_file", [" ", "\t\n", ""])
    @allure.title("TC-CONFIG-022: Empty or whitespace-only session_file")
    @allure.description("TC-CONFIG-022: Test empty or whitespace-only session_file.")
    def test_config_empty_whitespace_session_file(self, session_file: str) -> None:
        """Test empty or whitespace-only session_file."""
        with allure.step("Attempt to create Config with empty/whitespace session_file"):
            with raises(
                ValueError,
                match="session_file cannot be empty or contain only whitespace",
            ):
                Config(
                    api_id=12345,
                    api_hash="12345678901234567890123456789012",
                    session_file=session_file,
                )

    @mark.unit
    @allure.title(
        "TC-CONFIG-038: Frozen config raises AttributeError on attribute modification"
    )
    @allure.description(
        "TC-CONFIG-038: Test that frozen config raises AttributeError on attribute modification."
    )
    def test_config_frozen_attribute_error(self) -> None:
        """Test that frozen config raises AttributeError on attribute modification."""
        with allure.step("Create Config instance"):
            config = Config(
                api_id=12345,
                api_hash="12345678901234567890123456789012",
                session_string="test_session",
            )
        with allure.step("Attempt to modify frozen attribute"):
            with raises(AttributeError):
                config.api_id = 99999  # type: ignore


# ============================================================================
# VI. Дополнительные тесты Config.from_env()
# ============================================================================


class TestConfigFromEnvAdditional:
    """Additional tests for Config.from_env() method."""

    @mark.unit
    @allure.title("TC-CONFIG-028: from_env with missing TMA_API_ID only")
    @allure.description("TC-CONFIG-028: Test from_env with missing TMA_API_ID only.")
    def test_from_env_missing_api_id_only(self, monkeypatch) -> None:
        """Test from_env with missing TMA_API_ID only."""
        with allure.step("Clear all TMA_ environment variables"):
            # Clear all TMA_ env vars
            for key in list(os.environ.keys()):
                if key.startswith("TMA_"):
                    monkeypatch.delenv(key, raising=False)
        with allure.step("Set only required vars (without TMA_API_ID)"):
            # Set only required vars (without TMA_API_ID)
            monkeypatch.setenv("TMA_API_HASH", "12345678901234567890123456789012")
            monkeypatch.setenv("TMA_SESSION_STRING", "test_session")

        with allure.step("Attempt to create Config.from_env()"):
            with raises(
                ValueError, match="TMA_API_ID environment variable is required"
            ):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-029: from_env with missing TMA_API_HASH only")
    @allure.description("TC-CONFIG-029: Test from_env with missing TMA_API_HASH only.")
    def test_from_env_missing_api_hash_only(self, monkeypatch) -> None:
        """Test from_env with missing TMA_API_HASH only."""
        with allure.step("Clear all TMA_ environment variables"):
            # Clear all TMA_ env vars
            for key in list(os.environ.keys()):
                if key.startswith("TMA_"):
                    monkeypatch.delenv(key, raising=False)
        with allure.step("Set only required vars (without TMA_API_HASH)"):
            # Set only required vars (without TMA_API_HASH)
            monkeypatch.setenv("TMA_API_ID", "12345")
            monkeypatch.setenv("TMA_SESSION_STRING", "test_session")

        with allure.step("Attempt to create Config.from_env()"):
            with raises(
                ValueError, match="TMA_API_HASH environment variable is required"
            ):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-030: from_env with empty TMA_API_ID")
    @allure.description("TC-CONFIG-030: Test from_env with empty TMA_API_ID.")
    def test_from_env_invalid_api_id_empty_string(self, monkeypatch) -> None:
        """Test from_env with empty TMA_API_ID."""
        with allure.step("Clear all TMA_ environment variables"):
            # Clear all TMA_ env vars
            for key in list(os.environ.keys()):
                if key.startswith("TMA_"):
                    monkeypatch.delenv(key, raising=False)
        with allure.step("Set env vars with empty TMA_API_ID"):
            # Set env vars with empty TMA_API_ID
            monkeypatch.setenv("TMA_API_ID", "")
            monkeypatch.setenv("TMA_API_HASH", "12345678901234567890123456789012")
            monkeypatch.setenv("TMA_SESSION_STRING", "test_session")

        with allure.step("Attempt to create Config.from_env()"):
            with raises(ValueError):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-030: from_env with non-numeric TMA_API_ID")
    @allure.description("TC-CONFIG-030: Test from_env with non-numeric TMA_API_ID.")
    def test_from_env_invalid_api_id_non_numeric(self, monkeypatch) -> None:
        """Test from_env with non-numeric TMA_API_ID."""
        with allure.step("Clear all TMA_ environment variables"):
            # Clear all TMA_ env vars
            for key in list(os.environ.keys()):
                if key.startswith("TMA_"):
                    monkeypatch.delenv(key, raising=False)
        with allure.step("Set env vars with non-numeric TMA_API_ID"):
            # Set env vars with non-numeric TMA_API_ID
            monkeypatch.setenv("TMA_API_ID", "abc")
            monkeypatch.setenv("TMA_API_HASH", "12345678901234567890123456789012")
            monkeypatch.setenv("TMA_SESSION_STRING", "test_session")

        with allure.step("Attempt to create Config.from_env()"):
            with raises(ValueError):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-030: from_env with non-numeric TMA_TIMEOUT")
    @allure.description("TC-CONFIG-030: Test from_env with non-numeric TMA_TIMEOUT.")
    def test_from_env_invalid_timeout_non_numeric(self, monkeypatch) -> None:
        """Test from_env with non-numeric TMA_TIMEOUT."""
        with allure.step("Clear all TMA_ environment variables"):
            # Clear all TMA_ env vars
            for key in list(os.environ.keys()):
                if key.startswith("TMA_"):
                    monkeypatch.delenv(key, raising=False)
        with allure.step("Set env vars with non-numeric TMA_TIMEOUT"):
            # Set env vars with non-numeric TMA_TIMEOUT
            monkeypatch.setenv("TMA_API_ID", "12345")
            monkeypatch.setenv("TMA_API_HASH", "12345678901234567890123456789012")
            monkeypatch.setenv("TMA_SESSION_STRING", "test_session")
            monkeypatch.setenv("TMA_TIMEOUT", "abc")

        with allure.step("Attempt to create Config.from_env()"):
            with raises(ValueError):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-030: from_env with non-numeric TMA_RETRY_DELAY")
    @allure.description(
        "TC-CONFIG-030: Test from_env with non-numeric TMA_RETRY_DELAY."
    )
    def test_from_env_invalid_retry_delay_non_numeric(self, monkeypatch) -> None:
        """Test from_env with non-numeric TMA_RETRY_DELAY."""
        with allure.step("Clear all TMA_ environment variables"):
            # Clear all TMA_ env vars
            for key in list(os.environ.keys()):
                if key.startswith("TMA_"):
                    monkeypatch.delenv(key, raising=False)
        with allure.step("Set env vars with non-numeric TMA_RETRY_DELAY"):
            # Set env vars with non-numeric TMA_RETRY_DELAY
            monkeypatch.setenv("TMA_API_ID", "12345")
            monkeypatch.setenv("TMA_API_HASH", "12345678901234567890123456789012")
            monkeypatch.setenv("TMA_SESSION_STRING", "test_session")
            monkeypatch.setenv("TMA_RETRY_DELAY", "xyz")

        with allure.step("Attempt to create Config.from_env()"):
            with raises(ValueError):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-022: from_env with whitespace-only TMA_SESSION_STRING")
    @allure.description(
        "TC-CONFIG-022: Test from_env with whitespace-only TMA_SESSION_STRING."
    )
    def test_from_env_empty_session_string_whitespace(self, monkeypatch) -> None:
        """Test from_env with whitespace-only TMA_SESSION_STRING."""
        with allure.step("Clear all TMA_ environment variables"):
            # Clear all TMA_ env vars
            for key in list(os.environ.keys()):
                if key.startswith("TMA_"):
                    monkeypatch.delenv(key, raising=False)
        with allure.step("Set env vars with whitespace-only TMA_SESSION_STRING"):
            # Set env vars with whitespace-only TMA_SESSION_STRING
            monkeypatch.setenv("TMA_API_ID", "12345")
            monkeypatch.setenv("TMA_API_HASH", "12345678901234567890123456789012")
            monkeypatch.setenv("TMA_SESSION_STRING", " ")

        with allure.step("Attempt to create Config.from_env()"):
            with raises(
                ValueError,
                match="session_string cannot be empty or contain only whitespace",
            ):
                Config.from_env()

    @mark.unit
    @allure.title(
        "TC-CONFIG-027: from_env uses default values when optional env vars are missing"
    )
    @allure.description(
        "TC-CONFIG-027: Test from_env uses default values when optional env vars are missing."
    )
    def test_from_env_default_values_when_missing(self, monkeypatch) -> None:
        """Test from_env uses default values when optional env vars are missing."""
        with allure.step("Clear all TMA_ environment variables"):
            # Clear all TMA_ env vars
            for key in list(os.environ.keys()):
                if key.startswith("TMA_"):
                    monkeypatch.delenv(key, raising=False)
        with allure.step("Set only required vars (missing optional ones)"):
            # Set only required vars (missing optional ones)
            monkeypatch.setenv("TMA_API_ID", "12345")
            monkeypatch.setenv("TMA_API_HASH", "12345678901234567890123456789012")
            monkeypatch.setenv("TMA_SESSION_STRING", "test_session")

        with allure.step("Create Config.from_env()"):
            config = Config.from_env()
        with allure.step("Verify default values are used"):
            assert config.timeout == 30, "Default timeout should be 30"
            assert config.retry_count == 3, "Default retry_count should be 3"
            assert config.retry_delay == 1.0, "Default retry_delay should be 1.0"
            assert config.log_level == "INFO", "Default log_level should be INFO"

    @mark.unit
    @allure.title(
        "from_env with both TMA_SESSION_STRING and TMA_SESSION_FILE should raise ValueError"
    )
    @allure.description(
        "Test from_env with both TMA_SESSION_STRING and TMA_SESSION_FILE should raise ValueError."
    )
    def test_from_env_both_session_methods(self, monkeypatch) -> None:
        """Test from_env with both TMA_SESSION_STRING and TMA_SESSION_FILE should raise ValueError."""
        with allure.step("Clear all TMA_ environment variables"):
            # Clear all TMA_ env vars
            for key in list(os.environ.keys()):
                if key.startswith("TMA_"):
                    monkeypatch.delenv(key, raising=False)
        with allure.step("Set env vars with both session methods"):
            # Set env vars with both session methods
            monkeypatch.setenv("TMA_API_ID", "12345")
            monkeypatch.setenv("TMA_API_HASH", "12345678901234567890123456789012")
            monkeypatch.setenv("TMA_SESSION_STRING", "test_session")
            monkeypatch.setenv("TMA_SESSION_FILE", "test.session")

        with allure.step("Attempt to create Config.from_env()"):
            with raises(
                ValueError, match="Cannot provide both session_string and session_file"
            ):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-022: from_env with whitespace-only TMA_SESSION_FILE")
    @allure.description(
        "TC-CONFIG-022: Test from_env with whitespace-only TMA_SESSION_FILE."
    )
    def test_from_env_empty_session_file_whitespace(self, monkeypatch) -> None:
        """Test from_env with whitespace-only TMA_SESSION_FILE."""
        with allure.step("Clear all TMA_ environment variables"):
            # Clear all TMA_ env vars
            for key in list(os.environ.keys()):
                if key.startswith("TMA_"):
                    monkeypatch.delenv(key, raising=False)
        with allure.step("Set env vars with whitespace-only TMA_SESSION_FILE"):
            # Set env vars with whitespace-only TMA_SESSION_FILE
            monkeypatch.setenv("TMA_API_ID", "12345")
            monkeypatch.setenv("TMA_API_HASH", "12345678901234567890123456789012")
            monkeypatch.setenv("TMA_SESSION_FILE", " ")

        with allure.step("Attempt to create Config.from_env()"):
            with raises(
                ValueError,
                match="session_file cannot be empty or contain only whitespace",
            ):
                Config.from_env()


# ============================================================================
# VII. Дополнительные тесты Config.from_yaml()
# ============================================================================


class TestConfigFromYamlAdditional:
    """Additional tests for Config.from_yaml() method."""

    @mark.unit
    @allure.title("TC-CONFIG-043: from_yaml with null optional fields in YAML")
    @allure.description(
        "TC-CONFIG-043: Test from_yaml with null optional fields in YAML."
    )
    def test_from_yaml_with_null_optional_fields(
        self, yaml_config_file_valid: str
    ) -> None:
        """Test from_yaml with null optional fields in YAML."""
        with allure.step("Load Config from YAML file"):
            # This test verifies that None values in YAML are handled correctly
            config = Config.from_yaml(yaml_config_file_valid)
        with allure.step("Verify optional fields can be None"):
            # If mini_app_url is not in YAML, it should be None
            assert config.mini_app_url is None or isinstance(config.mini_app_url, str)

    @mark.unit
    @allure.title("TC-CONFIG-014: from_yaml with minimum boundary values")
    @allure.description("TC-CONFIG-014: Test from_yaml with minimum boundary values.")
    def test_from_yaml_boundary_values_min(self) -> None:
        """Test from_yaml with minimum boundary values."""

        with allure.step("Create temporary YAML file with minimum values"):
            yaml_content = """api_id: 1
api_hash: "12345678901234567890123456789012"
session_string: "test"
timeout: 1
retry_count: 0
retry_delay: 0.1
log_level: "DEBUG"
"""
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".yaml", delete=False
            ) as f:
                f.write(yaml_content)
                temp_path = f.name

        try:
            with allure.step("Load Config from YAML with minimum values"):
                config = Config.from_yaml(temp_path)
            with allure.step("Verify minimum boundary values"):
                assert config.api_id == 1
                assert config.timeout == 1
                assert config.retry_count == 0
                assert config.retry_delay == 0.1
        finally:
            os.unlink(temp_path)

    @mark.unit
    @allure.title("TC-CONFIG-014: from_yaml with maximum boundary values")
    @allure.description("TC-CONFIG-014: Test from_yaml with maximum boundary values.")
    def test_from_yaml_boundary_values_max(self) -> None:
        """Test from_yaml with maximum boundary values."""

        with allure.step("Create temporary YAML file with maximum values"):
            yaml_content = """api_id: 999999999
api_hash: "12345678901234567890123456789012"
session_string: "test"
timeout: 300
retry_count: 10
retry_delay: 10.0
log_level: "CRITICAL"
"""
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".yaml", delete=False
            ) as f:
                f.write(yaml_content)
                temp_path = f.name

        try:
            with allure.step("Load Config from YAML with maximum values"):
                config = Config.from_yaml(temp_path)
            with allure.step("Verify maximum boundary values"):
                assert config.api_id == 999999999
                assert config.timeout == 300
                assert config.retry_count == 10
                assert config.retry_delay == 10.0
        finally:
            os.unlink(temp_path)

    @mark.unit
    @allure.title("TC-CONFIG-037: from_yaml with missing api_id in YAML")
    @allure.description("TC-CONFIG-037: Test from_yaml with missing api_id in YAML.")
    def test_from_yaml_missing_api_id(self) -> None:
        """Test from_yaml with missing api_id in YAML."""

        with allure.step("Create temporary YAML file without api_id"):
            yaml_content = """api_hash: "12345678901234567890123456789012"
session_string: "test"
"""
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".yaml", delete=False
            ) as f:
                f.write(yaml_content)
                temp_path = f.name

        try:
            with allure.step("Attempt to load Config from YAML without api_id"):
                with raises(ValueError, match="Failed to load configuration"):
                    Config.from_yaml(temp_path)
        finally:
            os.unlink(temp_path)

    @mark.unit
    @allure.title("TC-CONFIG-006: from_yaml with api_id = 0 in YAML")
    @allure.description("TC-CONFIG-006: Test from_yaml with api_id = 0 in YAML.")
    def test_from_yaml_invalid_api_id_zero(self) -> None:
        """Test from_yaml with api_id = 0 in YAML."""

        with allure.step("Create temporary YAML file with api_id=0"):
            yaml_content = """api_id: 0
api_hash: "12345678901234567890123456789012"
session_string: "test"
"""
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".yaml", delete=False
            ) as f:
                f.write(yaml_content)
                temp_path = f.name

        try:
            with allure.step("Attempt to load Config from YAML with invalid api_id"):
                with raises(ValueError, match="api_id must be between 1 and 999999999"):
                    Config.from_yaml(temp_path)
        finally:
            os.unlink(temp_path)

    @mark.unit
    @allure.title("TC-CONFIG-023: from_yaml with lowercase log_level in YAML")
    @allure.description(
        "TC-CONFIG-023: Test from_yaml with lowercase log_level in YAML."
    )
    def test_from_yaml_invalid_log_level_lowercase(self) -> None:
        """Test from_yaml with lowercase log_level in YAML."""

        with allure.step("Create temporary YAML file with invalid log_level"):
            yaml_content = """api_id: 12345
api_hash: "12345678901234567890123456789012"
session_string: "test"
log_level: "debug"
"""
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".yaml", delete=False
            ) as f:
                f.write(yaml_content)
                temp_path = f.name

        try:
            with allure.step("Attempt to load Config from YAML with invalid log_level"):
                with raises(ValueError, match="Invalid log level"):
                    Config.from_yaml(temp_path)
        finally:
            os.unlink(temp_path)

    @mark.unit
    @allure.title(
        "TC-CONFIG-044: from_yaml overrides api_hash with TMA_API_HASH env variable"
    )
    @allure.description(
        "TC-CONFIG-044: Test from_yaml overrides api_hash with TMA_API_HASH env variable."
    )
    def test_from_yaml_override_api_hash_from_env(self, monkeypatch) -> None:
        """Test from_yaml overrides api_hash with TMA_API_HASH env variable. TC-CONFIG-044"""

        with allure.step("Create temporary YAML file with api_hash"):
            yaml_content = """api_id: 12345
api_hash: "old_hash_32_characters_long!!!!!"
session_string: "test_session"
"""
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".yaml", delete=False
            ) as f:
                f.write(yaml_content)
                temp_path = f.name

        try:
            with allure.step("Set TMA_API_HASH environment variable"):
                # Set environment variable
                monkeypatch.setenv("TMA_API_HASH", "new_hash_32_characters_long!!!!!")

            with allure.step("Load Config from YAML"):
                config = Config.from_yaml(temp_path)

            with allure.step("Verify api_hash is from environment variable, not YAML"):
                # Verify api_hash is from environment variable, not YAML
                assert config.api_hash == "new_hash_32_characters_long!!!!!"
                assert config.api_hash != "old_hash_32_characters_long!!!!!"
        finally:
            os.unlink(temp_path)

    @mark.unit
    @allure.title(
        "TC-CONFIG-045: from_yaml overrides session_string with TMA_SESSION_STRING env variable"
    )
    @allure.description(
        "TC-CONFIG-045: Test from_yaml overrides session_string with TMA_SESSION_STRING env variable."
    )
    def test_from_yaml_override_session_string_from_env(self, monkeypatch) -> None:
        """Test from_yaml overrides session_string with TMA_SESSION_STRING env variable. TC-CONFIG-045"""

        with allure.step("Create temporary YAML file with session_string"):
            yaml_content = """api_id: 12345
api_hash: "12345678901234567890123456789012"
session_string: "old_session"
session_file: "old_session.session"
"""
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".yaml", delete=False
            ) as f:
                f.write(yaml_content)
                temp_path = f.name

        try:
            with allure.step("Set TMA_SESSION_STRING environment variable"):
                # Set environment variable
                monkeypatch.setenv("TMA_SESSION_STRING", "new_session_from_env")

            with allure.step("Load Config from YAML"):
                config = Config.from_yaml(temp_path)

            with allure.step(
                "Verify session_string is from environment variable, not YAML"
            ):
                # Verify session_string is from environment variable, not YAML
                assert config.session_string == "new_session_from_env"
                assert config.session_string != "old_session"
                # Verify session_file is removed when session_string is provided via env
                assert (
                    config.session_file is None
                    or config.session_file != "old_session.session"
                )
        finally:
            os.unlink(temp_path)

    @mark.unit
    @allure.title(
        "TC-CONFIG-046: from_yaml overrides session_file with TMA_SESSION_FILE env variable"
    )
    @allure.description(
        "TC-CONFIG-046: Test from_yaml overrides session_file with TMA_SESSION_FILE env variable."
    )
    def test_from_yaml_override_session_file_from_env(self, monkeypatch) -> None:
        """Test from_yaml overrides session_file with TMA_SESSION_FILE env variable. TC-CONFIG-046"""

        with allure.step("Create temporary YAML file with session_file"):
            yaml_content = """api_id: 12345
api_hash: "12345678901234567890123456789012"
session_string: "old_session"
session_file: "old_session.session"
"""
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".yaml", delete=False
            ) as f:
                f.write(yaml_content)
                temp_path = f.name

        try:
            with allure.step("Set TMA_SESSION_FILE environment variable"):
                # Set environment variable
                monkeypatch.setenv("TMA_SESSION_FILE", "new_session.session")

            with allure.step("Load Config from YAML"):
                config = Config.from_yaml(temp_path)

            with allure.step(
                "Verify session_file is from environment variable, not YAML"
            ):
                # Verify session_file is from environment variable, not YAML
                assert config.session_file == "new_session.session"
                assert config.session_file != "old_session.session"
                # Verify session_string is removed when session_file is provided via env
                assert (
                    config.session_string is None
                    or config.session_string != "old_session"
                )
        finally:
            os.unlink(temp_path)


# ============================================================================
# VIII. Дополнительные свойства класса
# ============================================================================


class TestConfigAdditional:
    """Test additional Config class properties."""

    @mark.unit
    @allure.title("TC-CONFIG-001: Config serialization using msgspec.to_builtins")
    @allure.description("TC-CONFIG-001: Test serialization using msgspec.to_builtins.")
    def test_config_serialization_to_builtins(
        self,
        valid_config_data: dict[str, int | str | float],
    ) -> None:
        """Test serialization using msgspec.to_builtins."""
        with allure.step("Create Config instance"):
            config = Config(**valid_config_data)  # type: ignore[arg-type]
        with allure.step("Serialize Config to dict"):
            config_dict = to_builtins(config)
        with allure.step("Verify serialized dict contains all expected fields"):
            assert isinstance(config_dict, dict)
            assert config_dict.get("api_id") == valid_config_data.get("api_id")
            assert config_dict.get("api_hash") == valid_config_data.get("api_hash")
            assert config_dict.get("session_string") == valid_config_data.get(
                "session_string"
            )
            assert config_dict.get("timeout") == valid_config_data.get("timeout")
            assert config_dict.get("retry_count") == valid_config_data.get(
                "retry_count"
            )
            assert config_dict.get("retry_delay") == valid_config_data.get(
                "retry_delay"
            )
            assert config_dict.get("log_level") == valid_config_data.get("log_level")

    @mark.unit
    @allure.title(
        "TC-CONFIG-001: Config deserialization from dict using msgspec.convert"
    )
    @allure.description("TC-CONFIG-001: Test deserialization using msgspec.convert.")
    def test_config_deserialization_from_dict(
        self,
        valid_config_data: dict[str, int | str | float],
    ) -> None:
        """Test deserialization using msgspec.convert."""
        with allure.step("Deserialize dict to Config"):
            config = convert(valid_config_data, Config)
        with allure.step("Verify deserialized Config contains all expected fields"):
            assert isinstance(config, Config)
            assert config.api_id == valid_config_data.get("api_id")
            assert config.api_hash == valid_config_data.get("api_hash")
            assert config.session_string == valid_config_data.get("session_string")
            assert config.timeout == valid_config_data.get("timeout")
            assert config.retry_count == valid_config_data.get("retry_count")
            assert config.retry_delay == valid_config_data.get("retry_delay")
            assert config.log_level == valid_config_data.get("log_level")

    @mark.unit
    @allure.title("TC-CONFIG-001: Config repr contains class name")
    @allure.description("TC-CONFIG-001: Test that Config repr contains class name.")
    def test_config_repr_contains_class_name(
        self,
        valid_config_data: dict[str, int | str | float],
    ) -> None:
        """Test that repr(config) contains class name."""
        with allure.step("Create Config instance"):
            config = Config(**valid_config_data)  # type: ignore[arg-type]
        with allure.step("Get repr string"):
            repr_str = repr(config)
        with allure.step("Verify repr contains class name"):
            assert "Config" in repr_str
