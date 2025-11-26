# ApiClient Class - Unit Test Cases

## Overview
Tests for `tma_test_framework.clients.api_client.ApiClient` class - HTTP API client for Telegram Mini Apps.

## Test Categories

### 1. Initialization Tests

#### TC-API-001: Initialize ApiClient with URL and config
- **Purpose**: Verify ApiClient can be initialized with URL and Config
- **Preconditions**: Valid URL and Config object
- **Test Steps**:
  1. Create ApiClient(url, config)
  2. Verify url, config, and client are initialized
  3. Verify AsyncClient is created with correct timeout
- **Expected Result**: ApiClient created with httpx.AsyncClient initialized
- **Coverage**: `__init__` method

#### TC-API-002: Initialize ApiClient with config=None raises error
- **Purpose**: Verify ApiClient rejects None config with ValueError
- **Preconditions**: Valid URL, config=None
- **Test Steps**:
  1. Create ApiClient(url, config=None)
  2. Verify ValueError is raised
- **Expected Result**: ValueError raised (Config is required)
- **Coverage**: `__init__` validation

#### TC-API-003: Verify AsyncClient is initialized with correct timeout
- **Purpose**: Verify client uses config.timeout
- **Preconditions**: Config with custom timeout
- **Test Steps**:
  1. Create Config with timeout=60
  2. Create ApiClient with this config
  3. Verify client timeout matches config
- **Expected Result**: AsyncClient timeout equals config.timeout
- **Coverage**: Client initialization with timeout

#### TC-API-004: Verify AsyncClient limits are set correctly
- **Purpose**: Verify client has correct connection limits
- **Preconditions**: ApiClient instance
- **Test Steps**:
  1. Create ApiClient
  2. Verify client limits: max_keepalive_connections=5, max_connections=10
- **Expected Result**: Connection limits set correctly
- **Coverage**: Client limits configuration

### 2. Close Method Tests

#### TC-API-005: Close ApiClient client
- **Purpose**: Verify close() closes AsyncClient
- **Preconditions**: ApiClient instance with active client
- **Test Steps**:
  1. Create ApiClient
  2. Call await api.close()
  3. Verify client.aclose() was called
- **Expected Result**: AsyncClient closed successfully
- **Coverage**: `close()` method

#### TC-API-006: Close ApiClient multiple times
- **Purpose**: Verify close() can be called multiple times safely
- **Preconditions**: ApiClient instance
- **Test Steps**:
  1. Create ApiClient
  2. Call close() multiple times
- **Expected Result**: No errors, idempotent behavior
- **Coverage**: `close()` idempotency

### 3. validate_init_data() Tests

#### TC-API-007: Validate valid init_data
- **Purpose**: Verify validate_init_data() returns True for valid data
- **Preconditions**: Valid init_data string and bot_token
- **Test Steps**:
  1. Generate valid init_data with correct hash
  2. Call validate_init_data(init_data, bot_token)
  3. Verify returns True
- **Expected Result**: Returns True, logs "InitData validation: valid"
- **Coverage**: `validate_init_data()` success path

#### TC-API-008: Reject invalid init_data (wrong hash)
- **Purpose**: Verify validate_init_data() returns False for invalid hash
- **Preconditions**: init_data with incorrect hash
- **Test Steps**:
  1. Create init_data with wrong hash
  2. Call validate_init_data()
  3. Verify returns False
- **Expected Result**: Returns False, logs "InitData validation: invalid"
- **Coverage**: `validate_init_data()` invalid hash

#### TC-API-009: Reject init_data without hash parameter
- **Purpose**: Verify validate_init_data() returns False when hash is missing
- **Preconditions**: init_data without hash parameter
- **Test Steps**:
  1. Create init_data without hash
  2. Call validate_init_data()
  3. Verify returns False
- **Expected Result**: Returns False immediately
- **Coverage**: `validate_init_data()` missing hash check

#### TC-API-010: Reject empty init_data
- **Purpose**: Verify validate_init_data() returns False for empty string
- **Preconditions**: init_data = ""
- **Test Steps**:
  1. Call validate_init_data("", bot_token)
  2. Verify returns False
