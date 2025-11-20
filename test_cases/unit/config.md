# Config Class - Unit Test Cases

## Overview
Tests for `src.config.Config` class - configuration management for TMA Framework.

## Test Categories

### 1. Initialization Tests

#### TC-CONFIG-001: Create Config with valid parameters
- **Purpose**: Verify Config can be created with all valid parameters
- **Preconditions**: Valid configuration data
- **Test Steps**:
  1. Create Config with all required and optional parameters
  2. Verify all attributes are set correctly
- **Expected Result**: Config object created successfully with all attributes set
- **Coverage**: `__init__`, `__post_init__`

#### TC-CONFIG-002: Create Config with minimal required parameters
- **Purpose**: Verify Config can be created with only required parameters
- **Preconditions**: Minimal valid configuration data (api_id, api_hash, session_string)
- **Test Steps**:
  1. Create Config with only required parameters
  2. Verify default values are applied
- **Expected Result**: Config created with defaults (timeout=30, retry_count=3, retry_delay=1.0, log_level="INFO")
- **Coverage**: Default parameter values

#### TC-CONFIG-003: Create Config with session_string
- **Purpose**: Verify Config accepts session_string
- **Preconditions**: Valid api_id, api_hash, session_string
- **Test Steps**:
  1. Create Config with session_string
  2. Verify session_string is set
- **Expected Result**: Config created with session_string
- **Coverage**: session_string parameter

#### TC-CONFIG-004: Create Config with session_file
- **Purpose**: Verify Config accepts session_file
- **Preconditions**: Valid api_id, api_hash, session_file
- **Test Steps**:
  1. Create Config with session_file
  2. Verify session_file is set
- **Expected Result**: Config created with session_file
- **Coverage**: session_file parameter

#### TC-CONFIG-005: Create Config with both session_string and session_file
- **Purpose**: Verify Config accepts both session methods
- **Preconditions**: Valid api_id, api_hash, session_string, session_file
- **Test Steps**:
  1. Create Config with both session_string and session_file
  2. Verify both are set
- **Expected Result**: Config created with both session methods
- **Coverage**: Both session parameters

### 2. Validation Tests

#### TC-CONFIG-006: Reject Config with invalid api_id (too low)
- **Purpose**: Verify validation rejects api_id < 1
- **Preconditions**: api_id = 0
- **Test Steps**:
  1. Attempt to create Config with api_id = 0
- **Expected Result**: ValueError raised: "api_id must be between 1 and 999999999, got 0"
- **Coverage**: `__post_init__` api_id validation (lower bound)

#### TC-CONFIG-007: Reject Config with invalid api_id (too high)
- **Purpose**: Verify validation rejects api_id > 999999999
- **Preconditions**: api_id = 1000000000
- **Test Steps**:
  1. Attempt to create Config with api_id = 1000000000
- **Expected Result**: ValueError raised: "api_id must be between 1 and 999999999, got 1000000000"
- **Coverage**: `__post_init__` api_id validation (upper bound)

#### TC-CONFIG-008: Reject Config with invalid api_id (None)
- **Purpose**: Verify validation rejects None api_id
- **Preconditions**: api_id = None
- **Test Steps**:
  1. Attempt to create Config with api_id = None
- **Expected Result**: ValueError raised: "api_id must be between 1 and 999999999, got None"
- **Coverage**: `__post_init__` api_id validation (None check)

#### TC-CONFIG-009: Reject Config with invalid api_hash (too short)
- **Purpose**: Verify validation rejects api_hash with length != 32
- **Preconditions**: api_hash = "short"
- **Test Steps**:
  1. Attempt to create Config with api_hash = "short"
- **Expected Result**: ValueError raised: "api_hash must be exactly 32 characters long, got 5"
- **Coverage**: `__post_init__` api_hash validation (length check)

#### TC-CONFIG-010: Reject Config with invalid api_hash (too long)
- **Purpose**: Verify validation rejects api_hash with length != 32
- **Preconditions**: api_hash = "a" * 33
- **Test Steps**:
  1. Attempt to create Config with api_hash = "a" * 33
