"""
SQLite database adapter using aiosqlite.
"""

# Python imports
from typing import Optional, Dict, Any, List

# Local imports
from ..db_client import DBClient
from ...config import Config


class SQLiteAdapter(DBClient):
    """
    SQLite database adapter.

    Uses aiosqlite for async SQLite operations.
    """

    def __init__(
        self,
        url: str,
        config: Optional[Config] = None,
        connection_string: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize SQLite adapter.

        Args:
            url: Mini App URL (for BaseClient compatibility)
            config: Configuration object
            connection_string: SQLite connection string (e.g., 'sqlite:///path/to/db.sqlite')
            **kwargs: Additional parameters (database_path, timeout, etc.)
        """
        super().__init__(url, config, connection_string, **kwargs)
        self._database_path: Optional[str] = None
        self._in_transaction: bool = False
        self._transaction_level: int = 0  # Track transaction nesting level

        # Extract database path from connection_string or kwargs
        if connection_string:
            # Remove 'sqlite:///' prefix if present
            if connection_string.startswith("sqlite:///"):
                self._database_path = connection_string[10:]
            elif connection_string.startswith("sqlite://"):
                self._database_path = connection_string[9:]
            else:
                self._database_path = connection_string
        else:
            self._database_path = self._db_kwargs.get("database_path", ":memory:")

    async def connect(self) -> None:
        """Establish SQLite connection."""
        if self._is_connected:
            self.logger.debug("Already connected to SQLite")
            return

        try:
            import aiosqlite
        except ImportError:
            raise ImportError(
                "SQLite adapter requires 'aiosqlite' library. "
                "Install it with: uv add aiosqlite"
            )

        if self._database_path is None:
            raise ValueError("Database path is required")
        self._connection = await aiosqlite.connect(self._database_path)
        self._connection.row_factory = aiosqlite.Row
        self._is_connected = True
        self.logger.info(f"Connected to SQLite database: {self._database_path}")

    async def disconnect(self) -> None:
        """Close SQLite connection."""
        if self._connection:
            await self._connection.close()
            self._connection = None
        self._is_connected = False
        self._in_transaction = False
        self._transaction_level = 0
        self.logger.info("Disconnected from SQLite database")

    async def execute_query(
        self, query: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Execute SELECT query."""
        if not self._is_connected:
            await self.connect()

        if self._connection is None:
            raise RuntimeError("Connection is not established")
        # aiosqlite supports named parameters (dict) directly
        cursor = await self._connection.execute(query, params or {})
        rows = await cursor.fetchall()
        if cursor.description is None:
            return []
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    async def execute_command(
        self, command: str, params: Optional[Dict[str, Any]] = None
    ) -> int:
        """Execute INSERT/UPDATE/DELETE command."""
        if not self._is_connected:
            await self.connect()

        if self._connection is None:
            raise RuntimeError("Connection is not established")
        # aiosqlite supports named parameters (dict) directly
        cursor = await self._connection.execute(command, params or {})
        # Only commit if not in a transaction
        if not self._in_transaction:
            await self._connection.commit()
        return cursor.rowcount  # type: ignore[no-any-return]

    async def begin_transaction(self) -> None:
        """Start transaction."""
        if not self._is_connected:
            await self.connect()
        if self._connection is None:
            raise RuntimeError("Connection is not established")
        # SQLite doesn't support nested transactions, so we track nesting level
        # Only start a new transaction if we're not already in one
        if self._transaction_level == 0:
            await self._connection.execute("BEGIN")
            self._in_transaction = True
        self._transaction_level += 1

    async def commit_transaction(self) -> None:
        """Commit transaction."""
        if self._transaction_level > 0:
            self._transaction_level -= 1
            # Only commit if we're at the top level
            if self._transaction_level == 0 and self._connection:
                await self._connection.commit()
                self._in_transaction = False

    async def rollback_transaction(self) -> None:
        """Rollback transaction."""
        if self._transaction_level > 0:
            # In SQLite, rollback always rolls back the entire transaction
            # regardless of nesting level, so we rollback everything
            if self._connection and self._in_transaction:
                await self._connection.rollback()
                self._in_transaction = False
            # Reset transaction level to 0 (rollback affects all nested levels)
            self._transaction_level = 0
