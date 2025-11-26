# End-to-End Test Cases

## Overview
Complete user journey tests that verify full workflows from start to finish.

## Test Categories

### 1. Complete Testing Workflows

#### TC-INTEGRATION-E2E-001: Full workflow: Get Mini App → Test API → Test UI
- **Purpose**: Verify complete testing workflow combining all components
- **Preconditions**:
  - Valid Telegram session
  - Bot with Mini App
  - Mini App with both API and UI
- **Test Steps**:
  1. Create UserTelegramClient and connect
  2. Get Mini App from bot using `get_mini_app_from_bot()`
  3. Create `ApiClient` (or use `MiniAppApi` alias) and test API endpoints
  4. Create `UiClient` (or use `MiniAppUI` alias) and test UI elements
  5. Verify both API and UI tests pass
  6. Clean up resources
- **Expected Result**: Complete workflow executes successfully
- **Coverage**: Full integration of all components
- **Dependencies**: Complete Mini App setup

#### TC-INTEGRATION-E2E-002: Full workflow with start parameter
- **Purpose**: Verify complete workflow with start parameter
- **Preconditions**: Bot supporting start parameters
- **Test Steps**:
  1. Connect UserTelegramClient
  2. Get Mini App with start_param="test123"
  3. Test API with parameterized URL
  4. Test UI and verify parameter is reflected
  5. Verify parameter is used correctly in both API and UI
- **Expected Result**: Start parameter works in full workflow
- **Coverage**: Start parameter integration
- **Dependencies**: Bot with start parameter support

#### TC-INTEGRATION-E2E-003: Multiple Mini Apps testing workflow
- **Purpose**: Verify testing multiple Mini Apps in sequence
- **Preconditions**: Multiple bots with Mini Apps
- **Test Steps**:
  1. Connect UserTelegramClient
  2. Get Mini App 1 from bot A
  3. Test Mini App 1 (API + UI)
  4. Get Mini App 2 from bot B
  5. Test Mini App 2 (API + UI)
  6. Verify both tested successfully
- **Expected Result**: Multiple Mini Apps tested successfully
- **Coverage**: Multiple Mini Apps handling
- **Dependencies**: Multiple bots with Mini Apps

### 2. Authentication Workflows

#### TC-INTEGRATION-E2E-004: Authenticate and test Mini App
- **Purpose**: Verify authentication flow with Mini App
- **Preconditions**: Mini App requiring authentication
- **Test Steps**:
  1. Connect UserTelegramClient
  2. Get Mini App from bot
  3. Get initData from Mini App
  4. Validate initData using `ApiClient` (or `MiniAppApi` alias)
  5. Use validated initData for API requests
  6. Test UI with authenticated session
- **Expected Result**: Authentication flow works correctly
- **Coverage**: Authentication integration
- **Dependencies**: Mini App with auth

#### TC-INTEGRATION-E2E-005: Session management workflow
- **Purpose**: Verify session management across components
- **Preconditions**: Config with session_string
- **Test Steps**:
  1. Create Config from session_string
  2. Create UserTelegramClient with Config
  3. Connect and verify session is used
  4. Get Mini App and test
  5. Disconnect and reconnect
  6. Verify session persists
- **Expected Result**: Session management works correctly
- **Coverage**: Session management integration
- **Dependencies**: Valid session

### 3. Data Flow Workflows

#### TC-INTEGRATION-E2E-006: Get data from bot and use in Mini App
- **Purpose**: Verify data flow from bot to Mini App
- **Preconditions**: Bot that provides data for Mini App
- **Test Steps**:
  1. Connect UserTelegramClient
  2. Get message from bot with data
  3. Extract data from message
  4. Get Mini App from bot
  5. Use data in Mini App API requests
  6. Verify data is used correctly
- **Expected Result**: Data flows correctly from bot to Mini App
- **Coverage**: Data flow integration
- **Dependencies**: Bot providing data

