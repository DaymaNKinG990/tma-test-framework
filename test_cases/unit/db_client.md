# DBClient Class - Unit Test Cases

## Overview
Tests for `tma_test_framework.clients.db_client.DBClient` class - database client with support for multiple backends (PostgreSQL, SQLite, MySQL).

## Test Categories

### 1. Initialization Tests

#### TC-DB-001: Initialize DBClient with URL, config, and connection_string
- **Purpose**: Verify DBClient can be initialized with URL, Config, and connection string
- **Preconditions**: Valid URL, Config object, and connection string
- **Test Steps**:
  1. Create DBClient(url, config, connection_string="postgresql://user:pass@localhost/db")
  2. Verify url, config, and connection_string are set
  3. Verify _connection is None, _is_connected is False
- **Expected Result**: DBClient created with all parameters set
- **Coverage**: `__init__` method

#### TC-DB-002: Initialize DBClient with URL and config only
- **Purpose**: Verify DBClient can be initialized without connection_string
- **Preconditions**: Valid URL and Config object
- **Test Steps**:
  1. Create DBClient(url, config)
  2. Verify connection_string is None
  3. Verify _db_kwargs is empty dict
- **Expected Result**: DBClient created with connection_string=None
- **Coverage**: `__init__` with optional connection_string

#### TC-DB-003: Initialize DBClient with additional kwargs
- **Purpose**: Verify DBClient accepts database-specific parameters
- **Preconditions**: Valid URL, Config, and kwargs
- **Test Steps**:
  1. Create DBClient(url, config, host="localhost", port=5432, database="testdb")
  2. Verify _db_kwargs contains provided parameters
- **Expected Result**: Additional parameters stored in _db_kwargs
- **Coverage**: `__init__` with kwargs

#### TC-DB-004: Initialize DBClient with config=None raises error
- **Purpose**: Verify DBClient rejects None config (inherited from BaseClient)
- **Preconditions**: Valid URL, config=None
- **Test Steps**:
  1. Create DBClient(url, config=None)
  2. Verify ValueError is raised
- **Expected Result**: ValueError raised (Config is required)
- **Coverage**: `__init__` validation (inherited)

### 2. Factory Method Tests

#### TC-DB-005: Create PostgreSQL client using factory method
- **Purpose**: Verify DBClient.create() creates PostgreSQLAdapter
- **Preconditions**: asyncpg or psycopg library available
- **Test Steps**:
  1. Call DBClient.create('postgresql', url, config, connection_string)
  2. Verify returns PostgreSQLAdapter instance
  3. Verify isinstance(result, DBClient)
- **Expected Result**: PostgreSQLAdapter instance created
- **Coverage**: `create()` factory method (PostgreSQL)

#### TC-DB-006: Create SQLite client using factory method
- **Purpose**: Verify DBClient.create() creates SQLiteAdapter
- **Preconditions**: aiosqlite library available
- **Test Steps**:
  1. Call DBClient.create('sqlite', url, config, connection_string)
  2. Verify returns SQLiteAdapter instance
  3. Verify isinstance(result, DBClient)
- **Expected Result**: SQLiteAdapter instance created
- **Coverage**: `create()` factory method (SQLite)

#### TC-DB-007: Create MySQL client using factory method
- **Purpose**: Verify DBClient.create() creates MySQLAdapter
- **Preconditions**: aiomysql or pymysql library available
- **Test Steps**:
  1. Call DBClient.create('mysql', url, config, connection_string)
  2. Verify returns MySQLAdapter instance
  3. Verify isinstance(result, DBClient)
- **Expected Result**: MySQLAdapter instance created
- **Coverage**: `create()` factory method (MySQL)

#### TC-DB-008: Factory method with unsupported database type
- **Purpose**: Verify DBClient.create() raises ValueError for unsupported type
- **Preconditions**: Unsupported db_type
- **Test Steps**:
  1. Call DBClient.create('oracle', url, config)
  2. Verify ValueError is raised with message about unsupported type
- **Expected Result**: ValueError raised: "Unsupported database type: oracle"
- **Coverage**: `create()` error handling

#### TC-DB-009: Factory method with missing library
- **Purpose**: Verify DBClient.create() raises ImportError when library not installed
- **Preconditions**: Required library not installed
- **Test Steps**:
  1. Mock import to raise ImportError
  2. Call DBClient.create('postgresql', url, config)
  3. Verify ImportError is raised with installation instructions
- **Expected Result**: ImportError raised with helpful message
- **Coverage**: `create()` import error handling

#### TC-DB-045: Factory method with invalid parameters
- **Purpose**: Verify DBClient.create() handles invalid parameters correctly
- **Preconditions**: Invalid parameters (e.g., None instead of string)
- **Test Steps**:
  1. Call DBClient.create(None, url, config)
  2. Verify appropriate error is raised (TypeError or ValueError)
  3. Call DBClient.create('postgresql', None, config)
  4. Verify appropriate error is raised
- **Expected Result**: Error raised for invalid parameters
- **Coverage**: `create()` parameter validation

#### TC-DB-046: Factory method with partially invalid parameters
- **Purpose**: Verify DBClient.create() handles partially invalid parameters
- **Preconditions**: Valid db_type but invalid connection_string or config
- **Test Steps**:
  1. Call DBClient.create('postgresql', url, config, connection_string="invalid://")
  2. Verify adapter is created (validation happens during connect)
  3. Call DBClient.create('sqlite', url, None)
  4. Verify ValueError is raised (config is required)
- **Expected Result**: Partial validation, errors raised where appropriate
- **Coverage**: `create()` partial parameter validation

#### TC-DB-010: Factory method with case-insensitive db_type
- **Purpose**: Verify DBClient.create() handles case-insensitive db_type
- **Preconditions**: Different case variations
- **Test Steps**:
  1. Call DBClient.create('POSTGRESQL', url, config)
  2. Call DBClient.create('PostgreSQL', url, config)
  3. Call DBClient.create('postgres', url, config)
  4. Verify all work correctly
- **Expected Result**: All case variations work
- **Coverage**: `create()` case handling

### 3. Connection Management Tests

#### TC-DB-011: Connect to database successfully
- **Purpose**: Verify connect() establishes connection
- **Preconditions**: Valid connection parameters, database accessible
- **Test Steps**:
  1. Create DBClient instance
  2. Call await db.connect()
  3. Verify _is_connected is True
  4. Verify _connection is not None
- **Expected Result**: Connection established, _is_connected=True
- **Coverage**: `connect()` method

#### TC-DB-012: Connect when already connected
- **Purpose**: Verify connect() is idempotent
- **Preconditions**: Already connected
- **Test Steps**:
  1. Connect to database
  2. Call connect() again
  3. Verify no new connection is created
  4. Verify debug log "Already connected"
- **Expected Result**: No duplicate connection, idempotent behavior
- **Coverage**: `connect()` idempotency

#### TC-DB-013: Disconnect from database
- **Purpose**: Verify disconnect() closes connection
- **Preconditions**: Connected database client
- **Test Steps**:
  1. Connect to database
  2. Call await db.disconnect()
  3. Verify _is_connected is False
  4. Verify _connection is None
- **Expected Result**: Connection closed, _is_connected=False
- **Coverage**: `disconnect()` method

#### TC-DB-014: Disconnect when not connected
- **Purpose**: Verify disconnect() handles no connection gracefully
- **Preconditions**: Not connected
- **Test Steps**:
  1. Call await db.disconnect() without connecting
  2. Verify no errors
- **Expected Result**: No errors, graceful handling
- **Coverage**: `disconnect()` when not connected

