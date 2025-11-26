"""
Base class for Telegram Mini App testing clients.
"""

from typing import Optional
from loguru import logger

from ..config import Config


class BaseClient:
    """
    Base class for Telegram Mini App testing clients.

    Provides common functionality for all client types:
    - URL management
    - Configuration handling
    - Logging setup
    - Context manager support
    """

    def __init__(self, url: str, config: Optional[Config] = None) -> None:
        """
        Initialize base client.

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