#### TC-INTEGRATION-E2E-007: Send data from Mini App back to bot
- **Purpose**: Verify data flow from Mini App to bot
- **Preconditions**: Mini App that sends data to bot
- **Test Steps**:
  1. Connect UserTelegramClient
  2. Get Mini App from bot
  3. Interact with Mini App UI
  4. Submit data through Mini App
  5. Check bot messages for received data
  6. Verify data was received correctly
- **Expected Result**: Data flows correctly from Mini App to bot
- **Coverage**: Reverse data flow integration
- **Dependencies**: Mini App sending data to bot

### 4. Error Recovery Workflows

#### TC-INTEGRATION-E2E-008: Recover from connection error
- **Purpose**: Verify error recovery in full workflow
- **Preconditions**: Network that can be interrupted
- **Test Steps**:
  1. Start workflow: connect, get Mini App
  2. Simulate network interruption
  3. Verify error is detected
  4. Reconnect UserTelegramClient
  5. Retry Mini App operations
  6. Verify workflow continues successfully
- **Expected Result**: Error recovery works correctly
- **Coverage**: Error recovery integration
- **Dependencies**: Network interruption simulation

#### TC-INTEGRATION-E2E-009: Sequential calls after failure
- **Purpose**: Verify that sequential make_request calls work correctly after a failure
- **Preconditions**: Mini App with API endpoint
- **Test Steps**:
  1. Connect UserTelegramClient
  2. Get Mini App from bot
  3. Create `ApiClient` (or use `MiniAppApi` alias)
  4. Simulate temporary API failure on first call
  5. Verify first call fails
  6. Make second sequential call (not automatic retry)
  7. Verify second call succeeds
- **Expected Result**: Sequential calls work correctly after failure
- **Coverage**: Sequential request handling after failure
- **Dependencies**: Mini App with API endpoint

### 5. Configuration Workflows

#### TC-INTEGRATION-E2E-010: Context manager full workflow
- **Purpose**: Verify complete workflow using context managers
- **Preconditions**: Valid config and bot
- **Test Steps**:
  1. Use `async with UserTelegramClient(config) as client:`
  2. Get Mini App from bot
  3. Use `async with ApiClient(url, config) as api:` (or `MiniAppApi` alias)
  4. Test API endpoints
  5. Use `async with UiClient(url, config) as ui:` (or `MiniAppUI` alias)
  6. Setup browser and test UI
  7. Verify all close correctly on exit
- **Expected Result**: Complete workflow works with context managers
- **Coverage**: Context manager integration
- **Dependencies**: Valid setup

#### TC-INTEGRATION-E2E-011: Load config from YAML and test
- **Purpose**: Verify config loading from YAML file
- **Preconditions**: Valid YAML config file
- **Test Steps**:
  1. Create YAML config file
  2. Create Config using `Config.from_yaml()`
  3. Create UserTelegramClient with Config
  4. Get Mini App and test
  5. Verify all components use config correctly
- **Expected Result**: Config from YAML works
- **Coverage**: YAML config loading integration
- **Dependencies**: Valid YAML file

### 6. Performance Workflows

#### TC-INTEGRATION-E2E-012: Performance test: Full workflow timing
- **Purpose**: Verify full workflow completes in acceptable time
- **Preconditions**: All components available
- **Test Steps**:
  1. Measure start time
  2. Execute full workflow (connect → get Mini App → test API → test UI)
  3. Measure end time
  4. Calculate total time
  5. Verify time is within acceptable limits
- **Expected Result**: Workflow completes in reasonable time
- **Coverage**: Performance integration
- **Dependencies**: Fast components

#### TC-INTEGRATION-E2E-013: Load test: Multiple concurrent workflows
- **Purpose**: Verify system handles concurrent workflows
- **Preconditions**: Multiple test accounts or bots
- **Test Steps**:
  1. Start 3 concurrent workflows
  2. Each workflow: connect → get Mini App → test
  3. Wait for all to complete
  4. Verify all succeed
  5. Measure total time
- **Expected Result**: Concurrent workflows handled correctly
- **Coverage**: Concurrency integration
- **Dependencies**: Multiple test setups

### 7. Resource Management Workflows

