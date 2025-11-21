# MTProto Client - Unit Test Cases

## Overview
Tests for `tma_test_framework.mtproto_client` module:
- `UserTelegramClient` - MTProto client for user simulation
- `UserInfo` - User information model
- `ChatInfo` - Chat information model
- `MessageInfo` - Message information model

## UserInfo Model Tests

### TC-MODEL-USER-001: Create UserInfo with all parameters
- **Purpose**: Verify UserInfo can be created with all fields
- **Preconditions**: All user data available
- **Test Steps**:
  1. Create UserInfo with all parameters
  2. Verify all attributes are set
- **Expected Result**: UserInfo created successfully
- **Coverage**: `UserInfo.__init__`

### TC-MODEL-USER-002: Create UserInfo with minimal parameters
- **Purpose**: Verify UserInfo with only required fields
- **Preconditions**: Only id and first_name
- **Test Steps**:
  1. Create UserInfo with id, first_name, defaults
  2. Verify optional fields are None or defaults
- **Expected Result**: UserInfo created with defaults
- **Coverage**: Optional parameters

### TC-MODEL-USER-003: Verify UserInfo is frozen
- **Purpose**: Verify UserInfo is immutable
- **Preconditions**: Valid UserInfo instance
- **Test Steps**:
  1. Create UserInfo
  2. Attempt to modify attribute
- **Expected Result**: AttributeError raised
- **Coverage**: Frozen struct

## ChatInfo Model Tests

### TC-MODEL-CHAT-001: Create ChatInfo with all parameters
- **Purpose**: Verify ChatInfo creation
- **Preconditions**: All chat data
- **Test Steps**:
  1. Create ChatInfo with all parameters
  2. Verify attributes
- **Expected Result**: ChatInfo created
- **Coverage**: `ChatInfo.__init__`

### TC-MODEL-CHAT-002: Create ChatInfo with None username
- **Purpose**: Verify optional username
- **Preconditions**: Chat without username
- **Test Steps**:
  1. Create ChatInfo with username=None
- **Expected Result**: ChatInfo created successfully
- **Coverage**: Optional username

## MessageInfo Model Tests

### TC-MODEL-MSG-001: Create MessageInfo with all parameters
- **Purpose**: Verify MessageInfo creation
- **Preconditions**: All message data
- **Test Steps**:
  1. Create MessageInfo with all parameters
  2. Verify attributes including ChatInfo and UserInfo
- **Expected Result**: MessageInfo created
- **Coverage**: `MessageInfo.__init__`

### TC-MODEL-MSG-002: Create MessageInfo with None optional fields
- **Purpose**: Verify optional fields
- **Preconditions**: Message without text, from_user, reply_to, media
- **Test Steps**:
  1. Create MessageInfo with None optional fields
- **Expected Result**: MessageInfo created
- **Coverage**: Optional fields

## UserTelegramClient Tests

### 1. Initialization Tests

#### TC-CLIENT-001: Initialize with session_string
- **Purpose**: Verify initialization uses StringSession
- **Preconditions**: Config with session_string
- **Test Steps**:
  1. Create UserTelegramClient with session_string config
  2. Verify StringSession is used
- **Expected Result**: StringSession created, TelegramClient initialized
- **Coverage**: `__init__` with session_string

#### TC-CLIENT-002: Initialize with session_file
- **Purpose**: Verify initialization uses SQLiteSession
- **Preconditions**: Config with session_file
- **Test Steps**:
  1. Create UserTelegramClient with session_file config
  2. Verify SQLiteSession is used
- **Expected Result**: SQLiteSession created
- **Coverage**: `__init__` with session_file

#### TC-CLIENT-002a: Initialize without session (fallback)
- **Purpose**: Verify initialization uses fallback SQLiteSession when no session provided
- **Preconditions**: Config without session_string and session_file (bypassing validation)
- **Test Steps**:
  1. Create Config without session (bypassing __post_init__ validation)
  2. Create UserTelegramClient with this config
  3. Verify SQLiteSession("tma_session") is used as fallback
- **Expected Result**: SQLiteSession("tma_session") created as fallback
- **Coverage**: `__init__` else branch (line 75) - defensive code