- **Expected Result**: ValueError raised: "api_hash must be exactly 32 characters long, got 33"
- **Coverage**: `__post_init__` api_hash validation (length check)

#### TC-CONFIG-011: Reject Config with invalid api_hash (None)
- **Purpose**: Verify validation rejects None api_hash
- **Preconditions**: api_hash = None
- **Test Steps**:
  1. Attempt to create Config with api_hash = None
- **Expected Result**: ValueError raised: "api_hash must be exactly 32 characters long, got 0"
- **Coverage**: `__post_init__` api_hash validation (None check)

#### TC-CONFIG-012: Reject Config with invalid timeout (too low)
- **Purpose**: Verify validation rejects timeout < 1
- **Preconditions**: timeout = 0
- **Test Steps**:
  1. Attempt to create Config with timeout = 0
- **Expected Result**: ValueError raised: "timeout must be between 1 and 300 seconds, got 0"
- **Coverage**: `__post_init__` timeout validation (lower bound)

#### TC-CONFIG-013: Reject Config with invalid timeout (too high)
- **Purpose**: Verify validation rejects timeout > 300
- **Preconditions**: timeout = 301
- **Test Steps**:
  1. Attempt to create Config with timeout = 301
- **Expected Result**: ValueError raised: "timeout must be between 1 and 300 seconds, got 301"
- **Coverage**: `__post_init__` timeout validation (upper bound)

#### TC-CONFIG-014: Accept Config with valid timeout boundaries
- **Purpose**: Verify validation accepts boundary timeout values
- **Preconditions**: timeout = 1, timeout = 300
- **Test Steps**:
  1. Create Config with timeout = 1
  2. Create Config with timeout = 300
- **Expected Result**: Both Configs created successfully
- **Coverage**: `__post_init__` timeout validation (boundaries)

#### TC-CONFIG-015: Reject Config with invalid retry_count (too low)
- **Purpose**: Verify validation rejects retry_count < 0
- **Preconditions**: retry_count = -1
- **Test Steps**:
  1. Attempt to create Config with retry_count = -1
- **Expected Result**: ValueError raised: "retry_count must be between 0 and 10, got -1"
- **Coverage**: `__post_init__` retry_count validation (lower bound)

#### TC-CONFIG-016: Reject Config with invalid retry_count (too high)
- **Purpose**: Verify validation rejects retry_count > 10
- **Preconditions**: retry_count = 11
- **Test Steps**:
  1. Attempt to create Config with retry_count = 11
- **Expected Result**: ValueError raised: "retry_count must be between 0 and 10, got 11"
- **Coverage**: `__post_init__` retry_count validation (upper bound)

#### TC-CONFIG-017: Accept Config with valid retry_count boundaries
- **Purpose**: Verify validation accepts boundary retry_count values
- **Preconditions**: retry_count = 0, retry_count = 10
- **Test Steps**:
  1. Create Config with retry_count = 0
  2. Create Config with retry_count = 10
- **Expected Result**: Both Configs created successfully
- **Coverage**: `__post_init__` retry_count validation (boundaries)

#### TC-CONFIG-018: Reject Config with invalid retry_delay (too low)
- **Purpose**: Verify validation rejects retry_delay < 0.1
- **Preconditions**: retry_delay = 0.05
- **Test Steps**:
  1. Attempt to create Config with retry_delay = 0.05
- **Expected Result**: ValueError raised: "retry_delay must be between 0.1 and 10.0 seconds, got 0.05"
- **Coverage**: `__post_init__` retry_delay validation (lower bound)

#### TC-CONFIG-019: Reject Config with invalid retry_delay (too high)
- **Purpose**: Verify validation rejects retry_delay > 10.0
- **Preconditions**: retry_delay = 10.1
- **Test Steps**:
  1. Attempt to create Config with retry_delay = 10.1
- **Expected Result**: ValueError raised: "retry_delay must be between 0.1 and 10.0 seconds, got 10.1"
- **Coverage**: `__post_init__` retry_delay validation (upper bound)

