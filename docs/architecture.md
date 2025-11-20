# Architecture

This document describes the architecture and design decisions of TMA Framework.

## Overview

TMA Framework is designed as a simple, focused library for testing Telegram Mini Apps. It provides separate classes for different testing concerns, following the Single Responsibility Principle.

## Core Principles

### 1. Separation of Concerns

The framework separates different testing responsibilities:

- **UserTelegramClient**: Handles MTProto user simulation and bot interactions
- **MiniAppApi**: Focuses on HTTP API testing
- **MiniAppUI**: Handles browser-based UI testing

### 2. Async-First Design

All operations are asynchronous to support:
- Non-blocking HTTP requests
- Concurrent testing scenarios
- Better performance with I/O operations

### 3. High Performance

Uses `msgspec` for:
- Fast data serialization/deserialization
- Efficient validation
- Lower memory usage compared to alternatives

### 4. Simple Configuration

Configuration is handled through:
- Environment variables
- Config objects
- Sensible defaults

## Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│UserTelegramClient│   │   MiniAppApi    │    │   MiniAppUI     │
│                 │    │                 │    │                 │
│ • MTProto API   │    │ • HTTP Client   │    │ • Playwright    │
│ • User Sim      │    │ • initData      │    │ • Browser       │
│ • Bot Interact  │    │ • Validation    │    │ • UI Testing    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │     Config      │
                    │                 │
                    │ • API ID/Hash   │
                    │ • Session       │
                    │ • Timeouts      │
                    │ • Logging       │
                    └─────────────────┘
```

## Class Responsibilities

### UserTelegramClient

**Purpose**: Full user simulation with MTProto API

**Responsibilities**:
- User authentication and session management
- Bot interaction and message handling
- Mini App discovery from bot interactions
- Full user simulation capabilities

**Dependencies**:
- `telethon` for MTProto API
- `Config` for configuration

**Key Methods**:
- `get_me()` - Get user information
- `send_message()` - Send messages as user
- `get_messages()` - Get messages from chats
- `interact_with_bot()` - Interact with bots
- `get_mini_app_from_bot()` - Discover Mini Apps from bots

### MiniAppApi

**Purpose**: Test Mini App HTTP API endpoints

**Responsibilities**:
- HTTP request handling
- initData validation
- API response analysis

**Dependencies**:
- `httpx` for HTTP client
- `cryptography` for HMAC validation
- `Config` for configuration

**Key Methods**:
- `make_request()` - Make HTTP requests
- `validate_init_data()` - Validate Telegram initData

**Design Decisions**:
- No browser dependencies (pure HTTP)
- Focused on API testing only
- HMAC validation without browser context

### MiniAppUI

**Purpose**: Test Mini App user interface

**Responsibilities**:
- Browser automation
- UI element interaction
- Screenshot capture
- JavaScript execution

**Dependencies**:
- `playwright` for browser automation
- `Config` for configuration

**Key Methods**:
- `setup_browser()` - Initialize browser
- `click_element()` - Click elements
- `fill_input()` - Fill form fields
- `take_screenshot()` - Capture screenshots

**Design Decisions**:
- Uses Playwright for modern browser automation
- No Telegram WebApp API methods (they only work inside Telegram WebView)
- Focused on UI testing only

### Config

**Purpose**: Centralized configuration management

**Responsibilities**:
- Environment variable handling
- Configuration validation
- Default value management

**Dependencies**:
- `msgspec` for data validation
- `loguru` for logging configuration

**Key Features**:
- Type-safe configuration
- Environment variable support
- Validation with helpful error messages

## Data Models

### msgspec Integration

All data models use `msgspec.Struct` for:

**Benefits**:
- 2-4x faster serialization than Pydantic
- 2-3x faster validation
- 2-3x less memory usage
- Runtime type checking
- Zero-cost validation

**Models**:
- `BotInfo` - Bot information
- `WebViewResult` - WebView URL and parameters
- `MiniAppInfo` - Mini App metadata
- `ApiResult` - API request results

## Error Handling Strategy

### Exception Hierarchy

```
Exception
├── TMAFrameworkError (Base)
│   ├── ConfigurationError
│   ├── BotAPIError
│   ├── MiniAppError
│   └── ValidationError
```

### Error Handling Patterns

1. **Graceful Degradation**: Methods return results with error information
2. **Context Managers**: Automatic cleanup on exceptions
3. **Logging**: Comprehensive logging for debugging
4. **Type Safety**: Type hints for better error detection

## Resource Management

### Context Managers

All classes implement context managers for proper resource cleanup:

```python
async with MiniAppUI(url, config) as ui:
    # Automatic cleanup on exit
    await ui.setup_browser()
    # ... testing code ...
# Browser automatically closed
```

### Resource Lifecycle

1. **Initialization**: Create objects with configuration
2. **Setup**: Initialize resources (browser, HTTP client)
3. **Usage**: Perform testing operations
4. **Cleanup**: Automatic resource cleanup via context managers

## Performance Considerations

### HTTP Client Optimization

- Connection pooling with `httpx.Limits`
- Keep-alive connections
- Configurable timeouts
- Retry logic with exponential backoff

### Browser Optimization

- Headless mode for faster execution
- Single browser instance per test session
- Efficient element selection
- Screenshot optimization

### Memory Management

- `msgspec` for efficient serialization
- Automatic cleanup via context managers
- Minimal object creation
- Efficient data structures

## Testing Strategy

### Unit Testing

- Each class tested independently
- Mock external dependencies
- Test error conditions
- Validate configuration

### Integration Testing

- Test class interactions
- Real HTTP requests (with test endpoints)
- Browser automation tests
- End-to-end scenarios

### Performance Testing

- Benchmark serialization/deserialization
- Measure HTTP request times
- Browser automation performance
- Memory usage monitoring

## Security Considerations

### Bot Token Security

- Never log bot tokens
- Environment variable storage
- Validation of token format
- Secure transmission

### initData Validation

- HMAC-SHA256 validation
- Secure comparison using `compare_digest`
- Proper secret key derivation
- Timeout validation

### Browser Security

- Headless mode for security
- No sensitive data in screenshots
- Secure file handling
- Sandboxed execution

## Extensibility

### Plugin Architecture

The framework is designed for easy extension:

1. **Custom Validators**: Add custom validation logic
2. **Custom Clients**: Implement custom HTTP clients
3. **Custom Browsers**: Add support for other browsers
4. **Custom Models**: Extend data models

### Configuration Extensions

- Custom configuration sources
- Environment-specific settings
- Dynamic configuration updates
- Validation rule extensions

## Future Considerations

### Potential Enhancements

1. **Parallel Testing**: Support for concurrent test execution
2. **Test Reporting**: Integration with test reporting tools
3. **Mock Servers**: Built-in mock server for testing
4. **CI/CD Integration**: Better CI/CD pipeline support

### Scalability

- Horizontal scaling support
- Distributed testing capabilities
- Resource pooling
- Load balancing

## Design Trade-offs

### Simplicity vs. Features

**Chosen**: Simplicity
- Focused on core functionality
- Easy to understand and use
- Minimal dependencies
- Clear separation of concerns

### Performance vs. Flexibility

**Chosen**: Performance
- `msgspec` over Pydantic
- Optimized HTTP client
- Efficient browser usage
- Minimal overhead

### Synchronous vs. Asynchronous

**Chosen**: Asynchronous
- Better I/O performance
- Support for concurrent operations
- Modern Python patterns
- Future-proof design