#### TC-CLIENT-003: Initialize sets initial state
- **Purpose**: Verify initial state variables
- **Preconditions**: UserTelegramClient created
- **Test Steps**:
  1. Create client
  2. Verify _is_connected = False
  3. Verify _me = None
- **Expected Result**: Initial state set correctly
- **Coverage**: Initial state

### 2. Context Manager Tests

#### TC-CLIENT-004: Use as async context manager (enter)
- **Purpose**: Verify context manager entry
- **Preconditions**: UserTelegramClient instance
- **Test Steps**:
  1. Use async with UserTelegramClient
  2. Verify connect() is called
- **Expected Result**: Client connected, returns self
- **Coverage**: `__aenter__`

#### TC-CLIENT-005: Use as async context manager (exit)
- **Purpose**: Verify context manager exit
- **Preconditions**: Client in context
- **Test Steps**:
  1. Exit context
  2. Verify disconnect() is called
- **Expected Result**: Client disconnected
- **Coverage**: `__aexit__`

### 3. Connection Tests

#### TC-CLIENT-006: Connect successfully
- **Purpose**: Verify connect() establishes connection
- **Preconditions**: Valid session, authorized user
- **Test Steps**:
  1. Mock client.connect() and is_user_authorized()
  2. Call await client.connect()
  3. Verify _is_connected = True
  4. Verify get_me() is called
- **Expected Result**: Connected, authorized, _me set
- **Coverage**: `connect()` success

#### TC-CLIENT-007: Connect when already connected
- **Purpose**: Verify connect() is idempotent
- **Preconditions**: Already connected
- **Test Steps**:
  1. Connect once
  2. Call connect() again
  3. Verify "Already connected" logged
- **Expected Result**: No reconnection, logged
- **Coverage**: `connect()` idempotency

#### TC-CLIENT-008: Connect fails when not authorized
- **Purpose**: Verify connect() fails for unauthorized user
- **Preconditions**: Session exists but not authorized
- **Test Steps**:
  1. Mock is_user_authorized() = False
  2. Call connect()
- **Expected Result**: ValueError raised about authorization
- **Coverage**: `connect()` authorization check

#### TC-CLIENT-009: Connect handles connection error
- **Purpose**: Verify connect() handles errors
- **Preconditions**: Connection fails
- **Test Steps**:
  1. Mock client.connect() to raise exception
  2. Call connect()
- **Expected Result**: Exception logged and raised
- **Coverage**: `connect()` error handling

#### TC-CLIENT-010: Disconnect successfully
- **Purpose**: Verify disconnect() closes connection
- **Preconditions**: Connected client
- **Test Steps**:
  1. Connect client
  2. Call await disconnect()
  3. Verify client.disconnect() called
  4. Verify _is_connected = False
- **Expected Result**: Disconnected, state updated
- **Coverage**: `disconnect()` method

#### TC-CLIENT-011: Disconnect when not connected
- **Purpose**: Verify disconnect() handles not connected
- **Preconditions**: Not connected
- **Test Steps**:
  1. Call disconnect()
  2. Verify no errors
- **Expected Result**: No errors, graceful
- **Coverage**: `disconnect()` when not connected

#### TC-CLIENT-012: Check is_connected() when connected
- **Purpose**: Verify is_connected() returns True
- **Preconditions**: Connected client
- **Test Steps**:
  1. Connect client
  2. Call is_connected()
- **Expected Result**: Returns True
- **Coverage**: `is_connected()` method

#### TC-CLIENT-013: Check is_connected() when not connected
- **Purpose**: Verify is_connected() returns False
- **Preconditions**: Not connected
- **Test Steps**:
  1. Call is_connected()
- **Expected Result**: Returns False
- **Coverage**: `is_connected()` when disconnected

### 4. get_me() Tests

#### TC-CLIENT-014: Get current user information
- **Purpose**: Verify get_me() returns UserInfo
- **Preconditions**: Connected and authorized
- **Test Steps**:
  1. Mock client.get_me() to return user
  2. Call await get_me()
  3. Verify UserInfo is created and cached
- **Expected Result**: UserInfo returned, _me set
- **Coverage**: `get_me()` method