#### TC-DB-015: Check connection status
- **Purpose**: Verify is_connected() returns correct status
- **Preconditions**: DBClient instance
- **Test Steps**:
  1. Verify is_connected() returns False before connect()
  2. Connect to database
  3. Verify is_connected() returns True
  4. Disconnect
  5. Verify is_connected() returns False
- **Expected Result**: is_connected() returns correct status
- **Coverage**: `is_connected()` method

#### TC-DB-016: Close calls disconnect
- **Purpose**: Verify close() calls disconnect()
- **Preconditions**: Connected database client
- **Test Steps**:
  1. Connect to database
  2. Call await db.close()
  3. Verify disconnect() was called
  4. Verify _is_connected is False
- **Expected Result**: close() calls disconnect()
- **Coverage**: `close()` method

### 4. Query Execution Tests

#### TC-DB-017: Execute SELECT query successfully
- **Purpose**: Verify execute_query() executes SELECT and returns results
- **Preconditions**: Connected database, table with data
- **Test Steps**:
  1. Connect to database
  2. Call await db.execute_query("SELECT * FROM users WHERE id = :id", {"id": 1})
  3. Verify returns list of dictionaries
  4. Verify each row is a dict with column names as keys
- **Expected Result**: Query executed, results returned as list of dicts
- **Coverage**: `execute_query()` method

#### TC-DB-018: Execute query with no results
- **Purpose**: Verify execute_query() returns empty list for no results
- **Preconditions**: Connected database, empty result set
- **Test Steps**:
  1. Connect to database
  2. Call await db.execute_query("SELECT * FROM users WHERE id = :id", {"id": 999})
  3. Verify returns empty list []
- **Expected Result**: Empty list returned
- **Coverage**: `execute_query()` empty results

#### TC-DB-019: Execute query auto-connects if not connected
- **Purpose**: Verify execute_query() auto-connects if not connected
- **Preconditions**: DBClient not connected
- **Test Steps**:
  1. Create DBClient without connecting
  2. Call await db.execute_query("SELECT 1")
  3. Verify connect() was called automatically
  4. Verify query executed successfully
- **Expected Result**: Auto-connection works, query executed
- **Coverage**: `execute_query()` auto-connection

#### TC-DB-020: Execute query with invalid SQL
- **Purpose**: Verify execute_query() handles SQL errors
- **Preconditions**: Connected database
- **Test Steps**:
  1. Connect to database
  2. Call await db.execute_query("SELECT * FROM nonexistent_table")
  3. Verify exception is raised
- **Expected Result**: Exception raised (database-specific error)
- **Coverage**: `execute_query()` error handling

#### TC-DB-021: Execute INSERT command successfully
- **Purpose**: Verify execute_command() executes INSERT
- **Preconditions**: Connected database, table exists
- **Test Steps**:
  1. Connect to database
  2. Call await db.execute_command("INSERT INTO users (name) VALUES (:name)", {"name": "Test"})
  3. Verify returns number of affected rows (1)
- **Expected Result**: Command executed, returns 1
- **Coverage**: `execute_command()` INSERT

#### TC-DB-022: Execute UPDATE command successfully
- **Purpose**: Verify execute_command() executes UPDATE
- **Preconditions**: Connected database, existing row
- **Test Steps**:
  1. Connect to database
  2. Call await db.execute_command("UPDATE users SET name = :name WHERE id = :id", {"name": "Updated", "id": 1})
  3. Verify returns number of affected rows
- **Expected Result**: Command executed, returns affected rows count
- **Coverage**: `execute_command()` UPDATE

#### TC-DB-023: Execute DELETE command successfully
- **Purpose**: Verify execute_command() executes DELETE
- **Preconditions**: Connected database, existing row
- **Test Steps**:
  1. Connect to database
  2. Call await db.execute_command("DELETE FROM users WHERE id = :id", {"id": 1})
  3. Verify returns number of affected rows
- **Expected Result**: Command executed, returns affected rows count
- **Coverage**: `execute_command()` DELETE

#### TC-DB-024: Execute command auto-connects if not connected
- **Purpose**: Verify execute_command() auto-connects if not connected
- **Preconditions**: DBClient not connected
- **Test Steps**:
  1. Create DBClient without connecting
  2. Call await db.execute_command("INSERT INTO users (name) VALUES (:name)", {"name": "Test"})
  3. Verify connect() was called automatically
  4. Verify command executed successfully
- **Expected Result**: Auto-connection works, command executed
- **Coverage**: `execute_command()` auto-connection

#### TC-DB-025: Execute command with invalid SQL
- **Purpose**: Verify execute_command() handles SQL errors
- **Preconditions**: Connected database
- **Test Steps**:
  1. Connect to database
  2. Call await db.execute_command("INSERT INTO nonexistent_table VALUES (1)")
  3. Verify exception is raised
- **Expected Result**: Exception raised (database-specific error)
- **Coverage**: `execute_command()` error handling

### 5. Transaction Tests

#### TC-DB-026: Begin transaction successfully
- **Purpose**: Verify begin_transaction() starts transaction
- **Preconditions**: Connected database
- **Test Steps**:
  1. Connect to database
  2. Call await db.begin_transaction()
  3. Verify transaction is started (database-specific check)
- **Expected Result**: Transaction started
- **Coverage**: `begin_transaction()` method

#### TC-DB-027: Commit transaction successfully
- **Purpose**: Verify commit_transaction() commits changes
- **Preconditions**: Transaction in progress
- **Test Steps**:
  1. Begin transaction
  2. Execute INSERT command
  3. Call await db.commit_transaction()
  4. Verify changes are persisted
- **Expected Result**: Transaction committed, changes persisted
- **Coverage**: `commit_transaction()` method

#### TC-DB-028: Rollback transaction successfully
- **Purpose**: Verify rollback_transaction() rolls back changes
- **Preconditions**: Transaction in progress
- **Test Steps**:
  1. Begin transaction
  2. Execute INSERT command
  3. Call await db.rollback_transaction()
  4. Verify changes are not persisted
- **Expected Result**: Transaction rolled back, changes not persisted
- **Coverage**: `rollback_transaction()` method

#### TC-DB-029: Use transaction context manager successfully
- **Purpose**: Verify transaction() context manager commits on success
- **Preconditions**: Connected database
- **Test Steps**:
  1. Connect to database
  2. Use async with db.transaction():
  3. Execute multiple commands
  4. Verify all changes are committed
- **Expected Result**: Transaction committed automatically
- **Coverage**: `transaction()` context manager (success)

#### TC-DB-030: Transaction context manager rolls back on exception
- **Purpose**: Verify transaction() context manager rolls back on error
- **Preconditions**: Connected database
- **Test Steps**:
  1. Connect to database
  2. Use async with db.transaction():
  3. Execute command
  4. Raise exception
  5. Verify transaction is rolled back
- **Expected Result**: Transaction rolled back automatically on exception
- **Coverage**: `transaction()` context manager (error)

#### TC-DB-031: Nested transactions
- **Purpose**: Verify transaction() handles nested transactions
- **Preconditions**: Connected database
- **Test Steps**:
  1. Connect to database
  2. Use async with db.transaction():
  3. Use async with db.transaction(): (nested)
  4. Execute commands
  5. Verify behavior (database-specific)
- **Expected Result**: Nested transactions handled correctly
- **Coverage**: `transaction()` nested transactions

### 6. Adapter-Specific Tests

