# BaseMiniApp Class - Unit Test Cases

## Overview
Tests for `src.mini_app.base.BaseMiniApp` class - base class for Mini App testing.

## Test Categories

### 1. Initialization Tests

#### TC-BASE-001: Initialize BaseMiniApp with URL and config
- **Purpose**: Verify BaseMiniApp can be initialized with URL and Config
- **Preconditions**: Valid URL and Config object
- **Test Steps**:
  1. Create BaseMiniApp(url, config)
  2. Verify url and config attributes are set
  3. Verify logger is initialized
- **Expected Result**: BaseMiniApp created with url, config, and logger set
- **Coverage**: `__init__` method

#### TC-BASE-002: Initialize BaseMiniApp with URL only (no config)
- **Purpose**: Verify BaseMiniApp creates default Config when none provided
- **Preconditions**: Valid URL, no config
- **Test Steps**:
  1. Create BaseMiniApp(url) without config
  2. Verify default Config is created
- **Expected Result**: BaseMiniApp created with default Config instance
- **Coverage**: `__init__` default config creation

#### TC-BASE-003: Verify BaseMiniApp stores URL correctly
- **Purpose**: Verify URL is stored and accessible
- **Preconditions**: Valid URL string
- **Test Steps**:
  1. Create BaseMiniApp with URL
  2. Verify self.url equals provided URL
- **Expected Result**: URL stored correctly
- **Coverage**: URL attribute

#### TC-BASE-004: Verify BaseMiniApp logger is initialized
- **Purpose**: Verify logger is bound to class name
- **Preconditions**: BaseMiniApp instance
- **Test Steps**:
  1. Create BaseMiniApp
  2. Verify logger name contains class name
- **Expected Result**: Logger initialized with correct name binding
- **Coverage**: Logger initialization

### 2. Context Manager Tests

#### TC-BASE-005: Use BaseMiniApp as async context manager (enter)
- **Purpose**: Verify BaseMiniApp can be used with async with
- **Preconditions**: BaseMiniApp instance
- **Test Steps**:
  1. Use `async with BaseMiniApp(url) as app:`
  2. Verify __aenter__ returns self
- **Expected Result**: Context manager entry works, returns self
- **Coverage**: `__aenter__` method

#### TC-BASE-006: Use BaseMiniApp as async context manager (exit)
- **Purpose**: Verify BaseMiniApp calls close() on exit
- **Preconditions**: BaseMiniApp instance
- **Test Steps**:
  1. Use async with BaseMiniApp
  2. Exit context
  3. Verify close() is called
- **Expected Result**: close() method called on context exit
- **Coverage**: `__aexit__` method

#### TC-BASE-007: Use BaseMiniApp context manager with exception
- **Purpose**: Verify context manager handles exceptions
- **Preconditions**: BaseMiniApp instance
- **Test Steps**:
  1. Use async with BaseMiniApp
  2. Raise exception inside context
  3. Verify close() is still called
- **Expected Result**: close() called even when exception occurs
- **Coverage**: `__aexit__` exception handling

### 3. Close Method Tests

#### TC-BASE-008: Call close() on BaseMiniApp
- **Purpose**: Verify close() method exists and can be called
- **Preconditions**: BaseMiniApp instance
- **Test Steps**:
  1. Create BaseMiniApp
  2. Call await app.close()
  3. Verify no errors
- **Expected Result**: close() executes without error
- **Coverage**: `close()` method

#### TC-BASE-009: Verify close() logs debug message
- **Purpose**: Verify close() logs appropriate message
- **Preconditions**: BaseMiniApp instance, logger capture
- **Test Steps**:
  1. Create BaseMiniApp
  2. Call close()
  3. Verify "Closing resources" logged
- **Expected Result**: Debug log message appears
- **Coverage**: `close()` logging

### 4. Inheritance Tests

#### TC-BASE-010: Verify MiniAppApi inherits from BaseMiniApp
- **Purpose**: Verify inheritance relationship
- **Preconditions**: MiniAppApi class
- **Test Steps**:
  1. Check isinstance(MiniAppApi(), BaseMiniApp)
- **Expected Result**: True
- **Coverage**: Inheritance

#### TC-BASE-011: Verify MiniAppUI inherits from BaseMiniApp
- **Purpose**: Verify inheritance relationship
- **Preconditions**: MiniAppUI class
- **Test Steps**:
  1. Check isinstance(MiniAppUI(), BaseMiniApp)
- **Expected Result**: True
- **Coverage**: Inheritance

#### TC-BASE-012: Verify subclasses can override close()
- **Purpose**: Verify subclasses can override close() method
- **Preconditions**: MiniAppApi and MiniAppUI instances
- **Test Steps**:
  1. Call close() on MiniAppApi
  2. Call close() on MiniAppUI
  3. Verify subclass-specific close() is called
- **Expected Result**: Subclass close() methods execute
- **Coverage**: Method overriding

### 5. Edge Cases

#### TC-BASE-013: Initialize with empty URL string
- **Purpose**: Verify BaseMiniApp handles empty URL
- **Preconditions**: URL = ""
- **Test Steps**:
  1. Create BaseMiniApp with empty URL
- **Expected Result**: BaseMiniApp created (validation may be in subclasses)
- **Coverage**: Empty string handling

#### TC-BASE-014: Initialize with very long URL
- **Purpose**: Verify BaseMiniApp handles long URLs
- **Preconditions**: URL = "https://" + "a" * 10000
- **Test Steps**:
  1. Create BaseMiniApp with very long URL
- **Expected Result**: BaseMiniApp created successfully
- **Coverage**: Large data handling

#### TC-BASE-015: Initialize with URL containing special characters
- **Purpose**: Verify BaseMiniApp handles special characters in URL
- **Preconditions**: URL with unicode, query params, fragments
- **Test Steps**:
  1. Create BaseMiniApp with complex URL
- **Expected Result**: BaseMiniApp created successfully
- **Coverage**: Special character handling
