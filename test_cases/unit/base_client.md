# BaseClient Class - Unit Test Cases

## Overview
Tests for `tma_test_framework.clients.base_client.BaseClient` class - base class for Mini App testing clients.

## Test Categories

### 1. Initialization Tests

#### TC-BASE-001: Initialize BaseClient with URL and config
- **Purpose**: Verify BaseClient can be initialized with URL and Config
- **Preconditions**: Valid URL and Config object
- **Test Steps**:
  1. Create BaseClient(url, config)
  2. Verify url and config attributes are set
  3. Verify logger is initialized
- **Expected Result**: BaseClient created with url, config, and logger set
- **Coverage**: `__init__` method

#### TC-BASE-002: Initialize BaseClient with URL only (no config)
- **Purpose**: Verify BaseClient creates default Config when none provided
- **Preconditions**: Valid URL, no config
- **Test Steps**:
  1. Create BaseClient(url) without config
  2. Verify default Config is created
- **Expected Result**: BaseClient created with default Config instance
- **Coverage**: `__init__` default config creation

#### TC-BASE-003: Verify BaseClient stores URL correctly
- **Purpose**: Verify URL is stored and accessible
- **Preconditions**: Valid URL string
- **Test Steps**:
  1. Create BaseClient with URL
  2. Verify self.url equals provided URL
- **Expected Result**: URL stored correctly
- **Coverage**: URL attribute

#### TC-BASE-004: Verify BaseClient logger is initialized
- **Purpose**: Verify logger is bound to class name
- **Preconditions**: BaseClient instance
- **Test Steps**:
  1. Create BaseClient
  2. Verify logger name contains class name
- **Expected Result**: Logger initialized with correct name binding
- **Coverage**: Logger initialization

### 2. Context Manager Tests

#### TC-BASE-005: Use BaseClient as async context manager (enter)
- **Purpose**: Verify BaseClient can be used with async with
- **Preconditions**: BaseClient instance
- **Test Steps**:
  1. Use `async with BaseClient(url) as app:`
  2. Verify __aenter__ returns self
- **Expected Result**: Context manager entry works, returns self
- **Coverage**: `__aenter__` method

#### TC-BASE-006: Use BaseClient as async context manager (exit)
- **Purpose**: Verify BaseClient calls close() on exit
- **Preconditions**: BaseClient instance
- **Test Steps**:
  1. Use async with BaseClient
  2. Exit context
  3. Verify close() is called
- **Expected Result**: close() method called on context exit
- **Coverage**: `__aexit__` method

#### TC-BASE-007: Use BaseClient context manager with exception
- **Purpose**: Verify context manager handles exceptions
- **Preconditions**: BaseClient instance
- **Test Steps**:
  1. Use async with BaseClient
  2. Raise exception inside context
  3. Verify close() is still called
- **Expected Result**: close() called even when exception occurs
- **Coverage**: `__aexit__` exception handling

### 3. Close Method Tests

#### TC-BASE-008: Call close() on BaseClient
- **Purpose**: Verify close() method exists and can be called
- **Preconditions**: BaseClient instance
- **Test Steps**:
  1. Create BaseClient
  2. Call await app.close()
  3. Verify no errors
- **Expected Result**: close() executes without error
- **Coverage**: `close()` method

#### TC-BASE-009: Verify close() logs debug message
- **Purpose**: Verify close() logs appropriate message
- **Preconditions**: BaseClient instance, logger capture
- **Test Steps**:
  1. Create BaseClient
  2. Call close()
  3. Verify "Closing resources" logged
- **Expected Result**: Debug log message appears
- **Coverage**: `close()` logging

### 4. Inheritance Tests

#### TC-BASE-010: Verify ApiClient inherits from BaseClient
- **Purpose**: Verify inheritance relationship
- **Preconditions**: ApiClient class
- **Test Steps**:
  1. Check isinstance(ApiClient(), BaseClient)
- **Expected Result**: True
- **Coverage**: Inheritance

#### TC-BASE-011: Verify UiClient inherits from BaseClient
- **Purpose**: Verify inheritance relationship
- **Preconditions**: UiClient class
- **Test Steps**:
  1. Check isinstance(UiClient(), BaseClient)
- **Expected Result**: True
- **Coverage**: Inheritance

#### TC-BASE-012: Verify subclasses can override close()
- **Purpose**: Verify subclasses can override close() method
- **Preconditions**: ApiClient and UiClient instances
- **Test Steps**:
  1. Call close() on ApiClient
  2. Call close() on UiClient
  3. Verify subclass-specific close() is called
- **Expected Result**: Subclass close() methods execute
- **Coverage**: Method overriding

### 5. Edge Cases

#### TC-BASE-013: Initialize with empty URL string
- **Purpose**: Verify BaseClient handles empty URL
- **Preconditions**: URL = ""
- **Test Steps**:
  1. Create BaseClient with empty URL
- **Expected Result**: BaseClient created (validation may be in subclasses)
- **Coverage**: Empty string handling

#### TC-BASE-014: Initialize with very long URL
- **Purpose**: Verify BaseClient handles long URLs
- **Preconditions**: URL = "https://" + "a" * 10000
- **Test Steps**:
  1. Create BaseClient with very long URL
- **Expected Result**: BaseClient created successfully
- **Coverage**: Large data handling

#### TC-BASE-015: Initialize with URL containing special characters
- **Purpose**: Verify BaseClient handles special characters in URL
- **Preconditions**: URL with unicode, query params, fragments
- **Test Steps**:
  1. Create BaseClient with complex URL
- **Expected Result**: BaseClient created successfully
- **Coverage**: Special character handling
