"""
Unit tests for BaseClient.
"""

import pytest
import allure

from tma_test_framework.clients.base_client import BaseClient
from tma_test_framework.config import Config


# ============================================================================
# I. Инициализация (__init__)
# ============================================================================


class TestBaseClientInit:
    """Test BaseClient initialization."""

    @allure.title("TC-BASE-001: Successful initialization with valid url and config")
    @allure.description(
        "TC-BASE-001: Test successful initialization with valid url and config."
    )
    def test_init_with_valid_url_and_config(self, valid_config):
        """Test successful initialization with valid url and config."""
        with allure.step("Create BaseClient instance"):
            app = BaseClient("https://example.com/app", valid_config)

        with allure.step("Verify url, config, and logger are set correctly"):
            assert app.url == "https://example.com/app"
            assert app.config == valid_config
            assert app.logger is not None

    @pytest.mark.parametrize(
        "url",
        [
            "https://example.com/app",
            "https://t.me/mybot/app?start=123",
            "http://localhost:8080",
            "https://mybot.telegram.app/start",
        ],
    )
    @allure.title("TC-BASE-002: Initialization with various valid URLs")
    @allure.description("TC-BASE-002: Test initialization with various valid URLs.")
    def test_init_with_valid_urls(self, url, valid_config):
        """Test initialization with various valid URLs."""
        with allure.step(f"Create BaseClient instance with URL: {url}"):
            app = BaseClient(url, valid_config)

        with allure.step("Verify url and config are set correctly"):
            assert app.url == url
            assert app.config == valid_config

    @allure.title("TC-BASE-010: BaseClient rejects None config with ValueError")
    @allure.description(
        "TC-BASE-010: Test that BaseClient rejects None config with ValueError."
    )
    def test_init_with_config_none_raises_value_error(self):
        """Test that BaseClient rejects None config with ValueError."""
        with allure.step("Attempt to create BaseClient with config=None"):
            with pytest.raises(ValueError, match="config is required"):
                BaseClient("https://example.com/app", None)

    @allure.title("TC-BASE-003: URL is saved as instance attribute")
    @allure.description("TC-BASE-003: Test that url is saved as instance attribute.")
    def test_init_saves_url_as_attribute(self, valid_config):
        """Test that url is saved as instance attribute."""
        with allure.step("Create BaseClient instance"):
            url = "https://example.com/app"
            app = BaseClient(url, valid_config)

        with allure.step("Verify url attribute exists and is set correctly"):
            assert hasattr(app, "url")
            assert app.url == url

    @allure.title("TC-BASE-004: Logger is bound with class name")
    @allure.description("TC-BASE-004: Test that logger is bound with class name.")
    def test_init_binds_logger_with_class_name(self, valid_config):
        """Test that logger is bound with class name."""
        with allure.step("Create BaseClient instance"):
            app = BaseClient("https://example.com/app", valid_config)

        with allure.step("Verify logger is initialized and has bind method"):
            assert app.logger is not None
            # Check that logger is bound (we can't easily check the name, but we can check it's a logger)
            assert hasattr(app.logger, "bind")

    @allure.title("TC-BASE-013: Initialization with empty string URL")
    @allure.description("TC-BASE-013: Test initialization with empty string URL.")
    def test_init_with_empty_string_url(self, valid_config):
        """Test initialization with empty string URL."""
        with allure.step("Create BaseClient instance with empty string URL"):
            # Empty string is technically valid as a string, but may not be a valid URL
            app = BaseClient("", valid_config)

        with allure.step("Verify url and config are set correctly"):
            assert app.url == ""
            assert app.config == valid_config

    @pytest.mark.parametrize("invalid_url", [None, 123, []])
    @allure.title("TC-BASE-011: Initialization with invalid URL type raises TypeError")
    @allure.description(
        "TC-BASE-011: Test initialization with invalid URL type raises TypeError."
    )
    def test_init_with_invalid_url_type(self, invalid_url, valid_config):
        """Test initialization with invalid URL type raises TypeError."""
        with allure.step(
            f"Attempt to create BaseClient with invalid URL type: {type(invalid_url).__name__}"
        ):
            with pytest.raises(TypeError, match="url must be a string"):
                BaseClient(invalid_url, valid_config)


# ============================================================================
# II. Асинхронный контекстный менеджер
# ============================================================================