#### TC-INTEGRATION-E2E-014: Resource cleanup after workflow
- **Purpose**: Verify resources are cleaned up properly
- **Preconditions**: Full workflow setup
- **Test Steps**:
  1. Execute full workflow
  2. Verify UserTelegramClient is connected
  3. Verify `ApiClient` (or `MiniAppApi`) client is open
  4. Verify `UiClient` (or `MiniAppUI`) browser is open
  5. Exit context managers
  6. Verify all resources are closed
- **Expected Result**: All resources cleaned up
- **Coverage**: Resource management integration
- **Dependencies**: Full workflow

#### TC-INTEGRATION-E2E-015: Handle resource exhaustion
- **Purpose**: Verify handling when resources are exhausted
- **Preconditions**: Limited resources
- **Test Steps**:
  1. Open multiple browsers/clients
  2. Try to open more than limit
  3. Verify error is handled gracefully
  4. Close some resources
  5. Verify can open new resources
- **Expected Result**: Resource exhaustion handled correctly
- **Coverage**: Resource limit handling
- **Dependencies**: Resource limits

### 8. Real-World Scenarios

#### TC-INTEGRATION-E2E-016: Test real Mini App from Telegram
- **Purpose**: Verify framework works with real Telegram Mini App
- **Preconditions**: Real Telegram bot with Mini App
- **Test Steps**:
  1. Connect with real Telegram account
  2. Find real bot with Mini App
  3. Get Mini App from bot
  4. Test real API endpoints
  5. Test real UI
  6. Verify all work with real service
- **Expected Result**: Works with real Telegram Mini App
- **Coverage**: Real-world integration
- **Dependencies**: Real Telegram bot and account

#### TC-INTEGRATION-E2E-017: Test Mini App with complex UI
- **Purpose**: Verify framework handles complex UI
- **Preconditions**: Mini App with complex UI (forms, modals, etc.)
- **Test Steps**:
  1. Get Mini App from bot
  2. Setup browser and navigate
  3. Test complex form with multiple fields
  4. Test modal dialogs
  5. Test dynamic content loading
  6. Verify all interactions work
- **Expected Result**: Complex UI tested successfully
- **Coverage**: Complex UI handling
- **Dependencies**: Mini App with complex UI

#### TC-INTEGRATION-E2E-018: Test Mini App with real-time updates
- **Purpose**: Verify framework handles real-time updates
- **Preconditions**: Mini App with WebSocket or polling
- **Test Steps**:
  1. Get Mini App from bot
  2. Setup browser and navigate
  3. Wait for real-time update
  4. Verify UI updates correctly
  5. Interact with updated UI
- **Expected Result**: Real-time updates handled correctly
- **Coverage**: Real-time update handling
- **Dependencies**: Mini App with real-time features

### 9. Database Integration Workflows

#### TC-INTEGRATION-E2E-019: Database-backed Mini App testing
- **Purpose**: Verify testing Mini App with database backend using all components
- **Preconditions**: 
  - Mini App with database, API, and UI
  - Database connection available (SQLite, PostgreSQL, or MySQL)
  - Database schema prepared
- **Test Steps**:
  1. Setup database schema via `DBClient` (CREATE TABLE if needed)
  2. Seed test data via `DBClient.execute_command()` (INSERT)
  3. Connect `UserTelegramClient` and get user info
  4. Store user data in database via `DBClient`
  5. Test API endpoints that query database via `ApiClient.make_request()` (GET)
  6. Test API endpoints that write to database via `ApiClient.make_request()` (POST)
  7. Verify API responses match database data via `DBClient.execute_query()`
  8. Test UI that displays database data via `UiClient` interactions
  9. Verify UI content matches database data
  10. Verify data consistency across all layers (Database ↔ API ↔ UI)
  11. Clean up test data from database
- **Expected Result**: Database-backed Mini App tested successfully with all components
- **Coverage**: `DBClient` + `ApiClient` + `UiClient` + `UserTelegramClient` integration
- **Dependencies**: Complete Mini App with database, all components available, database schema