- **Expected Result**: Returns False immediately
- **Coverage**: `validate_init_data()` empty check

#### TC-API-011: Reject empty bot_token
- **Purpose**: Verify validate_init_data() returns False for empty token
- **Preconditions**: bot_token = ""
- **Test Steps**:
  1. Call validate_init_data(init_data, "")
  2. Verify returns False
- **Expected Result**: Returns False immediately
- **Coverage**: `validate_init_data()` empty token check

#### TC-API-012: Reject both empty init_data and bot_token
- **Purpose**: Verify validate_init_data() handles both empty
- **Preconditions**: Both parameters empty
- **Test Steps**:
  1. Call validate_init_data("", "")
  2. Verify returns False
- **Expected Result**: Returns False immediately
- **Coverage**: `validate_init_data()` both empty

#### TC-API-013: Handle hash at beginning of init_data
- **Purpose**: Verify hash removal works when hash is first parameter
- **Preconditions**: init_data with hash at start: "hash=abc&user=test"
- **Test Steps**:
  1. Create init_data with hash first
  2. Call validate_init_data()
  3. Verify hash is removed correctly
- **Expected Result**: Hash removed, validation proceeds
- **Coverage**: `validate_init_data()` hash removal (beginning)

#### TC-API-014: Handle hash in middle of init_data
- **Purpose**: Verify hash removal works when hash is in middle
- **Preconditions**: init_data with hash in middle: "user=test&hash=abc&auth_date=123"
- **Test Steps**:
  1. Create init_data with hash in middle
  2. Call validate_init_data()
  3. Verify hash is removed correctly
- **Expected Result**: Hash removed, validation proceeds
- **Coverage**: `validate_init_data()` hash removal (middle)

#### TC-API-015: Handle hash at end of init_data
- **Purpose**: Verify hash removal works when hash is last parameter
- **Preconditions**: init_data with hash at end: "user=test&hash=abc"
- **Test Steps**:
  1. Create init_data with hash at end
  2. Call validate_init_data()
  3. Verify hash is removed correctly
- **Expected Result**: Hash removed, validation proceeds
- **Coverage**: `validate_init_data()` hash removal (end)

#### TC-API-016: Verify validate_init_data uses compare_digest
- **Purpose**: Verify timing attack protection with compare_digest
- **Preconditions**: Valid init_data
- **Test Steps**:
  1. Mock hmac.compare_digest
  2. Call validate_init_data()
  3. Verify compare_digest was called (not ==)
- **Expected Result**: compare_digest used for hash comparison
- **Coverage**: `validate_init_data()` security (timing attack protection)

#### TC-API-017: Handle exception in validate_init_data
- **Purpose**: Verify exception handling returns False and logs error
- **Preconditions**: init_data that causes exception
- **Test Steps**:
  1. Mock hmac.new to raise exception
  2. Call validate_init_data()
  3. Verify returns False and logs error
- **Expected Result**: Returns False, logs "InitData validation failed: {e}"
- **Coverage**: `validate_init_data()` exception handling

#### TC-API-018: Validate init_data with unicode characters
- **Purpose**: Verify validate_init_data handles unicode
- **Preconditions**: init_data with unicode in values
- **Test Steps**:
  1. Create init_data with unicode
  2. Call validate_init_data()
  3. Verify works correctly
- **Expected Result**: Validation works with unicode
- **Coverage**: Unicode handling

#### TC-API-019: Validate init_data with special characters
- **Purpose**: Verify validate_init_data handles special chars
- **Preconditions**: init_data with &, =, etc.
- **Test Steps**:
  1. Create init_data with special characters
  2. Call validate_init_data()
  3. Verify works correctly
- **Expected Result**: Validation works with special characters
- **Coverage**: Special character handling

### 4. make_request() Tests

#### TC-API-020: Make GET request to relative endpoint
- **Purpose**: Verify make_request() constructs URL correctly for relative paths
- **Preconditions**: ApiClient with base URL, relative endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Call make_request("/api/status")
  3. Verify URL is constructed: base_url + "/api/status"
