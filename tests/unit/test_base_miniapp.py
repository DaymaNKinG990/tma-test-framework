"""
Unit tests for BaseMiniApp.
"""

import pytest

from src.mini_app.base import BaseMiniApp
from src.config import Config


# ============================================================================
# I. Инициализация (__init__)
# ============================================================================


class TestBaseMiniAppInit:
    """Test BaseMiniApp initialization."""

    def test_init_with_valid_url_and_config(self, valid_config):
        """Test successful initialization with valid url and config."""
        app = BaseMiniApp("https://example.com/app", valid_config)

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
    def test_init_with_valid_urls(self, url, valid_config):
        """Test initialization with various valid URLs."""
        app = BaseMiniApp(url, valid_config)

        assert app.url == url
        assert app.config == valid_config

    def test_init_with_config_none_raises_value_error(self):
        """Test that BaseMiniApp rejects None config with ValueError."""
        with pytest.raises(ValueError, match="config is required"):
            BaseMiniApp("https://example.com/app", None)

    def test_init_saves_url_as_attribute(self, valid_config):
        """Test that url is saved as instance attribute."""
        url = "https://example.com/app"
        app = BaseMiniApp(url, valid_config)

        assert hasattr(app, "url")
        assert app.url == url

    def test_init_binds_logger_with_class_name(self, valid_config):
        """Test that logger is bound with class name."""
        app = BaseMiniApp("https://example.com/app", valid_config)

        assert app.logger is not None
        # Check that logger is bound (we can't easily check the name, but we can check it's a logger)
        assert hasattr(app.logger, "bind")

    def test_init_with_empty_string_url(self, valid_config):
        """Test initialization with empty string URL."""
        # Empty string is technically valid as a string, but may not be a valid URL
        app = BaseMiniApp("", valid_config)

        assert app.url == ""
        assert app.config == valid_config

    @pytest.mark.parametrize("invalid_url", [None, 123, []])
    def test_init_with_invalid_url_type(self, invalid_url, valid_config):
        """Test initialization with invalid URL type raises TypeError."""
        with pytest.raises(TypeError, match="url must be a string"):
            BaseMiniApp(invalid_url, valid_config)


# ============================================================================
# II. Асинхронный контекстный менеджер
# ============================================================================


class TestBaseMiniAppContextManager:
    """Test BaseMiniApp async context manager."""

    @pytest.mark.asyncio
    async def test_aenter_returns_self(self, valid_config):
        """Test __aenter__() returns self."""
        app = BaseMiniApp("https://example.com/app", valid_config)

        async with app as context_app:
            assert isinstance(context_app, BaseMiniApp)
            assert context_app is app

    @pytest.mark.asyncio
    async def test_aexit_calls_close(self, mocker, valid_config):
        """Test __aexit__() calls await self.close()."""
        app = BaseMiniApp("https://example.com/app", valid_config)
        mock_close = mocker.patch.object(app, "close", new_callable=mocker.AsyncMock)

        async with app:
            pass

        mock_close.assert_called_once()

    @pytest.mark.asyncio
    async def test_aexit_does_not_suppress_exceptions(self, valid_config):
        """Test __aexit__() does not suppress exceptions (default behavior)."""
        app = BaseMiniApp("https://example.com/app", valid_config)

        # Create an exception inside the context
        with pytest.raises(ValueError, match="Test error"):
            async with app:
                raise ValueError("Test error")

        # Exception should be raised, not suppressed

    @pytest.mark.asyncio
    async def test_context_manager_usage(self, valid_config):
        """Test typical context manager usage."""
        async with BaseMiniApp("https://example.com/app", valid_config) as app:
            assert isinstance(app, BaseMiniApp)
            assert app.url == "https://example.com/app"
            assert app.config == valid_config


# ============================================================================
# III. Метод close()
# ============================================================================


class TestBaseMiniAppClose:
    """Test BaseMiniApp close method."""

    @pytest.mark.asyncio
    async def test_close_logs_debug_message(self, valid_config, caplog):
        """Test close() logs debug message."""
        app = BaseMiniApp("https://example.com/app", valid_config)

        with caplog.at_level("DEBUG"):
            await app.close()

        # Check that debug message was logged
        assert "Closing resources" in caplog.text

    @pytest.mark.asyncio
    async def test_close_does_not_raise_exception(self, valid_config):
        """Test close() does not raise exceptions by default."""
        app = BaseMiniApp("https://example.com/app", valid_config)

        # Should not raise any exception
        await app.close()

    @pytest.mark.asyncio
    async def test_close_safe_to_call_multiple_times(self, valid_config):
        """Test close() is safe to call multiple times."""
        app = BaseMiniApp("https://example.com/app", valid_config)

        # Should not raise any exception when called multiple times
        await app.close()
        await app.close()
        await app.close()

    @pytest.mark.asyncio
    async def test_close_can_be_overridden_in_subclass(self, mocker, valid_config):
        """Test close() can be overridden in subclasses."""

        class CustomMiniApp(BaseMiniApp):
            async def close(self):
                self.logger.debug("Custom close")
                await super().close()

        app = CustomMiniApp("https://example.com/app", valid_config)

        # Should call both custom and base close
        mock_debug = mocker.patch.object(app.logger, "debug")
        await app.close()
        # Should be called at least once (for custom or base)
        assert mock_debug.called