#### TC-CLIENT-015: Get_me() returns cached value
- **Purpose**: Verify get_me() uses cache
- **Preconditions**: _me already set
- **Test Steps**:
  1. Set _me
  2. Call get_me()
  3. Verify client.get_me() not called again
- **Expected Result**: Returns cached _me
- **Coverage**: `get_me()` caching

### 5. get_entity() Tests

#### TC-CLIENT-016: Get entity for User
- **Purpose**: Verify get_entity() handles User type
- **Preconditions**: Entity is User
- **Test Steps**:
  1. Mock client.get_entity() to return User
  2. Call await get_entity("@username")
  3. Verify ChatInfo created with type="private"
- **Expected Result**: ChatInfo with private type
- **Coverage**: `get_entity()` User handling

#### TC-CLIENT-017: Get entity for Channel
- **Purpose**: Verify get_entity() handles Channel type
- **Preconditions**: Entity is Channel
- **Test Steps**:
  1. Mock client.get_entity() to return Channel
  2. Call await get_entity("@channel")
  3. Verify ChatInfo with type="channel"
- **Expected Result**: ChatInfo with channel type
- **Coverage**: `get_entity()` Channel handling

#### TC-CLIENT-018: Get entity for Chat
- **Purpose**: Verify get_entity() handles Chat type
- **Preconditions**: Entity is Chat
- **Test Steps**:
  1. Mock client.get_entity() to return Chat
  2. Call await get_entity("@chat")
  3. Verify ChatInfo with type="group"
- **Expected Result**: ChatInfo with group type
- **Coverage**: `get_entity()` Chat handling

#### TC-CLIENT-019: Get entity with missing username
- **Purpose**: Verify get_entity() handles None username
- **Preconditions**: Entity without username
- **Test Steps**:
  1. Mock entity with username=None
  2. Call get_entity()
  3. Verify ChatInfo.username is None
- **Expected Result**: ChatInfo with None username
- **Coverage**: `get_entity()` None username

#### TC-CLIENT-020: Get entity with unsupported type
- **Purpose**: Verify get_entity() raises for unsupported type
- **Preconditions**: Entity type is Message or other
- **Test Steps**:
  1. Mock client.get_entity() to return Message
  2. Call get_entity()
- **Expected Result**: ValueError raised: "Unsupported entity type"
- **Coverage**: `get_entity()` unsupported type

#### TC-CLIENT-021: Get entity handles error
- **Purpose**: Verify get_entity() logs and raises errors
- **Preconditions**: client.get_entity() raises exception
- **Test Steps**:
  1. Mock client.get_entity() to raise exception
  2. Call get_entity()
- **Expected Result**: Error logged and raised
- **Coverage**: `get_entity()` error handling

### 6. send_message() Tests

#### TC-CLIENT-022: Send message successfully
- **Purpose**: Verify send_message() sends message
- **Preconditions**: Connected, valid entity
- **Test Steps**:
  1. Mock client.send_message()
  2. Call await send_message("@user", "Hello")
  3. Verify MessageInfo is returned
  4. Verify get_entity() is called for chat
- **Expected Result**: MessageInfo returned with correct data
- **Coverage**: `send_message()` method

#### TC-CLIENT-023: Send message with reply_to
- **Purpose**: Verify send_message() with reply
- **Preconditions**: Message ID to reply to
- **Test Steps**:
  1. Call send_message("@user", "Hello", reply_to=123)
  2. Verify reply_to is passed
- **Expected Result**: Message sent with reply
- **Coverage**: `send_message()` reply_to

#### TC-CLIENT-024: Send message with parse_mode
- **Purpose**: Verify send_message() with parse mode
- **Preconditions**: Parse mode specified
- **Test Steps**:
  1. Call send_message("@user", "Hello", parse_mode="HTML")
  2. Verify parse_mode is passed
- **Expected Result**: Message sent with parse mode
- **Coverage**: `send_message()` parse_mode

#### TC-CLIENT-025: Send message handles error
- **Purpose**: Verify send_message() handles errors
- **Preconditions**: client.send_message() raises exception
- **Test Steps**:
  1. Mock exception
  2. Call send_message()