- **Expected Result**: Request made to correct URL
- **Coverage**: `make_request()` URL construction (relative)

#### TC-API-021: Make GET request to absolute URL
- **Purpose**: Verify make_request() uses absolute URL as-is
- **Preconditions**: Absolute URL endpoint
- **Test Steps**:
  1. Call make_request("https://example.com/api")
  2. Verify absolute URL is used directly
- **Expected Result**: Request made to absolute URL
- **Coverage**: `make_request()` URL construction (absolute)

#### TC-API-022: Make GET request with relative URL starting with slash
- **Purpose**: Verify URL construction handles leading slash
- **Preconditions**: Endpoint starting with "/"
- **Test Steps**:
  1. Call make_request("/api/status")
  2. Verify URL doesn't have double slashes
- **Expected Result**: URL constructed correctly without double slashes
- **Coverage**: `make_request()` URL construction (slash handling)

#### TC-API-023: Make GET request with relative URL without slash
- **Purpose**: Verify URL construction handles missing leading slash
- **Preconditions**: Endpoint without leading "/"
- **Test Steps**:
  1. Call make_request("api/status")
  2. Verify URL has single slash between base and endpoint
- **Expected Result**: URL constructed correctly with single slash
- **Coverage**: `make_request()` URL construction (no leading slash)

#### TC-API-024: Make GET request and verify response
- **Purpose**: Verify make_request() returns ApiResult with correct data
- **Preconditions**: Mock HTTP response with status 200
- **Test Steps**:
  1. Mock client.request to return 200 response
  2. Call make_request("/api/status")
  3. Verify ApiResult has correct status_code, success=True
- **Expected Result**: ApiResult with status_code=200, success=True
- **Coverage**: `make_request()` response handling (GET)

#### TC-API-025: Make POST request with data
- **Purpose**: Verify make_request() sends POST with JSON data
- **Preconditions**: POST method and data dict
- **Test Steps**:
  1. Mock client.request
  2. Call make_request("/api/data", method="POST", data={"key": "value"})
  3. Verify request made with POST and JSON data
- **Expected Result**: POST request with JSON body
- **Coverage**: `make_request()` POST with data

#### TC-API-026: Make request with custom headers
- **Purpose**: Verify make_request() sends custom headers
- **Preconditions**: Headers dict
- **Test Steps**:
  1. Mock client.request
  2. Call make_request("/api", headers={"Authorization": "Bearer token"})
  3. Verify headers are sent
- **Expected Result**: Request includes custom headers
- **Coverage**: `make_request()` headers

#### TC-API-027: Make request and verify response_time is recorded
- **Purpose**: Verify ApiResult includes response_time
- **Preconditions**: Mock response with elapsed time
- **Test Steps**:
  1. Mock response.elapsed.total_seconds() = 0.5
  2. Call make_request()
  3. Verify ApiResult.response_time = 0.5
- **Expected Result**: response_time recorded correctly
- **Coverage**: `make_request()` response_time

#### TC-API-038: Handle response_time when elapsed is unavailable
- **Purpose**: Verify make_request() handles case when response.elapsed is not available
- **Preconditions**: Response where elapsed raises AttributeError or RuntimeError
- **Test Steps**:
  1. Mock response.elapsed to raise AttributeError or RuntimeError
  2. Call make_request()
  3. Verify ApiResult.response_time = 0.0
  4. Verify no exception is raised
- **Expected Result**: ApiResult with response_time=0.0, no exception
- **Coverage**: `make_request()` response_time exception handling

#### TC-API-028: Make request and verify response data is extracted to immutable fields
- **Purpose**: Verify response data is extracted into immutable fields of ApiResult
- **Preconditions**: Mock response
- **Test Steps**:
  1. Mock response object
  2. Call make_request()
  3. Verify ApiResult has headers and body as immutable fields (not response object)
  4. Verify response object is not stored in ApiResult
- **Expected Result**: Response data extracted to immutable fields (headers, body), response object not stored
- **Coverage**: `make_request()` response data extraction

