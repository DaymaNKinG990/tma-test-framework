# MTProto + ApiClient Authentication Integration Test Cases

## Overview
Tests for integration between `UserTelegramClient` and `ApiClient.setup_tma_auth()` method, which provides automated TMA authentication setup.

## Test Categories

### 1. Basic setup_tma_auth Integration

#### TC-INTEGRATION-AUTH-001: setup_tma_auth with UserTelegramClient
- **Purpose**: Verify `setup_tma_auth` integrates with UserTelegramClient to automatically get user info
- **Preconditions**: 
  - Valid Telegram session
  - Mini App with user creation endpoint (`v1/create/tma/`)
  - Valid `bot_token` in config
- **Test Steps**:
  1. Connect `UserTelegramClient` with valid config
  2. Create `ApiClient` (or use `MiniAppApi` alias) with Mini App URL
  3. Call `setup_tma_auth()` without `user_info` parameter (should get from UserTelegramClient)
  4. Verify `UserTelegramClient.get_me()` is called internally
  5. Verify user is created via API endpoint
  6. Verify `init_data` token is generated and set via `set_auth_token()`
  7. Verify authenticated API requests work with the token
- **Expected Result**: `setup_tma_auth` successfully creates user and sets auth token automatically
- **Coverage**: `ApiClient.setup_tma_auth()`, `UserTelegramClient.get_me()`, `ApiClient.set_auth_token()`
- **Dependencies**: Mini App with user creation endpoint, valid Telegram session

#### TC-INTEGRATION-AUTH-002: setup_tma_auth with existing user
- **Purpose**: Verify `setup_tma_auth` handles existing user gracefully (400 response)
- **Preconditions**: 
  - User already exists in Mini App database
  - Valid Telegram session
  - Valid `bot_token` in config
- **Test Steps**:
  1. Connect `UserTelegramClient`
  2. Create `ApiClient`
  3. Call `setup_tma_auth()` (user already exists)
  4. Verify API returns 400 (BAD_REQUEST) status
  5. Verify 400 response is handled gracefully (no exception raised)
  6. Verify `init_data` token is still generated and set
  7. Verify authenticated API requests work despite 400 response
- **Expected Result**: `setup_tma_auth` handles existing user correctly, sets token anyway
- **Coverage**: `ApiClient.setup_tma_auth()` error handling for 400 status
- **Dependencies**: Mini App with existing user, valid Telegram session

#### TC-INTEGRATION-AUTH-003: setup_tma_auth with provided user_info
- **Purpose**: Verify `setup_tma_auth` works with explicitly provided `user_info` parameter
- **Preconditions**: 
  - Valid `UserInfo` object from `UserTelegramClient`
  - Mini App with user creation endpoint
  - Valid `bot_token` in config
- **Test Steps**:
  1. Connect `UserTelegramClient`
  2. Get `UserInfo` from `UserTelegramClient.get_me()`
  3. Create `ApiClient`
  4. Call `setup_tma_auth(user_info=user_info)` with provided user_info
  5. Verify `UserTelegramClient` is NOT called internally (user_info provided)
  6. Verify user is created via API with provided user_info
  7. Verify `init_data` token is generated and set
- **Expected Result**: `setup_tma_auth` works with provided user_info, skips UserTelegramClient call
- **Coverage**: `ApiClient.setup_tma_auth()` with `user_info` parameter
- **Dependencies**: Mini App with user creation endpoint, valid Telegram session

### 2. Advanced setup_tma_auth Options

#### TC-INTEGRATION-AUTH-004: setup_tma_auth without creating user
- **Purpose**: Verify `setup_tma_auth` can skip user creation and only set auth token
- **Preconditions**: 
  - User already exists or user creation not needed
  - Valid Telegram session
  - Valid `bot_token` in config
- **Test Steps**:
  1. Connect `UserTelegramClient`
  2. Create `ApiClient`
  3. Call `setup_tma_auth(create_user=False)`
  4. Verify user creation API call is NOT made
  5. Verify `init_data` token is still generated and set
  6. Verify authenticated API requests work with the token
- **Expected Result**: `setup_tma_auth` sets auth token without creating user
- **Coverage**: `ApiClient.setup_tma_auth()` with `create_user=False` parameter
- **Dependencies**: Valid Telegram session, valid `bot_token`

#### TC-INTEGRATION-AUTH-005: setup_tma_auth with custom endpoint
- **Purpose**: Verify `setup_tma_auth` works with custom user creation endpoint
- **Preconditions**: 
  - Mini App with custom user creation endpoint (e.g., `/api/users/create`)
  - Valid Telegram session
  - Valid `bot_token` in config
- **Test Steps**:
  1. Connect `UserTelegramClient`
  2. Create `ApiClient`
  3. Call `setup_tma_auth(create_user_endpoint="/api/users/create")`
  4. Verify user creation API call is made to custom endpoint
  5. Verify `init_data` token is generated and set
  6. Verify authenticated API requests work
- **Expected Result**: `setup_tma_auth` works with custom endpoint
- **Coverage**: `ApiClient.setup_tma_auth()` with `create_user_endpoint` parameter
- **Dependencies**: Mini App with custom user creation endpoint

### 3. Error Handling

#### TC-INTEGRATION-AUTH-006: setup_tma_auth error handling
- **Purpose**: Verify `setup_tma_auth` handles various error conditions correctly
- **Preconditions**: 
  - Various error conditions can be simulated
- **Test Steps**:
  1. Test with `config=None` (should raise `ValueError`)
  2. Test with missing `bot_token` in config (should handle gracefully)
  3. Test with `UserTelegramClient` connection failure (should raise `ValueError` with message)
  4. Test with API endpoint failure (non-400/201 status, should raise exception)
  5. Test with invalid `user_info` (if applicable)
  6. Verify all errors are handled gracefully with appropriate exceptions
- **Expected Result**: All error cases are handled correctly with appropriate exceptions
- **Coverage**: `ApiClient.setup_tma_auth()` error handling for all error paths
- **Dependencies**: Ability to simulate various error conditions

### 4. Full Authentication Workflow

#### TC-INTEGRATION-AUTH-007: Full authentication workflow with setup_tma_auth
- **Purpose**: Verify complete authentication workflow using `setup_tma_auth` in real scenario
- **Preconditions**: 
  - Valid Telegram session
  - Mini App with authentication required
  - Valid `bot_token` in config
- **Test Steps**:
  1. Connect `UserTelegramClient`
  2. Get Mini App from bot using `get_mini_app_from_bot()`
  3. Create `ApiClient` with Mini App URL
  4. Call `setup_tma_auth()` to authenticate
  5. Test authenticated API endpoints (should work with token)
  6. Test authenticated UI interactions (if applicable)
  7. Verify complete authentication flow works end-to-end
- **Expected Result**: Complete authentication workflow works with `setup_tma_auth`
- **Coverage**: Full authentication integration using `setup_tma_auth`
- **Dependencies**: Mini App with authentication, valid Telegram session

## Summary

- **Total test cases**: 7
- **Categories**: 4 (Basic integration, Advanced options, Error handling, Full workflow)
- **Coverage**: Complete integration testing of `ApiClient.setup_tma_auth()` with `UserTelegramClient`