- **Expected Result**: Error logged and raised
- **Coverage**: `send_message()` error handling

### 7. get_messages() Tests

#### TC-CLIENT-026: Get messages successfully
- **Purpose**: Verify get_messages() returns messages
- **Preconditions**: Connected, messages exist
- **Test Steps**:
  1. Mock client.get_messages() to return messages
  2. Mock get_entity() for chat
  3. Call await get_messages("@user", limit=10)
  4. Verify list of MessageInfo returned
- **Expected Result**: List of MessageInfo objects
- **Coverage**: `get_messages()` method

#### TC-CLIENT-027: Get messages with from_user
- **Purpose**: Verify get_messages() includes from_user
- **Preconditions**: Messages with from_id
- **Test Steps**:
  1. Mock message with from_id
  2. Mock client.get_entity() for user
  3. Call get_messages()
  4. Verify MessageInfo.from_user is set
- **Expected Result**: from_user populated
- **Coverage**: `get_messages()` from_user

#### TC-CLIENT-028: Get messages with from_user error
- **Purpose**: Verify get_messages() handles from_user error
- **Preconditions**: Error getting user
- **Test Steps**:
  1. Mock get_entity() for user to raise error
  2. Call get_messages()
  3. Verify from_user is None, error logged
- **Expected Result**: from_user=None, message still returned
- **Coverage**: `get_messages()` from_user error

#### TC-CLIENT-029: Get messages with limit and offset
- **Purpose**: Verify get_messages() uses limit and offset
- **Preconditions**: Limit and offset specified
- **Test Steps**:
  1. Call get_messages("@user", limit=5, offset_id=100)
  2. Verify limit and offset_id passed to client
- **Expected Result**: Messages with limit and offset
- **Coverage**: `get_messages()` limit and offset

#### TC-CLIENT-030: Get messages handles error
- **Purpose**: Verify get_messages() returns empty list on error
- **Preconditions**: client.get_messages() raises exception
- **Test Steps**:
  1. Mock exception
  2. Call get_messages()
- **Expected Result**: Returns [], error logged
- **Coverage**: `get_messages()` error handling

#### TC-CLIENT-031: Get messages skips None messages
- **Preconditions**: Some messages are None
- **Test Steps**:
  1. Mock get_messages() to return list with None
  2. Call get_messages()
  3. Verify None messages are skipped
- **Expected Result**: None messages filtered out
- **Coverage**: `get_messages()` None filtering

### 8. interact_with_bot() Tests

#### TC-CLIENT-032: Interact with bot and get response
- **Purpose**: Verify interact_with_bot() sends command and waits
- **Preconditions**: Bot responds
- **Test Steps**:
  1. Mock send_message() and get_messages()
  2. Mock get_messages() to return bot response
  3. Call await interact_with_bot("@bot", "/start")
  4. Verify response MessageInfo returned
- **Expected Result**: Bot response returned
- **Coverage**: `interact_with_bot()` success

#### TC-CLIENT-033: Interact with bot without waiting
- **Purpose**: Verify interact_with_bot() with wait_for_response=False
- **Preconditions**: wait_for_response=False
- **Test Steps**:
  1. Call interact_with_bot("@bot", "/start", wait_for_response=False)
  2. Verify returns None immediately
- **Expected Result**: Returns None, no waiting
- **Coverage**: `interact_with_bot()` wait_for_response=False

#### TC-CLIENT-034: Interact with bot timeout
- **Purpose**: Verify interact_with_bot() times out
- **Preconditions**: Bot doesn't respond
- **Test Steps**:
  1. Mock get_messages() to return empty list
  2. Mock time progression
  3. Call interact_with_bot() with short timeout
- **Expected Result**: Returns None after timeout, warning logged
- **Coverage**: `interact_with_bot()` timeout

#### TC-CLIENT-035: Interact with bot multiple iterations
- **Purpose**: Verify interact_with_bot() calls sleep in loop
- **Preconditions**: Bot responds after delay
- **Test Steps**:
  1. Mock get_messages() to return empty, then response
  2. Mock time progression
  3. Call interact_with_bot()
  4. Verify sleep() is called
- **Expected Result**: Sleep called, response found
- **Coverage**: `interact_with_bot()` loop with sleep

