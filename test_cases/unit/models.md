# Mini App Models - Unit Test Cases

## Overview
Tests for data models in `tma_test_framework.clients.models`:
- `MiniAppInfo` - Mini App information structure
- `ApiResult` - API request result structure

## MiniAppInfo Test Cases

### 1. Initialization Tests

#### TC-MODEL-MINIAPP-001: Create MiniAppInfo with required URL
- **Purpose**: Verify MiniAppInfo can be created with only URL
- **Preconditions**: Valid URL string
- **Test Steps**:
  1. Create MiniAppInfo(url="https://example.com/app")
  2. Verify url is set
  3. Verify defaults: start_param=None, theme_params=None, platform="web"
- **Expected Result**: MiniAppInfo created with defaults
- **Coverage**: `__init__` with defaults

#### TC-MODEL-MINIAPP-002: Create MiniAppInfo with all parameters
- **Purpose**: Verify MiniAppInfo accepts all parameters
- **Preconditions**: All parameters provided
- **Test Steps**:
  1. Create MiniAppInfo with url, start_param, theme_params, platform
  2. Verify all attributes are set correctly
- **Expected Result**: MiniAppInfo created with all parameters
- **Coverage**: `__init__` with all parameters

#### TC-MODEL-MINIAPP-003: Create MiniAppInfo with start_param
- **Purpose**: Verify start_param is stored correctly
- **Preconditions**: URL and start_param
- **Test Steps**:
  1. Create MiniAppInfo with start_param
  2. Verify start_param attribute
- **Expected Result**: start_param stored correctly
- **Coverage**: start_param parameter

#### TC-MODEL-MINIAPP-004: Create MiniAppInfo with theme_params
- **Purpose**: Verify theme_params dict is stored correctly
- **Preconditions**: URL and theme_params dict
- **Test Steps**:
  1. Create MiniAppInfo with theme_params={"bg_color": "#fff"}
  2. Verify theme_params attribute
- **Expected Result**: theme_params stored correctly
- **Coverage**: theme_params parameter

#### TC-MODEL-MINIAPP-005: Create MiniAppInfo with different platform
- **Purpose**: Verify platform parameter works
- **Preconditions**: URL and platform value
- **Test Steps**:
  1. Create MiniAppInfo with platform="mobile"
  2. Verify platform attribute
- **Expected Result**: platform stored correctly
- **Coverage**: platform parameter

### 2. Type Validation Tests

#### TC-MODEL-MINIAPP-006: Verify MiniAppInfo accepts None for optional fields
- **Purpose**: Verify None values are accepted for optional fields
- **Preconditions**: URL with None optional params
- **Test Steps**:
  1. Create MiniAppInfo with start_param=None, theme_params=None
- **Expected Result**: MiniAppInfo created successfully
- **Coverage**: Optional None handling

#### TC-MODEL-MINIAPP-007: Verify MiniAppInfo stores types as-is (msgspec behavior)
- **Purpose**: Verify msgspec doesn't convert types at creation time
- **Preconditions**: Invalid type for url
- **Test Steps**:
  1. Create MiniAppInfo(url=123)
  2. Verify url is stored as int (not converted)
