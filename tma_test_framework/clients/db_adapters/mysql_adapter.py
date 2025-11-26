"""
MySQL database adapter using aiomysql or pymysql.
"""

# Python imports
from typing import Optional, Dict, Any, List

# Local imports
from ..db_client import DBClient
from ...config import Config


class MySQLAdapter(DBClient):
    """
    MySQL database adapter.

    Supports both aiomysql and pymysql libraries.
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
        Initialize MySQL adapter.

        Args:
            url: Mini App URL (for BaseClient compatibility)
            config: Configuration object
            connection_string: MySQL connection string
            **kwargs: Additional connection parameters (host, port, database, user, password)
        """
        super().__init__(url, config, connection_string, **kwargs)
        self._adapter_type: Optional[str] = None

    def _detect_adapter(self) -> str:
        """
        Detect which MySQL library is available.

        Returns:
            'aiomysql' or 'pymysql'

        Raises:
            ImportError: If neither library is available
        """
        try:
            import aiomysql  # type: ignore[import-not-found] # noqa: F401

            return "aiomysql"
        except ImportError:
            try:
                import pymysql  # type: ignore[import-untyped] # noqa: F401

                return "pymysql"
            except ImportError:
                raise ImportError(
                    "MySQL adapter requires either 'aiomysql' or 'pymysql' library. "
                    "Install one with: uv add aiomysql or uv add pymysql"
                )

    async def connect(self) -> None:
        """Establish MySQL connection."""
        if self._is_connected:
            self.logger.debug("Already connected to MySQL")
            return

        adapter_type = self._detect_adapter()
        self._adapter_type = adapter_type

        if adapter_type == "aiomysql":
            await self._connect_aiomysql()
        else:
            await self._connect_pymysql()

        self._is_connected = True
        self.logger.info("Connected to MySQL database")

    async def _connect_aiomysql(self) -> None:
        """Connect using aiomysql."""
        import aiomysql

        if self.connection_string:
            # Parse connection string if needed
            # For simplicity, assume kwargs are provided
            host = self._db_kwargs.get("host", "localhost")
            port = self._db_kwargs.get("port", 3306)
            database = self._db_kwargs.get("database", "mysql")
            user = self._db_kwargs.get("user", "root")
            password = self._db_kwargs.get("password", "")
        else:
            host = self._db_kwargs.get("host", "localhost")
            port = self._db_kwargs.get("port", 3306)
            database = self._db_kwargs.get("database", "mysql")
            user = self._db_kwargs.get("user", "root")
            password = self._db_kwargs.get("password", "")

        self._connection = await aiomysql.connect(
            host=host, port=port, db=database, user=user, password=password
        )

    async def _connect_pymysql(self) -> None:
        """Connect using pymysql."""
        import pymysql

        host = self._db_kwargs.get("host", "localhost")
        port = self._db_kwargs.get("port", 3306)
        database = self._db_kwargs.get("database", "mysql")
        user = self._db_kwargs.get("user", "root")
        password = self._db_kwargs.get("password", "")

        # pymysql is synchronous, so we need to run it in executor
        import asyncio

        loop = asyncio.get_event_loop()
        self._connection = await loop.run_in_executor(
            None,
            lambda: pymysql.connect(
                host=host, port=port, database=database, user=user, password=password
            ),
        )

    async def disconnect(self) -> None:
        """Close MySQL connection."""
        if self._connection:
            if self._adapter_type == "aiomysql":
                self._connection.close()
                await self._connection.ensure_closed()
            else:
                self._connection.close()
            self._connection = None
        self._is_connected = False
        self.logger.info("Disconnected from MySQL database")

    async def execute_query(
        self, query: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Execute SELECT query."""
        if not self._is_connected:
            await self.connect()

        if self._adapter_type == "aiomysql":
            return await self._execute_query_aiomysql(query, params)
        else:
            return await self._execute_query_pymysql(query, params)

    async def _execute_query_aiomysql(
        self, query: str, params: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Execute query using aiomysql."""
        import aiomysql

        if self._connection is None:
            raise RuntimeError("Connection is not established")
        async with self._connection.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(query, list((params or {}).values()))
            rows = await cursor.fetchall()
            return list(rows)

    async def _execute_query_pymysql(
        self, query: str, params: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Execute query using pymysql."""
        import asyncio
        import pymysql

        if self._connection is None:
            raise RuntimeError("Connection is not established")
        loop = asyncio.get_event_loop()

        def _execute():
            with self._connection.cursor(pymysql.cursors.DictCursor) as cursor:  # type: ignore[union-attr]
                cursor.execute(query, list((params or {}).values()))
                return cursor.fetchall()

        rows = await loop.run_in_executor(None, _execute)
        return list(rows)

    async def execute_command(
        self, command: str, params: Optional[Dict[str, Any]] = None
    ) -> int:
        """Execute INSERT/UPDATE/DELETE command."""
        if not self._is_connected:
            await self.connect()

        if self._adapter_type == "aiomysql":
            return await self._execute_command_aiomysql(command, params)
        else:
            return await self._execute_command_pymysql(command, params)

    async def _execute_command_aiomysql(
        self, command: str, params: Optional[Dict[str, Any]]
    ) -> int:
        """Execute command using aiomysql."""
        if self._connection is None:
            raise RuntimeError("Connection is not established")
        async with self._connection.cursor() as cursor:
            await cursor.execute(command, list((params or {}).values()))
            # Commit only if not in transaction
            if not self._connection.in_transaction:
                await self._connection.commit()
            return cursor.rowcount  # type: ignore[no-any-return]

    async def _execute_command_pymysql(
        self, command: str, params: Optional[Dict[str, Any]]
    ) -> int:
        """Execute command using pymysql."""
        import asyncio

        if self._connection is None:
            raise RuntimeError("Connection is not established")
        loop = asyncio.get_event_loop()

        def _execute():
            with self._connection.cursor() as cursor:  # type: ignore[union-attr]
                cursor.execute(command, list((params or {}).values()))
                self._connection.commit()  # type: ignore[union-attr]
                return cursor.rowcount

        return await loop.run_in_executor(None, _execute)

    async def begin_transaction(self) -> None:
        """Start transaction."""
        if not self._is_connected:
            await self.connect()
        if self._connection is None:
            raise RuntimeError("Connection is not established")
        if self._adapter_type == "aiomysql":
            await self._connection.begin()
        else:
            # pymysql autocommit is False by default
            pass

    async def commit_transaction(self) -> None:
        """Commit transaction."""
        if self._connection is None:
            raise RuntimeError("Connection is not established")
        if self._adapter_type == "aiomysql":
            await self._connection.commit()
        else:
            self._connection.commit()

    async def rollback_transaction(self) -> None:
        """Rollback transaction."""
        if self._connection is None:
            raise RuntimeError("Connection is not established")
        if self._adapter_type == "aiomysql":
            await self._connection.rollback()
        else:
            self._connection.rollback()
