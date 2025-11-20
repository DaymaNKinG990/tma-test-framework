# MTProto + MiniAppApi Integration Test Cases

## Overview
Tests for integration between `UserTelegramClient` and `MiniAppApi` components.

## Test Categories

### 1. Get Mini App and Test API

#### TC-INTEGRATION-MTAPI-001: Get Mini App from bot and test API endpoint
- **Purpose**: Verify complete flow: get Mini App from bot, then test its API
- **Preconditions**:
  - Valid Telegram session
  - Bot that responds with Mini App URL
  - Mini App with accessible API endpoint
- **Test Steps**:
  1. Create UserTelegramClient with valid config
  2. Connect to Telegram
  3. Call `get_mini_app_from_bot(bot_username)`
  4. Verify MiniAppUI is returned with correct URL
  5. Create MiniAppApi from the URL
  6. Test API endpoint using `make_request()`
  7. Verify response is valid
- **Expected Result**: Mini App retrieved and API tested successfully
- **Coverage**: `get_mini_app_from_bot()`, `MiniAppApi.make_request()`
- **Dependencies**: Real Telegram bot, Mini App with API

#### TC-INTEGRATION-MTAPI-002: Get Mini App with start_param and test API
- **Purpose**: Verify Mini App retrieval with start parameter
- **Preconditions**: Bot that accepts start parameters
- **Test Steps**:
  1. Connect UserTelegramClient
  2. Call `get_mini_app_from_bot(bot_username, start_param="123")`
  3. Verify Mini App URL contains start parameter
  4. Test API with the parameterized URL
- **Expected Result**: Mini App retrieved with start param, API works
- **Coverage**: `get_mini_app_from_bot()` with start_param
- **Dependencies**: Bot supporting start parameters

#### TC-INTEGRATION-MTAPI-003: Get Mini App from media and test API
- **Purpose**: Verify Mini App retrieval from message media
- **Preconditions**: Bot that sends Mini App in media
- **Test Steps**:
  1. Connect UserTelegramClient
  2. Get messages from bot
  3. Find message with web_app media
  4. Extract Mini App URL from media
  5. Create MiniAppApi and test endpoints
- **Expected Result**: Mini App extracted from media, API tested
- **Coverage**: `get_mini_app_from_bot()` media extraction
- **Dependencies**: Bot with web_app media

### 2. Validate InitData Integration

#### TC-INTEGRATION-MTAPI-004: Get initData from bot and validate
- **Purpose**: Verify initData validation in integration context
- **Preconditions**: Bot that provides initData
- **Test Steps**:
  1. Get Mini App from bot
  2. Receive initData from bot or Mini App
  3. Use MiniAppApi.validate_init_data()
  4. Verify validation succeeds
- **Expected Result**: initData validated successfully
- **Coverage**: `validate_init_data()` in real scenario
- **Dependencies**: Bot providing initData

#### TC-INTEGRATION-MTAPI-005: Validate initData with different bot tokens
- **Purpose**: Verify initData validation with multiple bots
- **Preconditions**: Multiple bots with different tokens
- **Test Steps**:
  1. Get initData from bot A
  2. Validate with bot A token (should succeed)
  3. Validate with bot B token (should fail)
- **Expected Result**: Validation works correctly with correct token
- **Coverage**: `validate_init_data()` security
- **Dependencies**: Multiple bots

### 3. API Testing Scenarios

#### TC-INTEGRATION-MTAPI-006: Test GET endpoint after getting Mini App
- **Purpose**: Verify GET request to Mini App API
- **Preconditions**: Mini App with GET endpoint
- **Test Steps**:
  1. Get Mini App from bot
  2. Create MiniAppApi
  3. Call `make_request("/api/status", method="GET")`
  4. Verify response status and data
- **Expected Result**: GET request successful
- **Coverage**: `make_request()` GET method
- **Dependencies**: Mini App with GET endpoint

#### TC-INTEGRATION-MTAPI-007: Test POST endpoint with data
- **Purpose**: Verify POST request with JSON data
- **Preconditions**: Mini App with POST endpoint
- **Test Steps**:
  1. Get Mini App from bot
  2. Create MiniAppApi
  3. Call `make_request("/api/data", method="POST", data={"key": "value"})`
  4. Verify response
- **Expected Result**: POST request successful with data
- **Coverage**: `make_request()` POST method
- **Dependencies**: Mini App with POST endpoint

