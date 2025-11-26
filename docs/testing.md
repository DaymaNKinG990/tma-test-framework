# Testing Documentation

This document provides comprehensive information about testing in TMA Framework, including test structure, coverage, and guidelines.

## Overview

TMA Framework has comprehensive test coverage with both unit and integration tests. The test suite ensures reliability, correctness, and maintainability of the framework.

## Test Structure

### Unit Tests

Unit tests are located in `tests/unit/` and cover individual components in isolation:

- **Config** - Configuration management and validation
- **BaseClient** - Base class functionality
- **ApiClient** (MiniAppApi) - HTTP API client
- **UiClient** (MiniAppUI) - Browser automation client
- **UserTelegramClient** - MTProto client
- **DBClient** - Database client
- **Models** - Data models and validation

### Integration Tests

Integration tests are located in `tests/integration/` and verify interactions between components:

- **MTProto + ApiClient** - Integration between Telegram client and API testing
- **MTProto + UiClient** - Integration between Telegram client and UI testing
- **End-to-End** - Complete workflows from start to finish
- **External Services** - Integration with real external services (optional)

## Test Case Documentation

Detailed test case specifications are documented in:

- `test_cases/unit/` - Unit test case specifications
- `test_cases/integration/` - Integration test case specifications

Each test case document includes:
- Test purpose and scope
- Preconditions
- Test steps
- Expected results
- Code coverage information

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Unit Tests Only

```bash
pytest tests/unit/
```

### Run Integration Tests Only

```bash
pytest tests/integration/
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/unit/test_config.py
```

### Run Specific Test

```bash
pytest tests/unit/test_config.py::TestConfig::test_init_with_valid_data
```

## Test Coverage

### Current Coverage Status

- **Unit Tests**: 100% test case coverage
- **Integration Tests**: 68.4% test case coverage (52/76 cases)
  - MTProto + MiniAppApi: 100% (15/15)
  - MTProto + MiniAppUI: 100% (19/19)
  - End-to-End: 100% (18/18)
  - External Services: 0% (0/24) - Requires real external services

### Coverage Goals

- ✅ **Unit Tests**: 100% coverage achieved
- ⏳ **Integration Tests**: Target 100% (excluding external services tests)

## Test Categories

### Unit Test Categories

1. **Initialization Tests** - Verify proper object creation
2. **Validation Tests** - Test input validation and error handling
3. **Method Tests** - Test individual methods and their behavior
4. **Edge Case Tests** - Test boundary conditions and unusual inputs
5. **Error Handling Tests** - Verify proper error handling

### Integration Test Categories

1. **Component Integration** - Test interactions between two components
2. **End-to-End Workflows** - Test complete user journeys
3. **Error Recovery** - Test error handling across components
4. **Performance** - Test system performance under load
5. **External Services** - Test with real external services (optional)

## Test Fixtures

The framework uses pytest fixtures for test setup and teardown:

- `valid_config` - Valid configuration object
- `user_telegram_client` - UserTelegramClient instance
- `user_telegram_client_connected` - Connected UserTelegramClient
- `miniapp_api_with_config` - ApiClient instance (aliased as MiniAppApi)
- `miniapp_ui_with_config` - UiClient instance (aliased as MiniAppUI)
- `mock_mini_app_url` - Mock Mini App URL

## Writing Tests

### Unit Test Example

```python
@pytest.mark.asyncio
async def test_make_request_get_method(
    self, mocker, miniapp_api_with_config, mock_httpx_response_200
):
    """Test make_request with GET method."""
    miniapp_api_with_config.client.request = mocker.AsyncMock(
        return_value=mock_httpx_response_200
    )

    result = await miniapp_api_with_config.make_request("/api/status")

    assert result.status_code == 200
    assert result.success is True
```

### Integration Test Example

```python
@pytest.mark.asyncio
async def test_get_mini_app_and_test_api(
    self, mocker, user_telegram_client_connected, mock_mini_app_url
):
    """Test getting Mini App from bot and testing API."""
    mock_mini_app_ui = mocker.MagicMock()
    mock_mini_app_ui.url = mock_mini_app_url
    user_telegram_client_connected.get_mini_app_from_bot = mocker.AsyncMock(
        return_value=mock_mini_app_ui
    )

    mini_app_ui = await user_telegram_client_connected.get_mini_app_from_bot("test_bot")
    config = user_telegram_client_connected.config
    from tma_test_framework.clients import ApiClient as MiniAppApi
    mini_app_api = MiniAppApi(mini_app_ui.url, config)

    # Test API...
```

## External Services Testing

Some integration tests require real external services. These tests are documented in `test_cases/integration/external_services_requirements.md` and include:

- Real Telegram MTProto API connection
- Real HTTP/HTTPS endpoints
- Real browser automation
- Network testing scenarios

These tests are optional and can be skipped in CI/CD environments where external services are not available.

## Best Practices

1. **Isolation** - Each test should be independent and not rely on other tests
2. **Mocking** - Use mocks for external dependencies to keep tests fast and reliable
3. **Clear Names** - Use descriptive test names that explain what is being tested
4. **Documentation** - Document complex test scenarios and edge cases
5. **Coverage** - Aim for high coverage but focus on meaningful tests
6. **Performance** - Keep tests fast; use async/await appropriately

## Continuous Integration

Tests are automatically run in CI/CD pipelines:

- All unit tests must pass
- Integration tests (excluding external services) must pass
- Code coverage must meet minimum threshold of 80% (configured in `pyproject.toml`)
- Linting and type checking must pass

## Troubleshooting Tests

### Common Issues

1. **Import Errors** - Ensure all dependencies are installed
2. **Async Issues** - Use `@pytest.mark.asyncio` for async tests
3. **Mock Issues** - Ensure mocks are set up before use
4. **Fixture Issues** - Check fixture scope and dependencies

### Getting Help

- Check test case documentation in `test_cases/`
- Review existing tests for examples
- Check pytest documentation for advanced features
