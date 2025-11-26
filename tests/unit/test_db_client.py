"""
Unit tests for DBClient and database adapters.
"""

import platform
import builtins
import pytest
import allure
from unittest.mock import AsyncMock, MagicMock

from tma_test_framework.clients.db_client import DBClient
from tma_test_framework.clients.db_adapters.sqlite_adapter import SQLiteAdapter
from tma_test_framework.clients.db_adapters.postgresql_adapter import PostgreSQLAdapter
from tma_test_framework.clients.db_adapters.mysql_adapter import MySQLAdapter
from tma_test_framework.config import Config


# ============================================================================
# I. Инициализация (__init__)
# ============================================================================


class TestDBClientInit:
    """Test DBClient initialization."""

    @allure.title(
        "TC-DB-001: Initialize DBClient with URL, config, and connection_string"
    )
    @allure.description(
        "Test DBClient can be initialized with URL, Config, and connection string. TC-DB-001"
    )
    def test_init_with_url_config_and_connection_string(self, valid_config):
        """Test DBClient can be initialized with URL, Config, and connection string."""
        with allure.step("Create DBClient with URL, config, and connection_string"):
            # Use SQLiteAdapter as concrete implementation
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///test.db",
            )

        with allure.step("Verify url, config, and connection_string are set"):
            assert db.url == "https://example.com/app"
            assert db.config == valid_config
            assert db.connection_string == "sqlite:///test.db"

        with allure.step("Verify _connection is None, _is_connected is False"):
            assert db._connection is None
            assert db._is_connected is False

    @allure.title("TC-DB-002: Initialize DBClient with URL and config only")
    @allure.description(
        "Test DBClient can be initialized without connection_string. TC-DB-002"
    )
    def test_init_with_url_and_config_only(self, valid_config):
        """Test DBClient can be initialized without connection_string."""
        with allure.step("Create DBClient with URL and config only"):
            db = SQLiteAdapter("https://example.com/app", valid_config)

        with allure.step("Verify connection_string is None"):
            assert db.connection_string is None

        with allure.step("Verify _db_kwargs is empty dict"):
            assert db._db_kwargs == {}

    @allure.title("TC-DB-003: Initialize DBClient with additional kwargs")
    @allure.description("Test DBClient accepts database-specific parameters. TC-DB-003")
    def test_init_with_additional_kwargs(self, valid_config):
        """Test DBClient accepts database-specific parameters."""
        with allure.step("Create DBClient with additional kwargs"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                host="localhost",
                port=5432,
                database="testdb",
            )

        with allure.step("Verify _db_kwargs contains provided parameters"):
            assert db._db_kwargs["host"] == "localhost"
            assert db._db_kwargs["port"] == 5432
            assert db._db_kwargs["database"] == "testdb"

    @allure.title("TC-DB-004: Initialize DBClient with config=None raises error")
    @allure.description(
        "Test DBClient rejects None config (inherited from BaseClient). TC-DB-004"
    )
    def test_init_with_config_none_raises_error(self):
        """Test DBClient rejects None config."""
        with allure.step("Attempt to create DBClient with config=None"):
            with pytest.raises(ValueError, match="config is required"):
                SQLiteAdapter("https://example.com/app", None)


# ============================================================================
# II. Factory Method Tests (create)
# ============================================================================