#### TC-API-029: Handle request exception
- **Purpose**: Verify make_request() handles exceptions gracefully
- **Preconditions**: client.request raises exception
- **Test Steps**:
  1. Mock client.request to raise exception
  2. Call make_request()
  3. Verify returns ApiResult with success=False, error_message set
- **Expected Result**: ApiResult with success=False, error_message, status_code=0
- **Coverage**: `make_request()` exception handling

#### TC-API-030: Verify make_request logs request
- **Purpose**: Verify request is logged
- **Preconditions**: Logger capture
- **Test Steps**:
  1. Call make_request("/api/status")
  2. Verify "Making request: GET {url}" is logged
- **Expected Result**: Request logged at INFO level
- **Coverage**: `make_request()` logging (request)

#### TC-API-031: Verify make_request logs response
- **Purpose**: Verify response is logged
- **Preconditions**: Logger capture, mock response
- **Test Steps**:
  1. Mock response
  2. Call make_request()
  3. Verify response details are logged
- **Expected Result**: Response logged with status_code, elapsed, content
- **Coverage**: `make_request()` logging (response)

#### TC-API-032: Verify make_request logs error on exception
- **Purpose**: Verify errors are logged
- **Preconditions**: Exception during request
- **Test Steps**:
  1. Mock exception
  2. Call make_request()
  3. Verify error is logged
- **Expected Result**: Error logged: "Request failed: {method} {endpoint} - {error}"
- **Coverage**: `make_request()` logging (error)

#### TC-API-033: Make request with different HTTP methods
- **Purpose**: Verify all HTTP methods work
- **Preconditions**: Different methods
- **Test Steps**:
  1. Call make_request with method="GET"
  2. Call make_request with method="POST"
  3. Call make_request with method="PUT"
  4. Call make_request with method="DELETE"
- **Expected Result**: All methods work correctly
- **Coverage**: `make_request()` HTTP methods

#### TC-API-034: Make request and verify status code flags
- **Purpose**: Verify ApiResult flags are set based on status code
- **Preconditions**: Different status codes
- **Test Steps**:
  1. Mock response with status_code=200, verify success=True
  2. Mock response with status_code=301, verify redirect=True
  3. Mock response with status_code=404, verify client_error=True
  4. Mock response with status_code=500, verify server_error=True
  5. Mock response with status_code=101, verify informational=True
- **Expected Result**: Correct flags set for each status code
- **Coverage**: `make_request()` status code flags

#### TC-API-035: Make request with base URL containing query params
- **Purpose**: Verify query params are removed from base URL
- **Preconditions**: Base URL with query params
- **Test Steps**:
  1. Create ApiClient with URL="https://example.com/app?start=123"
  2. Call make_request("/api/status")
  3. Verify base URL query params are removed
- **Expected Result**: URL constructed without base query params
- **Coverage**: `make_request()` URL construction (query params removal)

### 5. Edge Cases

#### TC-API-036: Make request with very long endpoint
- **Purpose**: Verify make_request handles long endpoints
- **Preconditions**: Very long endpoint string
- **Test Steps**:
  1. Call make_request with very long endpoint
- **Expected Result**: Request works correctly
- **Coverage**: Large data handling

#### TC-API-037: Make request with unicode in endpoint
- **Purpose**: Verify make_request handles unicode
- **Preconditions**: Endpoint with unicode characters
- **Test Steps**:
  1. Call make_request with unicode endpoint
- **Expected Result**: Request works correctly
- **Coverage**: Unicode handling

### 6. Authentication Token Management Tests

#### TC-API-039: Initialize ApiClient with default auth token values
- **Purpose**: Verify ApiClient initializes with default auth token values
- **Preconditions**: Valid URL and Config object
- **Test Steps**:
  1. Create ApiClient(url, config)
  2. Verify _auth_token is None
  3. Verify _auth_token_type is "Bearer"
- **Expected Result**: Default values: _auth_token=None, _auth_token_type="Bearer"
- **Coverage**: `__init__` auth token initialization