#### TC-CONFIG-020: Accept Config with valid retry_delay boundaries
- **Purpose**: Verify validation accepts boundary retry_delay values
- **Preconditions**: retry_delay = 0.1, retry_delay = 10.0
- **Test Steps**:
  1. Create Config with retry_delay = 0.1
  2. Create Config with retry_delay = 10.0
- **Expected Result**: Both Configs created successfully
- **Coverage**: `__post_init__` retry_delay validation (boundaries)

#### TC-CONFIG-021: Reject Config without session
- **Purpose**: Verify validation rejects Config without session_string or session_file
- **Preconditions**: api_id, api_hash valid, no session
- **Test Steps**:
  1. Attempt to create Config without session_string and session_file
- **Expected Result**: ValueError raised: "Session required. Provide one of: session_string (for saved session) or session_file (for file session). You need to authenticate manually first to get a session."
- **Coverage**: `__post_init__` session validation

#### TC-CONFIG-022: Reject Config with empty session_string
- **Purpose**: Verify validation rejects empty/whitespace session_string
- **Preconditions**: session_string = "   "
- **Test Steps**:
  1. Attempt to create Config with session_string = "   "
- **Expected Result**: ValueError raised: "Session required. Provide one of: session_string (for saved session) or session_file (for file session). You need to authenticate manually first to get a session."
- **Coverage**: `__post_init__` session_string validation (empty check)

#### TC-CONFIG-023: Reject Config with invalid log_level
- **Purpose**: Verify validation rejects invalid log_level
- **Preconditions**: log_level = "INVALID"
- **Test Steps**:
  1. Attempt to create Config with log_level = "INVALID"
- **Expected Result**: ValueError raised: "Invalid log level: INVALID. Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL"
- **Coverage**: `__post_init__` log_level validation

#### TC-CONFIG-024: Accept Config with all valid log_levels
- **Purpose**: Verify validation accepts all valid log_level values
- **Preconditions**: log_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
- **Test Steps**:
  1. Create Config with each valid log_level
- **Expected Result**: All Configs created successfully
- **Coverage**: `__post_init__` log_level validation (all values)

### 3. from_env() Tests

#### TC-CONFIG-025: Create Config from environment variables
- **Purpose**: Verify Config.from_env() reads from environment
- **Preconditions**: Environment variables set (TMA_API_ID, TMA_API_HASH, TMA_SESSION_STRING)
- **Test Steps**:
  1. Set environment variables
  2. Call Config.from_env()
  3. Verify Config created with correct values
- **Expected Result**: Config created from environment variables
- **Coverage**: `from_env()` method

#### TC-CONFIG-026: Create Config from_env with all optional variables
- **Purpose**: Verify from_env() reads all optional environment variables
- **Preconditions**: All TMA_* environment variables set
- **Test Steps**:
  1. Set all environment variables
  2. Call Config.from_env()
  3. Verify all values are read correctly
- **Expected Result**: Config created with all optional values from environment
- **Coverage**: `from_env()` with all parameters

#### TC-CONFIG-027: Create Config from_env with defaults
- **Purpose**: Verify from_env() uses defaults for missing optional variables
- **Preconditions**: Only required environment variables set
- **Test Steps**:
  1. Set only TMA_API_ID, TMA_API_HASH, TMA_SESSION_STRING
  2. Call Config.from_env()
  3. Verify defaults are used
- **Expected Result**: Config created with default values for optional parameters
- **Coverage**: `from_env()` default values

#### TC-CONFIG-028: Reject from_env() with missing TMA_API_ID
- **Purpose**: Verify from_env() fails when TMA_API_ID is missing
- **Preconditions**: TMA_API_ID not set
- **Test Steps**:
  1. Unset TMA_API_ID
  2. Call Config.from_env()
- **Expected Result**: ValueError raised: "TMA_API_ID and TMA_API_HASH environment variables are required"
- **Coverage**: `from_env()` validation

