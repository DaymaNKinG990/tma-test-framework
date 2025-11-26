"""
Unit tests for PostgreSQL and MySQL adapter functional methods.
"""

import builtins
import pytest
import allure
from unittest.mock import AsyncMock, MagicMock

from tma_test_framework.clients.db_adapters.postgresql_adapter import PostgreSQLAdapter
from tma_test_framework.clients.db_adapters.mysql_adapter import MySQLAdapter


# ============================================================================
# PostgreSQLAdapter Functional Tests
# ============================================================================


class TestPostgreSQLAdapterFunctional:
    """Test PostgreSQLAdapter functional methods."""

    @pytest.mark.asyncio
    @allure.title(
        "TC-DB-047: PostgreSQLAdapter connect() with asyncpg via connection_string"
    )
    @allure.description(
        "Test PostgreSQLAdapter connects using asyncpg with connection_string. TC-DB-047"
    )
    async def test_postgresql_connect_asyncpg_connection_string(
        self, valid_config, mocker, mock_asyncpg_module
    ):
        """Test PostgreSQLAdapter connects using asyncpg with connection_string."""
        with allure.step("Create PostgreSQLAdapter with connection_string"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )

        with allure.step("Mock asyncpg.connect() to return mock connection"):
            # Use fixture for mock asyncpg module
            mock_asyncpg_data = mock_asyncpg_module
            mock_connection = mock_asyncpg_data["connection"]
            mock_connect = mock_asyncpg_data["connect"]

        with allure.step("Mock _detect_adapter to return 'asyncpg'"):
            mocker.patch.object(adapter, "_detect_adapter", return_value="asyncpg")

        with allure.step("Call await adapter.connect()"):
            await adapter.connect()

        with allure.step("Verify _adapter_type is 'asyncpg'"):
            assert adapter._adapter_type == "asyncpg"

        with allure.step("Verify _connection is set"):
            assert adapter._connection == mock_connection

        with allure.step("Verify _is_connected is True"):
            assert adapter._is_connected is True

        with allure.step("Verify asyncpg.connect() was called"):
            mock_connect.assert_called_once_with("postgresql://user:pass@localhost/db")

    @pytest.mark.asyncio
    @allure.title("TC-DB-048: PostgreSQLAdapter connect() with asyncpg via kwargs")
    @allure.description(
        "Test PostgreSQLAdapter connects using asyncpg with kwargs. TC-DB-048"
    )
    async def test_postgresql_connect_asyncpg_kwargs(
        self, valid_config, mocker, mock_asyncpg_module
    ):
        """Test PostgreSQLAdapter connects using asyncpg with kwargs."""
        with allure.step(
            "Create PostgreSQLAdapter without connection_string, with kwargs"
        ):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                host="localhost",
                port=5432,
                database="testdb",
                user="testuser",
                password="testpass",
            )

        with allure.step("Mock asyncpg.connect() to return mock connection"):
            # Use fixture for mock asyncpg module
            mock_asyncpg_data = mock_asyncpg_module
            mock_connection = mock_asyncpg_data["connection"]
            mock_connect = mock_asyncpg_data["connect"]

        with allure.step("Mock _detect_adapter to return 'asyncpg'"):
            mocker.patch.object(adapter, "_detect_adapter", return_value="asyncpg")

        with allure.step("Call await adapter.connect()"):
            await adapter.connect()

        with allure.step("Verify asyncpg.connect() called with correct parameters"):
            mock_connect.assert_called_once_with(
                host="localhost",
                port=5432,
                database="testdb",
                user="testuser",
                password="testpass",
            )

        with allure.step("Verify _connection is set"):
            assert adapter._connection == mock_connection

    @pytest.mark.asyncio
    @allure.title(
        "TC-DB-049: PostgreSQLAdapter connect() with psycopg via connection_string"
    )
    @allure.description(
        "Test PostgreSQLAdapter connects using psycopg with connection_string. TC-DB-049"
    )
    async def test_postgresql_connect_psycopg_connection_string(
        self, valid_config, mocker, mock_psycopg_module
    ):
        """Test PostgreSQLAdapter connects using psycopg with connection_string."""
        with allure.step("Create PostgreSQLAdapter with connection_string"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )

        with allure.step(
            "Mock psycopg.AsyncConnection.connect() to return mock connection"
        ):
            # Use fixture for mock psycopg module
            mock_psycopg_data = mock_psycopg_module
            mock_psycopg = mock_psycopg_data["module"]
            mock_connection = mock_psycopg_data["connection"]
            mock_connect = mock_psycopg_data["connect"]
            # psycopg uses AsyncConnection.connect pattern
            mock_async_connection = MagicMock()
            mock_async_connection.connect = mock_connect
            mock_psycopg.AsyncConnection = mock_async_connection

        with allure.step("Mock _detect_adapter to return 'psycopg'"):
            mocker.patch.object(adapter, "_detect_adapter", return_value="psycopg")

        with allure.step("Call await adapter.connect()"):
            await adapter.connect()

        with allure.step("Verify _adapter_type is 'psycopg'"):
            assert adapter._adapter_type == "psycopg"

        with allure.step("Verify _connection is set"):
            assert adapter._connection == mock_connection

        with allure.step("Verify psycopg.AsyncConnection.connect() was called"):
            mock_connect.assert_called_once_with("postgresql://user:pass@localhost/db")

    @pytest.mark.asyncio
    @allure.title("TC-DB-050: PostgreSQLAdapter connect() with psycopg via kwargs")
    @allure.description(
        "Test PostgreSQLAdapter connects using psycopg with kwargs. TC-DB-050"
    )
    async def test_postgresql_connect_psycopg_kwargs(
        self, valid_config, mocker, mock_psycopg_module
    ):
        """Test PostgreSQLAdapter connects using psycopg with kwargs."""
        with allure.step(
            "Create PostgreSQLAdapter without connection_string, with kwargs"
        ):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                host="localhost",
                port=5432,
                database="testdb",
                user="testuser",
                password="testpass",
            )

        with allure.step("Mock psycopg.AsyncConnection.connect()"):
            # Use fixture for mock psycopg module
            mock_psycopg_data = mock_psycopg_module
            mock_psycopg = mock_psycopg_data["module"]
            mock_connection = mock_psycopg_data["connection"]
            mock_connect = mock_psycopg_data["connect"]
            # psycopg uses AsyncConnection.connect pattern
            mock_async_connection = MagicMock()
            mock_async_connection.connect = mock_connect
            mock_psycopg.AsyncConnection = mock_async_connection

            mock_connection = AsyncMock()
            mock_connect.return_value = mock_connection

        with allure.step("Mock _detect_adapter to return 'psycopg'"):
            mocker.patch.object(adapter, "_detect_adapter", return_value="psycopg")

        with allure.step("Call await adapter.connect()"):
            await adapter.connect()

        with allure.step(
            "Verify psycopg.AsyncConnection.connect() called with correct parameters"
        ):
            mock_connect.assert_called_once_with(
                host="localhost",
                port=5432,
                dbname="testdb",
                user="testuser",
                password="testpass",
            )

        with allure.step("Verify _connection is set"):
            assert adapter._connection == mock_connection

    @pytest.mark.asyncio
    @allure.title("TC-DB-051: PostgreSQLAdapter disconnect() with asyncpg")
    @allure.description("Test PostgreSQLAdapter disconnects using asyncpg. TC-DB-051")
    async def test_postgresql_disconnect_asyncpg(self, valid_config, mocker):
        """Test PostgreSQLAdapter disconnects using asyncpg."""
        with allure.step("Create and connect PostgreSQLAdapter with asyncpg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "asyncpg"

        with allure.step("Call await adapter.disconnect()"):
            await adapter.disconnect()

        with allure.step("Verify connection.close() was called"):
            mock_connection.close.assert_called_once()

        with allure.step("Verify _connection is None"):
            assert adapter._connection is None

        with allure.step("Verify _is_connected is False"):
            assert adapter._is_connected is False

    @pytest.mark.asyncio
    @allure.title("TC-DB-052: PostgreSQLAdapter disconnect() with psycopg")
    @allure.description("Test PostgreSQLAdapter disconnects using psycopg. TC-DB-052")
    async def test_postgresql_disconnect_psycopg(self, valid_config, mocker):
        """Test PostgreSQLAdapter disconnects using psycopg."""
        with allure.step("Create and connect PostgreSQLAdapter with psycopg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "psycopg"

        with allure.step("Call await adapter.disconnect()"):
            await adapter.disconnect()

        with allure.step("Verify connection.close() was called"):
            mock_connection.close.assert_called_once()

        with allure.step("Verify _connection is None"):
            assert adapter._connection is None

    @pytest.mark.asyncio
    @allure.title(
        "TC-DB-053: PostgreSQLAdapter connect() when already connected (idempotency)"
    )
    @allure.description("Test PostgreSQLAdapter connect() is idempotent. TC-DB-053")
    async def test_postgresql_connect_idempotent(self, valid_config, mocker):
        """Test PostgreSQLAdapter connect() is idempotent."""
        with allure.step("Create and connect PostgreSQLAdapter"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "asyncpg"

        with allure.step("Mock logger to verify debug message"):
            mock_logger = mocker.patch.object(adapter.logger, "debug")

        with allure.step("Call connect() again"):
            await adapter.connect()

        with allure.step("Verify no new connection is created"):
            assert adapter._connection == mock_connection

        with allure.step("Verify debug log 'Already connected'"):
            mock_logger.assert_called_once_with("Already connected to PostgreSQL")

    @pytest.mark.asyncio
    @allure.title("TC-DB-054: PostgreSQLAdapter execute_query() with asyncpg")
    @allure.description(
        "Test PostgreSQLAdapter executes SELECT query using asyncpg. TC-DB-054"
    )
    async def test_postgresql_execute_query_asyncpg(self, valid_config, mocker):
        """Test PostgreSQLAdapter executes SELECT query using asyncpg."""
        with allure.step("Create and connect PostgreSQLAdapter with asyncpg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "asyncpg"

        with allure.step("Mock connection.fetch() to return mock rows"):
            # Create mock rows that can be converted to dict
            mock_row1 = MagicMock()
            mock_row1.items = lambda: [("id", 1), ("name", "Test")]
            mock_row2 = MagicMock()
            mock_row2.items = lambda: [("id", 2), ("name", "Test2")]
            mock_rows = [mock_row1, mock_row2]
            mock_connection.fetch = AsyncMock(return_value=mock_rows)

        with allure.step(
            "Call await adapter.execute_query('SELECT * FROM users WHERE id = $1', {'id': 1})"
        ):
            result = await adapter.execute_query(
                "SELECT * FROM users WHERE id = $1", {"id": 1}
            )

        with allure.step(
            "Verify connection.fetch() called with correct query and parameters"
        ):
            mock_connection.fetch.assert_called_once()
            call_args = mock_connection.fetch.call_args
            assert call_args[0][0] == "SELECT * FROM users WHERE id = $1"
            assert 1 in call_args[0][1:]  # Check that id=1 is in positional args

        with allure.step("Verify returns list of dictionaries"):
            assert isinstance(result, list)
            assert len(result) == 2

    @pytest.mark.asyncio
    @allure.title("TC-DB-055: PostgreSQLAdapter execute_query() with psycopg")
    @allure.description(
        "Test PostgreSQLAdapter executes SELECT query using psycopg. TC-DB-055"
    )
    async def test_postgresql_execute_query_psycopg(
        self, valid_config, mocker, mock_db_cursor
    ):
        """Test PostgreSQLAdapter executes SELECT query using psycopg."""
        with allure.step("Create and connect PostgreSQLAdapter with psycopg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "psycopg"

        with allure.step("Mock cursor.execute() and cursor.fetchall()"):
            mock_cursor = mock_db_cursor
            mock_cursor.description = [("id",), ("name",)]
            mock_cursor.fetchall = AsyncMock(return_value=[(1, "Test"), (2, "Test2")])
            mock_connection.cursor = MagicMock(return_value=mock_cursor)

        with allure.step(
            "Call await adapter.execute_query('SELECT * FROM users WHERE id = :id', {'id': 1})"
        ):
            result = await adapter.execute_query(
                "SELECT * FROM users WHERE id = :id", {"id": 1}
            )

        with allure.step(
            "Verify cursor.execute() called with correct query and params"
        ):
            mock_cursor.execute.assert_called_once_with(
                "SELECT * FROM users WHERE id = :id", {"id": 1}
            )

        with allure.step("Verify returns list of dictionaries"):
            assert isinstance(result, list)
            assert len(result) == 2
            assert result[0]["id"] == 1
            assert result[0]["name"] == "Test"

    @pytest.mark.asyncio
    @allure.title(
        "TC-DB-056: PostgreSQLAdapter execute_query() with parameters (asyncpg)"
    )
    @allure.description(
        "Test PostgreSQLAdapter execute_query() handles parameters with asyncpg. TC-DB-056"
    )
    async def test_postgresql_execute_query_params_asyncpg(self, valid_config, mocker):
        """Test PostgreSQLAdapter execute_query() handles parameters with asyncpg."""
        with allure.step("Create and connect PostgreSQLAdapter with asyncpg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "asyncpg"

        with allure.step("Mock connection.fetch() to return mock rows"):
            mock_row1 = MagicMock()
            mock_row1.items = lambda: [("id", 1), ("name", "Test")]
            mock_connection.fetch = AsyncMock(return_value=[mock_row1])

        with allure.step("Call await adapter.execute_query() with multiple parameters"):
            result = await adapter.execute_query(
                "SELECT * FROM users WHERE id = $1 AND name = $2",
                {"id": 1, "name": "Test"},
            )

        with allure.step("Verify connection.fetch() called with positional parameters"):
            mock_connection.fetch.assert_called_once()
            call_args = mock_connection.fetch.call_args
            assert call_args[0][0] == "SELECT * FROM users WHERE id = $1 AND name = $2"
            # asyncpg uses positional parameters: *(params or {}).values()
            # So for {"id": 1, "name": "Test"}, it becomes (1, "Test")
            assert call_args[0][1:] == (1, "Test")

        with allure.step("Verify results returned correctly"):
            assert isinstance(result, list)
            assert len(result) == 1

    @pytest.mark.asyncio
    @allure.title(
        "TC-DB-057: PostgreSQLAdapter execute_query() with parameters (psycopg)"
    )
    @allure.description(
        "Test PostgreSQLAdapter execute_query() handles parameters with psycopg. TC-DB-057"
    )
    async def test_postgresql_execute_query_params_psycopg(
        self, valid_config, mocker, mock_db_cursor
    ):
        """Test PostgreSQLAdapter execute_query() handles parameters with psycopg."""
        with allure.step("Create and connect PostgreSQLAdapter with psycopg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "psycopg"

        with allure.step("Mock cursor.execute() and cursor.fetchall()"):
            mock_cursor = mock_db_cursor
            mock_cursor.description = [("id",), ("name",)]
            mock_cursor.fetchall = AsyncMock(return_value=[(1, "Test")])
            mock_connection.cursor = MagicMock(return_value=mock_cursor)

        with allure.step("Call await adapter.execute_query() with multiple parameters"):
            result = await adapter.execute_query(
                "SELECT * FROM users WHERE id = :id AND name = :name",
                {"id": 1, "name": "Test"},
            )

        with allure.step("Verify cursor.execute() called with named parameters"):
            mock_cursor.execute.assert_called_once_with(
                "SELECT * FROM users WHERE id = :id AND name = :name",
                {"id": 1, "name": "Test"},
            )

        with allure.step("Verify results returned correctly"):
            assert isinstance(result, list)
            assert len(result) == 1

    @pytest.mark.asyncio
    @allure.title(
        "TC-DB-058: PostgreSQLAdapter execute_query() with no results (asyncpg)"
    )
    @allure.description(
        "Test PostgreSQLAdapter execute_query() returns empty list with asyncpg. TC-DB-058"
    )
    async def test_postgresql_execute_query_no_results_asyncpg(
        self, valid_config, mocker
    ):
        """Test PostgreSQLAdapter execute_query() returns empty list with asyncpg."""
        with allure.step("Create and connect PostgreSQLAdapter with asyncpg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "asyncpg"

        with allure.step("Mock connection.fetch() to return empty list"):
            mock_connection.fetch = AsyncMock(return_value=[])

        with allure.step("Call await adapter.execute_query() with non-existent id"):
            result = await adapter.execute_query(
                "SELECT * FROM users WHERE id = $1", {"id": 999}
            )

        with allure.step("Verify returns empty list []"):
            assert isinstance(result, list)
            assert len(result) == 0

    @pytest.mark.asyncio
    @allure.title(
        "TC-DB-059: PostgreSQLAdapter execute_query() with no results (psycopg)"
    )
    @allure.description(
        "Test PostgreSQLAdapter execute_query() returns empty list with psycopg. TC-DB-059"
    )
    async def test_postgresql_execute_query_no_results_psycopg(
        self, valid_config, mocker, mock_db_cursor
    ):
        """Test PostgreSQLAdapter execute_query() returns empty list with psycopg."""
        with allure.step("Create and connect PostgreSQLAdapter with psycopg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "psycopg"

        with allure.step("Mock cursor.fetchall() to return empty list"):
            mock_cursor = mock_db_cursor
            mock_cursor.description = [("id",), ("name",)]
            mock_cursor.fetchall = AsyncMock(return_value=[])
            mock_connection.cursor = MagicMock(return_value=mock_cursor)

        with allure.step("Call await adapter.execute_query() with non-existent id"):
            result = await adapter.execute_query(
                "SELECT * FROM users WHERE id = :id", {"id": 999}
            )

        with allure.step("Verify returns empty list []"):
            assert isinstance(result, list)
            assert len(result) == 0

    @pytest.mark.asyncio
    @allure.title("TC-DB-060: PostgreSQLAdapter execute_command() INSERT with asyncpg")
    @allure.description(
        "Test PostgreSQLAdapter executes INSERT command using asyncpg. TC-DB-060"
    )
    async def test_postgresql_execute_command_insert_asyncpg(
        self, valid_config, mocker
    ):
        """Test PostgreSQLAdapter executes INSERT command using asyncpg."""
        with allure.step("Create and connect PostgreSQLAdapter with asyncpg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "asyncpg"

        with allure.step("Mock connection.execute() to return 'INSERT 0 1'"):
            mock_connection.execute = AsyncMock(return_value="INSERT 0 1")

        with allure.step("Call await adapter.execute_command()"):
            result = await adapter.execute_command(
                "INSERT INTO users (name) VALUES ($1)", {"name": "Test"}
            )

        with allure.step("Verify connection.execute() called with correct command"):
            mock_connection.execute.assert_called_once()
            call_args = mock_connection.execute.call_args
            assert call_args[0][0] == "INSERT INTO users (name) VALUES ($1)"
            # asyncpg uses positional parameters: *(params or {}).values()
            # So for {"name": "Test"}, it becomes ("Test",)
            assert call_args[0][1:] == ("Test",)
            # asyncpg uses positional parameters: *(params or {}).values()
            # So for {"name": "Test"}, it becomes ("Test",)
            assert call_args[0][1:] == ("Test",)

        with allure.step("Verify returns rowcount (1)"):
            assert result == 1

    @pytest.mark.asyncio
    @allure.title("TC-DB-061: PostgreSQLAdapter execute_command() INSERT with psycopg")
    @allure.description(
        "Test PostgreSQLAdapter executes INSERT command using psycopg. TC-DB-061"
    )
    async def test_postgresql_execute_command_insert_psycopg(
        self, valid_config, mocker, mock_db_cursor
    ):
        """Test PostgreSQLAdapter executes INSERT command using psycopg."""
        with allure.step("Create and connect PostgreSQLAdapter with psycopg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "psycopg"

        with allure.step("Mock cursor.execute() and cursor.rowcount"):
            mock_cursor = mock_db_cursor
            mock_cursor.rowcount = 1
            mock_connection.cursor = MagicMock(return_value=mock_cursor)

        with allure.step("Call await adapter.execute_command()"):
            result = await adapter.execute_command(
                "INSERT INTO users (name) VALUES (:name)", {"name": "Test"}
            )

        with allure.step("Verify cursor.execute() called with correct command"):
            mock_cursor.execute.assert_called_once_with(
                "INSERT INTO users (name) VALUES (:name)", {"name": "Test"}
            )

        with allure.step("Verify returns rowcount"):
            assert result == 1

    @pytest.mark.asyncio
    @allure.title("TC-DB-062: PostgreSQLAdapter execute_command() UPDATE with asyncpg")
    @allure.description(
        "Test PostgreSQLAdapter executes UPDATE command using asyncpg. TC-DB-062"
    )
    async def test_postgresql_execute_command_update_asyncpg(
        self, valid_config, mocker
    ):
        """Test PostgreSQLAdapter executes UPDATE command using asyncpg."""
        with allure.step("Create and connect PostgreSQLAdapter with asyncpg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "asyncpg"

        with allure.step("Mock connection.execute() to return 'UPDATE 2'"):
            mock_connection.execute = AsyncMock(return_value="UPDATE 2")

        with allure.step("Call await adapter.execute_command()"):
            result = await adapter.execute_command(
                "UPDATE users SET name = $1 WHERE id = $2",
                {"name": "Updated", "id": 1},
            )

        with allure.step("Verify returns rowcount (2)"):
            assert result == 2

    @pytest.mark.asyncio
    @allure.title("TC-DB-063: PostgreSQLAdapter execute_command() UPDATE with psycopg")
    @allure.description(
        "Test PostgreSQLAdapter executes UPDATE command using psycopg. TC-DB-063"
    )
    async def test_postgresql_execute_command_update_psycopg(
        self, valid_config, mocker, mock_db_cursor
    ):
        """Test PostgreSQLAdapter executes UPDATE command using psycopg."""
        with allure.step("Create and connect PostgreSQLAdapter with psycopg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "psycopg"

        with allure.step("Mock cursor.execute() and cursor.rowcount = 2"):
            mock_cursor = mock_db_cursor
            mock_cursor.rowcount = 2
            mock_connection.cursor = MagicMock(return_value=mock_cursor)

        with allure.step("Call await adapter.execute_command()"):
            result = await adapter.execute_command(
                "UPDATE users SET name = :name WHERE id = :id",
                {"name": "Updated", "id": 1},
            )

        with allure.step("Verify returns rowcount (2)"):
            assert result == 2

    @pytest.mark.asyncio
    @allure.title("TC-DB-064: PostgreSQLAdapter execute_command() DELETE with asyncpg")
    @allure.description(
        "Test PostgreSQLAdapter executes DELETE command using asyncpg. TC-DB-064"
    )
    async def test_postgresql_execute_command_delete_asyncpg(
        self, valid_config, mocker
    ):
        """Test PostgreSQLAdapter executes DELETE command using asyncpg."""
        with allure.step("Create and connect PostgreSQLAdapter with asyncpg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "asyncpg"

        with allure.step("Mock connection.execute() to return 'DELETE 1'"):
            mock_connection.execute = AsyncMock(return_value="DELETE 1")

        with allure.step("Call await adapter.execute_command()"):
            result = await adapter.execute_command(
                "DELETE FROM users WHERE id = $1", {"id": 1}
            )

        with allure.step("Verify returns rowcount (1)"):
            assert result == 1

    @pytest.mark.asyncio
    @allure.title("TC-DB-065: PostgreSQLAdapter execute_command() DELETE with psycopg")
    @allure.description(
        "Test PostgreSQLAdapter executes DELETE command using psycopg. TC-DB-065"
    )
    async def test_postgresql_execute_command_delete_psycopg(
        self, valid_config, mocker, mock_db_cursor
    ):
        """Test PostgreSQLAdapter executes DELETE command using psycopg."""
        with allure.step("Create and connect PostgreSQLAdapter with psycopg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "psycopg"

        with allure.step("Mock cursor.execute() and cursor.rowcount = 1"):
            mock_cursor = mock_db_cursor
            mock_cursor.rowcount = 1
            mock_connection.cursor = MagicMock(return_value=mock_cursor)

        with allure.step("Call await adapter.execute_command()"):
            result = await adapter.execute_command(
                "DELETE FROM users WHERE id = :id", {"id": 1}
            )

        with allure.step("Verify returns rowcount (1)"):
            assert result == 1

    @pytest.mark.asyncio
    @allure.title("TC-DB-066: PostgreSQLAdapter begin_transaction() with asyncpg")
    @allure.description(
        "Test PostgreSQLAdapter begins transaction with asyncpg. TC-DB-066"
    )
    async def test_postgresql_begin_transaction_asyncpg(self, valid_config, mocker):
        """Test PostgreSQLAdapter begins transaction with asyncpg."""
        with allure.step("Create and connect PostgreSQLAdapter with asyncpg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "asyncpg"

        with allure.step("Call await adapter.begin_transaction()"):
            # asyncpg handles transactions automatically, so no exception should be raised
            await adapter.begin_transaction()

        with allure.step("Verify no exception raised"):
            # Test passes if no exception
            assert True

    @pytest.mark.asyncio
    @allure.title("TC-DB-067: PostgreSQLAdapter begin_transaction() with psycopg")
    @allure.description(
        "Test PostgreSQLAdapter begins transaction with psycopg. TC-DB-067"
    )
    async def test_postgresql_begin_transaction_psycopg(self, valid_config, mocker):
        """Test PostgreSQLAdapter begins transaction with psycopg."""
        with allure.step("Create and connect PostgreSQLAdapter with psycopg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "psycopg"

        with allure.step("Mock connection.execute('BEGIN')"):
            mock_connection.execute = AsyncMock()

        with allure.step("Call await adapter.begin_transaction()"):
            await adapter.begin_transaction()

        with allure.step("Verify connection.execute('BEGIN') was called"):
            mock_connection.execute.assert_called_once_with("BEGIN")

    @pytest.mark.asyncio
    @allure.title("TC-DB-068: PostgreSQLAdapter commit_transaction() with asyncpg")
    @allure.description(
        "Test PostgreSQLAdapter commits transaction with asyncpg. TC-DB-068"
    )
    async def test_postgresql_commit_transaction_asyncpg(self, valid_config, mocker):
        """Test PostgreSQLAdapter commits transaction with asyncpg."""
        with allure.step("Create and connect PostgreSQLAdapter with asyncpg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "asyncpg"

        with allure.step("Begin transaction"):
            await adapter.begin_transaction()

        with allure.step("Call await adapter.commit_transaction()"):
            # asyncpg commits automatically, so no explicit commit needed
            await adapter.commit_transaction()

        with allure.step("Verify no exception raised"):
            # Test passes if no exception
            assert True

    @pytest.mark.asyncio
    @allure.title("TC-DB-069: PostgreSQLAdapter commit_transaction() with psycopg")
    @allure.description(
        "Test PostgreSQLAdapter commits transaction with psycopg. TC-DB-069"
    )
    async def test_postgresql_commit_transaction_psycopg(self, valid_config, mocker):
        """Test PostgreSQLAdapter commits transaction with psycopg."""
        with allure.step("Create and connect PostgreSQLAdapter with psycopg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "psycopg"

        with allure.step("Begin transaction"):
            await adapter.begin_transaction()

        with allure.step("Mock connection.commit()"):
            mock_connection.commit = AsyncMock()

        with allure.step("Call await adapter.commit_transaction()"):
            await adapter.commit_transaction()

        with allure.step("Verify connection.commit() was called"):
            mock_connection.commit.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("TC-DB-070: PostgreSQLAdapter rollback_transaction() with asyncpg")
    @allure.description(
        "Test PostgreSQLAdapter rolls back transaction with asyncpg. TC-DB-070"
    )
    async def test_postgresql_rollback_transaction_asyncpg(self, valid_config, mocker):
        """Test PostgreSQLAdapter rolls back transaction with asyncpg."""
        with allure.step("Create and connect PostgreSQLAdapter with asyncpg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "asyncpg"

        with allure.step("Begin transaction"):
            await adapter.begin_transaction()

        with allure.step("Call await adapter.rollback_transaction()"):
            # asyncpg doesn't have explicit rollback, so no-op
            await adapter.rollback_transaction()

        with allure.step("Verify no exception raised"):
            # Test passes if no exception
            assert True

    @pytest.mark.asyncio
    @allure.title("TC-DB-071: PostgreSQLAdapter rollback_transaction() with psycopg")
    @allure.description(
        "Test PostgreSQLAdapter rolls back transaction with psycopg. TC-DB-071"
    )
    async def test_postgresql_rollback_transaction_psycopg(self, valid_config, mocker):
        """Test PostgreSQLAdapter rolls back transaction with psycopg."""
        with allure.step("Create and connect PostgreSQLAdapter with psycopg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "psycopg"

        with allure.step("Begin transaction"):
            await adapter.begin_transaction()

        with allure.step("Mock connection.rollback()"):
            mock_connection.rollback = AsyncMock()

        with allure.step("Call await adapter.rollback_transaction()"):
            await adapter.rollback_transaction()

        with allure.step("Verify connection.rollback() was called"):
            mock_connection.rollback.assert_called_once()

    @pytest.mark.asyncio
    @allure.title(
        "TC-DB-072: PostgreSQLAdapter transaction() context manager with asyncpg"
    )
    @allure.description(
        "Test PostgreSQLAdapter transaction context manager with asyncpg. TC-DB-072"
    )
    async def test_postgresql_transaction_context_asyncpg(self, valid_config, mocker):
        """Test PostgreSQLAdapter transaction context manager with asyncpg."""
        with allure.step("Create and connect PostgreSQLAdapter with asyncpg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "asyncpg"

        with allure.step("Mock connection.execute()"):
            mock_connection.execute = AsyncMock(return_value="INSERT 0 1")

        with allure.step("Use async with adapter.transaction()"):
            async with adapter.transaction():
                await adapter.execute_command(
                    "INSERT INTO users (name) VALUES ($1)", {"name": "Test"}
                )

        with allure.step("Verify transaction commits on success"):
            # asyncpg commits automatically, so no explicit verification needed
            assert True

    @pytest.mark.asyncio
    @allure.title(
        "TC-DB-073: PostgreSQLAdapter transaction() context manager with psycopg"
    )
    @allure.description(
        "Test PostgreSQLAdapter transaction context manager with psycopg. TC-DB-073"
    )
    async def test_postgresql_transaction_context_psycopg(
        self, valid_config, mocker, mock_db_cursor
    ):
        """Test PostgreSQLAdapter transaction context manager with psycopg."""
        with allure.step("Create and connect PostgreSQLAdapter with psycopg"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "psycopg"

        with allure.step("Mock begin, commit, rollback"):
            mock_connection.execute = AsyncMock()  # BEGIN
            mock_connection.commit = AsyncMock()
            mock_connection.rollback = AsyncMock()

        with allure.step("Mock cursor for execute_command"):
            mock_cursor = mock_db_cursor
            mock_cursor.rowcount = 1
            mock_connection.cursor = MagicMock(return_value=mock_cursor)

        with allure.step("Use async with adapter.transaction()"):
            async with adapter.transaction():
                await adapter.execute_command(
                    "INSERT INTO users (name) VALUES (:name)", {"name": "Test"}
                )

        with allure.step("Verify BEGIN and COMMIT called"):
            mock_connection.execute.assert_called_with("BEGIN")
            mock_connection.commit.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("TC-DB-074: PostgreSQLAdapter execute_query() auto-connect")
    @allure.description(
        "Test PostgreSQLAdapter execute_query() auto-connects if not connected. TC-DB-074"
    )
    async def test_postgresql_execute_query_auto_connect(self, valid_config, mocker):
        """Test PostgreSQLAdapter execute_query() auto-connects if not connected."""
        with allure.step("Create PostgreSQLAdapter without connecting"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )

        with allure.step("Mock connect() and connection.fetch()"):
            mock_connect = mocker.patch.object(
                adapter, "connect", new_callable=AsyncMock
            )
            mock_connection = AsyncMock()
            mock_row = MagicMock()
            mock_row.items = lambda: [("id", 1)]
            mock_connection.fetch = AsyncMock(return_value=[mock_row])
            adapter._connection = mock_connection
            adapter._adapter_type = "asyncpg"

        with allure.step("Call await adapter.execute_query('SELECT 1')"):
            await adapter.execute_query("SELECT 1")

        with allure.step("Verify connect() was called automatically"):
            mock_connect.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("TC-DB-075: PostgreSQLAdapter execute_command() auto-connect")
    @allure.description(
        "Test PostgreSQLAdapter execute_command() auto-connects if not connected. TC-DB-075"
    )
    async def test_postgresql_execute_command_auto_connect(self, valid_config, mocker):
        """Test PostgreSQLAdapter execute_command() auto-connects if not connected."""
        with allure.step("Create PostgreSQLAdapter without connecting"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )

        with allure.step("Mock connect() and connection.execute()"):
            mock_connect = mocker.patch.object(
                adapter, "connect", new_callable=AsyncMock
            )
            mock_connection = AsyncMock()
            mock_connection.execute = AsyncMock(return_value="INSERT 0 1")
            adapter._connection = mock_connection
            adapter._adapter_type = "asyncpg"

        with allure.step(
            "Call await adapter.execute_command('INSERT INTO users VALUES (1)')"
        ):
            await adapter.execute_command("INSERT INTO users VALUES (1)")

        with allure.step("Verify connect() was called automatically"):
            mock_connect.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("TC-DB-076: PostgreSQLAdapter execute_query() with None params")
    @allure.description(
        "Test PostgreSQLAdapter execute_query() handles None params. TC-DB-076"
    )
    async def test_postgresql_execute_query_none_params(self, valid_config, mocker):
        """Test PostgreSQLAdapter execute_query() handles None params."""
        with allure.step("Create and connect PostgreSQLAdapter"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "asyncpg"

        with allure.step("Mock connection.fetch()"):
            mock_connection.fetch = AsyncMock(return_value=[])

        with allure.step("Call await adapter.execute_query('SELECT 1', params=None)"):
            result = await adapter.execute_query("SELECT 1", params=None)

        with allure.step("Verify works correctly with empty params"):
            assert isinstance(result, list)
            mock_connection.fetch.assert_called_once_with("SELECT 1")

    @pytest.mark.asyncio
    @allure.title("TC-DB-077: PostgreSQLAdapter execute_command() with None params")
    @allure.description(
        "Test PostgreSQLAdapter execute_command() handles None params. TC-DB-077"
    )
    async def test_postgresql_execute_command_none_params(self, valid_config, mocker):
        """Test PostgreSQLAdapter execute_command() handles None params."""
        with allure.step("Create and connect PostgreSQLAdapter"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "asyncpg"

        with allure.step("Mock connection.execute()"):
            mock_connection.execute = AsyncMock(return_value="SELECT 1")

        with allure.step("Call await adapter.execute_command('SELECT 1', params=None)"):
            await adapter.execute_command("SELECT 1", params=None)

        with allure.step("Verify works correctly with empty params"):
            mock_connection.execute.assert_called_once_with("SELECT 1")


# ============================================================================
# MySQLAdapter Functional Tests
# ============================================================================


class TestMySQLAdapterFunctional:
    """Test MySQLAdapter functional methods."""

    @pytest.mark.asyncio
    @allure.title(
        "TC-DB-078: MySQLAdapter connect() with aiomysql via connection_string"
    )
    @allure.description(
        "Test MySQLAdapter connects using aiomysql with connection_string. TC-DB-078"
    )
    async def test_mysql_connect_aiomysql_connection_string(
        self, valid_config, mocker, mock_aiomysql_module
    ):
        """Test MySQLAdapter connects using aiomysql with connection_string."""
        with allure.step("Create MySQLAdapter with connection_string"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )

        with allure.step("Mock aiomysql.connect() to return mock connection"):
            # Use fixture for mock aiomysql module
            mock_aiomysql_data = mock_aiomysql_module
            mock_connection = mock_aiomysql_data["connection"]

        with allure.step("Mock _detect_adapter to return 'aiomysql'"):
            mocker.patch.object(adapter, "_detect_adapter", return_value="aiomysql")

        with allure.step("Call await adapter.connect()"):
            await adapter.connect()

        with allure.step("Verify _adapter_type is 'aiomysql'"):
            assert adapter._adapter_type == "aiomysql"

        with allure.step("Verify _connection is set"):
            assert adapter._connection == mock_connection

    @pytest.mark.asyncio
    @allure.title("TC-DB-079: MySQLAdapter connect() with aiomysql via kwargs")
    @allure.description(
        "Test MySQLAdapter connects using aiomysql with kwargs. TC-DB-079"
    )
    async def test_mysql_connect_aiomysql_kwargs(
        self, valid_config, mocker, mock_aiomysql_module
    ):
        """Test MySQLAdapter connects using aiomysql with kwargs."""
        with allure.step("Create MySQLAdapter without connection_string, with kwargs"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                host="localhost",
                port=3306,
                database="testdb",
                user="testuser",
                password="testpass",
            )

        with allure.step("Mock aiomysql.connect() to return mock connection"):
            # Use fixture for mock aiomysql module
            mock_aiomysql_data = mock_aiomysql_module
            mock_connection = mock_aiomysql_data["connection"]
            mock_connect = mock_aiomysql_data["connect"]

        with allure.step("Mock _detect_adapter to return 'aiomysql'"):
            mocker.patch.object(adapter, "_detect_adapter", return_value="aiomysql")

        with allure.step("Call await adapter.connect()"):
            await adapter.connect()

        with allure.step("Verify aiomysql.connect() called with correct parameters"):
            mock_connect.assert_called_once_with(
                host="localhost",
                port=3306,
                db="testdb",
                user="testuser",
                password="testpass",
            )

        with allure.step("Verify _connection is set"):
            assert adapter._connection == mock_connection

    @pytest.mark.asyncio
    @allure.title("TC-DB-080: MySQLAdapter connect() with pymysql via kwargs")
    @allure.description(
        "Test MySQLAdapter connects using pymysql with kwargs. TC-DB-080"
    )
    async def test_mysql_connect_pymysql_kwargs(
        self, valid_config, mocker, mock_pymysql_module
    ):
        """Test MySQLAdapter connects using pymysql with kwargs."""
        with allure.step("Create MySQLAdapter without connection_string, with kwargs"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                host="localhost",
                port=3306,
                database="testdb",
                user="testuser",
                password="testpass",
            )

        with allure.step("Mock pymysql.connect() and asyncio.run_in_executor()"):
            # Use fixture for mock pymysql module
            mock_pymysql_data = mock_pymysql_module
            mock_connection = mock_pymysql_data["connection"]
            mock_pymysql_connect = mock_pymysql_data["connect"]

            # Mock run_in_executor to execute the lambda, which will call pymysql.connect
            mock_loop = MagicMock()

            async def mock_run_in_executor(executor, func):
                # Execute the lambda to trigger pymysql.connect call
                # The lambda captures pymysql from the local scope when import happens
                return func()

            mock_loop.run_in_executor = AsyncMock(side_effect=mock_run_in_executor)
            mocker.patch(
                "asyncio.get_event_loop",
                return_value=mock_loop,
            )

        with allure.step("Mock _detect_adapter to return 'pymysql'"):
            mocker.patch.object(adapter, "_detect_adapter", return_value="pymysql")

        with allure.step("Call await adapter.connect()"):
            await adapter.connect()

        with allure.step("Verify pymysql.connect() called with correct parameters"):
            mock_pymysql_connect.assert_called_once_with(
                host="localhost",
                port=3306,
                database="testdb",
                user="testuser",
                password="testpass",
            )

        with allure.step("Verify _connection is set"):
            assert adapter._connection == mock_connection

    @pytest.mark.asyncio
    @allure.title("TC-DB-081: MySQLAdapter disconnect() with aiomysql")
    @allure.description("Test MySQLAdapter disconnects using aiomysql. TC-DB-081")
    async def test_mysql_disconnect_aiomysql(self, valid_config, mocker):
        """Test MySQLAdapter disconnects using aiomysql."""
        with allure.step("Create and connect MySQLAdapter with aiomysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "aiomysql"

        with allure.step("Mock connection.close() and connection.ensure_closed()"):
            mock_connection.close = MagicMock()
            mock_connection.ensure_closed = AsyncMock()

        with allure.step("Call await adapter.disconnect()"):
            await adapter.disconnect()

        with allure.step("Verify connection.close() and ensure_closed() were called"):
            mock_connection.close.assert_called_once()
            mock_connection.ensure_closed.assert_called_once()

        with allure.step("Verify _connection is None"):
            assert adapter._connection is None

    @pytest.mark.asyncio
    @allure.title("TC-DB-082: MySQLAdapter disconnect() with pymysql")
    @allure.description("Test MySQLAdapter disconnects using pymysql. TC-DB-082")
    async def test_mysql_disconnect_pymysql(self, valid_config, mocker):
        """Test MySQLAdapter disconnects using pymysql."""
        with allure.step("Create and connect MySQLAdapter with pymysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = MagicMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "pymysql"

        with allure.step("Mock connection.close()"):
            mock_connection.close = MagicMock()

        with allure.step("Call await adapter.disconnect()"):
            await adapter.disconnect()

        with allure.step("Verify connection.close() was called"):
            mock_connection.close.assert_called_once()

        with allure.step("Verify _connection is None"):
            assert adapter._connection is None

    @pytest.mark.asyncio
    @allure.title(
        "TC-DB-083: MySQLAdapter connect() when already connected (idempotency)"
    )
    @allure.description("Test MySQLAdapter connect() is idempotent. TC-DB-083")
    async def test_mysql_connect_idempotent(self, valid_config, mocker):
        """Test MySQLAdapter connect() is idempotent."""
        with allure.step("Create and connect MySQLAdapter"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "aiomysql"

        with allure.step("Mock logger to verify debug message"):
            mock_logger = mocker.patch.object(adapter.logger, "debug")

        with allure.step("Call connect() again"):
            await adapter.connect()

        with allure.step("Verify no new connection is created"):
            assert adapter._connection == mock_connection

        with allure.step("Verify debug log 'Already connected'"):
            mock_logger.assert_called_once_with("Already connected to MySQL")

    @pytest.mark.asyncio
    @allure.title("TC-DB-084: MySQLAdapter execute_query() with aiomysql")
    @allure.description(
        "Test MySQLAdapter executes SELECT query using aiomysql. TC-DB-084"
    )
    async def test_mysql_execute_query_aiomysql(
        self, valid_config, mocker, mock_aiomysql_module, mock_db_cursor
    ):
        """Test MySQLAdapter executes SELECT query using aiomysql."""
        with allure.step("Create and connect MySQLAdapter with aiomysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "aiomysql"

        with allure.step("Mock cursor.execute() and cursor.fetchall()"):
            mock_cursor = mock_db_cursor
            mock_cursor.fetchall = AsyncMock(
                return_value=[{"id": 1, "name": "Test"}, {"id": 2, "name": "Test2"}]
            )
            # Use fixture for mock aiomysql module (DictCursor)
            mock_aiomysql_data = mock_aiomysql_module
            mocker.patch(
                "aiomysql.DictCursor",
                mock_aiomysql_data["DictCursor"],
            )
            mock_connection.cursor = MagicMock(return_value=mock_cursor)

        with allure.step(
            "Call await adapter.execute_query('SELECT * FROM users WHERE id = %s', {'id': 1})"
        ):
            result = await adapter.execute_query(
                "SELECT * FROM users WHERE id = %s", {"id": 1}
            )

        with allure.step(
            "Verify cursor.execute() called with correct query and parameters"
        ):
            mock_cursor.execute.assert_called_once()
            call_args = mock_cursor.execute.call_args
            assert call_args[0][0] == "SELECT * FROM users WHERE id = %s"
            # aiomysql uses positional parameters: list((params or {}).values())
            # So for {"id": 1}, it becomes [1]
            assert call_args[0][1] == [1]

        with allure.step("Verify returns list of dictionaries"):
            assert isinstance(result, list)
            assert len(result) == 2

    @pytest.mark.asyncio
    @allure.title("TC-DB-085: MySQLAdapter execute_query() with pymysql")
    @allure.description(
        "Test MySQLAdapter executes SELECT query using pymysql. TC-DB-085"
    )
    async def test_mysql_execute_query_pymysql(
        self, valid_config, mocker, mock_pymysql_module
    ):
        """Test MySQLAdapter executes SELECT query using pymysql."""
        with allure.step("Create and connect MySQLAdapter with pymysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = MagicMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "pymysql"

        with allure.step("Mock cursor.execute() and cursor.fetchall() via executor"):
            mock_cursor = MagicMock()
            mock_cursor.fetchall = MagicMock(
                return_value=[{"id": 1, "name": "Test"}, {"id": 2, "name": "Test2"}]
            )
            mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
            mock_cursor.__exit__ = MagicMock(return_value=None)
            mock_connection.cursor = MagicMock(return_value=mock_cursor)
            mock_loop = MagicMock()
            mock_loop.run_in_executor = AsyncMock(
                return_value=[{"id": 1, "name": "Test"}, {"id": 2, "name": "Test2"}]
            )
            mocker.patch(
                "asyncio.get_event_loop",
                return_value=mock_loop,
            )

        with allure.step(
            "Call await adapter.execute_query('SELECT * FROM users WHERE id = %s', {'id': 1})"
        ):
            result = await adapter.execute_query(
                "SELECT * FROM users WHERE id = %s", {"id": 1}
            )

        with allure.step(
            "Verify cursor.execute() called with correct query and parameters"
        ):
            # Verify executor was called
            mock_loop.run_in_executor.assert_called_once()

        with allure.step("Verify returns list of dictionaries"):
            assert isinstance(result, list)
            assert len(result) == 2

    @pytest.mark.asyncio
    @allure.title("TC-DB-086: MySQLAdapter execute_query() with parameters (aiomysql)")
    @allure.description(
        "Test MySQLAdapter execute_query() handles parameters with aiomysql. TC-DB-086"
    )
    async def test_mysql_execute_query_params_aiomysql(
        self, valid_config, mocker, mock_aiomysql_module, mock_db_cursor
    ):
        """Test MySQLAdapter execute_query() handles parameters with aiomysql."""
        with allure.step("Create and connect MySQLAdapter with aiomysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "aiomysql"

        with allure.step("Mock cursor.execute() and cursor.fetchall()"):
            mock_cursor = mock_db_cursor
            mock_cursor.fetchall = AsyncMock(return_value=[{"id": 1, "name": "Test"}])
            # Use fixture for mock aiomysql module (DictCursor)
            mock_aiomysql_data = mock_aiomysql_module
            mocker.patch(
                "aiomysql.DictCursor",
                mock_aiomysql_data["DictCursor"],
            )
            mock_connection.cursor = MagicMock(return_value=mock_cursor)

        with allure.step("Call await adapter.execute_query() with multiple parameters"):
            result = await adapter.execute_query(
                "SELECT * FROM users WHERE id = %s AND name = %s",
                {"id": 1, "name": "Test"},
            )

        with allure.step("Verify cursor.execute() called with positional parameters"):
            mock_cursor.execute.assert_called_once()
            call_args = mock_cursor.execute.call_args
            assert call_args[0][0] == "SELECT * FROM users WHERE id = %s AND name = %s"
            # aiomysql uses positional parameters: list((params or {}).values())
            # So for {"id": 1, "name": "Test"}, it becomes [1, "Test"]
            assert call_args[0][1] == [1, "Test"]

        with allure.step("Verify results returned correctly"):
            assert isinstance(result, list)
            assert len(result) == 1

    @pytest.mark.asyncio
    @allure.title("TC-DB-087: MySQLAdapter execute_query() with parameters (pymysql)")
    @allure.description(
        "Test MySQLAdapter execute_query() handles parameters with pymysql. TC-DB-087"
    )
    async def test_mysql_execute_query_params_pymysql(
        self, valid_config, mocker, mock_pymysql_module
    ):
        """Test MySQLAdapter execute_query() handles parameters with pymysql."""
        with allure.step("Create and connect MySQLAdapter with pymysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = MagicMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "pymysql"

        with allure.step("Mock cursor.execute() and cursor.fetchall() via executor"):
            mock_loop = MagicMock()
            mock_loop.run_in_executor = AsyncMock(
                return_value=[{"id": 1, "name": "Test"}]
            )
            mocker.patch(
                "asyncio.get_event_loop",
                return_value=mock_loop,
            )

        with allure.step("Call await adapter.execute_query() with multiple parameters"):
            result = await adapter.execute_query(
                "SELECT * FROM users WHERE id = %s AND name = %s",
                {"id": 1, "name": "Test"},
            )

        with allure.step("Verify executor was called"):
            mock_loop.run_in_executor.assert_called_once()

        with allure.step("Verify results returned correctly"):
            assert isinstance(result, list)
            assert len(result) == 1

    @pytest.mark.asyncio
    @allure.title("TC-DB-088: MySQLAdapter execute_query() with no results (aiomysql)")
    @allure.description(
        "Test MySQLAdapter execute_query() returns empty list with aiomysql. TC-DB-088"
    )
    async def test_mysql_execute_query_no_results_aiomysql(
        self, valid_config, mocker, mock_aiomysql_module, mock_db_cursor
    ):
        """Test MySQLAdapter execute_query() returns empty list with aiomysql."""
        with allure.step("Create and connect MySQLAdapter with aiomysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "aiomysql"

        with allure.step("Mock cursor.fetchall() to return empty list"):
            mock_cursor = mock_db_cursor
            mock_cursor.fetchall = AsyncMock(return_value=[])
            # Use fixture for mock aiomysql module (DictCursor)
            mock_aiomysql_data = mock_aiomysql_module
            mocker.patch(
                "aiomysql.DictCursor",
                mock_aiomysql_data["DictCursor"],
            )
            mock_connection.cursor = MagicMock(return_value=mock_cursor)

        with allure.step("Call await adapter.execute_query() with non-existent id"):
            result = await adapter.execute_query(
                "SELECT * FROM users WHERE id = %s", {"id": 999}
            )

        with allure.step("Verify returns empty list []"):
            assert isinstance(result, list)
            assert len(result) == 0

    @pytest.mark.asyncio
    @allure.title("TC-DB-089: MySQLAdapter execute_query() with no results (pymysql)")
    @allure.description(
        "Test MySQLAdapter execute_query() returns empty list with pymysql. TC-DB-089"
    )
    async def test_mysql_execute_query_no_results_pymysql(
        self, valid_config, mocker, mock_pymysql_module
    ):
        """Test MySQLAdapter execute_query() returns empty list with pymysql."""
        with allure.step("Create and connect MySQLAdapter with pymysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = MagicMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "pymysql"

        with allure.step("Mock cursor.fetchall() to return empty list via executor"):
            mock_loop = MagicMock()
            mock_loop.run_in_executor = AsyncMock(return_value=[])
            mocker.patch(
                "asyncio.get_event_loop",
                return_value=mock_loop,
            )

        with allure.step("Call await adapter.execute_query() with non-existent id"):
            result = await adapter.execute_query(
                "SELECT * FROM users WHERE id = %s", {"id": 999}
            )

        with allure.step("Verify returns empty list []"):
            assert isinstance(result, list)
            assert len(result) == 0

    @pytest.mark.asyncio
    @allure.title("TC-DB-090: MySQLAdapter execute_command() INSERT with aiomysql")
    @allure.description(
        "Test MySQLAdapter executes INSERT command using aiomysql. TC-DB-090"
    )
    async def test_mysql_execute_command_insert_aiomysql(
        self, valid_config, mocker, mock_aiomysql_module, mock_db_cursor
    ):
        """Test MySQLAdapter executes INSERT command using aiomysql."""
        with allure.step("Create and connect MySQLAdapter with aiomysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "aiomysql"

        with allure.step("Mock cursor.execute() and cursor.rowcount"):
            mock_cursor = mock_db_cursor
            mock_cursor.rowcount = 1
            mock_connection.cursor = MagicMock(return_value=mock_cursor)
            mock_connection.in_transaction = False
            mock_connection.commit = AsyncMock()

        with allure.step("Call await adapter.execute_command()"):
            result = await adapter.execute_command(
                "INSERT INTO users (name) VALUES (%s)", {"name": "Test"}
            )

        with allure.step("Verify cursor.execute() called with correct command"):
            mock_cursor.execute.assert_called_once()
            call_args = mock_cursor.execute.call_args
            assert call_args[0][0] == "INSERT INTO users (name) VALUES (%s)"
            # aiomysql uses positional parameters: list((params or {}).values())
            # So for {"name": "Test"}, it becomes ["Test"]
            assert call_args[0][1] == ["Test"]

        with allure.step("Verify connection.commit() called (not in transaction)"):
            mock_connection.commit.assert_called_once()

        with allure.step("Verify returns rowcount"):
            assert result == 1

    @pytest.mark.asyncio
    @allure.title("TC-DB-091: MySQLAdapter execute_command() INSERT with pymysql")
    @allure.description(
        "Test MySQLAdapter executes INSERT command using pymysql. TC-DB-091"
    )
    async def test_mysql_execute_command_insert_pymysql(
        self, valid_config, mocker, mock_pymysql_module
    ):
        """Test MySQLAdapter executes INSERT command using pymysql."""
        with allure.step("Create and connect MySQLAdapter with pymysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = MagicMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "pymysql"

        with allure.step("Mock pymysql module and cursor.execute()"):
            # Use fixture for mock pymysql module
            mock_pymysql_module  # Fixture already patches pymysql

            mock_cursor = MagicMock()
            mock_cursor.rowcount = 1
            mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
            mock_cursor.__exit__ = MagicMock(return_value=None)
            mock_connection.cursor = MagicMock(return_value=mock_cursor)
            mock_connection.commit = MagicMock()
            mock_loop = MagicMock()
            mock_loop.run_in_executor = AsyncMock(return_value=1)
            mocker.patch(
                "asyncio.get_event_loop",
                return_value=mock_loop,
            )

        with allure.step("Call await adapter.execute_command()"):
            result = await adapter.execute_command(
                "INSERT INTO users (name) VALUES (%s)", {"name": "Test"}
            )

        with allure.step("Verify executor was called"):
            mock_loop.run_in_executor.assert_called_once()

        with allure.step("Verify returns rowcount"):
            assert result == 1

    @pytest.mark.asyncio
    @allure.title("TC-DB-092: MySQLAdapter execute_command() UPDATE with aiomysql")
    @allure.description(
        "Test MySQLAdapter executes UPDATE command using aiomysql. TC-DB-092"
    )
    async def test_mysql_execute_command_update_aiomysql(
        self, valid_config, mocker, mock_aiomysql_module, mock_db_cursor
    ):
        """Test MySQLAdapter executes UPDATE command using aiomysql."""
        with allure.step("Create and connect MySQLAdapter with aiomysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "aiomysql"

        with allure.step("Mock cursor.execute() and cursor.rowcount = 2"):
            mock_cursor = mock_db_cursor
            mock_cursor.rowcount = 2
            mock_connection.cursor = MagicMock(return_value=mock_cursor)
            mock_connection.in_transaction = False

        with allure.step("Call await adapter.execute_command()"):
            result = await adapter.execute_command(
                "UPDATE users SET name = %s WHERE id = %s",
                {"name": "Updated", "id": 1},
            )

        with allure.step("Verify returns rowcount (2)"):
            assert result == 2

    @pytest.mark.asyncio
    @allure.title("TC-DB-093: MySQLAdapter execute_command() UPDATE with pymysql")
    @allure.description(
        "Test MySQLAdapter executes UPDATE command using pymysql. TC-DB-093"
    )
    async def test_mysql_execute_command_update_pymysql(
        self, valid_config, mocker, mock_pymysql_module
    ):
        """Test MySQLAdapter executes UPDATE command using pymysql."""
        with allure.step("Create and connect MySQLAdapter with pymysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = MagicMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "pymysql"

        with allure.step("Mock pymysql module and cursor.execute()"):
            # Use fixture for mock pymysql module
            mock_pymysql_module  # Fixture already patches pymysql

            mock_loop = MagicMock()
            mock_loop.run_in_executor = AsyncMock(return_value=2)
            mocker.patch(
                "asyncio.get_event_loop",
                return_value=mock_loop,
            )

        with allure.step("Call await adapter.execute_command()"):
            result = await adapter.execute_command(
                "UPDATE users SET name = %s WHERE id = %s",
                {"name": "Updated", "id": 1},
            )

        with allure.step("Verify returns rowcount (2)"):
            assert result == 2

    @pytest.mark.asyncio
    @allure.title("TC-DB-094: MySQLAdapter execute_command() DELETE with aiomysql")
    @allure.description(
        "Test MySQLAdapter executes DELETE command using aiomysql. TC-DB-094"
    )
    async def test_mysql_execute_command_delete_aiomysql(
        self, valid_config, mocker, mock_aiomysql_module, mock_db_cursor
    ):
        """Test MySQLAdapter executes DELETE command using aiomysql."""
        with allure.step("Create and connect MySQLAdapter with aiomysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "aiomysql"

        with allure.step("Mock cursor.execute() and cursor.rowcount = 1"):
            mock_cursor = mock_db_cursor
            mock_cursor.rowcount = 1
            mock_connection.cursor = MagicMock(return_value=mock_cursor)
            mock_connection.in_transaction = False

        with allure.step("Call await adapter.execute_command()"):
            result = await adapter.execute_command(
                "DELETE FROM users WHERE id = %s", {"id": 1}
            )

        with allure.step("Verify returns rowcount (1)"):
            assert result == 1

    @pytest.mark.asyncio
    @allure.title("TC-DB-095: MySQLAdapter execute_command() DELETE with pymysql")
    @allure.description(
        "Test MySQLAdapter executes DELETE command using pymysql. TC-DB-095"
    )
    async def test_mysql_execute_command_delete_pymysql(
        self, valid_config, mocker, mock_pymysql_module
    ):
        """Test MySQLAdapter executes DELETE command using pymysql."""
        with allure.step("Create and connect MySQLAdapter with pymysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = MagicMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "pymysql"

        with allure.step("Mock pymysql module and cursor.execute()"):
            # Use fixture for mock pymysql module
            mock_pymysql_module  # Fixture already patches pymysql

            mock_loop = MagicMock()
            mock_loop.run_in_executor = AsyncMock(return_value=1)
            mocker.patch(
                "asyncio.get_event_loop",
                return_value=mock_loop,
            )

        with allure.step("Call await adapter.execute_command()"):
            result = await adapter.execute_command(
                "DELETE FROM users WHERE id = %s", {"id": 1}
            )

        with allure.step("Verify returns rowcount (1)"):
            assert result == 1

    @pytest.mark.asyncio
    @allure.title("TC-DB-096: MySQLAdapter begin_transaction() with aiomysql")
    @allure.description("Test MySQLAdapter begins transaction with aiomysql. TC-DB-096")
    async def test_mysql_begin_transaction_aiomysql(self, valid_config, mocker):
        """Test MySQLAdapter begins transaction with aiomysql."""
        with allure.step("Create and connect MySQLAdapter with aiomysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "aiomysql"

        with allure.step("Mock connection.begin()"):
            mock_connection.begin = AsyncMock()

        with allure.step("Call await adapter.begin_transaction()"):
            await adapter.begin_transaction()

        with allure.step("Verify connection.begin() was called"):
            mock_connection.begin.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("TC-DB-097: MySQLAdapter begin_transaction() with pymysql")
    @allure.description("Test MySQLAdapter begins transaction with pymysql. TC-DB-097")
    async def test_mysql_begin_transaction_pymysql(
        self, valid_config, mocker, mock_pymysql_module
    ):
        """Test MySQLAdapter begins transaction with pymysql."""
        with allure.step("Create and connect MySQLAdapter with pymysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = MagicMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "pymysql"

        with allure.step("Call await adapter.begin_transaction()"):
            # pymysql autocommit is False by default, so no explicit begin needed
            await adapter.begin_transaction()

        with allure.step("Verify no exception raised"):
            # Test passes if no exception
            assert True

    @pytest.mark.asyncio
    @allure.title("TC-DB-098: MySQLAdapter commit_transaction() with aiomysql")
    @allure.description(
        "Test MySQLAdapter commits transaction with aiomysql. TC-DB-098"
    )
    async def test_mysql_commit_transaction_aiomysql(self, valid_config, mocker):
        """Test MySQLAdapter commits transaction with aiomysql."""
        with allure.step("Create and connect MySQLAdapter with aiomysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "aiomysql"

        with allure.step("Begin transaction"):
            await adapter.begin_transaction()

        with allure.step("Mock connection.commit()"):
            mock_connection.commit = AsyncMock()

        with allure.step("Call await adapter.commit_transaction()"):
            await adapter.commit_transaction()

        with allure.step("Verify connection.commit() was called"):
            mock_connection.commit.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("TC-DB-099: MySQLAdapter commit_transaction() with pymysql")
    @allure.description("Test MySQLAdapter commits transaction with pymysql. TC-DB-099")
    async def test_mysql_commit_transaction_pymysql(
        self, valid_config, mocker, mock_pymysql_module
    ):
        """Test MySQLAdapter commits transaction with pymysql."""
        with allure.step("Create and connect MySQLAdapter with pymysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = MagicMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "pymysql"

        with allure.step("Begin transaction"):
            await adapter.begin_transaction()

        with allure.step("Mock connection.commit()"):
            mock_connection.commit = MagicMock()

        with allure.step("Call await adapter.commit_transaction()"):
            await adapter.commit_transaction()

        with allure.step("Verify connection.commit() was called"):
            mock_connection.commit.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("TC-DB-100: MySQLAdapter rollback_transaction() with aiomysql")
    @allure.description(
        "Test MySQLAdapter rolls back transaction with aiomysql. TC-DB-100"
    )
    async def test_mysql_rollback_transaction_aiomysql(self, valid_config, mocker):
        """Test MySQLAdapter rolls back transaction with aiomysql."""
        with allure.step("Create and connect MySQLAdapter with aiomysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "aiomysql"

        with allure.step("Begin transaction"):
            await adapter.begin_transaction()

        with allure.step("Mock connection.rollback()"):
            mock_connection.rollback = AsyncMock()

        with allure.step("Call await adapter.rollback_transaction()"):
            await adapter.rollback_transaction()

        with allure.step("Verify connection.rollback() was called"):
            mock_connection.rollback.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("TC-DB-101: MySQLAdapter rollback_transaction() with pymysql")
    @allure.description(
        "Test MySQLAdapter rolls back transaction with pymysql. TC-DB-101"
    )
    async def test_mysql_rollback_transaction_pymysql(
        self, valid_config, mocker, mock_pymysql_module
    ):
        """Test MySQLAdapter rolls back transaction with pymysql."""
        with allure.step("Create and connect MySQLAdapter with pymysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = MagicMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "pymysql"

        with allure.step("Begin transaction"):
            await adapter.begin_transaction()

        with allure.step("Mock connection.rollback()"):
            mock_connection.rollback = MagicMock()

        with allure.step("Call await adapter.rollback_transaction()"):
            await adapter.rollback_transaction()

        with allure.step("Verify connection.rollback() was called"):
            mock_connection.rollback.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("TC-DB-102: MySQLAdapter transaction() context manager with aiomysql")
    @allure.description(
        "Test MySQLAdapter transaction context manager with aiomysql. TC-DB-102"
    )
    async def test_mysql_transaction_context_aiomysql(
        self, valid_config, mocker, mock_db_cursor
    ):
        """Test MySQLAdapter transaction context manager with aiomysql."""
        with allure.step("Create and connect MySQLAdapter with aiomysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "aiomysql"

        with allure.step("Mock begin, commit, rollback"):
            mock_connection.begin = AsyncMock()
            mock_connection.commit = AsyncMock()
            mock_connection.rollback = AsyncMock()

        with allure.step("Mock cursor for execute_command"):
            mock_cursor = mock_db_cursor
            mock_cursor.rowcount = 1
            mock_connection.cursor = MagicMock(return_value=mock_cursor)
            mock_connection.in_transaction = True

        with allure.step("Use async with adapter.transaction()"):
            async with adapter.transaction():
                await adapter.execute_command(
                    "INSERT INTO users (name) VALUES (%s)", {"name": "Test"}
                )

        with allure.step("Verify begin() and commit() called"):
            mock_connection.begin.assert_called_once()
            mock_connection.commit.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("TC-DB-103: MySQLAdapter transaction() context manager with pymysql")
    @allure.description(
        "Test MySQLAdapter transaction context manager with pymysql. TC-DB-103"
    )
    async def test_mysql_transaction_context_pymysql(
        self, valid_config, mocker, mock_pymysql_module
    ):
        """Test MySQLAdapter transaction context manager with pymysql."""
        with allure.step("Create and connect MySQLAdapter with pymysql"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = MagicMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "pymysql"

        with allure.step("Mock commit, rollback"):
            mock_connection.commit = MagicMock()
            mock_connection.rollback = MagicMock()

        with allure.step("Mock pymysql module and cursor for execute_command"):
            # Use fixture for mock pymysql module
            mock_pymysql_module  # Fixture already patches pymysql

            mock_loop = MagicMock()
            mock_loop.run_in_executor = AsyncMock(return_value=1)
            mocker.patch(
                "asyncio.get_event_loop",
                return_value=mock_loop,
            )

        with allure.step("Use async with adapter.transaction()"):
            async with adapter.transaction():
                await adapter.execute_command(
                    "INSERT INTO users (name) VALUES (%s)", {"name": "Test"}
                )

        with allure.step("Verify commit() called on success"):
            mock_connection.commit.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("TC-DB-104: MySQLAdapter execute_query() auto-connect")
    @allure.description(
        "Test MySQLAdapter execute_query() auto-connects if not connected. TC-DB-104"
    )
    async def test_mysql_execute_query_auto_connect(
        self, valid_config, mocker, mock_aiomysql_module, mock_db_cursor
    ):
        """Test MySQLAdapter execute_query() auto-connects if not connected."""
        with allure.step("Create MySQLAdapter without connecting"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )

        with allure.step("Mock connect() and cursor operations"):
            mock_connect = mocker.patch.object(
                adapter, "connect", new_callable=AsyncMock
            )
            mock_connection = AsyncMock()
            mock_cursor = mock_db_cursor
            mock_cursor.fetchall = AsyncMock(return_value=[])
            # Use fixture for mock aiomysql module (DictCursor)
            mock_aiomysql_data = mock_aiomysql_module
            mocker.patch(
                "aiomysql.DictCursor",
                mock_aiomysql_data["DictCursor"],
            )
            mock_connection.cursor = MagicMock(return_value=mock_cursor)
            adapter._connection = mock_connection
            adapter._adapter_type = "aiomysql"

        with allure.step("Call await adapter.execute_query('SELECT 1')"):
            await adapter.execute_query("SELECT 1")

        with allure.step("Verify connect() was called automatically"):
            mock_connect.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("TC-DB-105: MySQLAdapter execute_command() auto-connect")
    @allure.description(
        "Test MySQLAdapter execute_command() auto-connects if not connected. TC-DB-105"
    )
    async def test_mysql_execute_command_auto_connect(
        self, valid_config, mocker, mock_aiomysql_module, mock_db_cursor
    ):
        """Test MySQLAdapter execute_command() auto-connects if not connected."""
        with allure.step("Create MySQLAdapter without connecting"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )

        with allure.step("Mock connect() and cursor operations"):
            mock_connect = mocker.patch.object(
                adapter, "connect", new_callable=AsyncMock
            )
            mock_connection = AsyncMock()
            mock_cursor = mock_db_cursor
            mock_cursor.rowcount = 1
            mock_connection.cursor = MagicMock(return_value=mock_cursor)
            mock_connection.in_transaction = False
            mock_connection.commit = AsyncMock()
            adapter._connection = mock_connection
            adapter._adapter_type = "aiomysql"

        with allure.step(
            "Call await adapter.execute_command('INSERT INTO users VALUES (1)')"
        ):
            await adapter.execute_command("INSERT INTO users VALUES (1)")

        with allure.step("Verify connect() was called automatically"):
            mock_connect.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("TC-DB-106: MySQLAdapter execute_query() with None params")
    @allure.description(
        "Test MySQLAdapter execute_query() handles None params. TC-DB-106"
    )
    async def test_mysql_execute_query_none_params(
        self, valid_config, mocker, mock_aiomysql_module, mock_db_cursor
    ):
        """Test MySQLAdapter execute_query() handles None params."""
        with allure.step("Create and connect MySQLAdapter"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "aiomysql"

        with allure.step("Mock cursor operations"):
            mock_cursor = mock_db_cursor
            mock_cursor.fetchall = AsyncMock(return_value=[])
            # Use fixture for mock aiomysql module (DictCursor)
            mock_aiomysql_data = mock_aiomysql_module
            mocker.patch(
                "aiomysql.DictCursor",
                mock_aiomysql_data["DictCursor"],
            )
            mock_connection.cursor = MagicMock(return_value=mock_cursor)

        with allure.step("Call await adapter.execute_query('SELECT 1', params=None)"):
            result = await adapter.execute_query("SELECT 1", params=None)

        with allure.step("Verify works correctly with empty params"):
            assert isinstance(result, list)
            mock_cursor.execute.assert_called_once_with("SELECT 1", [])

    @pytest.mark.asyncio
    @allure.title("TC-DB-107: MySQLAdapter execute_command() with None params")
    @allure.description(
        "Test MySQLAdapter execute_command() handles None params. TC-DB-107"
    )
    async def test_mysql_execute_command_none_params(
        self, valid_config, mocker, mock_aiomysql_module, mock_db_cursor
    ):
        """Test MySQLAdapter execute_command() handles None params."""
        with allure.step("Create and connect MySQLAdapter"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "aiomysql"

        with allure.step("Mock cursor operations"):
            mock_cursor = mock_db_cursor
            mock_cursor.rowcount = 0
            mock_connection.cursor = MagicMock(return_value=mock_cursor)
            mock_connection.in_transaction = False
            mock_connection.commit = AsyncMock()

        with allure.step("Call await adapter.execute_command('SELECT 1', params=None)"):
            await adapter.execute_command("SELECT 1", params=None)

        with allure.step("Verify works correctly with empty params"):
            mock_cursor.execute.assert_called_once_with("SELECT 1", [])

    @pytest.mark.asyncio
    @allure.title(
        "TC-DB-108: MySQLAdapter execute_command() in transaction (doesn't auto-commit)"
    )
    @allure.description(
        "Test MySQLAdapter execute_command() doesn't auto-commit in transaction. TC-DB-108"
    )
    async def test_mysql_execute_command_in_transaction(
        self, valid_config, mocker, mock_db_cursor
    ):
        """Test MySQLAdapter execute_command() doesn't auto-commit in transaction."""
        with allure.step(
            "Create and connect MySQLAdapter with transaction in progress"
        ):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._adapter_type = "aiomysql"

        with allure.step("Begin transaction"):
            await adapter.begin_transaction()

        with allure.step("Mock connection.in_transaction = True (aiomysql)"):
            mock_connection.in_transaction = True

        with allure.step("Mock cursor.execute()"):
            mock_cursor = mock_db_cursor
            mock_cursor.rowcount = 1
            mock_connection.cursor = MagicMock(return_value=mock_cursor)
            mock_connection.commit = AsyncMock()

        with allure.step("Call await adapter.execute_command()"):
            await adapter.execute_command(
                "INSERT INTO users (name) VALUES (%s)", {"name": "Test"}
            )

        with allure.step("Verify connection.commit() was NOT called (in transaction)"):
            mock_connection.commit.assert_not_called()

    @pytest.mark.asyncio
    @allure.title(
        "TC-DB-109: MySQLAdapter _detect_adapter() when neither aiomysql nor pymysql available"
    )
    @allure.description(
        "Test MySQLAdapter _detect_adapter() raises ImportError when neither library is available. TC-DB-109"
    )
    async def test_mysql_detect_adapter_no_libraries(self, valid_config, mocker):
        """Test MySQLAdapter _detect_adapter() raises ImportError when neither library is available."""
        with allure.step("Create MySQLAdapter instance"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )

        with allure.step("Mock both aiomysql and pymysql imports to raise ImportError"):
            original_import = builtins.__import__

            def mock_import(name, *args, **kwargs):
                if name == "aiomysql" or name == "pymysql":
                    raise ImportError(f"No module named '{name}'")
                return original_import(name, *args, **kwargs)

            mocker.patch("builtins.__import__", side_effect=mock_import)

        with allure.step("Call adapter._detect_adapter()"):
            with pytest.raises(ImportError) as exc_info:
                adapter._detect_adapter()

        with allure.step("Verify ImportError is raised with appropriate message"):
            assert (
                "MySQL adapter requires either 'aiomysql' or 'pymysql' library"
                in str(exc_info.value)
            )

    @pytest.mark.asyncio
    @allure.title(
        "TC-DB-110: MySQLAdapter begin_transaction() auto-connect for pymysql"
    )
    @allure.description(
        "Test MySQLAdapter begin_transaction() automatically connects when not connected (pymysql). TC-DB-110"
    )
    async def test_mysql_begin_transaction_auto_connect_pymysql(
        self, valid_config, mocker, mock_pymysql_module
    ):
        """Test MySQLAdapter begin_transaction() automatically connects when not connected (pymysql)."""
        with allure.step("Create MySQLAdapter with pymysql (not connected)"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            adapter._is_connected = False
            adapter._adapter_type = "pymysql"

        with allure.step("Mock connect() method"):
            mock_connect = mocker.AsyncMock()

            async def connect_side_effect():
                adapter._is_connected = True
                mock_conn = mocker.AsyncMock()
                if adapter._adapter_type == "aiomysql":
                    mock_conn.begin = mocker.AsyncMock()
                adapter._connection = mock_conn

            mock_connect.side_effect = connect_side_effect
            mocker.patch.object(adapter, "connect", mock_connect)

        with allure.step("Call await adapter.begin_transaction()"):
            await adapter.begin_transaction()

        with allure.step("Verify connect() was called before beginning transaction"):
            mock_connect.assert_called_once()

    @pytest.mark.asyncio
    @allure.title(
        "TC-DB-111: MySQLAdapter begin_transaction() auto-connect for aiomysql"
    )
    @allure.description(
        "Test MySQLAdapter begin_transaction() automatically connects when not connected (aiomysql). TC-DB-111"
    )
    async def test_mysql_begin_transaction_auto_connect_aiomysql(
        self, valid_config, mocker, mock_aiomysql_module
    ):
        """Test MySQLAdapter begin_transaction() automatically connects when not connected (aiomysql)."""
        with allure.step("Create MySQLAdapter with aiomysql (not connected)"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )
            adapter._is_connected = False
            adapter._adapter_type = "aiomysql"

        with allure.step("Mock connect() method"):
            mock_connect = mocker.AsyncMock()

            async def connect_side_effect():
                adapter._is_connected = True
                mock_conn = mocker.AsyncMock()
                if adapter._adapter_type == "aiomysql":
                    mock_conn.begin = mocker.AsyncMock()
                adapter._connection = mock_conn

            mock_connect.side_effect = connect_side_effect
            mocker.patch.object(adapter, "connect", mock_connect)

        with allure.step("Call await adapter.begin_transaction()"):
            await adapter.begin_transaction()

        with allure.step("Verify connect() was called before beginning transaction"):
            mock_connect.assert_called_once()

    @pytest.mark.asyncio
    @allure.title(
        "TC-DB-112: PostgreSQLAdapter _detect_adapter() when neither asyncpg nor psycopg available"
    )
    @allure.description(
        "Test PostgreSQLAdapter _detect_adapter() raises ImportError when neither library is available. TC-DB-112"
    )
    async def test_postgresql_detect_adapter_no_libraries(self, valid_config, mocker):
        """Test PostgreSQLAdapter _detect_adapter() raises ImportError when neither library is available."""
        with allure.step("Create PostgreSQLAdapter instance"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )

        with allure.step("Mock both asyncpg and psycopg imports to raise ImportError"):
            original_import = builtins.__import__

            def mock_import(name, *args, **kwargs):
                if name == "asyncpg" or name == "psycopg":
                    raise ImportError(f"No module named '{name}'")
                return original_import(name, *args, **kwargs)

            mocker.patch("builtins.__import__", side_effect=mock_import)

        with allure.step("Call adapter._detect_adapter()"):
            with pytest.raises(ImportError) as exc_info:
                adapter._detect_adapter()

        with allure.step("Verify ImportError is raised with appropriate message"):
            assert (
                "PostgreSQL adapter requires either 'asyncpg' or 'psycopg' library"
                in str(exc_info.value)
            )

    @pytest.mark.asyncio
    @allure.title(
        "TC-DB-113: PostgreSQLAdapter begin_transaction() auto-connect for asyncpg"
    )
    @allure.description(
        "Test PostgreSQLAdapter begin_transaction() automatically connects when not connected (asyncpg). TC-DB-113"
    )
    async def test_postgresql_begin_transaction_auto_connect_asyncpg(
        self, valid_config, mocker
    ):
        """Test PostgreSQLAdapter begin_transaction() automatically connects when not connected (asyncpg)."""
        with allure.step("Create PostgreSQLAdapter with asyncpg (not connected)"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            adapter._is_connected = False
            adapter._adapter_type = "asyncpg"

        with allure.step("Mock connect() method"):
            mock_connect = mocker.AsyncMock()

            async def connect_side_effect():
                adapter._is_connected = True
                mock_conn = mocker.AsyncMock()
                adapter._connection = mock_conn

            mock_connect.side_effect = connect_side_effect
            mocker.patch.object(adapter, "connect", mock_connect)

        with allure.step("Call await adapter.begin_transaction()"):
            await adapter.begin_transaction()

        with allure.step("Verify connect() was called before beginning transaction"):
            mock_connect.assert_called_once()

    @pytest.mark.asyncio
    @allure.title(
        "TC-DB-114: PostgreSQLAdapter begin_transaction() auto-connect for psycopg"
    )
    @allure.description(
        "Test PostgreSQLAdapter begin_transaction() automatically connects when not connected (psycopg). TC-DB-114"
    )
    async def test_postgresql_begin_transaction_auto_connect_psycopg(
        self, valid_config, mocker
    ):
        """Test PostgreSQLAdapter begin_transaction() automatically connects when not connected (psycopg)."""
        with allure.step("Create PostgreSQLAdapter with psycopg (not connected)"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )
            adapter._is_connected = False
            adapter._adapter_type = "psycopg"

        with allure.step("Mock connect() method"):
            mock_connect = mocker.AsyncMock()

            async def connect_side_effect():
                adapter._is_connected = True
                mock_conn = mocker.AsyncMock()
                mock_conn.execute = mocker.AsyncMock()
                adapter._connection = mock_conn

            mock_connect.side_effect = connect_side_effect
            mocker.patch.object(adapter, "connect", mock_connect)

        with allure.step("Call await adapter.begin_transaction()"):
            await adapter.begin_transaction()

        with allure.step("Verify connect() was called before beginning transaction"):
            mock_connect.assert_called_once()
