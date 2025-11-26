# Integration Test Cases

## Overview

This directory contains test case documentation for integration tests of the TMA Framework. Integration tests verify the interaction between multiple components and real services.

## Structure

Integration tests are organized by component interactions:

1. **mtproto_miniapp_api.md** - Integration between UserTelegramClient and ApiClient (MiniAppApi)
2. **mtproto_miniapp_ui.md** - Integration between UserTelegramClient and UiClient (MiniAppUI)
3. **end_to_end.md** - End-to-end workflows (full user journeys)
4. **external_services.md** - Integration with external services (Telegram API, HTTP endpoints)
5. **mtproto_api_auth.md** - Integration for `setup_tma_auth` method (NEW - 7 test cases)
6. **db_client_integration.md** - Integration for DBClient with all components (NEW - 9 test cases)
7. **MISSING_INTEGRATION_TEST_CASES.md** - Analysis of missing integration test cases (reference)

> **Note**: All previously identified missing test cases have been added. See [MISSING_INTEGRATION_TEST_CASES.md](./MISSING_INTEGRATION_TEST_CASES.md) for original analysis.

## Test Categories

### 1. Component Integration Tests
Tests that verify interaction between two or more components:
- UserTelegramClient ↔ ApiClient (MiniAppApi) - see [mtproto_miniapp_api.md](./mtproto_miniapp_api.md)
- UserTelegramClient ↔ UiClient (MiniAppUI) - see [mtproto_miniapp_ui.md](./mtproto_miniapp_ui.md)
- UserTelegramClient ↔ DBClient - see [db_client_integration.md](./db_client_integration.md)
- ApiClient ↔ DBClient - see [db_client_integration.md](./db_client_integration.md)
- UiClient ↔ DBClient - see [db_client_integration.md](./db_client_integration.md)
- ApiClient.setup_tma_auth ↔ UserTelegramClient - see [mtproto_api_auth.md](./mtproto_api_auth.md)
- Config ↔ All components

### 2. End-to-End Tests
Complete user workflows:
- Getting Mini App from bot → Testing via API
- Getting Mini App from bot → Testing via UI
- Full testing cycle: API + UI

### 3. External Service Integration
Tests with real or mocked external services:
- Telegram MTProto API
- HTTP endpoints
- Browser automation (Playwright)

## Test Case Format

Each test case follows this structure:

```
#### TC-INTEGRATION-XXX: Test Name
- **Purpose**: What this test verifies
- **Preconditions**: Required setup and state
- **Test Steps**:
  1. Step 1
  2. Step 2
  3. Step 3
- **Expected Result**: What should happen
- **Coverage**: Which components/interactions are tested
- **Dependencies**: External services or data required
```

## Markers

Integration tests use the `@pytest.mark.integration` marker and may also use:
- `@pytest.mark.slow` - Tests that take significant time
- `@pytest.mark.external` - Tests requiring external services
- `@pytest.mark.async` - Async integration tests

## Notes

- Integration tests may require real credentials or test accounts
- Some tests may be skipped in CI/CD if external services are unavailable
- Integration tests should be isolated and not depend on execution order
