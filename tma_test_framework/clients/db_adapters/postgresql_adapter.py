"""
PostgreSQL database adapter using asyncpg or psycopg.
"""

# Python imports
from typing import Optional, Dict, Any, List

# Local imports
from ..db_client import DBClient
from ...config import Config


class PostgreSQLAdapter(DBClient):
    """
    PostgreSQL database adapter.

    Supports both asyncpg and psycopg libraries.
    Automatically detects which library is available.
    """

    def __init__(
        self,
        url: str,
        config: Optional[Config] = None,
        connection_string: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize PostgreSQL adapter.

        Args:
            url: Mini App URL (for BaseClient compatibility)
            config: Configuration object
            connection_string: PostgreSQL connection string
            **kwargs: Additional connection parameters (host, port, database, user, password)
        """
        super().__init__(url, config, connection_string, **kwargs)
        self._adapter_type: Optional[str] = None
        self._pool: Optional[Any] = None

    def _detect_adapter(self) -> str:
        """
        Detect which PostgreSQL library is available.

        Returns:
            'asyncpg' or 'psycopg'

        Raises:
            ImportError: If neither library is available
        """
        try:
            import asyncpg  # type: ignore[import-not-found] # noqa: F401

            return "asyncpg"
        except ImportError:
            try:
                import psycopg  # type: ignore[import-not-found] # noqa: F401

                return "psycopg"
            except ImportError:
                raise ImportError(
                    "PostgreSQL adapter requires either 'asyncpg' or 'psycopg' library. "
                    "Install one with: uv add asyncpg or uv add psycopg[binary]"
                )

    async def connect(self) -> None:
        """Establish PostgreSQL connection."""
        if self._is_connected:
            self.logger.debug("Already connected to PostgreSQL")
            return

        adapter_type = self._detect_adapter()
        self._adapter_type = adapter_type

        if adapter_type == "asyncpg":
            await self._connect_asyncpg()
        else:
            await self._connect_psycopg()

        self._is_connected = True
        self.logger.info("Connected to PostgreSQL database")

    async def _connect_asyncpg(self) -> None:
        """Connect using asyncpg."""
        import asyncpg

        if self.connection_string:
            self._connection = await asyncpg.connect(self.connection_string)
        else:
            # Build connection from kwargs
            host = self._db_kwargs.get("host", "localhost")
            port = self._db_kwargs.get("port", 5432)
            database = self._db_kwargs.get("database", "postgres")
            user = self._db_kwargs.get("user", "postgres")
            password = self._db_kwargs.get("password", "")

            self._connection = await asyncpg.connect(
                host=host, port=port, database=database, user=user, password=password
            )

    async def _connect_psycopg(self) -> None:
        """Connect using psycopg."""
        import psycopg

        if self.connection_string:
            self._connection = await psycopg.AsyncConnection.connect(
                self.connection_string
            )
        else:
            # Build connection from kwargs
            host = self._db_kwargs.get("host", "localhost")
            port = self._db_kwargs.get("port", 5432)
            database = self._db_kwargs.get("database", "postgres")
            user = self._db_kwargs.get("user", "postgres")
            password = self._db_kwargs.get("password", "")

            self._connection = await psycopg.AsyncConnection.connect(
                host=host,
                port=port,
                dbname=database,
                user=user,
                password=password,
            )

    async def disconnect(self) -> None:
        """Close PostgreSQL connection."""
        if self._connection:
            if self._adapter_type == "asyncpg":
                await self._connection.close()
            else:
                await self._connection.close()
            self._connection = None
        self._is_connected = False
        self.logger.info("Disconnected from PostgreSQL database")

    async def execute_query(
        self, query: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Execute SELECT query."""
        if not self._is_connected:
            await self.connect()

        if self._adapter_type == "asyncpg":
            return await self._execute_query_asyncpg(query, params)
        else:
            return await self._execute_query_psycopg(query, params)

    async def _execute_query_asyncpg(
        self, query: str, params: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Execute query using asyncpg."""
        if self._connection is None:
            raise RuntimeError("Connection is not established")
        rows = await self._connection.fetch(query, *(params or {}).values())
        return [dict(row) for row in rows]

    async def _execute_query_psycopg(
        self, query: str, params: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Execute query using psycopg."""
        if self._connection is None:
            raise RuntimeError("Connection is not established")
        async with self._connection.cursor() as cursor:
            await cursor.execute(query, params or {})
            if cursor.description is None:
                return []
            columns = [desc[0] for desc in cursor.description]
            rows = await cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]

    async def execute_command(
        self, command: str, params: Optional[Dict[str, Any]] = None
    ) -> int:
        """Execute INSERT/UPDATE/DELETE command."""
        if not self._is_connected:
            await self.connect()

        if self._adapter_type == "asyncpg":
            return await self._execute_command_asyncpg(command, params)
        else:
            return await self._execute_command_psycopg(command, params)

    async def _execute_command_asyncpg(
        self, command: str, params: Optional[Dict[str, Any]]
    ) -> int:
        """Execute command using asyncpg."""
        if self._connection is None:
            raise RuntimeError("Connection is not established")
        result = await self._connection.execute(command, *(params or {}).values())
        return int(result.split()[-1]) if result else 0

    async def _execute_command_psycopg(
        self, command: str, params: Optional[Dict[str, Any]]
    ) -> int:
        """Execute command using psycopg."""
        if self._connection is None:
            raise RuntimeError("Connection is not established")
        async with self._connection.cursor() as cursor:
            await cursor.execute(command, params or {})
            return cursor.rowcount  # type: ignore[no-any-return]

    async def begin_transaction(self) -> None:
        """Start transaction."""
        if not self._is_connected:
            await self.connect()
        # PostgreSQL uses autocommit=False by default, but we'll be explicit
        if self._adapter_type == "psycopg":
            if self._connection is None:
                raise RuntimeError("Connection is not established")
            await self._connection.execute("BEGIN")

    async def commit_transaction(self) -> None:
        """Commit transaction."""
        if self._connection is None:
            raise RuntimeError("Connection is not established")
        if self._adapter_type == "asyncpg":
            # asyncpg commits automatically unless in a transaction block
            pass
        else:
            await self._connection.commit()

    async def rollback_transaction(self) -> None:
        """Rollback transaction."""
        if self._connection is None:
            raise RuntimeError("Connection is not established")
        if self._adapter_type == "asyncpg":
            # asyncpg doesn't have explicit rollback in connection
            pass
        else:
            await self._connection.rollback()