#### TC-API-040: Set authentication token with default type
- **Purpose**: Verify set_auth_token sets token with default Bearer type
- **Preconditions**: ApiClient instance
- **Test Steps**:
  1. Call set_auth_token("test_token_123")
  2. Verify _auth_token equals "test_token_123"
  3. Verify _auth_token_type equals "Bearer"
- **Expected Result**: Token and type are set correctly
- **Coverage**: `set_auth_token()` method

#### TC-API-041: Set authentication token with custom type
- **Purpose**: Verify set_auth_token accepts custom token type
- **Preconditions**: ApiClient instance
- **Test Steps**:
  1. Call set_auth_token("api_key_456", "ApiKey")
  2. Verify _auth_token equals "api_key_456"
  3. Verify _auth_token_type equals "ApiKey"
- **Expected Result**: Token and custom type are set correctly
- **Coverage**: `set_auth_token()` with custom type

#### TC-API-042: Clear authentication token
- **Purpose**: Verify clear_auth_token resets token to None
- **Preconditions**: ApiClient instance with token set
- **Test Steps**:
  1. Call set_auth_token("test_token")
  2. Verify _auth_token is set
  3. Call clear_auth_token()
  4. Verify _auth_token is None
  5. Verify _auth_token_type is reset to "Bearer"
- **Expected Result**: Token cleared, type reset to default
- **Coverage**: `clear_auth_token()` method

#### TC-API-043: Make request automatically adds auth token to headers
- **Purpose**: Verify make_request automatically adds Authorization header when token is set
- **Preconditions**: ApiClient instance with token set
- **Test Steps**:
  1. Call set_auth_token("test_token_123")
  2. Call make_request("/api/data")
  3. Verify Authorization header is present in request
  4. Verify Authorization header value is "Bearer test_token_123"
- **Expected Result**: Authorization header automatically added to request
- **Coverage**: `make_request()` automatic token injection

#### TC-API-044: Make request without token does not add Authorization header
- **Purpose**: Verify make_request does not add Authorization header when token is not set
- **Preconditions**: ApiClient instance without token
- **Test Steps**:
  1. Call make_request("/api/data") without setting token
  2. Verify Authorization header is not present in request headers
- **Expected Result**: No Authorization header in request
- **Coverage**: `make_request()` without token

#### TC-API-045: Make request uses custom token type
- **Purpose**: Verify make_request uses custom token type in Authorization header
- **Preconditions**: ApiClient instance with custom token type
- **Test Steps**:
  1. Call set_auth_token("api_key_456", "ApiKey")
  2. Call make_request("/api/data")
  3. Verify Authorization header value is "ApiKey api_key_456"
- **Expected Result**: Authorization header uses custom token type
- **Coverage**: `make_request()` with custom token type

#### TC-API-046: Make request allows overriding Authorization header
- **Purpose**: Verify make_request allows overriding Authorization header in headers parameter
- **Preconditions**: ApiClient instance with token set
- **Test Steps**:
  1. Call set_auth_token("default_token")
  2. Call make_request("/api/data", headers={"Authorization": "Bearer custom_token"})
  3. Verify Authorization header in request is "Bearer custom_token" (not default)
- **Expected Result**: Custom Authorization header overrides automatic token
- **Coverage**: `make_request()` header override

#### TC-API-047: Make request merges custom headers with auth token
- **Purpose**: Verify make_request merges custom headers with automatically added token
- **Preconditions**: ApiClient instance with token set
- **Test Steps**:
  1. Call set_auth_token("test_token")
  2. Call make_request("/api/data", headers={"X-Custom-Header": "custom_value"})
  3. Verify Authorization header is present
  4. Verify X-Custom-Header is present
- **Expected Result**: Both Authorization and custom headers are present
- **Coverage**: `make_request()` header merging

#### TC-API-048: Make request sets Content-Type for requests with data
- **Purpose**: Verify make_request automatically sets Content-Type when data is provided
- **Preconditions**: ApiClient instance
- **Test Steps**:
  1. Call make_request("/api/data", method="POST", data={"key": "value"})
  2. Verify Content-Type header is "application/json"