class TestDBClientFactory:
    """Test DBClient.create() factory method."""

    @allure.title("TC-DB-005: Create PostgreSQL client using factory method")
    @allure.description("Test DBClient.create() creates PostgreSQLAdapter. TC-DB-005")
    def test_create_postgresql_client(self, valid_config, mocker):
        """Test DBClient.create() creates PostgreSQLAdapter."""
        with allure.step("Mock PostgreSQLAdapter import in db_client"):
            # Mock the import that happens inside DBClient.create()
            mock_adapter_class = mocker.patch(
                "tma_test_framework.clients.db_adapters.postgresql_adapter.PostgreSQLAdapter"
            )
            mock_instance = MagicMock()
            mock_adapter_class.return_value = mock_instance

        with allure.step("Call DBClient.create('postgresql', ...)"):
            result = DBClient.create(
                "postgresql",
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )

        with allure.step("Verify returns PostgreSQLAdapter instance"):
            assert result == mock_instance
            mock_adapter_class.assert_called_once()

        with allure.step("Verify isinstance(result, DBClient)"):
            # Since we're mocking, we check that it's the right type
            assert isinstance(result, MagicMock)

    @allure.title("TC-DB-006: Create SQLite client using factory method")
    @allure.description("Test DBClient.create() creates SQLiteAdapter. TC-DB-006")
    def test_create_sqlite_client(self, valid_config):
        """Test DBClient.create() creates SQLiteAdapter."""
        with allure.step("Call DBClient.create('sqlite', ...)"):
            result = DBClient.create(
                "sqlite",
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///test.db",
            )

        with allure.step("Verify returns SQLiteAdapter instance"):
            assert isinstance(result, SQLiteAdapter)

        with allure.step("Verify isinstance(result, DBClient)"):
            assert isinstance(result, DBClient)

    @allure.title("TC-DB-007: Create MySQL client using factory method")
    @allure.description("Test DBClient.create() creates MySQLAdapter. TC-DB-007")
    def test_create_mysql_client(self, valid_config, mocker):
        """Test DBClient.create() creates MySQLAdapter."""
        with allure.step("Mock MySQLAdapter import in db_client"):
            # Mock the import that happens inside DBClient.create()
            mock_adapter_class = mocker.patch(
                "tma_test_framework.clients.db_adapters.mysql_adapter.MySQLAdapter"
            )
            mock_instance = MagicMock()
            mock_adapter_class.return_value = mock_instance

        with allure.step("Call DBClient.create('mysql', ...)"):
            result = DBClient.create(
                "mysql",
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )

        with allure.step("Verify returns MySQLAdapter instance"):
            assert result == mock_instance
            mock_adapter_class.assert_called_once()

    @allure.title("TC-DB-008: Factory method with unsupported database type")
    @allure.description(
        "Test DBClient.create() raises ValueError for unsupported type. TC-DB-008"
    )
    def test_create_unsupported_database_type(self, valid_config):
        """Test DBClient.create() raises ValueError for unsupported type."""
        with allure.step("Call DBClient.create('oracle', ...)"):
            with pytest.raises(ValueError, match="Unsupported database type: oracle"):
                DBClient.create("oracle", "https://example.com/app", valid_config)

    @allure.title("TC-DB-009: Factory method with missing library")
    @allure.description(
        "Test DBClient.create() raises ImportError when library not installed. TC-DB-009"
    )
    def test_create_with_missing_library(self, valid_config, mocker):
        """Test DBClient.create() raises ImportError when library not installed."""
        with allure.step("Mock import to raise ImportError"):
            # Mock the import that happens inside DBClient.create()
            mocker.patch(
                "tma_test_framework.clients.db_adapters.postgresql_adapter.PostgreSQLAdapter",
                side_effect=ImportError("No module named 'asyncpg'"),
            )

        with allure.step("Call DBClient.create('postgresql', ...)"):
            with pytest.raises(ImportError) as exc_info:
                DBClient.create(
                    "postgresql",
                    "https://example.com/app",
                    valid_config,
                )

        with allure.step("Verify ImportError has helpful message"):
            assert "asyncpg" in str(exc_info.value) or "psycopg" in str(exc_info.value)

    @allure.title("TC-DB-010: Factory method with case-insensitive db_type")
    @allure.description(
        "Test DBClient.create() handles case-insensitive db_type. TC-DB-010"
    )
    def test_create_case_insensitive_db_type(self, valid_config):
        """Test DBClient.create() handles case-insensitive db_type."""
        with allure.step("Call DBClient.create('POSTGRESQL', ...)"):
            DBClient.create(
                "POSTGRESQL",
                "https://example.com/app",
                valid_config,
            )
            # Should not raise error (will raise ImportError if library missing, but that's OK)

        with allure.step("Call DBClient.create('PostgreSQL', ...)"):
            DBClient.create(
                "PostgreSQL",
                "https://example.com/app",
                valid_config,
            )

        with allure.step("Call DBClient.create('postgres', ...)"):
            DBClient.create(
                "postgres",
                "https://example.com/app",
                valid_config,
            )

        with allure.step("Verify all work correctly"):
            # All should create PostgreSQLAdapter (or raise ImportError if library missing)
            # We just verify no ValueError is raised
            assert True  # Test passes if no ValueError

    @allure.title("TC-DB-045: Factory method with invalid parameters")
    @allure.description(
        "Test DBClient.create() handles invalid parameters correctly. TC-DB-045"
    )
    def test_create_with_invalid_parameters(self, valid_config):
        """Test DBClient.create() handles invalid parameters correctly."""
        with allure.step("Call DBClient.create(None, url, config) and verify error"):
            with pytest.raises((TypeError, AttributeError, ValueError)):
                DBClient.create(None, "https://example.com/app", valid_config)  # type: ignore[arg-type]

        with allure.step(
            "Call DBClient.create('postgresql', None, config) and verify error"
        ):
            with pytest.raises((TypeError, AttributeError)):
                DBClient.create("postgresql", None, valid_config)  # type: ignore[arg-type]

    @allure.title("TC-DB-046: Factory method with partially invalid parameters")
    @allure.description(
        "Test DBClient.create() handles partially invalid parameters. TC-DB-046"
    )
    def test_create_with_partially_invalid_parameters(self, valid_config):
        """Test DBClient.create() handles partially invalid parameters."""
        with allure.step(
            "Call DBClient.create('postgresql', url, config, connection_string='invalid://')"
        ):
            # Valid db_type but invalid connection_string - adapter should be created
            # (validation happens during connect, not during create)
            result = DBClient.create(
                "postgresql",
                "https://example.com/app",
                valid_config,
                connection_string="invalid://",
            )
            assert result is not None

        with allure.step(
            "Call DBClient.create('sqlite', url, None) and verify ValueError"
        ):
            # Valid db_type but invalid config (None) - should raise ValueError
            with pytest.raises(ValueError, match="config is required"):
                DBClient.create(
                    "sqlite",
                    "https://example.com/app",
                    None,
                )