#### TC-DB-032: PostgreSQL adapter detects asyncpg
- **Purpose**: Verify PostgreSQLAdapter uses asyncpg when available
- **Preconditions**: asyncpg library installed
- **Test Steps**:
  1. Create PostgreSQLAdapter
  2. Connect to database
  3. Verify _adapter_type is "asyncpg"
- **Expected Result**: asyncpg adapter detected and used
- **Coverage**: PostgreSQLAdapter library detection

#### TC-DB-033: PostgreSQL adapter detects psycopg
- **Purpose**: Verify PostgreSQLAdapter uses psycopg when asyncpg not available
- **Preconditions**: psycopg installed, asyncpg not installed
- **Test Steps**:
  1. Mock import to simulate asyncpg missing
  2. Create PostgreSQLAdapter
  3. Connect to database
  4. Verify _adapter_type is "psycopg"
- **Expected Result**: psycopg adapter detected and used
- **Coverage**: PostgreSQLAdapter fallback detection

#### TC-DB-034: SQLite adapter uses aiosqlite
- **Purpose**: Verify SQLiteAdapter uses aiosqlite
- **Preconditions**: aiosqlite library installed
- **Test Steps**:
  1. Create SQLiteAdapter
  2. Connect to database
  3. Verify connection is aiosqlite connection
- **Expected Result**: aiosqlite connection established
- **Coverage**: SQLiteAdapter library usage

#### TC-DB-035: MySQL adapter detects aiomysql
- **Purpose**: Verify MySQLAdapter uses aiomysql when available
- **Preconditions**: aiomysql library installed
- **Test Steps**:
  1. Create MySQLAdapter
  2. Connect to database
  3. Verify _adapter_type is "aiomysql"
- **Expected Result**: aiomysql adapter detected and used
- **Coverage**: MySQLAdapter library detection

#### TC-DB-036: MySQL adapter detects pymysql
- **Purpose**: Verify MySQLAdapter uses pymysql when aiomysql not available
- **Preconditions**: pymysql installed, aiomysql not installed
- **Test Steps**:
  1. Mock import to simulate aiomysql missing
  2. Create MySQLAdapter
  3. Connect to database
  4. Verify _adapter_type is "pymysql"
- **Expected Result**: pymysql adapter detected and used
- **Coverage**: MySQLAdapter fallback detection

### 7. Edge Cases

#### TC-DB-037: Execute query with None params
- **Purpose**: Verify execute_query() handles None params
- **Preconditions**: Connected database
- **Test Steps**:
  1. Connect to database
  2. Call await db.execute_query("SELECT 1", params=None)
  3. Verify works correctly
- **Expected Result**: Query executed with empty params
- **Coverage**: `execute_query()` None params handling

#### TC-DB-038: Execute command with None params
- **Purpose**: Verify execute_command() handles None params
- **Preconditions**: Connected database
- **Test Steps**:
  1. Connect to database
  2. Call await db.execute_command("SELECT 1", params=None)
  3. Verify works correctly
- **Expected Result**: Command executed with empty params
- **Coverage**: `execute_command()` None params handling

#### TC-DB-039: Execute query with empty params dict
- **Purpose**: Verify execute_query() handles empty params dict
- **Preconditions**: Connected database
- **Test Steps**:
  1. Connect to database
  2. Call await db.execute_query("SELECT 1", params={})
  3. Verify works correctly
- **Expected Result**: Query executed with empty params
- **Coverage**: `execute_query()` empty params handling

#### TC-DB-040: Connection string parsing (SQLite)
- **Purpose**: Verify SQLiteAdapter parses connection string correctly
- **Preconditions**: SQLite connection string
- **Test Steps**:
  1. Create SQLiteAdapter with connection_string="sqlite:///path/to/db.sqlite"
  2. Verify _database_path is extracted correctly
  3. Create SQLiteAdapter with connection_string="sqlite://path/to/db.sqlite"
  4. Verify _database_path is extracted correctly
- **Expected Result**: Connection string parsed correctly
- **Coverage**: SQLiteAdapter connection string parsing

#### TC-DB-041: Multiple queries in sequence
- **Purpose**: Verify multiple queries work in sequence
- **Preconditions**: Connected database
- **Test Steps**:
  1. Connect to database
  2. Execute multiple queries in sequence
  3. Verify all queries execute successfully
- **Expected Result**: All queries execute successfully
- **Coverage**: Sequential query execution

#### TC-DB-042: Connection error handling
- **Purpose**: Verify connect() handles connection errors
- **Preconditions**: Invalid connection parameters
- **Test Steps**:
  1. Create DBClient with invalid connection_string
  2. Call await db.connect()
  3. Verify exception is raised
- **Expected Result**: Exception raised with connection error
- **Coverage**: `connect()` error handling

#### TC-DB-043: SQLiteAdapter initialization without connection_string (uses kwargs)
- **Purpose**: Verify SQLiteAdapter can be initialized without connection_string using kwargs
- **Preconditions**: Valid URL, Config, and database_path in kwargs
- **Test Steps**:
  1. Create SQLiteAdapter without connection_string, with kwargs database_path="test.db"
  2. Verify _database_path is set to "test.db"
  3. Create SQLiteAdapter without connection_string and without database_path in kwargs
  4. Verify _database_path is set to ":memory:" (default)
- **Expected Result**: SQLiteAdapter initialized correctly with kwargs, default to ":memory:" if not provided
- **Coverage**: `SQLiteAdapter.__init__()` kwargs handling (line 52)

#### TC-DB-044: SQLiteAdapter ImportError when aiosqlite is missing
- **Purpose**: Verify SQLiteAdapter raises ImportError when aiosqlite library is not available
- **Preconditions**: aiosqlite library not installed
- **Test Steps**:
  1. Mock import aiosqlite to raise ImportError
  2. Create SQLiteAdapter instance
  3. Call await adapter.connect()
  4. Verify ImportError is raised with helpful message about installing aiosqlite
- **Expected Result**: ImportError raised: "SQLite adapter requires 'aiosqlite' library. Install it with: uv add aiosqlite"
- **Coverage**: `SQLiteAdapter.connect()` ImportError handling (lines 62-63)

### 8. PostgreSQLAdapter Functional Tests

#### TC-DB-047: PostgreSQLAdapter connect() with asyncpg via connection_string
- **Purpose**: Verify PostgreSQLAdapter connects using asyncpg with connection_string
- **Preconditions**: asyncpg library available, connection_string provided
- **Test Steps**:
  1. Create PostgreSQLAdapter with connection_string
  2. Mock asyncpg.connect() to return mock connection
  3. Call await adapter.connect()
  4. Verify _adapter_type is "asyncpg"
  5. Verify _connection is set
  6. Verify _is_connected is True
- **Expected Result**: Connection established using asyncpg
- **Coverage**: `_connect_asyncpg()` with connection_string

#### TC-DB-048: PostgreSQLAdapter connect() with asyncpg via kwargs
- **Purpose**: Verify PostgreSQLAdapter connects using asyncpg with kwargs
- **Preconditions**: asyncpg library available, kwargs provided
- **Test Steps**:
  1. Create PostgreSQLAdapter without connection_string, with kwargs (host, port, database, user, password)
  2. Mock asyncpg.connect() to return mock connection
  3. Call await adapter.connect()
  4. Verify asyncpg.connect() called with correct parameters
  5. Verify _connection is set
- **Expected Result**: Connection established using asyncpg with kwargs
- **Coverage**: `_connect_asyncpg()` with kwargs