- **Expected Result**: Content-Type automatically set to application/json
- **Coverage**: `make_request()` Content-Type handling

#### TC-API-049: Make request preserves custom Content-Type header
- **Purpose**: Verify make_request preserves custom Content-Type if provided
- **Preconditions**: ApiClient instance
- **Test Steps**:
  1. Call make_request("/api/data", method="POST", data={"key": "value"}, headers={"Content-Type": "application/xml"})
  2. Verify Content-Type header is "application/xml" (not overridden)
- **Expected Result**: Custom Content-Type is preserved
- **Coverage**: `make_request()` Content-Type override

### 7. Query Parameters Tests

#### TC-API-050: Make request with query parameters
- **Purpose**: Verify make_request adds query params to URL
- **Preconditions**: ApiClient instance
- **Test Steps**:
  1. Call make_request("/api/data", params={"page": 1, "limit": 10})
  2. Verify URL contains query parameters: "?page=1&limit=10" or "?limit=10&page=1"
- **Expected Result**: Query parameters are added to URL
- **Coverage**: `make_request()` query params handling

#### TC-API-051: Make request with query params and existing query string
- **Purpose**: Verify make_request appends query params to URL with existing query string
- **Preconditions**: ApiClient instance, endpoint with existing query params
- **Test Steps**:
  1. Call make_request("https://example.com/api/data?existing=param", params={"filter": "active"})
  2. Verify URL contains both existing and new query params
  3. Verify separator is "&" (not "?")
- **Expected Result**: Query params are appended with "&" separator
- **Coverage**: `make_request()` query params appending

#### TC-API-052: Make request with empty params dict
- **Purpose**: Verify make_request handles empty params dict gracefully
- **Preconditions**: ApiClient instance
- **Test Steps**:
  1. Call make_request("/api/data", params={})
  2. Verify URL does not contain "?" or query params
- **Expected Result**: Empty params dict does not add query string to URL
- **Coverage**: `make_request()` empty params handling

### 8. TMA Authentication Setup (setup_tma_auth)

#### TC-API-053: Setup TMA auth with user_info and create_user=True
- **Purpose**: Verify setup_tma_auth() creates user and sets init_data token
- **Preconditions**: ApiClient instance, UserInfo object, valid config
- **Test Steps**:
  1. Create ApiClient instance
  2. Mock make_request to return 201 (CREATED)
  3. Call await setup_tma_auth(user_info, config, create_user=True)
  4. Verify make_request was called with POST to "v1/create/tma/"
  5. Verify auth token is set with type "tma"
- **Expected Result**: User created, init_data token set
- **Coverage**: `setup_tma_auth()` with user_info

#### TC-API-054: Setup TMA auth with user_info and create_user=False
- **Purpose**: Verify setup_tma_auth() skips user creation when create_user=False
- **Preconditions**: ApiClient instance, UserInfo object, valid config
- **Test Steps**:
  1. Create ApiClient instance
  2. Call await setup_tma_auth(user_info, config, create_user=False)
  3. Verify make_request was NOT called
  4. Verify auth token is set with type "tma"
- **Expected Result**: User not created, init_data token set
- **Coverage**: `setup_tma_auth()` with create_user=False

#### TC-API-055: Setup TMA auth without user_info (gets from UserTelegramClient)
- **Purpose**: Verify setup_tma_auth() gets user_info from UserTelegramClient when not provided
- **Preconditions**: ApiClient instance, valid config with MTProto credentials
- **Test Steps**:
  1. Create ApiClient instance
  2. Mock UserTelegramClient to return UserInfo
  3. Mock make_request to return 201
  4. Call await setup_tma_auth(config=config, user_info=None)
  5. Verify UserTelegramClient was used to get user_info
  6. Verify auth token is set
- **Expected Result**: User info obtained from Telegram, user created, token set
- **Coverage**: `setup_tma_auth()` without user_info