#### TC-CONFIG-029: Reject from_env() with missing TMA_API_HASH
- **Purpose**: Verify from_env() fails when TMA_API_HASH is missing
- **Preconditions**: TMA_API_HASH not set
- **Test Steps**:
  1. Unset TMA_API_HASH
  2. Call Config.from_env()
- **Expected Result**: ValueError raised: "TMA_API_ID and TMA_API_HASH environment variables are required"
- **Coverage**: `from_env()` validation

#### TC-CONFIG-030: Reject from_env() with invalid TMA_API_ID type
- **Purpose**: Verify from_env() fails when TMA_API_ID cannot be converted to int
- **Preconditions**: TMA_API_ID = "invalid"
- **Test Steps**:
  1. Set TMA_API_ID = "invalid"
  2. Call Config.from_env()
- **Expected Result**: ValueError raised: "invalid literal for int() with base 10: 'invalid'"
- **Coverage**: `from_env()` type conversion

#### TC-CONFIG-031: Reject from_env() with empty session
- **Purpose**: Verify from_env() fails when session is missing
- **Preconditions**: TMA_SESSION_STRING and TMA_SESSION_FILE not set
- **Test Steps**:
  1. Unset both session environment variables
  2. Call Config.from_env()
- **Expected Result**: ValueError raised in __post_init__ about missing session
- **Coverage**: `from_env()` session validation

### 4. from_yaml() Tests

#### TC-CONFIG-032: Create Config from valid YAML file
- **Purpose**: Verify Config.from_yaml() reads from YAML file
- **Preconditions**: Valid YAML file exists
- **Test Steps**:
  1. Create valid YAML file with config data
  2. Call Config.from_yaml(file_path)
  3. Verify Config created with correct values
- **Expected Result**: Config created from YAML file
- **Coverage**: `from_yaml()` method

#### TC-CONFIG-033: Create Config from_yaml with all parameters
- **Purpose**: Verify from_yaml() reads all parameters from YAML
- **Preconditions**: YAML file with all config parameters
- **Test Steps**:
  1. Create YAML with all parameters
  2. Call Config.from_yaml()
  3. Verify all values are read
- **Expected Result**: Config created with all parameters from YAML
- **Coverage**: `from_yaml()` with all parameters

#### TC-CONFIG-034: Create Config from_yaml with minimal parameters
- **Purpose**: Verify from_yaml() works with minimal YAML
- **Preconditions**: YAML file with only required parameters
- **Test Steps**:
  1. Create minimal YAML
  2. Call Config.from_yaml()
  3. Verify defaults are applied
- **Expected Result**: Config created with defaults for missing parameters
- **Coverage**: `from_yaml()` with defaults

#### TC-CONFIG-035: Reject from_yaml() with invalid file path
- **Purpose**: Verify from_yaml() fails with non-existent file
- **Preconditions**: File does not exist
- **Test Steps**:
  1. Call Config.from_yaml("nonexistent.yaml")
- **Expected Result**: FileNotFoundError or similar exception
- **Coverage**: `from_yaml()` error handling

#### TC-CONFIG-036: Reject from_yaml() with invalid YAML format
- **Purpose**: Verify from_yaml() fails with malformed YAML
- **Preconditions**: Invalid YAML file exists
- **Test Steps**:
  1. Create file with invalid YAML syntax
  2. Call Config.from_yaml()
- **Expected Result**: YAML parsing error
- **Coverage**: `from_yaml()` error handling

#### TC-CONFIG-037: Reject from_yaml() with invalid data
- **Purpose**: Verify from_yaml() fails when YAML data doesn't pass validation
- **Preconditions**: YAML file with invalid config values
- **Test Steps**:
  1. Create YAML with invalid api_id
  2. Call Config.from_yaml()
- **Expected Result**: ValueError raised in __post_init__
- **Coverage**: `from_yaml()` validation