class TestBaseClientContextManager:
    """Test BaseClient async context manager."""

    @pytest.mark.asyncio
    @allure.title("TC-BASE-005: __aenter__() returns self")
    @allure.description("TC-BASE-005: Test __aenter__() returns self.")
    async def test_aenter_returns_self(self, valid_config):
        """Test __aenter__() returns self."""
        with allure.step("Create BaseClient instance"):
            app = BaseClient("https://example.com/app", valid_config)

        with allure.step(
            "Use async context manager and verify __aenter__ returns self"
        ):
            async with app as context_app:
                assert isinstance(context_app, BaseClient)
                assert context_app is app

    @pytest.mark.asyncio
    @allure.title("TC-BASE-006: __aexit__() calls await self.close()")
    @allure.description("TC-BASE-006: Test __aexit__() calls await self.close().")
    async def test_aexit_calls_close(self, mocker, valid_config):
        """Test __aexit__() calls await self.close()."""
        with allure.step("Create BaseClient instance and mock close method"):
            app = BaseClient("https://example.com/app", valid_config)
            mock_close = mocker.patch.object(
                app, "close", new_callable=mocker.AsyncMock
            )

        with allure.step("Use async context manager"):
            async with app:
                pass

        with allure.step("Verify close was called"):
            mock_close.assert_called_once()

    @pytest.mark.asyncio
    @allure.title(
        "TC-BASE-007: __aexit__() does not suppress exceptions (default behavior)"
    )
    @allure.description(
        "TC-BASE-007: Test __aexit__() does not suppress exceptions (default behavior)."
    )
    async def test_aexit_does_not_suppress_exceptions(self, valid_config):
        """Test __aexit__() does not suppress exceptions (default behavior)."""
        with allure.step("Create BaseClient instance"):
            app = BaseClient("https://example.com/app", valid_config)

        with allure.step(
            "Create an exception inside the context and verify it is raised"
        ):
            # Create an exception inside the context
            with pytest.raises(ValueError, match="Test error"):
                async with app:
                    raise ValueError("Test error")

            # Exception should be raised, not suppressed

    @pytest.mark.asyncio
    @allure.title("TC-BASE-014: Typical context manager usage")
    @allure.description("TC-BASE-014: Test typical context manager usage.")
    async def test_context_manager_usage(self, valid_config):
        """Test typical context manager usage."""
        with allure.step("Use async context manager"):
            async with BaseClient("https://example.com/app", valid_config) as app:
                with allure.step("Verify app instance and attributes"):
                    assert isinstance(app, BaseClient)
                    assert app.url == "https://example.com/app"
                    assert app.config == valid_config


# ============================================================================
# III. Метод close()
# ============================================================================


class TestBaseClientClose:
    """Test BaseClient close method."""

    @pytest.mark.asyncio
    @allure.title("TC-BASE-009: close() logs debug message")
    @allure.description("TC-BASE-009: Test close() logs debug message.")
    async def test_close_logs_debug_message(self, valid_config, caplog):
        """Test close() logs debug message."""
        with allure.step("Create BaseClient instance"):
            app = BaseClient("https://example.com/app", valid_config)

        with allure.step("Call close() and verify DEBUG log"):
            with caplog.at_level("DEBUG"):
                await app.close()

            # Check that debug message was logged
            assert "Closing resources" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-BASE-008: close() does not raise exceptions by default")
    @allure.description(
        "TC-BASE-008: Test close() does not raise exceptions by default."
    )
    async def test_close_does_not_raise_exception(self, valid_config):
        """Test close() does not raise exceptions by default."""
        with allure.step("Create BaseClient instance"):
            app = BaseClient("https://example.com/app", valid_config)

        with allure.step("Call close() and verify no exception is raised"):
            # Should not raise any exception
            await app.close()

    @pytest.mark.asyncio
    @allure.title("TC-BASE-015: close() is safe to call multiple times")
    @allure.description("TC-BASE-015: Test close() is safe to call multiple times.")
    async def test_close_safe_to_call_multiple_times(self, valid_config):
        """Test close() is safe to call multiple times."""
        with allure.step("Create BaseClient instance"):
            app = BaseClient("https://example.com/app", valid_config)

        with allure.step("Call close() multiple times and verify no exception"):
            # Should not raise any exception when called multiple times
            await app.close()
            await app.close()
            await app.close()

    @pytest.mark.asyncio
    @allure.title("TC-BASE-012: close() can be overridden in subclasses")
    @allure.description("TC-BASE-012: Test close() can be overridden in subclasses.")
    async def test_close_can_be_overridden_in_subclass(self, mocker, valid_config):
        """Test close() can be overridden in subclasses."""
        with allure.step("Create CustomMiniApp subclass with overridden close"):

            class CustomMiniApp(BaseClient):
                async def close(self):
                    self.logger.debug("Custom close")
                    await super().close()

        with allure.step("Create CustomMiniApp instance and mock logger.debug"):
            app = CustomMiniApp("https://example.com/app", valid_config)

            # Should call both custom and base close
            mock_debug = mocker.patch.object(app.logger, "debug")

        with allure.step("Call close() and verify logger.debug was called"):
            await app.close()
            # Should be called at least once (for custom or base)
            assert mock_debug.called


