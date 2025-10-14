"""
Configuration management for TMA Framework.
"""

import os
from typing import Optional, Annotated
import msgspec
from msgspec import Meta


class Config(msgspec.Struct):
    """Configuration for TMA Framework."""
    
    # Bot configuration
    bot_token: Annotated[str, Meta(min_length=20)]
    bot_username: Optional[str] = None
    
    # Mini App configuration
    mini_app_url: Optional[str] = None
    mini_app_start_param: Optional[str] = None
    
    # Testing configuration
    timeout: Annotated[int, Meta(ge=1, le=300)] = 30
    retry_count: Annotated[int, Meta(ge=0, le=10)] = 3
    retry_delay: Annotated[float, Meta(ge=0.1, le=10.0)] = 1.0
    
    # Logging
    log_level: str = "INFO"
    
    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        # Validate bot token format
        if ":" not in self.bot_token or len(self.bot_token.split(":")[1]) < 20:
            raise ValueError("Invalid bot token format. Expected format: <bot_id>:<token>")
        
        # Validate log level
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.log_level not in valid_levels:
            raise ValueError(f"Invalid log level '{self.log_level}'. Must be one of: {valid_levels}")
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables."""
        bot_token = os.getenv("TMA_BOT_TOKEN")
        if not bot_token:
            raise ValueError("TMA_BOT_TOKEN environment variable is required")
        
        return cls(
            bot_token=bot_token,
            bot_username=os.getenv("TMA_BOT_USERNAME"),
            mini_app_url=os.getenv("TMA_MINI_APP_URL"),
            mini_app_start_param=os.getenv("TMA_MINI_APP_START_PARAM"),
            timeout=int(os.getenv("TMA_TIMEOUT", "30")),
            retry_count=int(os.getenv("TMA_RETRY_COUNT", "3")),
            retry_delay=float(os.getenv("TMA_RETRY_DELAY", "1.0")),
            log_level=os.getenv("TMA_LOG_LEVEL", "INFO"),
        )