#### TC-CLIENT-036: Interact with bot ignores non-bot messages
- **Purpose**: Verify only bot messages are considered
- **Preconditions**: Messages from user and bot
- **Test Steps**:
  1. Mock get_messages() with user and bot messages
  2. Call interact_with_bot()
  3. Verify only bot message is returned
- **Expected Result**: Only bot message returned
- **Coverage**: `interact_with_bot()` bot filtering

#### TC-CLIENT-037: Interact with bot handles error
- **Purpose**: Verify interact_with_bot() handles errors
- **Preconditions**: send_message() raises exception
- **Test Steps**:
  1. Mock exception
  2. Call interact_with_bot()
- **Expected Result**: Error logged and raised
- **Coverage**: `interact_with_bot()` error handling

### 9. get_mini_app_from_bot() Tests

#### TC-CLIENT-038: Get Mini App from bot response text
- **Purpose**: Verify Mini App URL extracted from text
- **Preconditions**: Bot response contains URL
- **Test Steps**:
  1. Mock interact_with_bot() to return message with URL
  2. Call await get_mini_app_from_bot("@bot")
  3. Verify MiniAppUI created with URL
- **Expected Result**: MiniAppUI returned
- **Coverage**: `get_mini_app_from_bot()` from text

#### TC-CLIENT-039: Get Mini App from bot with start_param
- **Purpose**: Verify start_param is used in command
- **Preconditions**: start_param provided
- **Test Steps**:
  1. Call get_mini_app_from_bot("@bot", start_param="123")
  2. Verify command is "/start 123"
- **Expected Result**: Command includes start_param
- **Coverage**: `get_mini_app_from_bot()` start_param

#### TC-CLIENT-040: Get Mini App from bot media
- **Purpose**: Verify Mini App found in media
- **Preconditions**: Message with web_app media
- **Test Steps**:
  1. Mock get_messages() with web_app media
  2. Call get_mini_app_from_bot()
  3. Verify MiniAppUI created from media URL
- **Expected Result**: MiniAppUI from media
- **Coverage**: `get_mini_app_from_bot()` from media

#### TC-CLIENT-041: Get Mini App from bot not found
- **Purpose**: Verify returns None when no Mini App
- **Preconditions**: No Mini App in response
- **Test Steps**:
  1. Mock response without Mini App
  2. Call get_mini_app_from_bot()
- **Expected Result**: Returns None, warning logged
- **Coverage**: `get_mini_app_from_bot()` not found

#### TC-CLIENT-042: Get Mini App from bot handles error
- **Purpose**: Verify error handling
- **Preconditions**: Exception during process
- **Test Steps**:
  1. Mock exception
  2. Call get_mini_app_from_bot()
- **Expected Result**: Error logged and raised
- **Coverage**: `get_mini_app_from_bot()` error handling

### 10. Event Handler Tests

#### TC-CLIENT-043: Add event handler
- **Purpose**: Verify add_event_handler() adds handler
- **Preconditions**: Handler function
- **Test Steps**:
  1. Create handler function
  2. Call add_event_handler(handler)
  3. Verify client.add_event_handler() called
- **Expected Result**: Handler added
- **Coverage**: `add_event_handler()` method

#### TC-CLIENT-044: Start listening with handler
- **Purpose**: Verify start_listening() starts listening
- **Preconditions**: Connected, handler provided
- **Test Steps**:
  1. Connect client
  2. Call await start_listening(handler)
  3. Verify handler added and run_until_disconnected() called
- **Expected Result**: Listening started
- **Coverage**: `start_listening()` with handler

#### TC-CLIENT-045: Start listening without handler
- **Purpose**: Verify start_listening() without handler
- **Preconditions**: Connected, no handler
- **Test Steps**:
  1. Connect client
  2. Call await start_listening()
  3. Verify run_until_disconnected() called
- **Expected Result**: Listening started without handler
- **Coverage**: `start_listening()` without handler

#### TC-CLIENT-046: Start listening auto-connects
- **Purpose**: Verify start_listening() connects if not connected
- **Preconditions**: Not connected
- **Test Steps**:
  1. Call start_listening()
  2. Verify connect() is called first