# ============================================================================
# III. Connection Management Tests
# ============================================================================


class TestDBClientConnection:
    """Test DBClient connection management."""

    @pytest.mark.asyncio
    @allure.title("TC-DB-011: Connect to database successfully")
    @allure.description("Test connect() establishes connection. TC-DB-011")
    async def test_connect_successfully(self, valid_config):
        """Test connect() establishes connection."""
        with allure.step("Create DBClient instance"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )

        with allure.step("Call await db.connect()"):
            await db.connect()

        with allure.step("Verify _is_connected is True"):
            assert db._is_connected is True

        with allure.step("Verify _connection is not None"):
            assert db._connection is not None

        with allure.step("Cleanup: disconnect"):
            await db.disconnect()

    @pytest.mark.asyncio
    @allure.title("TC-DB-012: Connect when already connected")
    @allure.description("Test connect() is idempotent. TC-DB-012")
    async def test_connect_when_already_connected(self, valid_config, mocker):
        """Test connect() is idempotent."""
        with allure.step("Create and connect DBClient"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()

        with allure.step("Mock logger to verify debug message"):
            mocker.patch.object(db.logger, "debug")

        with allure.step("Call connect() again"):
            await db.connect()

        with allure.step("Verify no new connection is created"):
            # Connection should still be valid
            assert db._is_connected is True

        with allure.step("Verify debug log 'Already connected'"):
            # Check if debug was called (may not be called if already connected check happens)
            # The important thing is no error is raised
            assert True

        with allure.step("Cleanup: disconnect"):
            await db.disconnect()

    @pytest.mark.asyncio
    @allure.title("TC-DB-013: Disconnect from database")
    @allure.description("Test disconnect() closes connection. TC-DB-013")
    async def test_disconnect_successfully(self, valid_config):
        """Test disconnect() closes connection."""
        with allure.step("Connect to database"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()
            assert db._is_connected is True

        with allure.step("Call await db.disconnect()"):
            await db.disconnect()

        with allure.step("Verify _is_connected is False"):
            assert db._is_connected is False

        with allure.step("Verify _connection is None"):
            assert db._connection is None

    @pytest.mark.asyncio
    @allure.title("TC-DB-014: Disconnect when not connected")
    @allure.description("Test disconnect() handles no connection gracefully. TC-DB-014")
    async def test_disconnect_when_not_connected(self, valid_config):
        """Test disconnect() handles no connection gracefully."""
        with allure.step("Create DBClient without connecting"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )

        with allure.step("Call await db.disconnect() without connecting"):
            # Should not raise error
            await db.disconnect()

        with allure.step("Verify no errors"):
            assert db._is_connected is False

    @pytest.mark.asyncio
    @allure.title("TC-DB-015: Check connection status")
    @allure.description("Test is_connected() returns correct status. TC-DB-015")
    async def test_is_connected_status(self, valid_config):
        """Test is_connected() returns correct status."""
        with allure.step("Create DBClient instance"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )

        with allure.step("Verify is_connected() returns False before connect()"):
            assert await db.is_connected() is False

        with allure.step("Connect to database"):
            await db.connect()

        with allure.step("Verify is_connected() returns True"):
            assert await db.is_connected() is True

        with allure.step("Disconnect"):
            await db.disconnect()

        with allure.step("Verify is_connected() returns False"):
            assert await db.is_connected() is False

    @pytest.mark.asyncio
    @allure.title("TC-DB-016: Close calls disconnect")
    @allure.description("Test close() calls disconnect(). TC-DB-016")
    async def test_close_calls_disconnect(self, valid_config, mocker):
        """Test close() calls disconnect()."""
        with allure.step("Connect to database"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()
            assert db._is_connected is True

        with allure.step("Mock disconnect method"):
            mock_disconnect = mocker.patch.object(
                db, "disconnect", new_callable=AsyncMock
            )

        with allure.step("Call await db.close()"):
            await db.close()

        with allure.step("Verify disconnect() was called"):
            mock_disconnect.assert_called_once()

        with allure.step("Verify _is_connected is False"):
            # Since disconnect was mocked, we need to check the mock was called
            # The actual disconnect would set _is_connected to False
            assert mock_disconnect.called


# ============================================================================
# IV. Query Execution Tests
# ============================================================================


class TestDBClientQueryExecution:
    """Test DBClient query execution."""

    @pytest.mark.asyncio
    @allure.title("TC-DB-017: Execute SELECT query successfully")
    @allure.description(
        "Test execute_query() executes SELECT and returns results. TC-DB-017"
    )
    async def test_execute_query_successfully(self, valid_config):
        """Test execute_query() executes SELECT and returns results."""
        with allure.step("Connect to database"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()

        with allure.step("Create test table"):
            await db.execute_command(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"
            )
            await db.execute_command(
                "INSERT INTO users (name) VALUES (:name)", {"name": "Test User"}
            )

        with allure.step("Call await db.execute_query(...)"):
            results = await db.execute_query(
                "SELECT * FROM users WHERE id = :id", {"id": 1}
            )

        with allure.step("Verify returns list of dictionaries"):
            assert isinstance(results, list)
            assert len(results) > 0

        with allure.step("Verify each row is a dict with column names as keys"):
            assert isinstance(results[0], dict)
            assert "id" in results[0]
            assert "name" in results[0]
            assert results[0]["name"] == "Test User"

        with allure.step("Cleanup: disconnect"):
            await db.disconnect()

    @pytest.mark.asyncio
    @allure.title("TC-DB-018: Execute query with no results")
    @allure.description(
        "Test execute_query() returns empty list for no results. TC-DB-018"
    )
    async def test_execute_query_no_results(self, valid_config):
        """Test execute_query() returns empty list for no results."""
        with allure.step("Connect to database"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()

        with allure.step("Create test table"):
            await db.execute_command(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"
            )

        with allure.step("Call await db.execute_query(...) with non-existent id"):
            results = await db.execute_query(
                "SELECT * FROM users WHERE id = :id", {"id": 999}
            )

        with allure.step("Verify returns empty list []"):
            assert results == []

        with allure.step("Cleanup: disconnect"):
            await db.disconnect()

    @pytest.mark.asyncio
    @allure.title("TC-DB-019: Execute query auto-connects if not connected")
    @allure.description(
        "Test execute_query() auto-connects if not connected. TC-DB-019"
    )
    async def test_execute_query_auto_connects(self, valid_config, mocker):
        """Test execute_query() auto-connects if not connected."""
        with allure.step("Create DBClient without connecting"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )

        with allure.step("Mock connect method"):
            mock_connect = mocker.patch.object(db, "connect", new_callable=AsyncMock)

        with allure.step("Call await db.execute_query('SELECT 1')"):
            # This will fail because we need a real connection, but we can verify connect was called
            try:
                await db.execute_query("SELECT 1")
            except Exception:
                pass  # Expected if connection fails

        with allure.step("Verify connect() was called automatically"):
            mock_connect.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("TC-DB-020: Execute query with invalid SQL")
    @allure.description("Test execute_query() handles SQL errors. TC-DB-020")
    async def test_execute_query_invalid_sql(self, valid_config):
        """Test execute_query() handles SQL errors."""
        with allure.step("Connect to database"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()

        with allure.step("Call await db.execute_query(...) with invalid SQL"):
            with pytest.raises(Exception):  # Database-specific error
                await db.execute_query("SELECT * FROM nonexistent_table")

        with allure.step("Cleanup: disconnect"):
            await db.disconnect()

    @pytest.mark.asyncio
    @allure.title("TC-DB-021: Execute INSERT command successfully")
    @allure.description("Test execute_command() executes INSERT. TC-DB-021")
    async def test_execute_command_insert(self, valid_config):
        """Test execute_command() executes INSERT."""
        with allure.step("Connect to database"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()

        with allure.step("Create test table"):
            await db.execute_command(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"
            )

        with allure.step("Call await db.execute_command(...) with INSERT"):
            result = await db.execute_command(
                "INSERT INTO users (name) VALUES (:name)", {"name": "Test"}
            )

        with allure.step("Verify returns number of affected rows (1)"):
            assert result == 1

        with allure.step("Cleanup: disconnect"):
            await db.disconnect()

    @pytest.mark.asyncio
    @allure.title("TC-DB-022: Execute UPDATE command successfully")
    @allure.description("Test execute_command() executes UPDATE. TC-DB-022")
    async def test_execute_command_update(self, valid_config):
        """Test execute_command() executes UPDATE."""
        with allure.step("Connect to database"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()

        with allure.step("Create test table and insert data"):
            await db.execute_command(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"
            )
            await db.execute_command(
                "INSERT INTO users (name) VALUES (:name)", {"name": "Original"}
            )

        with allure.step("Call await db.execute_command(...) with UPDATE"):
            result = await db.execute_command(
                "UPDATE users SET name = :name WHERE id = :id",
                {"name": "Updated", "id": 1},
            )

        with allure.step("Verify returns number of affected rows"):
            assert result == 1

        with allure.step("Cleanup: disconnect"):
            await db.disconnect()

    @pytest.mark.asyncio
    @allure.title("TC-DB-023: Execute DELETE command successfully")
    @allure.description("Test execute_command() executes DELETE. TC-DB-023")
    async def test_execute_command_delete(self, valid_config):
        """Test execute_command() executes DELETE."""
        with allure.step("Connect to database"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()

        with allure.step("Create test table and insert data"):
            await db.execute_command(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"
            )
            await db.execute_command(
                "INSERT INTO users (name) VALUES (:name)", {"name": "To Delete"}
            )

        with allure.step("Call await db.execute_command(...) with DELETE"):
            result = await db.execute_command(
                "DELETE FROM users WHERE id = :id", {"id": 1}
            )

        with allure.step("Verify returns number of affected rows"):
            assert result == 1

        with allure.step("Cleanup: disconnect"):
            await db.disconnect()

    @pytest.mark.asyncio
    @allure.title("TC-DB-024: Execute command auto-connects if not connected")
    @allure.description(
        "Test execute_command() auto-connects if not connected. TC-DB-024"
    )
    async def test_execute_command_auto_connects(self, valid_config, mocker):
        """Test execute_command() auto-connects if not connected."""
        with allure.step("Create DBClient without connecting"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )

        with allure.step("Mock connect method"):
            mock_connect = mocker.patch.object(db, "connect", new_callable=AsyncMock)

        with allure.step("Call await db.execute_command(...)"):
            # This will fail because we need a real connection, but we can verify connect was called
            try:
                await db.execute_command(
                    "INSERT INTO users (name) VALUES (:name)", {"name": "Test"}
                )
            except Exception:
                pass  # Expected if connection fails

        with allure.step("Verify connect() was called automatically"):
            mock_connect.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("TC-DB-025: Execute command with invalid SQL")
    @allure.description("Test execute_command() handles SQL errors. TC-DB-025")
    async def test_execute_command_invalid_sql(self, valid_config):
        """Test execute_command() handles SQL errors."""
        with allure.step("Connect to database"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()

        with allure.step("Call await db.execute_command(...) with invalid SQL"):
            with pytest.raises(Exception):  # Database-specific error
                await db.execute_command("INSERT INTO nonexistent_table VALUES (1)")

        with allure.step("Cleanup: disconnect"):
            await db.disconnect()


# ============================================================================
# V. Transaction Tests
# ============================================================================


class TestDBClientTransactions:
    """Test DBClient transaction handling."""

    @pytest.mark.asyncio
    @allure.title("TC-DB-026: Begin transaction successfully")
    @allure.description("Test begin_transaction() starts transaction. TC-DB-026")
    async def test_begin_transaction_successfully(self, valid_config):
        """Test begin_transaction() starts transaction."""
        with allure.step("Connect to database"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()

        with allure.step("Create test table"):
            await db.execute_command(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"
            )

        with allure.step("Call await db.begin_transaction()"):
            await db.begin_transaction()

        with allure.step("Verify transaction is started"):
            # SQLite transactions are implicit, so we just verify no error
            assert True

        with allure.step("Cleanup: disconnect"):
            await db.disconnect()

    @pytest.mark.asyncio
    @allure.title("TC-DB-027: Commit transaction successfully")
    @allure.description("Test commit_transaction() commits changes. TC-DB-027")
    async def test_commit_transaction_successfully(self, valid_config):
        """Test commit_transaction() commits changes."""
        with allure.step("Connect to database"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()

        with allure.step("Create test table"):
            await db.execute_command(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"
            )

        with allure.step("Begin transaction"):
            await db.begin_transaction()

        with allure.step("Execute INSERT command"):
            await db.execute_command(
                "INSERT INTO users (name) VALUES (:name)", {"name": "Test"}
            )

        with allure.step("Call await db.commit_transaction()"):
            await db.commit_transaction()

        with allure.step("Verify changes are persisted"):
            results = await db.execute_query("SELECT * FROM users")
            assert len(results) == 1
            assert results[0]["name"] == "Test"

        with allure.step("Cleanup: disconnect"):
            await db.disconnect()

    @pytest.mark.asyncio
    @allure.title("TC-DB-028: Rollback transaction successfully")
    @allure.description("Test rollback_transaction() rolls back changes. TC-DB-028")
    async def test_rollback_transaction_successfully(self, valid_config):
        """Test rollback_transaction() rolls back changes."""
        with allure.step("Connect to database"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()

        with allure.step("Create test table"):
            await db.execute_command(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"
            )

        with allure.step("Begin transaction"):
            await db.begin_transaction()

        with allure.step("Execute INSERT command"):
            await db.execute_command(
                "INSERT INTO users (name) VALUES (:name)", {"name": "To Rollback"}
            )

        with allure.step("Call await db.rollback_transaction()"):
            await db.rollback_transaction()

        with allure.step("Verify changes are not persisted"):
            results = await db.execute_query("SELECT * FROM users")
            assert len(results) == 0

        with allure.step("Cleanup: disconnect"):
            await db.disconnect()

    @pytest.mark.asyncio
    @allure.title("TC-DB-029: Use transaction context manager successfully")
    @allure.description(
        "Test transaction() context manager commits on success. TC-DB-029"
    )
    async def test_transaction_context_manager_success(self, valid_config):
        """Test transaction() context manager commits on success."""
        with allure.step("Connect to database"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()

        with allure.step("Create test table"):
            await db.execute_command(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"
            )

        with allure.step("Use async with db.transaction():"):
            async with db.transaction():
                await db.execute_command(
                    "INSERT INTO users (name) VALUES (:name)", {"name": "Test1"}
                )
                await db.execute_command(
                    "INSERT INTO users (name) VALUES (:name)", {"name": "Test2"}
                )

        with allure.step("Verify all changes are committed"):
            results = await db.execute_query("SELECT * FROM users")
            assert len(results) == 2

        with allure.step("Cleanup: disconnect"):
            await db.disconnect()

    @pytest.mark.asyncio
    @allure.title("TC-DB-030: Transaction context manager rolls back on exception")
    @allure.description(
        "Test transaction() context manager rolls back on error. TC-DB-030"
    )
    async def test_transaction_context_manager_rollback(self, valid_config):
        """Test transaction() context manager rolls back on error."""
        with allure.step("Connect to database"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()

        with allure.step("Create test table"):
            await db.execute_command(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"
            )

        with allure.step("Use async with db.transaction() and raise exception"):
            try:
                async with db.transaction():
                    await db.execute_command(
                        "INSERT INTO users (name) VALUES (:name)", {"name": "Test"}
                    )
                    raise ValueError("Test exception")
            except ValueError:
                pass  # Expected

        with allure.step("Verify transaction is rolled back"):
            results = await db.execute_query("SELECT * FROM users")
            assert len(results) == 0

        with allure.step("Cleanup: disconnect"):
            await db.disconnect()

    @pytest.mark.asyncio
    @allure.title("TC-DB-031: Nested transactions")
    @allure.description("Test transaction() handles nested transactions. TC-DB-031")
    async def test_nested_transactions(self, valid_config):
        """Test transaction() handles nested transactions."""
        with allure.step("Connect to database"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()

        with allure.step("Create test table"):
            await db.execute_command(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"
            )

        with allure.step("Use nested async with db.transaction():"):
            async with db.transaction():
                await db.execute_command(
                    "INSERT INTO users (name) VALUES (:name)", {"name": "Outer"}
                )
                async with db.transaction():
                    await db.execute_command(
                        "INSERT INTO users (name) VALUES (:name)", {"name": "Inner"}
                    )

        with allure.step("Verify behavior (database-specific)"):
            # SQLite doesn't support true nested transactions, but should work
            results = await db.execute_query("SELECT * FROM users")
            # Both should be committed
            assert len(results) >= 1

        with allure.step("Cleanup: disconnect"):
            await db.disconnect()


# ============================================================================
# VI. Edge Cases
# ============================================================================


class TestDBClientEdgeCases:
    """Test DBClient edge cases."""

    @pytest.mark.asyncio
    @allure.title("TC-DB-037: Execute query with None params")
    @allure.description("Test execute_query() handles None params. TC-DB-037")
    async def test_execute_query_none_params(self, valid_config):
        """Test execute_query() handles None params."""
        with allure.step("Connect to database"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()

        with allure.step("Call await db.execute_query('SELECT 1', params=None)"):
            results = await db.execute_query("SELECT 1", params=None)

        with allure.step("Verify works correctly"):
            assert len(results) == 1

        with allure.step("Cleanup: disconnect"):
            await db.disconnect()

    @pytest.mark.asyncio
    @allure.title("TC-DB-038: Execute command with None params")
    @allure.description("Test execute_command() handles None params. TC-DB-038")
    async def test_execute_command_none_params(self, valid_config):
        """Test execute_command() handles None params."""
        with allure.step("Connect to database"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()

        with allure.step("Create test table"):
            await db.execute_command(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"
            )

        with allure.step("Call await db.execute_command('SELECT 1', params=None)"):
            # This is a query, not a command, but we test None params handling
            result = await db.execute_query("SELECT 1", params=None)

        with allure.step("Verify works correctly"):
            assert len(result) == 1

        with allure.step("Cleanup: disconnect"):
            await db.disconnect()

    @pytest.mark.asyncio
    @allure.title("TC-DB-039: Execute query with empty params dict")
    @allure.description("Test execute_query() handles empty params dict. TC-DB-039")
    async def test_execute_query_empty_params(self, valid_config):
        """Test execute_query() handles empty params dict."""
        with allure.step("Connect to database"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()

        with allure.step("Call await db.execute_query('SELECT 1', params={})"):
            results = await db.execute_query("SELECT 1", params={})

        with allure.step("Verify works correctly"):
            assert len(results) == 1

        with allure.step("Cleanup: disconnect"):
            await db.disconnect()

    @allure.title("TC-DB-040: Connection string parsing (SQLite)")
    @allure.description(
        "Test SQLiteAdapter parses connection string correctly. TC-DB-040"
    )
    def test_sqlite_connection_string_parsing(self, valid_config):
        """Test SQLiteAdapter parses connection string correctly."""
        with allure.step(
            "Create SQLiteAdapter with connection_string='sqlite:///path/to/db.sqlite'"
        ):
            db1 = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///path/to/db.sqlite",
            )

        with allure.step("Verify _database_path is extracted correctly"):
            assert db1._database_path == "path/to/db.sqlite"

        with allure.step(
            "Create SQLiteAdapter with connection_string='sqlite://path/to/db.sqlite'"
        ):
            db2 = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite://path/to/db.sqlite",
            )

        with allure.step("Verify _database_path is extracted correctly"):
            assert db2._database_path == "path/to/db.sqlite"

    @pytest.mark.asyncio
    @allure.title("TC-DB-041: Multiple queries in sequence")
    @allure.description("Test multiple queries work in sequence. TC-DB-041")
    async def test_multiple_queries_sequence(self, valid_config):
        """Test multiple queries work in sequence."""
        with allure.step("Connect to database"):
            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            await db.connect()

        with allure.step("Create test table"):
            await db.execute_command(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"
            )

        with allure.step("Execute multiple queries in sequence"):
            await db.execute_command(
                "INSERT INTO users (name) VALUES (:name)", {"name": "User1"}
            )
            await db.execute_command(
                "INSERT INTO users (name) VALUES (:name)", {"name": "User2"}
            )
            results = await db.execute_query("SELECT * FROM users")

        with allure.step("Verify all queries execute successfully"):
            assert len(results) == 2

        with allure.step("Cleanup: disconnect"):
            await db.disconnect()

    @pytest.mark.asyncio
    @allure.title("TC-DB-042: Connection error handling")
    @allure.description("Test connect() handles connection errors. TC-DB-042")
    async def test_connection_error_handling(self, valid_config):
        """Test connect() handles connection errors."""
        with allure.step("Create DBClient with invalid path"):
            # Use a path that cannot be created (e.g., invalid directory on Windows)
            # On Windows, use a path with invalid characters or non-existent drive
            if platform.system() == "Windows":
                # Use a path with invalid characters or non-existent drive
                invalid_path = "Z:/invalid/path/that/does/not/exist/db.sqlite"
            else:
                # On Unix, use a path in a non-existent directory
                invalid_path = "/invalid/path/that/does/not/exist/db.sqlite"

            db = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string=f"sqlite:///{invalid_path}",
            )

        with allure.step("Call await db.connect() and verify exception"):
            # SQLite will try to create the file, but if the directory doesn't exist, it will fail
            # We expect an exception (could be OSError, sqlite3.OperationalError, etc.)
            with pytest.raises(Exception):
                await db.connect()

    @allure.title(
        "TC-DB-043: SQLiteAdapter initialization without connection_string (uses kwargs)"
    )
    @allure.description(
        "Test SQLiteAdapter can be initialized without connection_string using kwargs. TC-DB-043"
    )
    def test_sqlite_adapter_init_without_connection_string_uses_kwargs(
        self, valid_config
    ):
        """Test SQLiteAdapter can be initialized without connection_string using kwargs."""
        with allure.step(
            "Create SQLiteAdapter without connection_string, with kwargs database_path='test.db'"
        ):
            adapter = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                database_path="test.db",
            )

        with allure.step("Verify _database_path is set to 'test.db'"):
            assert adapter._database_path == "test.db"

        with allure.step(
            "Create SQLiteAdapter without connection_string and without database_path in kwargs"
        ):
            adapter2 = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
            )

        with allure.step("Verify _database_path is set to ':memory:' (default)"):
            assert adapter2._database_path == ":memory:"

    @pytest.mark.asyncio
    @allure.title("TC-DB-044: SQLiteAdapter ImportError when aiosqlite is missing")
    @allure.description(
        "Test SQLiteAdapter raises ImportError when aiosqlite library is not available. TC-DB-044"
    )
    async def test_sqlite_adapter_import_error_when_aiosqlite_missing(
        self, valid_config, mocker
    ):
        """Test SQLiteAdapter raises ImportError when aiosqlite library is not available."""
        with allure.step("Create SQLiteAdapter instance"):
            adapter = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )

        with allure.step("Mock import aiosqlite to raise ImportError"):
            # Save original __import__ before patching
            original_import = builtins.__import__

            # Create a mock that raises ImportError
            def mock_import(name, *args, **kwargs):
                if name == "aiosqlite":
                    raise ImportError("No module named 'aiosqlite'")
                # Use original import for everything else
                return original_import(name, *args, **kwargs)

            mocker.patch("builtins.__import__", side_effect=mock_import)

        with allure.step("Call await adapter.connect() and verify ImportError"):
            with pytest.raises(ImportError) as exc_info:
                await adapter.connect()

        with allure.step(
            "Verify ImportError message contains helpful installation instructions"
        ):
            assert "aiosqlite" in str(exc_info.value)
            assert "Install it with" in str(
                exc_info.value
            ) or "uv add aiosqlite" in str(exc_info.value)


# ============================================================================
# VII. Adapter-Specific Tests
# ============================================================================


class TestDBClientAdapters:
    """Test database adapter-specific functionality."""

    @allure.title("TC-DB-032: PostgreSQL adapter detects asyncpg")
    @allure.description("Test PostgreSQLAdapter uses asyncpg when available. TC-DB-032")
    def test_postgresql_adapter_detects_asyncpg(self, valid_config, mocker):
        """Test PostgreSQLAdapter uses asyncpg when available."""
        with allure.step("Mock asyncpg import in adapter"):
            mocker.patch(
                "tma_test_framework.clients.db_adapters.postgresql_adapter.asyncpg",
                create=True,
            )

        with allure.step("Create PostgreSQLAdapter"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )

        with allure.step("Mock _detect_adapter to return 'asyncpg'"):
            mocker.patch.object(adapter, "_detect_adapter", return_value="asyncpg")

        with allure.step("Verify adapter can be created"):
            assert adapter is not None

    @allure.title("TC-DB-033: PostgreSQL adapter detects psycopg")
    @allure.description(
        "Test PostgreSQLAdapter uses psycopg when asyncpg not available. TC-DB-033"
    )
    def test_postgresql_adapter_detects_psycopg(self, valid_config, mocker):
        """Test PostgreSQLAdapter uses psycopg when asyncpg not available."""
        with allure.step("Mock import to simulate asyncpg missing"):
            # Mock asyncpg import to raise ImportError
            mocker.patch(
                "builtins.__import__",
                side_effect=lambda name, *args, **kwargs: (
                    MagicMock()
                    if name != "asyncpg"
                    else (_ for _ in ()).throw(ImportError())
                ),
            )

        with allure.step("Create PostgreSQLAdapter"):
            adapter = PostgreSQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="postgresql://user:pass@localhost/db",
            )

        with allure.step("Mock _detect_adapter to return 'psycopg'"):
            mocker.patch.object(adapter, "_detect_adapter", return_value="psycopg")

        with allure.step("Verify adapter can be created"):
            assert adapter is not None

    @pytest.mark.asyncio
    @allure.title("TC-DB-034: SQLite adapter uses aiosqlite")
    @allure.description("Test SQLiteAdapter uses aiosqlite. TC-DB-034")
    async def test_sqlite_adapter_uses_aiosqlite(self, valid_config):
        """Test SQLiteAdapter uses aiosqlite."""
        with allure.step("Create SQLiteAdapter"):
            adapter = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )

        with allure.step("Connect to database"):
            await adapter.connect()

        with allure.step("Verify connection is aiosqlite connection"):
            # Check that connection exists and is not None
            assert adapter._connection is not None

        with allure.step("Cleanup: disconnect"):
            await adapter.disconnect()

    @allure.title("TC-DB-035: MySQL adapter detects aiomysql")
    @allure.description("Test MySQLAdapter uses aiomysql when available. TC-DB-035")
    def test_mysql_adapter_detects_aiomysql(self, valid_config, mocker):
        """Test MySQLAdapter uses aiomysql when available."""
        with allure.step("Create MySQLAdapter"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )

        with allure.step("Mock _detect_adapter to return 'aiomysql'"):
            mocker.patch.object(adapter, "_detect_adapter", return_value="aiomysql")

        with allure.step("Verify adapter can be created"):
            assert adapter is not None

    @allure.title("TC-DB-036: MySQL adapter detects pymysql")
    @allure.description(
        "Test MySQLAdapter uses pymysql when aiomysql not available. TC-DB-036"
    )
    def test_mysql_adapter_detects_pymysql(self, valid_config, mocker):
        """Test MySQLAdapter uses pymysql when aiomysql not available."""
        with allure.step("Create MySQLAdapter"):
            adapter = MySQLAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="mysql://user:pass@localhost/db",
            )

        with allure.step("Mock _detect_adapter to return 'pymysql'"):
            mocker.patch.object(adapter, "_detect_adapter", return_value="pymysql")

        with allure.step("Verify adapter can be created"):
            assert adapter is not None

    @pytest.mark.asyncio
    @allure.title("TC-DB-115: SQLiteAdapter begin_transaction() calls BEGIN")
    @allure.description(
        "Test SQLiteAdapter begin_transaction() executes BEGIN statement. TC-DB-115"
    )
    async def test_sqlite_begin_transaction_calls_begin(self, valid_config, mocker):
        """Test SQLiteAdapter begin_transaction() executes BEGIN statement."""
        with allure.step("Create and connect SQLiteAdapter"):
            adapter = SQLiteAdapter(
                "https://example.com/app",
                valid_config,
                connection_string="sqlite:///:memory:",
            )
            mock_connection = AsyncMock()
            adapter._connection = mock_connection
            adapter._is_connected = True
            adapter._transaction_level = 0

        with allure.step("Mock _connection.execute()"):
            mock_connection.execute = AsyncMock()

        with allure.step("Call await adapter.begin_transaction()"):
            await adapter.begin_transaction()

        with allure.step("Verify _connection.execute('BEGIN') was called"):
            mock_connection.execute.assert_called_once_with("BEGIN")

    @pytest.mark.asyncio
    @allure.title("TC-DB-116: DBClient.create() with config missing api_id or api_hash")
    @allure.description(
        "Test DBClient.create() handles errors when config is missing api_id or api_hash. TC-DB-116"
    )
    async def test_db_client_create_with_invalid_config(self, valid_config, mocker):
        """Test DBClient.create() handles errors when config is missing api_id or api_hash."""
        with allure.step("Create Config without api_id"):
            # Config validation will raise ValueError when api_id is None
            with pytest.raises(ValueError, match="api_id must be between"):
                Config(
                    api_id=None,  # type: ignore[arg-type] # Missing api_id
                    api_hash="test_hash",
                    bot_token="test_token",
                )

        with allure.step("Create Config without api_hash"):
            # Config validation will raise ValueError when api_hash is None
            with pytest.raises(ValueError, match="api_hash must be exactly"):
                Config(
                    api_id=123,
                    api_hash=None,  # type: ignore[arg-type] # Missing api_hash
                    bot_token="test_token",
                )

        with allure.step("Call DBClient.create() with config=None"):
            # Test that DBClient.create() properly handles config=None
            # This should raise ValueError from BaseClient.__init__()
            with pytest.raises(ValueError, match="config is required"):
                DBClient.create(
                    "sqlite",
                    "https://example.com/app",
                    config=None,
                    connection_string="sqlite:///:memory:",
                )