#### TC-CONFIG-044: Override api_hash from environment variable in from_yaml
- **Purpose**: Verify from_yaml() overrides api_hash with TMA_API_HASH env variable
- **Preconditions**: YAML file with api_hash, TMA_API_HASH env variable set
- **Test Steps**:
  1. Create YAML file with api_hash="old_hash_32_characters_long!!"
  2. Set TMA_API_HASH="new_hash_32_characters_long!!"
  3. Call Config.from_yaml()
  4. Verify Config uses env variable value, not YAML value
- **Expected Result**: Config created with api_hash from environment variable
- **Coverage**: `from_yaml()` env override (api_hash)

#### TC-CONFIG-045: Override session_string from environment variable in from_yaml
- **Purpose**: Verify from_yaml() overrides session_string with TMA_SESSION_STRING env variable
- **Preconditions**: YAML file with session_string, TMA_SESSION_STRING env variable set
- **Test Steps**:
  1. Create YAML file with session_string="old_session"
  2. Set TMA_SESSION_STRING="new_session"
  3. Call Config.from_yaml()
  4. Verify Config uses env variable value, not YAML value
  5. Verify session_file is removed from config_data if present
- **Expected Result**: Config created with session_string from environment variable, session_file removed
- **Coverage**: `from_yaml()` env override (session_string)

#### TC-CONFIG-046: Override session_file from environment variable in from_yaml
- **Purpose**: Verify from_yaml() overrides session_file with TMA_SESSION_FILE env variable
- **Preconditions**: YAML file with session_file, TMA_SESSION_FILE env variable set
- **Test Steps**:
  1. Create YAML file with session_file="old_session.session"
  2. Set TMA_SESSION_FILE="new_session.session"
  3. Call Config.from_yaml()
  4. Verify Config uses env variable value, not YAML value
  5. Verify session_string is removed from config_data if present
- **Expected Result**: Config created with session_file from environment variable, session_string removed
- **Coverage**: `from_yaml()` env override (session_file)

### 5. Immutability Tests

#### TC-CONFIG-038: Verify Config is frozen (immutable)
- **Purpose**: Verify Config objects cannot be modified after creation
- **Preconditions**: Valid Config object created
- **Test Steps**:
  1. Create Config
  2. Attempt to modify an attribute
- **Expected Result**: AttributeError raised: "immutable type: 'Config'"
- **Coverage**: Frozen struct behavior

#### TC-CONFIG-039: Verify Config can be used in sets/dicts
- **Purpose**: Verify Config is hashable (can be used as dict key)
- **Preconditions**: Two Config objects with same values
- **Test Steps**:
  1. Create two Config objects with identical values
  2. Verify hash(config1) == hash(config2)
  3. Use Config as dict key
- **Expected Result**: Config is hashable and can be used in sets/dicts
- **Coverage**: Hashable behavior

### 6. Edge Cases

#### TC-CONFIG-040: Create Config with boundary api_id values
- **Purpose**: Verify Config accepts boundary api_id values
- **Preconditions**: api_id = 1, api_id = 999999999
- **Test Steps**:
  1. Create Config with api_id = 1
  2. Create Config with api_id = 999999999
- **Expected Result**: Both Configs created successfully
- **Coverage**: Boundary conditions

#### TC-CONFIG-041: Create Config with very long session_string
- **Purpose**: Verify Config accepts long session strings
- **Preconditions**: session_string = "a" * 10000
- **Test Steps**:
  1. Create Config with very long session_string
- **Expected Result**: Config created successfully
- **Coverage**: Large data handling

#### TC-CONFIG-042: Create Config with special characters in strings
- **Purpose**: Verify Config handles special characters
- **Preconditions**: Strings with unicode, special chars
- **Test Steps**:
  1. Create Config with unicode in session_string
  2. Create Config with special characters
- **Expected Result**: Configs created successfully
- **Coverage**: Special character handling

#### TC-CONFIG-043: Create Config with None optional parameters
- **Purpose**: Verify Config accepts None for optional parameters
- **Preconditions**: Optional parameters set to None
- **Test Steps**:
  1. Create Config with mini_app_url=None, mini_app_start_param=None
- **Expected Result**: Config created successfully
- **Coverage**: Optional None handling