- **Expected Result**: Auto-connects then starts listening
- **Coverage**: `start_listening()` auto-connect

### 11. Helper Method Tests

#### TC-CLIENT-047: Extract media info from message
- **Purpose**: Verify _extract_media_info() extracts info
- **Preconditions**: Message with media
- **Test Steps**:
  1. Create message with media
  2. Call _extract_media_info(message)
  3. Verify dict with type and url
- **Expected Result**: Media info dict returned
- **Coverage**: `_extract_media_info()` method

#### TC-CLIENT-048: Extract media info with webpage
- **Purpose**: Verify webpage URL is extracted
- **Preconditions**: Media with webpage
- **Test Steps**:
  1. Create message with media.webpage
  2. Call _extract_media_info()
  3. Verify webpage URL in dict
- **Expected Result**: Webpage URL included
- **Coverage**: `_extract_media_info()` webpage

#### TC-CLIENT-049: Extract media info returns None
- **Purpose**: Verify returns None when no media
- **Preconditions**: Message without media
- **Test Steps**:
  1. Create message without media
  2. Call _extract_media_info()
- **Expected Result**: Returns None
- **Coverage**: `_extract_media_info()` no media

#### TC-CLIENT-050: Extract Mini App URL from text
- **Purpose**: Verify _extract_mini_app_url() finds URL
- **Preconditions**: Text with Mini App URL
- **Test Steps**:
  1. Call _extract_mini_app_url() with URL in text
  2. Verify URL is extracted
- **Expected Result**: URL returned
- **Coverage**: `_extract_mini_app_url()` method

#### TC-CLIENT-051: Extract Mini App URL with different patterns
- **Purpose**: Verify all URL patterns are matched
- **Preconditions**: Different URL formats
- **Test Steps**:
  1. Test pattern: https://t.me/bot/app?start=123
  2. Test pattern: https://bot.t.me/app
  3. Test pattern: https://bot.telegram.app/app
- **Expected Result**: All patterns matched
- **Coverage**: `_extract_mini_app_url()` patterns

#### TC-CLIENT-052: Extract Mini App URL returns None
- **Purpose**: Verify returns None when no URL
- **Preconditions**: Text without URL
- **Test Steps**:
  1. Call _extract_mini_app_url() with no URL
- **Expected Result**: Returns None
- **Coverage**: `_extract_mini_app_url()` not found

### 12. Session Management Tests

#### TC-CLIENT-053: Get session_string from connected client
- **Purpose**: Verify session_string property returns session string
- **Preconditions**: Connected client with StringSession
- **Test Steps**:
  1. Create client with StringSession
  2. Connect client
  3. Mock client.session.save() to return session string
  4. Access client.session_string property
- **Expected Result**: Session string returned
- **Coverage**: `session_string` property

#### TC-CLIENT-054: Get session_string raises when not connected
- **Purpose**: Verify session_string raises ValueError when not connected
- **Preconditions**: Client not connected
- **Test Steps**:
  1. Create client but don't connect
  2. Access session_string property
- **Expected Result**: ValueError raised: "Client is not connected"
- **Coverage**: `session_string` property validation

#### TC-CLIENT-055: Get session_string raises with SQLiteSession
- **Purpose**: Verify session_string raises ValueError with SQLiteSession
- **Preconditions**: Connected client with SQLiteSession
- **Test Steps**:
  1. Create client with SQLiteSession
  2. Connect client
  3. Access session_string property
- **Expected Result**: ValueError raised: "Session is not a StringSession"
- **Coverage**: `session_string` property type check

#### TC-CLIENT-056: Create session with api_id and api_hash
- **Purpose**: Verify create_session() creates new session
- **Preconditions**: Valid api_id, api_hash, phone_number
- **Test Steps**:
  1. Mock TelegramClient and authentication flow
  2. Call await UserTelegramClient.create_session(api_id, api_hash, phone_number)
  3. Verify session string is returned
- **Expected Result**: Session string returned
- **Coverage**: `create_session()` classmethod

