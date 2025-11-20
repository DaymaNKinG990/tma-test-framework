"""
Base class for Telegram Mini App testing.
"""

from typing import Optional
from loguru import logger

from ..config import Config


class BaseMiniApp:
    """
    Base class for Telegram Mini App testing.

    Provides common functionality for both API and UI testing.
    """

    def __init__(self, url: str, config: Optional[Config] = None) -> None:
        """
        Initialize base Mini App client.

        Args:
            url: Mini App URL
            config: Configuration object

        Raises:
            TypeError: If url is not a string
            ValueError: If config is None
        """
        if not isinstance(url, str):
            raise TypeError(f"url must be a string, got {type(url).__name__}")
        if config is None:
            raise ValueError("config is required")
        self.url = url
        self.config = config
        self.logger = logger.bind(name=self.__class__.__name__)

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def close(self) -> None:
        """Close resources."""
        self.logger.debug("Closing resources")
        # Override in subclasses for specific cleanup