#### TC-API-056: Setup TMA auth with custom endpoint
- **Purpose**: Verify setup_tma_auth() uses custom create_user_endpoint
- **Preconditions**: ApiClient instance, UserInfo object, valid config
- **Test Steps**:
  1. Create ApiClient instance
  2. Mock make_request to return 201
  3. Call await setup_tma_auth(user_info, config, create_user_endpoint="v1/custom/endpoint/")
  4. Verify make_request was called with POST to "v1/custom/endpoint/"
- **Expected Result**: Custom endpoint used for user creation
- **Coverage**: `setup_tma_auth()` with custom endpoint

#### TC-API-057: Setup TMA auth with config=None raises error
- **Purpose**: Verify setup_tma_auth() raises ValueError when config is None
- **Preconditions**: ApiClient instance, UserInfo object
- **Test Steps**:
  1. Create ApiClient instance
  2. Call await setup_tma_auth(user_info, config=None)
  3. Verify ValueError is raised with message about config
- **Expected Result**: ValueError raised: "config is required for generating init_data"
- **Coverage**: `setup_tma_auth()` validation

#### TC-API-058: Setup TMA auth fails when UserTelegramClient cannot get user_info
- **Purpose**: Verify setup_tma_auth() raises ValueError when UserTelegramClient fails
- **Preconditions**: ApiClient instance, config without valid MTProto credentials
- **Test Steps**:
  1. Create ApiClient instance
  2. Mock UserTelegramClient to raise exception
  3. Call await setup_tma_auth(config=config, user_info=None)
  4. Verify ValueError is raised with error message
- **Expected Result**: ValueError raised: "Failed to get user info from Telegram: ..."
- **Coverage**: `setup_tma_auth()` error handling (UserTelegramClient)

#### TC-API-059: Setup TMA auth handles user already exists (400 status)
- **Purpose**: Verify setup_tma_auth() handles 400 status (user already exists) gracefully
- **Preconditions**: ApiClient instance, UserInfo object, valid config
- **Test Steps**:
  1. Create ApiClient instance
  2. Mock make_request to return 400 (BAD_REQUEST)
  3. Call await setup_tma_auth(user_info, config, create_user=True)
  4. Verify no exception is raised
  5. Verify auth token is still set
- **Expected Result**: No exception, auth token set (400 is acceptable)
- **Coverage**: `setup_tma_auth()` handling user already exists

#### TC-API-060: Setup TMA auth raises error on user creation failure
- **Purpose**: Verify setup_tma_auth() raises error when user creation fails (non-400/201 status)
- **Preconditions**: ApiClient instance, UserInfo object, valid config
- **Test Steps**:
  1. Create ApiClient instance
  2. Mock make_request to return 500 (SERVER_ERROR)
  3. Call await setup_tma_auth(user_info, config, create_user=True)
  4. Verify exception is raised
- **Expected Result**: Exception raised (from raise_for_status)
- **Coverage**: `setup_tma_auth()` error handling (user creation)

#### TC-API-061: Setup TMA auth generates correct init_data
- **Purpose**: Verify setup_tma_auth() generates init_data with correct user data
- **Preconditions**: ApiClient instance, UserInfo object, valid config with bot_token
- **Test Steps**:
  1. Create ApiClient instance
  2. Mock make_request to return 201
  3. Mock generate_telegram_init_data to verify it's called with correct params
  4. Call await setup_tma_auth(user_info, config)
  5. Verify generate_telegram_init_data called with user_info fields
- **Expected Result**: init_data generated with correct user data
- **Coverage**: `setup_tma_auth()` init_data generation

#### TC-API-062: Setup TMA auth sets token type to "tma"
- **Purpose**: Verify setup_tma_auth() sets auth token with type "tma"
- **Preconditions**: ApiClient instance, UserInfo object, valid config
- **Test Steps**:
  1. Create ApiClient instance
  2. Mock make_request to return 201
  3. Call await setup_tma_auth(user_info, config)
  4. Verify _auth_token_type is "tma"
  5. Verify _auth_token is set (init_data string)
- **Expected Result**: Auth token type is "tma", token is init_data
- **Coverage**: `setup_tma_auth()` token type