#### TC-CLIENT-057: Create session with Config object
- **Purpose**: Verify create_session() accepts Config object
- **Preconditions**: Config with api_id and api_hash
- **Test Steps**:
  1. Create Config with api_id and api_hash
  2. Mock TelegramClient and authentication flow
  3. Call await UserTelegramClient.create_session(config=config)
  4. Verify session string is returned
- **Expected Result**: Session string returned
- **Coverage**: `create_session()` with Config

#### TC-CLIENT-058: Create session interactive mode
- **Purpose**: Verify create_session() prompts for phone and code in interactive mode
- **Preconditions**: interactive=True (default)
- **Test Steps**:
  1. Mock input() and getpass.getpass() for phone and code
  2. Mock TelegramClient authentication flow
  3. Call await UserTelegramClient.create_session(api_id, api_hash)
  4. Verify input() and getpass.getpass() are called
- **Expected Result**: Prompts shown, session string returned
- **Coverage**: `create_session()` interactive mode

#### TC-CLIENT-059: Create session non-interactive mode
- **Purpose**: Verify create_session() uses provided phone_number when interactive=False
- **Preconditions**: interactive=False, phone_number provided
- **Test Steps**:
  1. Mock TelegramClient authentication flow
  2. Call await UserTelegramClient.create_session(api_id, api_hash, phone_number, interactive=False)
  3. Verify input() is not called
- **Expected Result**: No prompts, session string returned
- **Coverage**: `create_session()` non-interactive mode

#### TC-CLIENT-060: Create session with 2FA password
- **Purpose**: Verify create_session() handles 2FA password
- **Preconditions**: Account with 2FA enabled
- **Test Steps**:
  1. Mock sign_in() to raise password error
  2. Mock getpass.getpass() for password
  3. Mock successful sign_in() with password
  4. Call create_session()
- **Expected Result**: Password prompted, session string returned
- **Coverage**: `create_session()` 2FA handling

#### TC-CLIENT-061: Create session validates api_id
- **Purpose**: Verify create_session() validates api_id
- **Preconditions**: Invalid api_id (<= 0)
- **Test Steps**:
  1. Call create_session(api_id=0, api_hash="hash")
- **Expected Result**: ValueError raised: "api_id must be a positive number"
- **Coverage**: `create_session()` validation

#### TC-CLIENT-062: Create session validates phone number format
- **Purpose**: Verify create_session() validates phone number format
- **Preconditions**: Invalid phone number format
- **Test Steps**:
  1. Call create_session(api_id=123, api_hash="hash", phone_number="invalid")
- **Expected Result**: ValueError raised: "Invalid phone number format"
- **Coverage**: `create_session()` phone validation

#### TC-CLIENT-063: Create session requires phone_number when non-interactive
- **Purpose**: Verify create_session() requires phone_number when interactive=False
- **Preconditions**: interactive=False, phone_number=None
- **Test Steps**:
  1. Call create_session(api_id=123, api_hash="hash", interactive=False)
- **Expected Result**: ValueError raised: "phone_number is required when interactive=False"
- **Coverage**: `create_session()` parameter validation

#### TC-CLIENT-064: Create session requires api_id and api_hash
- **Purpose**: Verify create_session() requires api_id and api_hash
- **Preconditions**: Missing api_id or api_hash
- **Test Steps**:
  1. Call create_session(api_id=None, api_hash="hash")
  2. Call create_session(api_id=123, api_hash=None)
- **Expected Result**: ValueError raised: "api_id and api_hash are required"
- **Coverage**: `create_session()` required parameters

#### TC-CLIENT-065: Create session handles already authorized user
- **Purpose**: Verify create_session() handles already authorized user
- **Preconditions**: User already authorized
- **Test Steps**:
  1. Mock client.is_user_authorized() to return True
  2. Call create_session()
  3. Verify no authentication flow is triggered
- **Expected Result**: Session string returned without authentication
- **Coverage**: `create_session()` already authorized

#### TC-CLIENT-066: Create session disconnects client after use
- **Purpose**: Verify create_session() disconnects temporary client
- **Preconditions**: Successful session creation
- **Test Steps**:
  1. Mock TelegramClient
  2. Call create_session()
  3. Verify client.disconnect() is called in finally block
- **Expected Result**: Client disconnected
- **Coverage**: `create_session()` cleanup
