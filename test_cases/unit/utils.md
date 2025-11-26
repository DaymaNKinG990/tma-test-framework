# Utility Functions - Unit Test Cases

## Overview
Tests for utility functions in `tma_test_framework.utils`:
- `parse_json()` - Parse JSON from response body
- `validate_response_structure()` - Validate response structure
- `extract_pagination_info()` - Extract pagination information
- `get_error_detail()` - Extract error detail from response
- `generate_telegram_init_data()` - Generate Telegram init data for testing

## parse_json() Test Cases

### 1. Basic Functionality Tests

#### TC-UTILS-001: Parse valid JSON
- **Purpose**: Verify parse_json() parses valid JSON correctly
- **Preconditions**: Valid JSON bytes
- **Test Steps**:
  1. Call parse_json(b'{"key": "value", "number": 123}')
  2. Verify returned dict matches JSON content
- **Expected Result**: Returns parsed dictionary with correct values
- **Coverage**: `parse_json()` basic functionality

#### TC-UTILS-002: Parse invalid JSON returns empty dict
- **Purpose**: Verify parse_json() returns empty dict for invalid JSON
- **Preconditions**: Invalid JSON bytes
- **Test Steps**:
  1. Call parse_json(b"not valid json")
  2. Verify returned dict is empty: {}
- **Expected Result**: Returns empty dictionary
- **Coverage**: `parse_json()` error handling

#### TC-UTILS-003: Parse empty body returns empty dict
- **Purpose**: Verify parse_json() handles empty body
- **Preconditions**: Empty bytes
- **Test Steps**:
  1. Call parse_json(b"")
  2. Verify returned dict is empty: {}
- **Expected Result**: Returns empty dictionary
- **Coverage**: `parse_json()` empty input handling

#### TC-UTILS-004: Parse JSON with unicode characters
- **Purpose**: Verify parse_json() handles unicode characters
- **Preconditions**: JSON with unicode characters
- **Test Steps**:
  1. Call parse_json(b'{"message": "Привет", "emoji": "🎉"}')
  2. Verify returned dict contains unicode values correctly
- **Expected Result**: Unicode characters parsed correctly
- **Coverage**: `parse_json()` unicode handling

## validate_response_structure() Test Cases

### 1. Basic Functionality Tests

#### TC-UTILS-005: Validate structure with all fields present
- **Purpose**: Verify validate_response_structure() returns True when all fields present
- **Preconditions**: Data dict with all expected fields
- **Test Steps**:
  1. Call validate_response_structure({"name": "test", "id": 123, "status": "active"}, ["name", "id", "status"])
  2. Verify returns True
- **Expected Result**: Returns True
- **Coverage**: `validate_response_structure()` success case

#### TC-UTILS-006: Validate structure with missing fields
- **Purpose**: Verify validate_response_structure() returns False when fields missing
- **Preconditions**: Data dict missing some expected fields
- **Test Steps**:
  1. Call validate_response_structure({"name": "test", "id": 123}, ["name", "id", "status", "email"])
  2. Verify returns False
- **Expected Result**: Returns False
- **Coverage**: `validate_response_structure()` failure case

#### TC-UTILS-007: Validate structure with empty expected fields
- **Purpose**: Verify validate_response_structure() returns True for empty expected fields
- **Preconditions**: Empty expected_fields list
- **Test Steps**:
  1. Call validate_response_structure({"name": "test"}, [])
  2. Verify returns True
- **Expected Result**: Returns True (all zero fields are present)
- **Coverage**: `validate_response_structure()` edge case

## extract_pagination_info() Test Cases

### 1. Basic Functionality Tests

#### TC-UTILS-008: Extract complete pagination info
- **Purpose**: Verify extract_pagination_info() extracts all pagination fields
- **Preconditions**: Data dict with complete pagination info
- **Test Steps**:
  1. Call extract_pagination_info({"count": 100, "next": "http://api.example.com/items/?page=2", "previous": None, "results": [{"id": 1}, {"id": 2}]})
  2. Verify returned dict contains count, next, previous, results
- **Expected Result**: Returns dict with all pagination fields
- **Coverage**: `extract_pagination_info()` complete data

