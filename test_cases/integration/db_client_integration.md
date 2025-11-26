# DBClient Integration Test Cases

## Overview
Tests for integration between `DBClient` and other framework components (`UserTelegramClient`, `ApiClient`, `UiClient`).

## Test Categories

### 1. UserTelegramClient + DBClient Integration

#### TC-INTEGRATION-DB-001: UserTelegramClient + DBClient Integration
- **Purpose**: Verify integration between `UserTelegramClient` and `DBClient` for storing and retrieving user data
- **Preconditions**: 
  - Valid Telegram session
  - Database connection available (SQLite, PostgreSQL, or MySQL)
  - Database schema prepared (e.g., users table)
- **Test Steps**:
  1. Connect `UserTelegramClient` with valid config
  2. Get user info from Telegram using `get_me()`
  3. Create `DBClient` instance using `DBClient.create()` with appropriate database type
  4. Connect to database using `connect()`
  5. Store user data in database using `execute_command()` (INSERT)
  6. Query user data from database using `execute_query()` (SELECT)
  7. Verify retrieved data matches Telegram user info
  8. Disconnect from database
- **Expected Result**: User data successfully stored and retrieved from database, matches Telegram user info
- **Coverage**: `UserTelegramClient.get_me()`, `DBClient.connect()`, `DBClient.execute_command()`, `DBClient.execute_query()`, `DBClient.disconnect()`
- **Dependencies**: Database setup, Telegram session, database schema

### 2. ApiClient + DBClient Integration

#### TC-INTEGRATION-DB-002: ApiClient + DBClient Integration
- **Purpose**: Verify integration between `ApiClient` and `DBClient` for database-backed API testing
- **Preconditions**: 
  - Mini App with API endpoints that query database
  - Database connection available
  - Test data in database
- **Test Steps**:
  1. Create `DBClient` instance and connect
  2. Store test data in database via `DBClient.execute_command()` (INSERT)
  3. Create `ApiClient` (or use `MiniAppApi` alias) with Mini App URL
  4. Query data via API using `ApiClient.make_request()` (GET endpoint that queries database)
  5. Verify API returns data from database
  6. Verify API response matches database data
  7. Clean up test data from database
- **Expected Result**: API successfully retrieves data stored via DBClient
- **Coverage**: `DBClient.execute_command()`, `DBClient.execute_query()`, `ApiClient.make_request()`
- **Dependencies**: Mini App with database-backed API, database connection

#### TC-INTEGRATION-DB-003: ApiClient writes to database via API
- **Purpose**: Verify data written via API is accessible via DBClient
- **Preconditions**: 
  - Mini App with API endpoints that write to database
  - Database connection available
- **Test Steps**:
  1. Create `ApiClient` and `DBClient`
  2. Connect `DBClient` to database
  3. Create data via API using `ApiClient.make_request()` (POST endpoint)
  4. Query database directly via `DBClient.execute_query()` (SELECT)
  5. Verify data written via API is present in database
  6. Verify data integrity and format
- **Expected Result**: Data written via API is correctly stored in database and accessible via DBClient
- **Coverage**: `ApiClient.make_request()` POST, `DBClient.execute_query()`
- **Dependencies**: Mini App with write API endpoints, database connection

### 3. UiClient + DBClient Integration

#### TC-INTEGRATION-DB-004: UiClient + DBClient Integration
- **Purpose**: Verify integration between `UiClient` and `DBClient` for database-backed UI testing
- **Preconditions**: 
  - Mini App with UI that displays database data
  - Database connection available
  - Test data in database
- **Test Steps**:
  1. Create `DBClient` instance and connect
  2. Store test data in database via `DBClient.execute_command()` (INSERT)
  3. Create `UiClient` (or use `MiniAppUI` alias) with Mini App URL
  4. Setup browser using `setup_browser()`
  5. Navigate to Mini App UI
  6. Verify UI displays data from database (check text content, elements)
  7. Verify data matches database content
  8. Clean up test data
- **Expected Result**: UI successfully displays data stored via DBClient
- **Coverage**: `DBClient.execute_command()`, `DBClient.execute_query()`, `UiClient` UI interactions
- **Dependencies**: Mini App with database-backed UI, database connection, browser setup

### 4. Full Workflow Integration