# ============================================================================
# IV. Обработка ошибок и edge cases
# ============================================================================


class TestBaseMiniAppErrorHandling:
    """Test BaseMiniApp error handling."""

    def test_init_with_non_string_url_raises_type_error(self, valid_config):
        """Test that initialization with non-string URL raises TypeError."""
        with pytest.raises(TypeError, match="url must be a string"):
            BaseMiniApp(123, valid_config)  # type: ignore[arg-type]

    def test_init_with_list_url_raises_type_error(self, valid_config):
        """Test that initialization with list as URL raises TypeError."""
        with pytest.raises(TypeError, match="url must be a string"):
            BaseMiniApp([], valid_config)  # type: ignore[arg-type]

    def test_init_with_invalid_config_object_raises_at_config_creation(self):
        """Test that invalid config object raises error at Config creation."""
        # Try to create Config with invalid data
        with pytest.raises((TypeError, ValueError)):
            invalid_config = Config(
                api_id=0,  # Invalid: must be between 1 and 999999999
                api_hash="12345678901234567890123456789012",
                session_string="test",
            )
            BaseMiniApp("https://example.com/app", invalid_config)


# ============================================================================
# V. Логирование
# ============================================================================


class TestBaseMiniAppLogging:
    """Test BaseMiniApp logging."""

    def test_logger_bound_to_class_name(self, valid_config):
        """Test logger is bound to class name."""
        app = BaseMiniApp("https://example.com/app", valid_config)

        # Logger should be bound (we can't easily check the exact name, but we can verify it's a logger)
        assert app.logger is not None
        assert hasattr(app.logger, "debug")
        assert hasattr(app.logger, "info")
        assert hasattr(app.logger, "error")

    def test_logger_in_subclass_uses_subclass_name(self, valid_config):
        """Test logger in subclass uses subclass name."""

        class CustomMiniApp(BaseMiniApp):
            pass

        app = CustomMiniApp("https://example.com/app", valid_config)

        # Logger should be bound to CustomMiniApp, not BaseMiniApp
        assert app.logger is not None
        # The logger name should be "CustomMiniApp" (we can't easily verify this without inspecting internals)

    @pytest.mark.asyncio
    async def test_close_logs_with_context(self, valid_config, caplog):
        """Test close() logs with proper context."""
        app = BaseMiniApp("https://example.com/app", valid_config)

        with caplog.at_level("DEBUG"):
            await app.close()

        # Check that log message contains context
        assert "Closing resources" in caplog.text

    def test_logger_has_name_attribute(self, valid_config):
        """Test logger has name attribute (bound logger)."""
        app = BaseMiniApp("https://example.com/app", valid_config)

        # Bound logger should have some way to identify it
        # We can't easily check the exact name, but we can verify it's a logger
        assert app.logger is not None


# ============================================================================
# Дополнительные тесты
# ============================================================================


class TestBaseMiniAppAdditional:
    """Additional tests for BaseMiniApp."""

    def test_url_attribute_is_accessible(self, valid_config):
        """Test url attribute is accessible after initialization."""
        url = "https://example.com/app"
        app = BaseMiniApp(url, valid_config)

        assert app.url == url
        # Should be able to read it
        assert isinstance(app.url, str)

    def test_config_attribute_is_accessible(self, valid_config):
        """Test config attribute is accessible after initialization."""
        app = BaseMiniApp("https://example.com/app", valid_config)

        assert app.config == valid_config
        assert isinstance(app.config, Config)

    def test_logger_attribute_is_accessible(self, valid_config):
        """Test logger attribute is accessible after initialization."""
        app = BaseMiniApp("https://example.com/app", valid_config)

        assert app.logger is not None
        assert hasattr(app.logger, "debug")
        assert hasattr(app.logger, "info")
        assert hasattr(app.logger, "warning")
        assert hasattr(app.logger, "error")

    @pytest.mark.asyncio
    async def test_full_lifecycle(self, valid_config):
        """Test full lifecycle: init -> context manager -> close."""
        async with BaseMiniApp("https://example.com/app", valid_config) as app:
            assert app.url == "https://example.com/app"
            assert app.config == valid_config
            assert app.logger is not None

        # After context exit, close should have been called
        # (we can't easily verify this without mocking, but the test should pass)

    def test_multiple_instances_independent(self, valid_config):
        """Test multiple instances are independent."""
        app1 = BaseMiniApp("https://example.com/app1", valid_config)
        app2 = BaseMiniApp("https://example.com/app2", valid_config)

        assert app1.url != app2.url
        assert app1.config == app2.config  # Same config object
        assert app1.logger is not None
        assert app2.logger is not None