#### TC-UTILS-009: Extract partial pagination info
- **Purpose**: Verify extract_pagination_info() handles partial pagination data
- **Preconditions**: Data dict with only count field
- **Test Steps**:
  1. Call extract_pagination_info({"count": 50})
  2. Verify returned dict has count=50, next=None, previous=None, results=[]
- **Expected Result**: Returns dict with available fields, None/[] for missing
- **Coverage**: `extract_pagination_info()` partial data

#### TC-UTILS-010: Extract pagination info from empty data
- **Purpose**: Verify extract_pagination_info() handles empty data dict
- **Preconditions**: Empty data dict
- **Test Steps**:
  1. Call extract_pagination_info({})
  2. Verify returned dict has all fields as None or []
- **Expected Result**: Returns dict with count=None, next=None, previous=None, results=[]
- **Coverage**: `extract_pagination_info()` empty input

## get_error_detail() Test Cases

### 1. Basic Functionality Tests

#### TC-UTILS-011: Extract error detail from 'detail' field
- **Purpose**: Verify get_error_detail() extracts 'detail' field
- **Preconditions**: Data dict with 'detail' field
- **Test Steps**:
  1. Call get_error_detail({"detail": "Error message"})
  2. Verify returns "Error message"
- **Expected Result**: Returns value from 'detail' field
- **Coverage**: `get_error_detail()` detail field

#### TC-UTILS-012: Extract error detail from 'error' field
- **Purpose**: Verify get_error_detail() extracts 'error' field when 'detail' missing
- **Preconditions**: Data dict with 'error' field but no 'detail'
- **Test Steps**:
  1. Call get_error_detail({"error": "Error message"})
  2. Verify returns "Error message"
- **Expected Result**: Returns value from 'error' field
- **Coverage**: `get_error_detail()` error field fallback

#### TC-UTILS-013: Extract error detail fallback to string representation
- **Purpose**: Verify get_error_detail() falls back to string representation
- **Preconditions**: Data dict without 'detail' or 'error' fields
- **Test Steps**:
  1. Call get_error_detail({"message": "Some message"})
  2. Verify returns string representation of dict
- **Expected Result**: Returns string representation of data
- **Coverage**: `get_error_detail()` fallback behavior

## generate_telegram_init_data() Test Cases

### 1. Basic Functionality Tests

#### TC-UTILS-014: Generate init data with default parameters
- **Purpose**: Verify generate_telegram_init_data() generates valid init data with defaults
- **Preconditions**: Bot token provided
- **Test Steps**:
  1. Call generate_telegram_init_data(bot_token="123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
  2. Verify returned string contains "user=", "auth_date=", "hash="
- **Expected Result**: Returns valid init data string with all required fields
- **Coverage**: `generate_telegram_init_data()` default parameters

#### TC-UTILS-015: Generate init data with custom parameters
- **Purpose**: Verify generate_telegram_init_data() accepts custom user parameters
- **Preconditions**: Custom user parameters and bot token
- **Test Steps**:
  1. Call generate_telegram_init_data(user_id=999999999, username="custom_user", first_name="Custom", last_name="User", bot_token="123456789:ABCdefGHIjklMNOpqrsTUVwxyz", language_code="en", is_premium=True)
  2. Verify returned string contains custom user data
- **Expected Result**: Returns init data with custom user information
- **Coverage**: `generate_telegram_init_data()` custom parameters

#### TC-UTILS-016: Generate init data with valid hash format
- **Purpose**: Verify generated hash is valid SHA256 hex string
- **Preconditions**: Bot token provided
- **Test Steps**:
  1. Call generate_telegram_init_data(bot_token="123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
  2. Extract hash from returned init data
  3. Verify hash is 64 character hex string (SHA256)
- **Expected Result**: Hash is valid 64-character hex string
- **Coverage**: `generate_telegram_init_data()` hash validation

#### TC-UTILS-017: Generate init data can be validated
- **Purpose**: Verify generated init data can be validated by ApiClient.validate_init_data()
- **Preconditions**: Bot token and generated init data
- **Test Steps**:
  1. Generate init data with bot_token
  2. Call ApiClient.validate_init_data() with generated init_data and same bot_token
  3. Verify validation passes (if validation logic available)
- **Expected Result**: Generated init data passes validation
- **Coverage**: `generate_telegram_init_data()` validation compatibility