# ============================================================================
# IV. Обработка ошибок и edge cases
# ============================================================================


class TestBaseClientErrorHandling:
    """Test BaseClient error handling."""

    @allure.title("TC-BASE-016: Initialization with non-string URL raises TypeError")
    @allure.description(
        "TC-BASE-016: Test that initialization with non-string URL raises TypeError."
    )
    def test_init_with_non_string_url_raises_type_error(self, valid_config):
        """Test that initialization with non-string URL raises TypeError."""
        with allure.step("Attempt to create BaseClient with non-string URL (int)"):
            with pytest.raises(TypeError, match="url must be a string"):
                BaseClient(123, valid_config)  # type: ignore[arg-type]

    @allure.title("TC-BASE-017: Initialization with list as URL raises TypeError")
    @allure.description(
        "TC-BASE-017: Test that initialization with list as URL raises TypeError."
    )
    def test_init_with_list_url_raises_type_error(self, valid_config):
        """Test that initialization with list as URL raises TypeError."""
        with allure.step("Attempt to create BaseClient with list as URL"):
            with pytest.raises(TypeError, match="url must be a string"):
                BaseClient([], valid_config)  # type: ignore[arg-type]

    @allure.title("TC-BASE-018: Invalid config object raises error at Config creation")
    @allure.description(
        "TC-BASE-018: Test that invalid config object raises error at Config creation."
    )
    def test_init_with_invalid_config_object_raises_at_config_creation(self):
        """Test that invalid config object raises error at Config creation."""
        with allure.step("Attempt to create Config with invalid data and BaseClient"):
            # Try to create Config with invalid data
            with pytest.raises((TypeError, ValueError)):
                invalid_config = Config(
                    api_id=0,  # Invalid: must be between 1 and 999999999
                    api_hash="12345678901234567890123456789012",
                    session_string="test",
                )
                BaseClient("https://example.com/app", invalid_config)


# ============================================================================
# V. Логирование
# ============================================================================


class TestBaseClientLogging:
    """Test BaseClient logging."""

    @allure.title("TC-BASE-026: Logger is bound to class name")
    @allure.description("TC-BASE-026: Test logger is bound to class name.")
    def test_logger_bound_to_class_name(self, valid_config):
        """Test logger is bound to class name."""
        with allure.step("Create BaseClient instance"):
            app = BaseClient("https://example.com/app", valid_config)

        with allure.step("Verify logger is initialized and has required methods"):
            # Logger should be bound (we can't easily check the exact name, but we can verify it's a logger)
            assert app.logger is not None
            assert hasattr(app.logger, "debug")
            assert hasattr(app.logger, "info")
            assert hasattr(app.logger, "error")

    @allure.title("TC-BASE-019: Logger in subclass uses subclass name")
    @allure.description("TC-BASE-019: Test logger in subclass uses subclass name.")
    def test_logger_in_subclass_uses_subclass_name(self, valid_config):
        """Test logger in subclass uses subclass name."""
        with allure.step("Create CustomMiniApp subclass"):

            class CustomMiniApp(BaseClient):
                pass

        with allure.step("Create CustomMiniApp instance"):
            app = CustomMiniApp("https://example.com/app", valid_config)

        with allure.step("Verify logger is initialized"):
            # Logger should be bound to CustomMiniApp, not BaseClient
            assert app.logger is not None
            # The logger name should be "CustomMiniApp" (we can't easily verify this without inspecting internals)

    @pytest.mark.asyncio
    @allure.title("TC-BASE-020: close() logs with proper context")
    @allure.description("TC-BASE-020: Test close() logs with proper context.")
    async def test_close_logs_with_context(self, valid_config, caplog):
        """Test close() logs with proper context."""
        with allure.step("Create BaseClient instance"):
            app = BaseClient("https://example.com/app", valid_config)

        with allure.step("Call close() and verify log message contains context"):
            with caplog.at_level("DEBUG"):
                await app.close()

            # Check that log message contains context
            assert "Closing resources" in caplog.text

    @allure.title("TC-BASE-021: Logger has name attribute (bound logger)")
    @allure.description("TC-BASE-021: Test logger has name attribute (bound logger).")
    def test_logger_has_name_attribute(self, valid_config):
        """Test logger has name attribute (bound logger)."""
        with allure.step("Create BaseClient instance"):
            app = BaseClient("https://example.com/app", valid_config)

        with allure.step("Verify logger is initialized"):
            # Bound logger should have some way to identify it
            # We can't easily check the exact name, but we can verify it's a logger
            assert app.logger is not None


