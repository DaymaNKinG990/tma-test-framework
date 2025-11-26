"""
Database client for Telegram Mini App testing framework.

Supports multiple database backends (PostgreSQL, SQLite, MySQL, etc.)
through pluggable database adapters.
"""

# Python imports
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List, TYPE_CHECKING
from contextlib import asynccontextmanager

# Local imports
from .base_client import BaseClient
from ..config import Config

if TYPE_CHECKING:
    pass


class DBClient(BaseClient, ABC):
    """
    Abstract base class for database clients.

    Provides common interface for database operations:
    - Connection management
    - Query execution
    - Transaction handling
    - Connection pooling

    Subclasses should implement database-specific logic.
    """

    def __init__(
        self,
        url: str,
        config: Optional[Config] = None,
        connection_string: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize database client.

        Args:
            url: Mini App URL (for BaseClient compatibility)
            config: Configuration object
            connection_string: Database connection string
            **kwargs: Additional database-specific parameters
        """
        super().__init__(url, config)
        self.connection_string = connection_string
        self._connection: Optional[Any] = None
        self._is_connected = False
        self._db_kwargs = kwargs

    @abstractmethod
    async def connect(self) -> None:
        """
        Establish database connection.

        Raises:
            Exception: If connection fails
        """
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close database connection."""
        pass

    @abstractmethod
    async def execute_query(
        self, query: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute SELECT query and return results.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            List of result rows as dictionaries

        Raises:
            Exception: If query execution fails
        """
        pass

    @abstractmethod
    async def execute_command(
        self, command: str, params: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Execute INSERT/UPDATE/DELETE command.

        Args:
            command: SQL command string
            params: Command parameters

        Returns:
            Number of affected rows

        Raises:
            Exception: If command execution fails
        """
        pass

    @abstractmethod
    async def begin_transaction(self) -> None:
        """Start a database transaction."""
        pass

    @abstractmethod
    async def commit_transaction(self) -> None:
        """Commit current transaction."""
        pass

    @abstractmethod
    async def rollback_transaction(self) -> None:
        """Rollback current transaction."""
        pass

    @asynccontextmanager
    async def transaction(self):
        """
        Context manager for database transactions.

        Usage:
            async with db_client.transaction():
                await db_client.execute_command("INSERT INTO ...")
                await db_client.execute_command("UPDATE ...")
        """
        await self.begin_transaction()
        try:
            yield
            await self.commit_transaction()
        except Exception:
            await self.rollback_transaction()
            raise

    async def close(self) -> None:
        """Close database connection."""
        await self.disconnect()

    async def is_connected(self) -> bool:
        """
        Check if client is connected to database.

        Returns:
            True if connected, False otherwise
        """
        return self._is_connected

    @classmethod
    def create(
        cls,
        db_type: str,
        url: str,
        config: Optional[Config] = None,
        connection_string: Optional[str] = None,
        **kwargs: Any,
    ) -> "DBClient":
        """
        Factory method to create database client by type.

        Args:
            db_type: Database type ('postgresql', 'sqlite', 'mysql', etc.)
            url: Mini App URL (for BaseClient compatibility)
            config: Configuration object
            connection_string: Database connection string
            **kwargs: Additional database-specific parameters

        Returns:
            DBClient instance

        Raises:
            ValueError: If db_type is not supported
            ImportError: If required database library is not installed

        Example:
            >>> # PostgreSQL
            >>> db = DBClient.create(
            ...     'postgresql',
            ...     'https://example.com',
            ...     config,
            ...     connection_string='postgresql://user:pass@localhost/db'
            ... )
            >>> # SQLite
            >>> db = DBClient.create(
            ...     'sqlite',
            ...     'https://example.com',
            ...     config,
            ...     connection_string='sqlite:///path/to/db.sqlite'
            ... )
        """
        db_type_lower = db_type.lower()

        if db_type_lower in ("postgresql", "postgres"):
            try:
                from .db_adapters.postgresql_adapter import PostgreSQLAdapter

                return PostgreSQLAdapter(url, config, connection_string, **kwargs)
            except ImportError as e:
                raise ImportError(
                    "PostgreSQL adapter requires 'asyncpg' or 'psycopg' library. "
                    "Install it with: uv add asyncpg"
                ) from e

        elif db_type_lower == "sqlite":
            try:
                from .db_adapters.sqlite_adapter import SQLiteAdapter

                return SQLiteAdapter(url, config, connection_string, **kwargs)
            except ImportError as e:
                raise ImportError(
                    "SQLite adapter requires 'aiosqlite' library. "
                    "Install it with: uv add aiosqlite"
                ) from e

        elif db_type_lower == "mysql":
            try:
                from .db_adapters.mysql_adapter import MySQLAdapter

                return MySQLAdapter(url, config, connection_string, **kwargs)
            except ImportError as e:
                raise ImportError(
                    "MySQL adapter requires 'aiomysql' or 'pymysql' library. "
                    "Install it with: uv add aiomysql"
                ) from e

        else:
            raise ValueError(
                f"Unsupported database type: {db_type}. "
                f"Supported types: postgresql, sqlite, mysql"
            )