#### TC-DB-049: PostgreSQLAdapter connect() with psycopg via connection_string
- **Purpose**: Verify PostgreSQLAdapter connects using psycopg with connection_string
- **Preconditions**: psycopg library available, asyncpg not available
- **Test Steps**:
  1. Create PostgreSQLAdapter with connection_string
  2. Mock psycopg.AsyncConnection.connect() to return mock connection
  3. Mock _detect_adapter to return "psycopg"
  4. Call await adapter.connect()
  5. Verify _adapter_type is "psycopg"
  6. Verify _connection is set
- **Expected Result**: Connection established using psycopg
- **Coverage**: `_connect_psycopg()` with connection_string

#### TC-DB-050: PostgreSQLAdapter connect() with psycopg via kwargs
- **Purpose**: Verify PostgreSQLAdapter connects using psycopg with kwargs
- **Preconditions**: psycopg library available, kwargs provided
- **Test Steps**:
  1. Create PostgreSQLAdapter without connection_string, with kwargs
  2. Mock psycopg.AsyncConnection.connect() to return mock connection
  3. Mock _detect_adapter to return "psycopg"
  4. Call await adapter.connect()
  5. Verify psycopg.AsyncConnection.connect() called with correct parameters
  6. Verify _connection is set
- **Expected Result**: Connection established using psycopg with kwargs
- **Coverage**: `_connect_psycopg()` with kwargs

#### TC-DB-051: PostgreSQLAdapter disconnect() with asyncpg
- **Purpose**: Verify PostgreSQLAdapter disconnects using asyncpg
- **Preconditions**: Connected adapter with asyncpg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with asyncpg
  2. Mock connection.close()
  3. Call await adapter.disconnect()
  4. Verify connection.close() was called
  5. Verify _connection is None
  6. Verify _is_connected is False
- **Expected Result**: Connection closed, state reset
- **Coverage**: `disconnect()` with asyncpg

#### TC-DB-052: PostgreSQLAdapter disconnect() with psycopg
- **Purpose**: Verify PostgreSQLAdapter disconnects using psycopg
- **Preconditions**: Connected adapter with psycopg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with psycopg
  2. Mock connection.close()
  3. Call await adapter.disconnect()
  4. Verify connection.close() was called
  5. Verify _connection is None
- **Expected Result**: Connection closed, state reset
- **Coverage**: `disconnect()` with psycopg

#### TC-DB-053: PostgreSQLAdapter connect() when already connected (idempotency)
- **Purpose**: Verify PostgreSQLAdapter connect() is idempotent
- **Preconditions**: Already connected adapter
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter
  2. Call connect() again
  3. Verify no new connection is created
  4. Verify debug log "Already connected"
- **Expected Result**: No duplicate connection, idempotent behavior
- **Coverage**: `connect()` idempotency

#### TC-DB-054: PostgreSQLAdapter execute_query() with asyncpg
- **Purpose**: Verify PostgreSQLAdapter executes SELECT query using asyncpg
- **Preconditions**: Connected adapter with asyncpg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with asyncpg
  2. Mock connection.fetch() to return mock rows
  3. Call await adapter.execute_query("SELECT * FROM users WHERE id = $1", {"id": 1})
  4. Verify connection.fetch() called with correct query and parameters
  5. Verify returns list of dictionaries
- **Expected Result**: Query executed, results returned
- **Coverage**: `_execute_query_asyncpg()`

#### TC-DB-055: PostgreSQLAdapter execute_query() with psycopg
- **Purpose**: Verify PostgreSQLAdapter executes SELECT query using psycopg
- **Preconditions**: Connected adapter with psycopg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with psycopg
  2. Mock cursor.execute() and cursor.fetchall()
  3. Call await adapter.execute_query("SELECT * FROM users WHERE id = :id", {"id": 1})
  4. Verify cursor.execute() called with correct query and params
  5. Verify returns list of dictionaries
- **Expected Result**: Query executed, results returned
- **Coverage**: `_execute_query_psycopg()`

#### TC-DB-056: PostgreSQLAdapter execute_query() with parameters (asyncpg)
- **Purpose**: Verify PostgreSQLAdapter execute_query() handles parameters with asyncpg
- **Preconditions**: Connected adapter with asyncpg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with asyncpg
  2. Mock connection.fetch() to return mock rows
  3. Call await adapter.execute_query("SELECT * FROM users WHERE id = $1 AND name = $2", {"id": 1, "name": "Test"})
  4. Verify connection.fetch() called with positional parameters
  5. Verify results returned correctly
- **Expected Result**: Query executed with parameters
- **Coverage**: `_execute_query_asyncpg()` parameter handling

#### TC-DB-057: PostgreSQLAdapter execute_query() with parameters (psycopg)
- **Purpose**: Verify PostgreSQLAdapter execute_query() handles parameters with psycopg
- **Preconditions**: Connected adapter with psycopg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with psycopg
  2. Mock cursor.execute() and cursor.fetchall()
  3. Call await adapter.execute_query("SELECT * FROM users WHERE id = :id AND name = :name", {"id": 1, "name": "Test"})
  4. Verify cursor.execute() called with named parameters
  5. Verify results returned correctly
- **Expected Result**: Query executed with parameters
- **Coverage**: `_execute_query_psycopg()` parameter handling

#### TC-DB-058: PostgreSQLAdapter execute_query() with no results (asyncpg)
- **Purpose**: Verify PostgreSQLAdapter execute_query() returns empty list with asyncpg
- **Preconditions**: Connected adapter with asyncpg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with asyncpg
  2. Mock connection.fetch() to return empty list
  3. Call await adapter.execute_query("SELECT * FROM users WHERE id = $1", {"id": 999})
  4. Verify returns empty list []
- **Expected Result**: Empty list returned
- **Coverage**: `_execute_query_asyncpg()` empty results

#### TC-DB-059: PostgreSQLAdapter execute_query() with no results (psycopg)
- **Purpose**: Verify PostgreSQLAdapter execute_query() returns empty list with psycopg
- **Preconditions**: Connected adapter with psycopg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with psycopg
  2. Mock cursor.fetchall() to return empty list
  3. Call await adapter.execute_query("SELECT * FROM users WHERE id = :id", {"id": 999})
  4. Verify returns empty list []
- **Expected Result**: Empty list returned
- **Coverage**: `_execute_query_psycopg()` empty results

#### TC-DB-060: PostgreSQLAdapter execute_command() INSERT with asyncpg
- **Purpose**: Verify PostgreSQLAdapter executes INSERT command using asyncpg
- **Preconditions**: Connected adapter with asyncpg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with asyncpg
  2. Mock connection.execute() to return "INSERT 0 1"
  3. Call await adapter.execute_command("INSERT INTO users (name) VALUES ($1)", {"name": "Test"})
  4. Verify connection.execute() called with correct command
  5. Verify returns rowcount (1)
- **Expected Result**: Command executed, returns rowcount
- **Coverage**: `_execute_command_asyncpg()` INSERT

#### TC-DB-061: PostgreSQLAdapter execute_command() INSERT with psycopg
- **Purpose**: Verify PostgreSQLAdapter executes INSERT command using psycopg
- **Preconditions**: Connected adapter with psycopg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with psycopg
  2. Mock cursor.execute() and cursor.rowcount
  3. Call await adapter.execute_command("INSERT INTO users (name) VALUES (:name)", {"name": "Test"})
  4. Verify cursor.execute() called with correct command
  5. Verify returns rowcount
- **Expected Result**: Command executed, returns rowcount
- **Coverage**: `_execute_command_psycopg()` INSERT

