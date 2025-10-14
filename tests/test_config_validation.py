"""
Test configuration validation for TMA Framework.
"""

import pytest
import os
from tma_framework import Config


def test_config_valid_creation():
    """Test valid config creation."""
    config = Config(
        bot_token="123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
        bot_username="test_bot",
        timeout=60,
        log_level="DEBUG"
    )
    
    assert config.bot_token == "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
    assert config.bot_username == "test_bot"
    assert config.timeout == 60
    assert config.log_level == "DEBUG"


def test_config_invalid_bot_token():
    """Test invalid bot token validation."""
    with pytest.raises(ValueError, match="Invalid bot token format"):
        Config(bot_token="invalid_token")
    
    with pytest.raises(ValueError, match="Invalid bot token format"):
        Config(bot_token="123:short")
    
    with pytest.raises(ValueError, match="Invalid bot token format"):
        Config(bot_token="")


def test_config_invalid_log_level():
    """Test invalid log level validation."""
    with pytest.raises(ValueError, match="Invalid log level"):
        Config(
            bot_token="123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
            log_level="INVALID"
        )
    
    with pytest.raises(ValueError, match="Invalid log level"):
        Config(
            bot_token="123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
            log_level="debug"  # lowercase should fail
        )


def test_config_valid_log_levels():
    """Test all valid log levels."""
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    
    for level in valid_levels:
        config = Config(
            bot_token="123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
            log_level=level
        )
        assert config.log_level == level


def test_config_timeout_validation():
    """Test timeout validation with msgspec Meta."""
    # Valid timeout
    config = Config(
        bot_token="123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
        timeout=1
    )
    assert config.timeout == 1
    
    config = Config(
        bot_token="123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
        timeout=300
    )
    assert config.timeout == 300


def test_config_retry_count_validation():
    """Test retry count validation with msgspec Meta."""
    # Valid retry count
    config = Config(
        bot_token="123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
        retry_count=0
    )
    assert config.retry_count == 0
    
    config = Config(
        bot_token="123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
        retry_count=10
    )
    assert config.retry_count == 10


def test_config_retry_delay_validation():
    """Test retry delay validation with msgspec Meta."""
    # Valid retry delay
    config = Config(
        bot_token="123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
        retry_delay=0.1
    )
    assert config.retry_delay == 0.1
    
    config = Config(
        bot_token="123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
        retry_delay=10.0
    )
    assert config.retry_delay == 10.0


def test_config_from_env_with_token():
    """Test from_env with valid token."""
    os.environ["TMA_BOT_TOKEN"] = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
    os.environ["TMA_BOT_USERNAME"] = "test_bot"
    os.environ["TMA_LOG_LEVEL"] = "DEBUG"
    
    config = Config.from_env()
    
    assert config.bot_token == "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
    assert config.bot_username == "test_bot"
    assert config.log_level == "DEBUG"
    
    # Cleanup
    del os.environ["TMA_BOT_TOKEN"]
    del os.environ["TMA_BOT_USERNAME"]
    del os.environ["TMA_LOG_LEVEL"]


def test_config_from_env_without_token():
    """Test from_env without token should fail."""
    # Remove token if it exists
    if "TMA_BOT_TOKEN" in os.environ:
        del os.environ["TMA_BOT_TOKEN"]
    
    with pytest.raises(ValueError, match="TMA_BOT_TOKEN environment variable is required"):
        Config.from_env()


def test_config_from_env_invalid_token():
    """Test from_env with invalid token should fail."""
    os.environ["TMA_BOT_TOKEN"] = "invalid_token"
    
    with pytest.raises(ValueError, match="Invalid bot token format"):
        Config.from_env()
    
    # Cleanup
    del os.environ["TMA_BOT_TOKEN"]


def test_config_default_values():
    """Test default values."""
    config = Config(bot_token="123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
    
    assert config.bot_username is None
    assert config.mini_app_url is None
    assert config.mini_app_start_param is None
    assert config.timeout == 30
    assert config.retry_count == 3
    assert config.retry_delay == 1.0
    assert config.log_level == "INFO"


def test_config_serialization():
    """Test config serialization with msgspec."""
    import msgspec
    
    config = Config(
        bot_token="123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
        bot_username="test_bot",
        timeout=60
    )
    
    # Serialize to JSON
    json_data = msgspec.json.encode(config)
    assert isinstance(json_data, bytes)
    
    # Deserialize from JSON
    config_restored = msgspec.json.decode(json_data, type=Config)
    assert config_restored.bot_token == config.bot_token
    assert config_restored.bot_username == config.bot_username
    assert config_restored.timeout == config.timeout


if __name__ == "__main__":
    pytest.main([__file__])