#### TC-INTEGRATION-DB-005: Full Workflow with DBClient
- **Purpose**: Verify complete workflow: UserTelegramClient → DBClient → ApiClient → UiClient
- **Preconditions**: 
  - Complete Mini App setup with database backend
  - All components available (UserTelegramClient, DBClient, ApiClient, UiClient)
  - Database schema prepared
- **Test Steps**:
  1. Connect `UserTelegramClient`
  2. Get user info from Telegram using `get_me()`
  3. Store user data in database via `DBClient.execute_command()`
  4. Test API endpoints that use database data via `ApiClient.make_request()`
  5. Test UI that displays database data via `UiClient` interactions
  6. Verify end-to-end data flow: Telegram → Database → API → UI
  7. Verify data consistency across all layers
  8. Clean up resources
- **Expected Result**: Complete workflow with database integration works correctly
- **Coverage**: Full integration with database across all components
- **Dependencies**: Complete Mini App with database, all components available

### 5. Transaction Integration

#### TC-INTEGRATION-DB-006: DBClient Transaction Integration
- **Purpose**: Verify database transactions work correctly in integration context
- **Preconditions**: 
  - Database connection available
  - Database with transaction support
  - Mini App with transaction-aware operations
- **Test Steps**:
  1. Create `DBClient` and connect
  2. Begin transaction using `begin_transaction()`
  3. Execute multiple commands using `execute_command()` (INSERT, UPDATE)
  4. Test API that uses transaction data (if applicable)
  5. Commit transaction using `commit_transaction()`
  6. Verify all changes persisted to database
  7. Verify API can access committed data
- **Expected Result**: Transactions work correctly in integration, all changes persisted after commit
- **Coverage**: `DBClient.begin_transaction()`, `DBClient.commit_transaction()`, `DBClient.execute_command()` in transaction
- **Dependencies**: Database with transaction support

#### TC-INTEGRATION-DB-007: DBClient Transaction Rollback
- **Purpose**: Verify transaction rollback works correctly in integration
- **Preconditions**: 
  - Database connection available
  - Database with transaction support
- **Test Steps**:
  1. Create `DBClient` and connect
  2. Begin transaction using `begin_transaction()`
  3. Execute commands using `execute_command()` (INSERT, UPDATE)
  4. Rollback transaction using `rollback_transaction()`
  5. Verify changes are NOT persisted to database
  6. Verify database state is unchanged
- **Expected Result**: Transaction rollback works correctly, no changes persisted
- **Coverage**: `DBClient.begin_transaction()`, `DBClient.rollback_transaction()`
- **Dependencies**: Database with transaction support

#### TC-INTEGRATION-DB-008: DBClient Transaction Context Manager
- **Purpose**: Verify transaction context manager works in integration
- **Preconditions**: 
  - Database connection available
  - Database with transaction support
- **Test Steps**:
  1. Create `DBClient` and connect
  2. Use transaction context manager: `async with db_client.transaction():`
  3. Execute commands within context
  4. Verify transaction commits automatically on success
  5. Test with exception within context (should rollback)
  6. Verify rollback works correctly on exception
- **Expected Result**: Transaction context manager works correctly, commits on success, rolls back on exception
- **Coverage**: `DBClient.transaction()` context manager
- **Dependencies**: Database with transaction support

### 6. Multiple Database Types

#### TC-INTEGRATION-DB-009: DBClient with Multiple Database Types
- **Purpose**: Verify `DBClient` works with different database backends in integration
- **Preconditions**: 
  - Multiple database types available (SQLite, PostgreSQL, MySQL)
  - Database adapters installed (aiosqlite, asyncpg/psycopg, aiomysql/pymysql)
- **Test Steps**:
  1. Test SQLite integration: create `DBClient.create('sqlite', ...)`, connect, execute operations
  2. Test PostgreSQL integration (if available): create `DBClient.create('postgresql', ...)`, connect, execute operations
  3. Test MySQL integration (if available): create `DBClient.create('mysql', ...)`, connect, execute operations
  4. Verify same operations work across all types
  5. Verify data format consistency
- **Expected Result**: `DBClient` works with all supported database types in integration
- **Coverage**: `DBClient.create()` with different `db_type` values, all adapters
- **Dependencies**: Multiple database backends, appropriate adapters installed

## Summary

- **Total test cases**: 9
- **Categories**: 6 (UserTelegramClient integration, ApiClient integration, UiClient integration, Full workflow, Transactions, Multiple database types)
- **Coverage**: Complete integration testing of `DBClient` with all framework components