#### TC-DB-062: PostgreSQLAdapter execute_command() UPDATE with asyncpg
- **Purpose**: Verify PostgreSQLAdapter executes UPDATE command using asyncpg
- **Preconditions**: Connected adapter with asyncpg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with asyncpg
  2. Mock connection.execute() to return "UPDATE 2"
  3. Call await adapter.execute_command("UPDATE users SET name = $1 WHERE id = $2", {"name": "Updated", "id": 1})
  4. Verify returns rowcount (2)
- **Expected Result**: Command executed, returns affected rows
- **Coverage**: `_execute_command_asyncpg()` UPDATE

#### TC-DB-063: PostgreSQLAdapter execute_command() UPDATE with psycopg
- **Purpose**: Verify PostgreSQLAdapter executes UPDATE command using psycopg
- **Preconditions**: Connected adapter with psycopg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with psycopg
  2. Mock cursor.execute() and cursor.rowcount = 2
  3. Call await adapter.execute_command("UPDATE users SET name = :name WHERE id = :id", {"name": "Updated", "id": 1})
  4. Verify returns rowcount (2)
- **Expected Result**: Command executed, returns affected rows
- **Coverage**: `_execute_command_psycopg()` UPDATE

#### TC-DB-064: PostgreSQLAdapter execute_command() DELETE with asyncpg
- **Purpose**: Verify PostgreSQLAdapter executes DELETE command using asyncpg
- **Preconditions**: Connected adapter with asyncpg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with asyncpg
  2. Mock connection.execute() to return "DELETE 1"
  3. Call await adapter.execute_command("DELETE FROM users WHERE id = $1", {"id": 1})
  4. Verify returns rowcount (1)
- **Expected Result**: Command executed, returns affected rows
- **Coverage**: `_execute_command_asyncpg()` DELETE

#### TC-DB-065: PostgreSQLAdapter execute_command() DELETE with psycopg
- **Purpose**: Verify PostgreSQLAdapter executes DELETE command using psycopg
- **Preconditions**: Connected adapter with psycopg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with psycopg
  2. Mock cursor.execute() and cursor.rowcount = 1
  3. Call await adapter.execute_command("DELETE FROM users WHERE id = :id", {"id": 1})
  4. Verify returns rowcount (1)
- **Expected Result**: Command executed, returns affected rows
- **Coverage**: `_execute_command_psycopg()` DELETE

#### TC-DB-066: PostgreSQLAdapter begin_transaction() with asyncpg
- **Purpose**: Verify PostgreSQLAdapter begins transaction with asyncpg
- **Preconditions**: Connected adapter with asyncpg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with asyncpg
  2. Call await adapter.begin_transaction()
  3. Verify no exception raised (asyncpg handles transactions automatically)
- **Expected Result**: Transaction can be started
- **Coverage**: `begin_transaction()` with asyncpg

#### TC-DB-067: PostgreSQLAdapter begin_transaction() with psycopg
- **Purpose**: Verify PostgreSQLAdapter begins transaction with psycopg
- **Preconditions**: Connected adapter with psycopg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with psycopg
  2. Mock connection.execute("BEGIN")
  3. Call await adapter.begin_transaction()
  4. Verify connection.execute("BEGIN") was called
- **Expected Result**: BEGIN statement executed
- **Coverage**: `begin_transaction()` with psycopg

#### TC-DB-068: PostgreSQLAdapter commit_transaction() with asyncpg
- **Purpose**: Verify PostgreSQLAdapter commits transaction with asyncpg
- **Preconditions**: Transaction in progress with asyncpg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with asyncpg
  2. Begin transaction
  3. Call await adapter.commit_transaction()
  4. Verify no exception raised (asyncpg commits automatically)
- **Expected Result**: Transaction committed
- **Coverage**: `commit_transaction()` with asyncpg

#### TC-DB-069: PostgreSQLAdapter commit_transaction() with psycopg
- **Purpose**: Verify PostgreSQLAdapter commits transaction with psycopg
- **Preconditions**: Transaction in progress with psycopg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with psycopg
  2. Begin transaction
  3. Mock connection.commit()
  4. Call await adapter.commit_transaction()
  5. Verify connection.commit() was called
- **Expected Result**: COMMIT executed
- **Coverage**: `commit_transaction()` with psycopg

