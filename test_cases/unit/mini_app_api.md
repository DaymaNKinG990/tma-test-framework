# MiniAppApi Class - Unit Test Cases

## Overview
Tests for `tma_test_framework.mini_app.api.MiniAppApi` class - HTTP API client for Telegram Mini Apps.

## Test Categories

### 1. Initialization Tests

#### TC-API-001: Initialize MiniAppApi with URL and config
- **Purpose**: Verify MiniAppApi can be initialized with URL and Config
- **Preconditions**: Valid URL and Config object
- **Test Steps**:
  1. Create MiniAppApi(url, config)
  2. Verify url, config, and client are initialized
  3. Verify AsyncClient is created with correct timeout
- **Expected Result**: MiniAppApi created with httpx.AsyncClient initialized
- **Coverage**: `__init__` method

#### TC-API-002: Initialize MiniAppApi with config=None raises error
- **Purpose**: Verify MiniAppApi rejects None config with TypeError
- **Preconditions**: Valid URL, config=None
- **Test Steps**:
  1. Create MiniAppApi(url, config=None)
  2. Verify TypeError is raised
- **Expected Result**: TypeError raised (Config is required)
- **Coverage**: `__init__` validation

#### TC-API-003: Verify AsyncClient is initialized with correct timeout
- **Purpose**: Verify client uses config.timeout
- **Preconditions**: Config with custom timeout
- **Test Steps**:
  1. Create Config with timeout=60
  2. Create MiniAppApi with this config
  3. Verify client timeout matches config
- **Expected Result**: AsyncClient timeout equals config.timeout
- **Coverage**: Client initialization with timeout

#### TC-API-004: Verify AsyncClient limits are set correctly
- **Purpose**: Verify client has correct connection limits
- **Preconditions**: MiniAppApi instance
- **Test Steps**:
  1. Create MiniAppApi
  2. Verify client limits: max_keepalive_connections=5, max_connections=10
- **Expected Result**: Connection limits set correctly
- **Coverage**: Client limits configuration

### 2. Close Method Tests

#### TC-API-005: Close MiniAppApi client
- **Purpose**: Verify close() closes AsyncClient
- **Preconditions**: MiniAppApi instance with active client
- **Test Steps**:
  1. Create MiniAppApi
  2. Call await api.close()
  3. Verify client.aclose() was called
- **Expected Result**: AsyncClient closed successfully
- **Coverage**: `close()` method

#### TC-API-006: Close MiniAppApi multiple times
- **Purpose**: Verify close() can be called multiple times safely
- **Preconditions**: MiniAppApi instance
- **Test Steps**:
  1. Create MiniAppApi
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
- **Preconditions**: MiniAppApi with base URL, relative endpoint
- **Test Steps**:
  1. Create MiniAppApi with base URL
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
  1. Create MiniAppApi with URL="https://example.com/app?start=123"
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