#### TC-INTEGRATION-MTAPI-008: Test multiple API endpoints
- **Purpose**: Verify testing multiple endpoints in sequence
- **Preconditions**: Mini App with multiple endpoints
- **Test Steps**:
  1. Get Mini App from bot
  2. Create MiniAppApi
  3. Test endpoint 1: `/api/status`
  4. Test endpoint 2: `/api/data`
  5. Test endpoint 3: `/api/users`
  6. Verify all responses
- **Expected Result**: All endpoints tested successfully
- **Coverage**: Multiple `make_request()` calls
- **Dependencies**: Mini App with multiple endpoints

#### TC-INTEGRATION-MTAPI-009: Test API with authentication
- **Purpose**: Verify API requests with authentication headers
- **Preconditions**: Mini App requiring authentication
- **Test Steps**:
  1. Get Mini App from bot
  2. Get auth token from bot or initData
  3. Create MiniAppApi
  4. Call `make_request()` with auth headers
  5. Verify authenticated request succeeds
- **Expected Result**: Authenticated request successful
- **Coverage**: `make_request()` with headers
- **Dependencies**: Mini App with auth

### 4. Error Handling Integration

#### TC-INTEGRATION-MTAPI-010: Handle bot not responding
- **Purpose**: Verify error handling when bot doesn't respond
- **Preconditions**: Invalid bot or bot that doesn't respond
- **Test Steps**:
  1. Connect UserTelegramClient
  2. Call `get_mini_app_from_bot("nonexistent_bot")`
  3. Verify error is handled gracefully
  4. Verify returns None or raises appropriate exception
- **Expected Result**: Error handled, no crash
- **Coverage**: Error handling in `get_mini_app_from_bot()`
- **Dependencies**: Nonexistent bot

#### TC-INTEGRATION-MTAPI-011: Handle Mini App API errors
- **Purpose**: Verify error handling for API failures
- **Preconditions**: Mini App with failing endpoint
- **Test Steps**:
  1. Get Mini App from bot
  2. Create MiniAppApi
  3. Call `make_request()` to failing endpoint
  4. Verify error is caught and returned in ApiResult
- **Expected Result**: Error handled, ApiResult with error_message
- **Coverage**: Error handling in `make_request()`
- **Dependencies**: Mini App with failing endpoint

#### TC-INTEGRATION-MTAPI-012: Handle network timeout
- **Purpose**: Verify timeout handling in integration
- **Preconditions**: Mini App with slow endpoint
- **Test Steps**:
  1. Get Mini App from bot
  2. Create MiniAppApi with short timeout
  3. Call `make_request()` to slow endpoint
  4. Verify timeout is handled
- **Expected Result**: Timeout handled gracefully
- **Coverage**: Timeout handling
- **Dependencies**: Slow endpoint or timeout simulation

### 5. Context Manager Integration

#### TC-INTEGRATION-MTAPI-013: Use context manager for full flow
- **Purpose**: Verify context manager usage in integration
- **Preconditions**: Valid config and bot
- **Test Steps**:
  1. Use `async with UserTelegramClient(config) as client:`
  2. Get Mini App from bot
  3. Use `async with MiniAppApi(url, config) as api:`
  4. Test API endpoints
  5. Verify both close correctly on exit
- **Expected Result**: Both clients close properly
- **Coverage**: Context managers integration
- **Dependencies**: Valid setup

### 6. Performance Integration

#### TC-INTEGRATION-MTAPI-014: Test multiple API calls performance
- **Purpose**: Verify performance with multiple requests
- **Preconditions**: Mini App with fast endpoints
- **Test Steps**:
  1. Get Mini App from bot
  2. Create MiniAppApi
  3. Make 10 sequential API calls
  4. Measure total time
  5. Verify all succeed
- **Expected Result**: All requests complete in reasonable time
- **Coverage**: Performance with multiple requests
- **Dependencies**: Fast endpoints

#### TC-INTEGRATION-MTAPI-015: Test concurrent API calls
- **Purpose**: Verify concurrent request handling
- **Preconditions**: Mini App supporting concurrent requests
- **Test Steps**:
  1. Get Mini App from bot
  2. Create MiniAppApi
  3. Make 5 concurrent API calls using asyncio.gather
  4. Verify all complete
- **Expected Result**: Concurrent requests handled correctly
- **Coverage**: Concurrent request handling
- **Dependencies**: Mini App supporting concurrency