#### TC-DB-070: PostgreSQLAdapter rollback_transaction() with asyncpg
- **Purpose**: Verify PostgreSQLAdapter rolls back transaction with asyncpg
- **Preconditions**: Transaction in progress with asyncpg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with asyncpg
  2. Begin transaction
  3. Call await adapter.rollback_transaction()
  4. Verify no exception raised (asyncpg doesn't have explicit rollback)
- **Expected Result**: Transaction can be rolled back (no-op for asyncpg)
- **Coverage**: `rollback_transaction()` with asyncpg

#### TC-DB-071: PostgreSQLAdapter rollback_transaction() with psycopg
- **Purpose**: Verify PostgreSQLAdapter rolls back transaction with psycopg
- **Preconditions**: Transaction in progress with psycopg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with psycopg
  2. Begin transaction
  3. Mock connection.rollback()
  4. Call await adapter.rollback_transaction()
  5. Verify connection.rollback() was called
- **Expected Result**: ROLLBACK executed
- **Coverage**: `rollback_transaction()` with psycopg

#### TC-DB-072: PostgreSQLAdapter transaction() context manager with asyncpg
- **Purpose**: Verify PostgreSQLAdapter transaction context manager with asyncpg
- **Preconditions**: Connected adapter with asyncpg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with asyncpg
  2. Use async with adapter.transaction():
  3. Execute command
  4. Verify transaction commits on success
- **Expected Result**: Transaction context manager works
- **Coverage**: `transaction()` context manager with asyncpg

#### TC-DB-073: PostgreSQLAdapter transaction() context manager with psycopg
- **Purpose**: Verify PostgreSQLAdapter transaction context manager with psycopg
- **Preconditions**: Connected adapter with psycopg
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter with psycopg
  2. Mock begin, commit, rollback
  3. Use async with adapter.transaction():
  4. Execute command
  5. Verify BEGIN and COMMIT called
- **Expected Result**: Transaction context manager works
- **Coverage**: `transaction()` context manager with psycopg

#### TC-DB-074: PostgreSQLAdapter execute_query() auto-connect
- **Purpose**: Verify PostgreSQLAdapter execute_query() auto-connects if not connected
- **Preconditions**: Adapter not connected
- **Test Steps**:
  1. Create PostgreSQLAdapter without connecting
  2. Mock connect() and connection.fetch()
  3. Call await adapter.execute_query("SELECT 1")
  4. Verify connect() was called automatically
- **Expected Result**: Auto-connection works
- **Coverage**: `execute_query()` auto-connection

#### TC-DB-075: PostgreSQLAdapter execute_command() auto-connect
- **Purpose**: Verify PostgreSQLAdapter execute_command() auto-connects if not connected
- **Preconditions**: Adapter not connected
- **Test Steps**:
  1. Create PostgreSQLAdapter without connecting
  2. Mock connect() and connection.execute()
  3. Call await adapter.execute_command("INSERT INTO users VALUES (1)")
  4. Verify connect() was called automatically
- **Expected Result**: Auto-connection works
- **Coverage**: `execute_command()` auto-connection

#### TC-DB-076: PostgreSQLAdapter execute_query() with None params
- **Purpose**: Verify PostgreSQLAdapter execute_query() handles None params
- **Preconditions**: Connected adapter
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter
  2. Mock connection.fetch() or cursor.execute()
  3. Call await adapter.execute_query("SELECT 1", params=None)
  4. Verify works correctly with empty params
- **Expected Result**: Query executed with empty params
- **Coverage**: `execute_query()` None params handling

#### TC-DB-077: PostgreSQLAdapter execute_command() with None params
- **Purpose**: Verify PostgreSQLAdapter execute_command() handles None params
- **Preconditions**: Connected adapter
- **Test Steps**:
  1. Create and connect PostgreSQLAdapter
  2. Mock connection.execute() or cursor.execute()
  3. Call await adapter.execute_command("SELECT 1", params=None)
  4. Verify works correctly with empty params
- **Expected Result**: Command executed with empty params
- **Coverage**: `execute_command()` None params handling

### 9. MySQLAdapter Functional Tests

#### TC-DB-078: MySQLAdapter connect() with aiomysql via connection_string
- **Purpose**: Verify MySQLAdapter connects using aiomysql with connection_string
- **Preconditions**: aiomysql library available, connection_string provided
- **Test Steps**:
  1. Create MySQLAdapter with connection_string
  2. Mock aiomysql.connect() to return mock connection
  3. Mock _detect_adapter to return "aiomysql"
  4. Call await adapter.connect()
  5. Verify _adapter_type is "aiomysql"
  6. Verify _connection is set
- **Expected Result**: Connection established using aiomysql
- **Coverage**: `_connect_aiomysql()` with connection_string

#### TC-DB-079: MySQLAdapter connect() with aiomysql via kwargs
- **Purpose**: Verify MySQLAdapter connects using aiomysql with kwargs
- **Preconditions**: aiomysql library available, kwargs provided
- **Test Steps**:
  1. Create MySQLAdapter without connection_string, with kwargs
  2. Mock aiomysql.connect() to return mock connection
  3. Mock _detect_adapter to return "aiomysql"
  4. Call await adapter.connect()
  5. Verify aiomysql.connect() called with correct parameters
- **Expected Result**: Connection established using aiomysql with kwargs
- **Coverage**: `_connect_aiomysql()` with kwargs

#### TC-DB-080: MySQLAdapter connect() with pymysql via kwargs
- **Purpose**: Verify MySQLAdapter connects using pymysql with kwargs
- **Preconditions**: pymysql library available, aiomysql not available
- **Test Steps**:
  1. Create MySQLAdapter without connection_string, with kwargs
  2. Mock pymysql.connect() and asyncio.run_in_executor()
  3. Mock _detect_adapter to return "pymysql"
  4. Call await adapter.connect()
  5. Verify pymysql.connect() called with correct parameters
- **Expected Result**: Connection established using pymysql
- **Coverage**: `_connect_pymysql()` with kwargs

#### TC-DB-081: MySQLAdapter disconnect() with aiomysql
- **Purpose**: Verify MySQLAdapter disconnects using aiomysql
- **Preconditions**: Connected adapter with aiomysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with aiomysql
  2. Mock connection.close() and connection.ensure_closed()
  3. Call await adapter.disconnect()
  4. Verify connection.close() and ensure_closed() were called
  5. Verify _connection is None
- **Expected Result**: Connection closed, state reset
- **Coverage**: `disconnect()` with aiomysql

#### TC-DB-082: MySQLAdapter disconnect() with pymysql
- **Purpose**: Verify MySQLAdapter disconnects using pymysql
- **Preconditions**: Connected adapter with pymysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with pymysql
  2. Mock connection.close()
  3. Call await adapter.disconnect()
  4. Verify connection.close() was called
  5. Verify _connection is None
- **Expected Result**: Connection closed, state reset
- **Coverage**: `disconnect()` with pymysql

#### TC-DB-083: MySQLAdapter connect() when already connected (idempotency)
- **Purpose**: Verify MySQLAdapter connect() is idempotent
- **Preconditions**: Already connected adapter
- **Test Steps**:
  1. Create and connect MySQLAdapter
  2. Call connect() again
  3. Verify no new connection is created
  4. Verify debug log "Already connected"
- **Expected Result**: No duplicate connection, idempotent behavior
- **Coverage**: `connect()` idempotency

#### TC-DB-084: MySQLAdapter execute_query() with aiomysql
- **Purpose**: Verify MySQLAdapter executes SELECT query using aiomysql
- **Preconditions**: Connected adapter with aiomysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with aiomysql
  2. Mock cursor.execute() and cursor.fetchall()
  3. Call await adapter.execute_query("SELECT * FROM users WHERE id = %s", {"id": 1})
  4. Verify cursor.execute() called with correct query and parameters
  5. Verify returns list of dictionaries
- **Expected Result**: Query executed, results returned
- **Coverage**: `_execute_query_aiomysql()`

#### TC-DB-085: MySQLAdapter execute_query() with pymysql
- **Purpose**: Verify MySQLAdapter executes SELECT query using pymysql
- **Preconditions**: Connected adapter with pymysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with pymysql
  2. Mock cursor.execute() and cursor.fetchall() via executor
  3. Call await adapter.execute_query("SELECT * FROM users WHERE id = %s", {"id": 1})
  4. Verify cursor.execute() called with correct query and parameters
  5. Verify returns list of dictionaries
- **Expected Result**: Query executed, results returned
- **Coverage**: `_execute_query_pymysql()`

#### TC-DB-086: MySQLAdapter execute_query() with parameters (aiomysql)
- **Purpose**: Verify MySQLAdapter execute_query() handles parameters with aiomysql
- **Preconditions**: Connected adapter with aiomysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with aiomysql
  2. Mock cursor.execute() and cursor.fetchall()
  3. Call await adapter.execute_query("SELECT * FROM users WHERE id = %s AND name = %s", {"id": 1, "name": "Test"})
  4. Verify cursor.execute() called with positional parameters
  5. Verify results returned correctly
- **Expected Result**: Query executed with parameters
- **Coverage**: `_execute_query_aiomysql()` parameter handling

#### TC-DB-087: MySQLAdapter execute_query() with parameters (pymysql)
- **Purpose**: Verify MySQLAdapter execute_query() handles parameters with pymysql
- **Preconditions**: Connected adapter with pymysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with pymysql
  2. Mock cursor.execute() and cursor.fetchall() via executor
  3. Call await adapter.execute_query("SELECT * FROM users WHERE id = %s AND name = %s", {"id": 1, "name": "Test"})
  4. Verify cursor.execute() called with positional parameters
  5. Verify results returned correctly
- **Expected Result**: Query executed with parameters
- **Coverage**: `_execute_query_pymysql()` parameter handling

#### TC-DB-088: MySQLAdapter execute_query() with no results (aiomysql)
- **Purpose**: Verify MySQLAdapter execute_query() returns empty list with aiomysql
- **Preconditions**: Connected adapter with aiomysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with aiomysql
  2. Mock cursor.fetchall() to return empty list
  3. Call await adapter.execute_query("SELECT * FROM users WHERE id = %s", {"id": 999})
  4. Verify returns empty list []
- **Expected Result**: Empty list returned
- **Coverage**: `_execute_query_aiomysql()` empty results

#### TC-DB-089: MySQLAdapter execute_query() with no results (pymysql)
- **Purpose**: Verify MySQLAdapter execute_query() returns empty list with pymysql
- **Preconditions**: Connected adapter with pymysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with pymysql
  2. Mock cursor.fetchall() to return empty list via executor
  3. Call await adapter.execute_query("SELECT * FROM users WHERE id = %s", {"id": 999})
  4. Verify returns empty list []
- **Expected Result**: Empty list returned
- **Coverage**: `_execute_query_pymysql()` empty results

#### TC-DB-090: MySQLAdapter execute_command() INSERT with aiomysql
- **Purpose**: Verify MySQLAdapter executes INSERT command using aiomysql
- **Preconditions**: Connected adapter with aiomysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with aiomysql
  2. Mock cursor.execute() and cursor.rowcount
  3. Mock connection.in_transaction = False
  4. Mock connection.commit()
  5. Call await adapter.execute_command("INSERT INTO users (name) VALUES (%s)", {"name": "Test"})
  6. Verify cursor.execute() called with correct command
  7. Verify connection.commit() called (not in transaction)
  8. Verify returns rowcount
- **Expected Result**: Command executed, returns rowcount
- **Coverage**: `_execute_command_aiomysql()` INSERT

#### TC-DB-091: MySQLAdapter execute_command() INSERT with pymysql
- **Purpose**: Verify MySQLAdapter executes INSERT command using pymysql
- **Preconditions**: Connected adapter with pymysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with pymysql
  2. Mock cursor.execute() and cursor.rowcount via executor
  3. Mock connection.commit() via executor
  4. Call await adapter.execute_command("INSERT INTO users (name) VALUES (%s)", {"name": "Test"})
  5. Verify cursor.execute() and connection.commit() called
  6. Verify returns rowcount
- **Expected Result**: Command executed, returns rowcount
- **Coverage**: `_execute_command_pymysql()` INSERT

#### TC-DB-092: MySQLAdapter execute_command() UPDATE with aiomysql
- **Purpose**: Verify MySQLAdapter executes UPDATE command using aiomysql
- **Preconditions**: Connected adapter with aiomysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with aiomysql
  2. Mock cursor.execute() and cursor.rowcount = 2
  3. Mock connection.in_transaction = False
  4. Call await adapter.execute_command("UPDATE users SET name = %s WHERE id = %s", {"name": "Updated", "id": 1})
  5. Verify returns rowcount (2)
- **Expected Result**: Command executed, returns affected rows
- **Coverage**: `_execute_command_aiomysql()` UPDATE

#### TC-DB-093: MySQLAdapter execute_command() UPDATE with pymysql
- **Purpose**: Verify MySQLAdapter executes UPDATE command using pymysql
- **Preconditions**: Connected adapter with pymysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with pymysql
  2. Mock cursor.execute() and cursor.rowcount = 2 via executor
  3. Mock connection.commit() via executor
  4. Call await adapter.execute_command("UPDATE users SET name = %s WHERE id = %s", {"name": "Updated", "id": 1})
  5. Verify returns rowcount (2)
- **Expected Result**: Command executed, returns affected rows
- **Coverage**: `_execute_command_pymysql()` UPDATE

#### TC-DB-094: MySQLAdapter execute_command() DELETE with aiomysql
- **Purpose**: Verify MySQLAdapter executes DELETE command using aiomysql
- **Preconditions**: Connected adapter with aiomysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with aiomysql
  2. Mock cursor.execute() and cursor.rowcount = 1
  3. Mock connection.in_transaction = False
  4. Call await adapter.execute_command("DELETE FROM users WHERE id = %s", {"id": 1})
  5. Verify returns rowcount (1)
- **Expected Result**: Command executed, returns affected rows
- **Coverage**: `_execute_command_aiomysql()` DELETE

#### TC-DB-095: MySQLAdapter execute_command() DELETE with pymysql
- **Purpose**: Verify MySQLAdapter executes DELETE command using pymysql
- **Preconditions**: Connected adapter with pymysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with pymysql
  2. Mock cursor.execute() and cursor.rowcount = 1 via executor
  3. Mock connection.commit() via executor
  4. Call await adapter.execute_command("DELETE FROM users WHERE id = %s", {"id": 1})
  5. Verify returns rowcount (1)
- **Expected Result**: Command executed, returns affected rows
- **Coverage**: `_execute_command_pymysql()` DELETE

#### TC-DB-096: MySQLAdapter begin_transaction() with aiomysql
- **Purpose**: Verify MySQLAdapter begins transaction with aiomysql
- **Preconditions**: Connected adapter with aiomysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with aiomysql
  2. Mock connection.begin()
  3. Call await adapter.begin_transaction()
  4. Verify connection.begin() was called
- **Expected Result**: Transaction started
- **Coverage**: `begin_transaction()` with aiomysql

#### TC-DB-097: MySQLAdapter begin_transaction() with pymysql
- **Purpose**: Verify MySQLAdapter begins transaction with pymysql
- **Preconditions**: Connected adapter with pymysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with pymysql
  2. Call await adapter.begin_transaction()
  3. Verify no exception raised (pymysql autocommit=False by default)
- **Expected Result**: Transaction can be started
- **Coverage**: `begin_transaction()` with pymysql

#### TC-DB-098: MySQLAdapter commit_transaction() with aiomysql
- **Purpose**: Verify MySQLAdapter commits transaction with aiomysql
- **Preconditions**: Transaction in progress with aiomysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with aiomysql
  2. Begin transaction
  3. Mock connection.commit()
  4. Call await adapter.commit_transaction()
  5. Verify connection.commit() was called
- **Expected Result**: Transaction committed
- **Coverage**: `commit_transaction()` with aiomysql

#### TC-DB-099: MySQLAdapter commit_transaction() with pymysql
- **Purpose**: Verify MySQLAdapter commits transaction with pymysql
- **Preconditions**: Transaction in progress with pymysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with pymysql
  2. Begin transaction
  3. Mock connection.commit()
  4. Call await adapter.commit_transaction()
  5. Verify connection.commit() was called
- **Expected Result**: Transaction committed
- **Coverage**: `commit_transaction()` with pymysql

#### TC-DB-100: MySQLAdapter rollback_transaction() with aiomysql
- **Purpose**: Verify MySQLAdapter rolls back transaction with aiomysql
- **Preconditions**: Transaction in progress with aiomysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with aiomysql
  2. Begin transaction
  3. Mock connection.rollback()
  4. Call await adapter.rollback_transaction()
  5. Verify connection.rollback() was called
- **Expected Result**: Transaction rolled back
- **Coverage**: `rollback_transaction()` with aiomysql

#### TC-DB-101: MySQLAdapter rollback_transaction() with pymysql
- **Purpose**: Verify MySQLAdapter rolls back transaction with pymysql
- **Preconditions**: Transaction in progress with pymysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with pymysql
  2. Begin transaction
  3. Mock connection.rollback()
  4. Call await adapter.rollback_transaction()
  5. Verify connection.rollback() was called
- **Expected Result**: Transaction rolled back
- **Coverage**: `rollback_transaction()` with pymysql

#### TC-DB-102: MySQLAdapter transaction() context manager with aiomysql
- **Purpose**: Verify MySQLAdapter transaction context manager with aiomysql
- **Preconditions**: Connected adapter with aiomysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with aiomysql
  2. Mock begin, commit, rollback
  3. Use async with adapter.transaction():
  4. Execute command
  5. Verify begin() and commit() called
- **Expected Result**: Transaction context manager works
- **Coverage**: `transaction()` context manager with aiomysql

#### TC-DB-103: MySQLAdapter transaction() context manager with pymysql
- **Purpose**: Verify MySQLAdapter transaction context manager with pymysql
- **Preconditions**: Connected adapter with pymysql
- **Test Steps**:
  1. Create and connect MySQLAdapter with pymysql
  2. Mock commit, rollback
  3. Use async with adapter.transaction():
  4. Execute command
  5. Verify commit() called on success
- **Expected Result**: Transaction context manager works
- **Coverage**: `transaction()` context manager with pymysql

#### TC-DB-104: MySQLAdapter execute_query() auto-connect
- **Purpose**: Verify MySQLAdapter execute_query() auto-connects if not connected
- **Preconditions**: Adapter not connected
- **Test Steps**:
  1. Create MySQLAdapter without connecting
  2. Mock connect() and cursor operations
  3. Call await adapter.execute_query("SELECT 1")
  4. Verify connect() was called automatically
- **Expected Result**: Auto-connection works
- **Coverage**: `execute_query()` auto-connection

#### TC-DB-105: MySQLAdapter execute_command() auto-connect
- **Purpose**: Verify MySQLAdapter execute_command() auto-connects if not connected
- **Preconditions**: Adapter not connected
- **Test Steps**:
  1. Create MySQLAdapter without connecting
  2. Mock connect() and cursor operations
  3. Call await adapter.execute_command("INSERT INTO users VALUES (1)")
  4. Verify connect() was called automatically
- **Expected Result**: Auto-connection works
- **Coverage**: `execute_command()` auto-connection

#### TC-DB-106: MySQLAdapter execute_query() with None params
- **Purpose**: Verify MySQLAdapter execute_query() handles None params
- **Preconditions**: Connected adapter
- **Test Steps**:
  1. Create and connect MySQLAdapter
  2. Mock cursor operations
  3. Call await adapter.execute_query("SELECT 1", params=None)
  4. Verify works correctly with empty params
- **Expected Result**: Query executed with empty params
- **Coverage**: `execute_query()` None params handling

#### TC-DB-107: MySQLAdapter execute_command() with None params
- **Purpose**: Verify MySQLAdapter execute_command() handles None params
- **Preconditions**: Connected adapter
- **Test Steps**:
  1. Create and connect MySQLAdapter
  2. Mock cursor operations
  3. Call await adapter.execute_command("SELECT 1", params=None)
  4. Verify works correctly with empty params
- **Expected Result**: Command executed with empty params
- **Coverage**: `execute_command()` None params handling

#### TC-DB-108: MySQLAdapter execute_command() in transaction (doesn't auto-commit)
- **Purpose**: Verify MySQLAdapter execute_command() doesn't auto-commit in transaction
- **Preconditions**: Connected adapter with transaction in progress
- **Test Steps**:
  1. Create and connect MySQLAdapter
  2. Begin transaction
  3. Mock connection.in_transaction = True (aiomysql) or autocommit=False (pymysql)
  4. Mock cursor.execute()
  5. Call await adapter.execute_command("INSERT INTO users (name) VALUES (%s)", {"name": "Test"})
  6. Verify connection.commit() was NOT called (in transaction)
- **Expected Result**: Command executed without auto-commit
- **Coverage**: `execute_command()` transaction handling

#### TC-DB-109: MySQLAdapter _detect_adapter() when neither aiomysql nor pymysql available
- **Purpose**: Verify MySQLAdapter _detect_adapter() raises ImportError when neither library is available
- **Preconditions**: Neither aiomysql nor pymysql installed
- **Test Steps**:
  1. Create MySQLAdapter instance
  2. Mock both aiomysql and pymysql imports to raise ImportError
  3. Call adapter._detect_adapter()
  4. Verify ImportError is raised with appropriate message
- **Expected Result**: ImportError raised: "MySQL adapter requires either 'aiomysql' or 'pymysql' library..."
- **Coverage**: `_detect_adapter()` ImportError handling (lines 51-61)

#### TC-DB-110: MySQLAdapter begin_transaction() auto-connect for pymysql
- **Purpose**: Verify MySQLAdapter begin_transaction() automatically connects when not connected (pymysql)
- **Preconditions**: MySQLAdapter with pymysql, not connected
- **Test Steps**:
  1. Create MySQLAdapter with pymysql (not connected)
  2. Mock connect() method
  3. Call await adapter.begin_transaction()
  4. Verify connect() was called before beginning transaction
- **Expected Result**: connect() called automatically, transaction begins
- **Coverage**: `begin_transaction()` auto-connect (line 221)

#### TC-DB-111: MySQLAdapter begin_transaction() auto-connect for aiomysql
- **Purpose**: Verify MySQLAdapter begin_transaction() automatically connects when not connected (aiomysql)
- **Preconditions**: MySQLAdapter with aiomysql, not connected
- **Test Steps**:
  1. Create MySQLAdapter with aiomysql (not connected)
  2. Mock connect() method
  3. Call await adapter.begin_transaction()
  4. Verify connect() was called before beginning transaction
- **Expected Result**: connect() called automatically, transaction begins
- **Coverage**: `begin_transaction()` auto-connect (line 221)

#### TC-DB-112: PostgreSQLAdapter _detect_adapter() when neither asyncpg nor psycopg available
- **Purpose**: Verify PostgreSQLAdapter _detect_adapter() raises ImportError when neither library is available
- **Preconditions**: Neither asyncpg nor psycopg installed
- **Test Steps**:
  1. Create PostgreSQLAdapter instance
  2. Mock both asyncpg and psycopg imports to raise ImportError
  3. Call adapter._detect_adapter()
  4. Verify ImportError is raised with appropriate message
- **Expected Result**: ImportError raised: "PostgreSQL adapter requires either 'asyncpg' or 'psycopg' library..."
- **Coverage**: `_detect_adapter()` ImportError handling (lines 52-62)

#### TC-DB-113: PostgreSQLAdapter begin_transaction() auto-connect for asyncpg
- **Purpose**: Verify PostgreSQLAdapter begin_transaction() automatically connects when not connected (asyncpg)
- **Preconditions**: PostgreSQLAdapter with asyncpg, not connected
- **Test Steps**:
  1. Create PostgreSQLAdapter with asyncpg (not connected)
  2. Mock connect() method
  3. Call await adapter.begin_transaction()
  4. Verify connect() was called before beginning transaction
- **Expected Result**: connect() called automatically, transaction begins
- **Coverage**: `begin_transaction()` auto-connect (line 196)

#### TC-DB-114: PostgreSQLAdapter begin_transaction() auto-connect for psycopg
- **Purpose**: Verify PostgreSQLAdapter begin_transaction() automatically connects when not connected (psycopg)
- **Preconditions**: PostgreSQLAdapter with psycopg, not connected
- **Test Steps**:
  1. Create PostgreSQLAdapter with psycopg (not connected)
  2. Mock connect() method
  3. Call await adapter.begin_transaction()
  4. Verify connect() was called before beginning transaction
- **Expected Result**: connect() called automatically, transaction begins
- **Coverage**: `begin_transaction()` auto-connect (line 196)

#### TC-DB-115: SQLiteAdapter begin_transaction() calls BEGIN
- **Purpose**: Verify SQLiteAdapter begin_transaction() executes BEGIN statement
- **Preconditions**: Connected SQLiteAdapter
- **Test Steps**:
  1. Create and connect SQLiteAdapter
  2. Mock _connection.execute()
  3. Call await adapter.begin_transaction()
  4. Verify _connection.execute("BEGIN") was called
- **Expected Result**: BEGIN statement executed
- **Coverage**: `begin_transaction()` BEGIN execution (line 113)

#### TC-DB-116: DBClient.create() with config missing api_id or api_hash
- **Purpose**: Verify DBClient.create() handles errors when config is missing api_id or api_hash
- **Preconditions**: Config object without api_id or api_hash
- **Test Steps**:
  1. Create Config without api_id or api_hash
  2. Call DBClient.create() with invalid config
  3. Verify appropriate error handling
- **Expected Result**: Error handled gracefully (ImportError or ValueError)
- **Coverage**: `create()` error handling (lines 217, 227-228)