- **Expected Result**: url stored as int (msgspec doesn't validate at creation)
- **Coverage**: Type handling (msgspec behavior)

### 3. Immutability Tests

#### TC-MODEL-MINIAPP-008: Verify MiniAppInfo is frozen (immutable)
- **Purpose**: Verify MiniAppInfo cannot be modified after creation
- **Preconditions**: Valid MiniAppInfo instance
- **Test Steps**:
  1. Create MiniAppInfo
  2. Attempt to modify url attribute
- **Expected Result**: AttributeError raised: "immutable type: 'MiniAppInfo'"
- **Coverage**: Frozen struct behavior

#### TC-MODEL-MINIAPP-009: Verify MiniAppInfo is hashable
- **Purpose**: Verify MiniAppInfo can be used in sets/dicts when all fields contain hashable types
- **Preconditions**: Two MiniAppInfo objects with same values, theme_params contains only hashable types (e.g., strings, numbers, tuples of hashable types)
- **Test Steps**:
  1. Create two MiniAppInfo with identical values, ensuring theme_params contains only hashable types (e.g., {"bg_color": "#fff", "text_color": "#000"})
  2. Verify hash(app1) == hash(app2)
  3. Use as dict key: {app1: "value"}
  4. Verify both objects can be added to a set
- **Expected Result**: MiniAppInfo is hashable when all fields (including theme_params) contain hashable types. Objects with same values produce same hash and can be used as dict keys and in sets.
- **Coverage**: Hashable behavior with hashable field types

### 4. Equality Tests

#### TC-MODEL-MINIAPP-010: Verify MiniAppInfo equality with same values
- **Purpose**: Verify two MiniAppInfo with same values are equal
- **Preconditions**: Two MiniAppInfo with identical attributes
- **Test Steps**:
  1. Create two MiniAppInfo with same values
  2. Verify app1 == app2
- **Expected Result**: Objects are equal
- **Coverage**: Equality comparison

#### TC-MODEL-MINIAPP-011: Verify MiniAppInfo inequality with different values
- **Purpose**: Verify two MiniAppInfo with different values are not equal
- **Preconditions**: Two MiniAppInfo with different URLs
- **Test Steps**:
  1. Create two MiniAppInfo with different URLs
  2. Verify app1 != app2
- **Expected Result**: Objects are not equal
- **Coverage**: Inequality comparison

### 5. Edge Cases

#### TC-MODEL-MINIAPP-012: Create MiniAppInfo with empty URL
- **Purpose**: Verify MiniAppInfo handles empty URL
- **Preconditions**: URL = ""
- **Test Steps**:
  1. Create MiniAppInfo with empty URL
- **Expected Result**: MiniAppInfo created (validation may be elsewhere)
- **Coverage**: Empty string handling

#### TC-MODEL-MINIAPP-013: Create MiniAppInfo with empty theme_params dict
- **Purpose**: Verify MiniAppInfo accepts empty dict
- **Preconditions**: theme_params = {}
- **Test Steps**:
  1. Create MiniAppInfo with empty theme_params
- **Expected Result**: MiniAppInfo created successfully
- **Coverage**: Empty dict handling

#### TC-MODEL-MINIAPP-014: Create MiniAppInfo with unicode in URL
- **Purpose**: Verify MiniAppInfo handles unicode characters
- **Preconditions**: URL with unicode characters
- **Test Steps**:
  1. Create MiniAppInfo with unicode URL
- **Expected Result**: MiniAppInfo created successfully
- **Coverage**: Unicode handling

## ApiResult Test Cases

### 1. Initialization Tests

#### TC-MODEL-API-001: Create ApiResult with required parameters
- **Purpose**: Verify ApiResult can be created with required fields
- **Preconditions**: All required parameters
- **Test Steps**:
  1. Create ApiResult with endpoint, method, status_code, response_time, success flags
  2. Verify all attributes are set
- **Expected Result**: ApiResult created successfully
- **Coverage**: `__init__` with required parameters

#### TC-MODEL-API-002: Create ApiResult with all parameters
- **Purpose**: Verify ApiResult accepts all parameters including optional
- **Preconditions**: All parameters including response and error_message
- **Test Steps**:
  1. Create ApiResult with all parameters
  2. Verify all attributes including optional ones
- **Expected Result**: ApiResult created with all parameters
- **Coverage**: `__init__` with all parameters

#### TC-MODEL-API-003: Create ApiResult with None optional parameters
- **Purpose**: Verify ApiResult accepts None for optional fields
- **Preconditions**: response=None, error_message=None
- **Test Steps**:
  1. Create ApiResult with None optional params
- **Expected Result**: ApiResult created successfully
- **Coverage**: Optional None handling

#### TC-MODEL-API-004: Create ApiResult with response object
- **Purpose**: Verify ApiResult stores Response object
- **Preconditions**: httpx.Response object
- **Test Steps**:
  1. Create ApiResult with response parameter
  2. Verify response attribute
- **Expected Result**: response stored correctly
- **Coverage**: response parameter

#### TC-MODEL-API-005: Create ApiResult with error_message
- **Purpose**: Verify ApiResult stores error message
- **Preconditions**: error_message string
- **Test Steps**:
  1. Create ApiResult with error_message
  2. Verify error_message attribute
- **Expected Result**: error_message stored correctly
- **Coverage**: error_message parameter

### 2. Status Code Tests

#### TC-MODEL-API-006: Create ApiResult with different status codes
- **Purpose**: Verify ApiResult handles various HTTP status codes
- **Preconditions**: Different status codes
- **Test Steps**:
  1. Create ApiResult with status_code=200 (success)
  2. Create ApiResult with status_code=301 (redirect)
  3. Create ApiResult with status_code=404 (client error)
  4. Create ApiResult with status_code=500 (server error)
  5. Create ApiResult with status_code=101 (informational)
  6. Verify success flags are set correctly
- **Expected Result**: Each status code sets appropriate flags
- **Coverage**: Status code flag logic

#### TC-MODEL-API-007: Verify success flag for 2xx status codes
- **Purpose**: Verify is_success flag is True for 2xx
- **Preconditions**: status_code in 200-299
- **Test Steps**:
  1. Create ApiResult with status_code=200
  2. Verify success=True
- **Expected Result**: success flag is True
- **Coverage**: Success flag logic

#### TC-MODEL-API-008: Verify redirect flag for 3xx status codes
- **Purpose**: Verify is_redirect flag is True for 3xx
- **Preconditions**: status_code in 300-399
- **Test Steps**:
  1. Create ApiResult with status_code=301
  2. Verify redirect=True
- **Expected Result**: redirect flag is True
- **Coverage**: Redirect flag logic

#### TC-MODEL-API-009: Verify client_error flag for 4xx status codes
- **Purpose**: Verify is_client_error flag is True for 4xx
- **Preconditions**: status_code in 400-499
- **Test Steps**:
  1. Create ApiResult with status_code=404
  2. Verify client_error=True
- **Expected Result**: client_error flag is True
- **Coverage**: Client error flag logic

#### TC-MODEL-API-010: Verify server_error flag for 5xx status codes
- **Purpose**: Verify is_server_error flag is True for 5xx
- **Preconditions**: status_code in 500-599
- **Test Steps**:
  1. Create ApiResult with status_code=500
  2. Verify server_error=True
- **Expected Result**: server_error flag is True
- **Coverage**: Server error flag logic

#### TC-MODEL-API-011: Verify informational flag for 1xx status codes
- **Purpose**: Verify is_informational flag is True for 1xx
- **Preconditions**: status_code in 100-199
- **Test Steps**:
  1. Create ApiResult with status_code=101
  2. Verify informational=True
- **Expected Result**: informational flag is True
- **Coverage**: Informational flag logic

### 3. Type Validation Tests

#### TC-MODEL-API-012: Verify ApiResult stores types as-is (msgspec behavior)
- **Purpose**: Verify msgspec doesn't convert types at creation time
- **Preconditions**: Invalid types for status_code, response_time
- **Test Steps**:
  1. Create ApiResult with status_code="200" (string)
  2. Create ApiResult with response_time="fast" (string)
  3. Verify types are stored as-is
- **Expected Result**: Types stored as provided (msgspec behavior)
- **Coverage**: Type handling (msgspec behavior)

### 4. Immutability Tests

#### TC-MODEL-API-013: Verify ApiResult is frozen (immutable)
- **Purpose**: Verify ApiResult cannot be modified after creation
- **Preconditions**: Valid ApiResult instance
- **Test Steps**:
  1. Create ApiResult
  2. Attempt to modify endpoint attribute
- **Expected Result**: AttributeError raised: "immutable type: 'ApiResult'"
- **Coverage**: Frozen struct behavior

#### TC-MODEL-API-014: Verify ApiResult is hashable when response is None
- **Purpose**: Verify ApiResult can be used in sets/dicts only when response is None (since httpx.Response is not hashable)
- **Preconditions**: Two ApiResult objects with same values, response=None
- **Test Steps**:
  1. Create two ApiResult with identical values, ensuring response=None
  2. Verify hash(result1) == hash(result2)
  3. Use as dict key: {result1: "value"}
  4. Verify both objects can be added to a set
- **Expected Result**: ApiResult is hashable when response is None. Objects with same values produce same hash and can be used as dict keys and in sets. When response contains httpx.Response (which is not hashable), hashing will raise TypeError.
- **Coverage**: Hashable behavior when response is None

### 5. Equality Tests

#### TC-MODEL-API-015: Verify ApiResult equality with same values
- **Purpose**: Verify two ApiResult with same values are equal
- **Preconditions**: Two ApiResult with identical attributes
- **Test Steps**:
  1. Create two ApiResult with same values
  2. Verify result1 == result2
- **Expected Result**: Objects are equal
- **Coverage**: Equality comparison

#### TC-MODEL-API-016: Verify ApiResult inequality with different values
- **Purpose**: Verify two ApiResult with different values are not equal
- **Preconditions**: Two ApiResult with different endpoints
- **Test Steps**:
  1. Create two ApiResult with different endpoints
  2. Verify result1 != result2
- **Expected Result**: Objects are not equal
- **Coverage**: Inequality comparison

### 6. Edge Cases

#### TC-MODEL-API-017: Create ApiResult with zero status_code
- **Purpose**: Verify ApiResult handles status_code=0 (error case)
- **Preconditions**: status_code=0
- **Test Steps**:
  1. Create ApiResult with status_code=0
- **Expected Result**: ApiResult created (used for error cases)
- **Coverage**: Zero status code handling

#### TC-MODEL-API-018: Create ApiResult with zero response_time
- **Purpose**: Verify ApiResult handles response_time=0
- **Preconditions**: response_time=0.0
- **Test Steps**:
  1. Create ApiResult with response_time=0.0
- **Expected Result**: ApiResult created successfully
- **Coverage**: Zero response time handling

#### TC-MODEL-API-019: Create ApiResult with very large response_time
- **Purpose**: Verify ApiResult handles large response times
- **Preconditions**: response_time=999.999
- **Test Steps**:
  1. Create ApiResult with large response_time
- **Expected Result**: ApiResult created successfully
- **Coverage**: Large number handling

#### TC-MODEL-API-020: Create ApiResult with empty strings
- **Purpose**: Verify ApiResult handles empty strings
- **Preconditions**: endpoint="", method=""
- **Test Steps**:
  1. Create ApiResult with empty strings
- **Expected Result**: ApiResult created successfully
- **Coverage**: Empty string handling

#### TC-MODEL-API-021: Create ApiResult with unicode in error_message
- **Purpose**: Verify ApiResult handles unicode in error messages
- **Preconditions**: error_message with unicode
- **Test Steps**:
  1. Create ApiResult with unicode error_message
- **Expected Result**: ApiResult created successfully
- **Coverage**: Unicode handling

### 7. ApiResult Methods Tests

#### TC-MODEL-API-022: ApiResult.json() parses valid JSON
- **Purpose**: Verify json() method parses JSON from response body
- **Preconditions**: ApiResult with valid JSON in body
- **Test Steps**:
  1. Create ApiResult with body containing valid JSON: b'{"key": "value", "number": 123}'
  2. Call result.json()
  3. Verify returned dict matches JSON content
- **Expected Result**: json() returns parsed dictionary
- **Coverage**: `json()` method

#### TC-MODEL-API-023: ApiResult.json() raises ValueError for invalid JSON
- **Purpose**: Verify json() method raises ValueError for invalid JSON
- **Preconditions**: ApiResult with invalid JSON in body
- **Test Steps**:
  1. Create ApiResult with body containing invalid JSON: b"not valid json"
  2. Call result.json()
- **Expected Result**: ValueError raised with message "Failed to parse JSON"
- **Coverage**: `json()` error handling

#### TC-MODEL-API-024: ApiResult.text() returns decoded body
- **Purpose**: Verify text() method returns body as UTF-8 string
- **Preconditions**: ApiResult with text body
- **Test Steps**:
  1. Create ApiResult with body: b"Hello, World!"
  2. Call result.text()
  3. Verify returned string is "Hello, World!"
- **Expected Result**: text() returns decoded string
- **Coverage**: `text()` method

#### TC-MODEL-API-025: ApiResult.text() handles decode errors gracefully
- **Purpose**: Verify text() method handles invalid UTF-8 sequences
- **Preconditions**: ApiResult with invalid UTF-8 in body
- **Test Steps**:
  1. Create ApiResult with body containing invalid UTF-8: b"\xff\xfe\x00\x01"
  2. Call result.text()
  3. Verify method does not raise exception, returns string with replacement characters
- **Expected Result**: text() returns string without raising exception
- **Coverage**: `text()` error handling

#### TC-MODEL-API-026: ApiResult.raise_for_status() does not raise for success
- **Purpose**: Verify raise_for_status() does not raise for 2xx status codes
- **Preconditions**: ApiResult with status_code=200
- **Test Steps**:
  1. Create ApiResult with status_code=200
  2. Call result.raise_for_status()
- **Expected Result**: No exception raised
- **Coverage**: `raise_for_status()` success handling

#### TC-MODEL-API-027: ApiResult.raise_for_status() raises for 4xx status
- **Purpose**: Verify raise_for_status() raises exception for client errors
- **Preconditions**: ApiResult with status_code=404
- **Test Steps**:
  1. Create ApiResult with status_code=404, error_message="Not Found"
  2. Call result.raise_for_status()
- **Expected Result**: Exception raised with message "HTTP 404: Not Found"
- **Coverage**: `raise_for_status()` client error handling

#### TC-MODEL-API-028: ApiResult.raise_for_status() raises for 5xx status
- **Purpose**: Verify raise_for_status() raises exception for server errors
- **Preconditions**: ApiResult with status_code=500
- **Test Steps**:
  1. Create ApiResult with status_code=500, error_message="Internal Server Error"
  2. Call result.raise_for_status()
- **Expected Result**: Exception raised with message "HTTP 500: Internal Server Error"
- **Coverage**: `raise_for_status()` server error handling

#### TC-MODEL-API-029: ApiResult.assert_status_code() with matching code
- **Purpose**: Verify assert_status_code() does not raise for matching status code
- **Preconditions**: ApiResult with status_code=200
- **Test Steps**:
  1. Create ApiResult with status_code=200
  2. Call result.assert_status_code(200)
- **Expected Result**: No AssertionError raised
- **Coverage**: `assert_status_code()` success case

#### TC-MODEL-API-030: ApiResult.assert_status_code() raises for mismatch
- **Purpose**: Verify assert_status_code() raises AssertionError for non-matching status code
- **Preconditions**: ApiResult with status_code=404
- **Test Steps**:
  1. Create ApiResult with status_code=404, body=b"Not Found"
  2. Call result.assert_status_code(200)
- **Expected Result**: AssertionError raised with message containing "Expected status code 200, got 404"
- **Coverage**: `assert_status_code()` failure case

#### TC-MODEL-API-031: ApiResult.assert_success() for successful request
- **Purpose**: Verify assert_success() does not raise for 2xx status codes
- **Preconditions**: ApiResult with status_code=200, success=True
- **Test Steps**:
  1. Create ApiResult with status_code=200, success=True
  2. Call result.assert_success()
- **Expected Result**: No AssertionError raised
- **Coverage**: `assert_success()` success case

#### TC-MODEL-API-032: ApiResult.assert_success() raises for failed request
- **Purpose**: Verify assert_success() raises AssertionError for non-2xx status codes
- **Preconditions**: ApiResult with status_code=500, success=False
- **Test Steps**:
  1. Create ApiResult with status_code=500, success=False, body=b"Server Error"
  2. Call result.assert_success()
- **Expected Result**: AssertionError raised with message containing "Request failed with status 500"
- **Coverage**: `assert_success()` failure case

#### TC-MODEL-API-033: ApiResult.assert_has_fields() with all fields present
- **Purpose**: Verify assert_has_fields() does not raise when all fields are present
- **Preconditions**: ApiResult with JSON body containing required fields
- **Test Steps**:
  1. Create ApiResult with body: b'{"name": "test", "id": 123, "status": "active"}'
  2. Call result.assert_has_fields("name", "id", "status")
- **Expected Result**: No AssertionError raised
- **Coverage**: `assert_has_fields()` success case

#### TC-MODEL-API-034: ApiResult.assert_has_fields() raises for missing fields
- **Purpose**: Verify assert_has_fields() raises AssertionError when fields are missing
- **Preconditions**: ApiResult with JSON body missing some fields
- **Test Steps**:
  1. Create ApiResult with body: b'{"name": "test", "id": 123}'
  2. Call result.assert_has_fields("name", "id", "status", "email")
- **Expected Result**: AssertionError raised with message containing "Missing required fields: status, email"
- **Coverage**: `assert_has_fields()` failure case