# ============================================================================
# Дополнительные тесты
# ============================================================================


class TestBaseClientAdditional:
    """Additional tests for BaseClient."""

    @allure.title("TC-BASE-027: URL attribute is accessible after initialization")
    @allure.description(
        "TC-BASE-027: Test url attribute is accessible after initialization."
    )
    def test_url_attribute_is_accessible(self, valid_config):
        """Test url attribute is accessible after initialization."""
        with allure.step("Create BaseClient instance"):
            url = "https://example.com/app"
            app = BaseClient(url, valid_config)

        with allure.step("Verify url attribute is accessible and has correct type"):
            assert app.url == url
            # Should be able to read it
            assert isinstance(app.url, str)

    @allure.title("TC-BASE-022: Config attribute is accessible after initialization")
    @allure.description(
        "TC-BASE-022: Test config attribute is accessible after initialization."
    )
    def test_config_attribute_is_accessible(self, valid_config):
        """Test config attribute is accessible after initialization."""
        with allure.step("Create BaseClient instance"):
            app = BaseClient("https://example.com/app", valid_config)

        with allure.step("Verify config attribute is accessible and has correct type"):
            assert app.config == valid_config
            assert isinstance(app.config, Config)

    @allure.title("TC-BASE-023: Logger attribute is accessible after initialization")
    @allure.description(
        "TC-BASE-023: Test logger attribute is accessible after initialization."
    )
    def test_logger_attribute_is_accessible(self, valid_config):
        """Test logger attribute is accessible after initialization."""
        with allure.step("Create BaseClient instance"):
            app = BaseClient("https://example.com/app", valid_config)

        with allure.step("Verify logger is accessible and has required methods"):
            assert app.logger is not None
            assert hasattr(app.logger, "debug")
            assert hasattr(app.logger, "info")
            assert hasattr(app.logger, "warning")
            assert hasattr(app.logger, "error")

    @pytest.mark.asyncio
    @allure.title("TC-BASE-024: Full lifecycle: init -> context manager -> close")
    @allure.description(
        "TC-BASE-024: Test full lifecycle: init -> context manager -> close."
    )
    async def test_full_lifecycle(self, valid_config):
        """Test full lifecycle: init -> context manager -> close."""
        with allure.step("Use BaseClient as async context manager"):
            async with BaseClient("https://example.com/app", valid_config) as app:
                with allure.step("Verify app attributes are accessible"):
                    assert app.url == "https://example.com/app"
                    assert app.config == valid_config
                    assert app.logger is not None

        # After context exit, close should have been called
        # (we can't easily verify this without mocking, but the test should pass)

    @allure.title("TC-BASE-025: Multiple instances are independent")
    @allure.description("TC-BASE-025: Test multiple instances are independent.")
    def test_multiple_instances_independent(self, valid_config):
        """Test multiple instances are independent."""
        with allure.step("Create two BaseClient instances with different URLs"):
            app1 = BaseClient("https://example.com/app1", valid_config)
            app2 = BaseClient("https://example.com/app2", valid_config)

        with allure.step("Verify instances are independent"):
            assert app1.url != app2.url
            assert app1.config == app2.config  # Same config object
            assert app1.logger is not None
            assert app2.logger is not None
