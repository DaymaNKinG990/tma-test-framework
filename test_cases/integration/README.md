# Integration Test Cases

## Overview

This directory contains test case documentation for integration tests of the TMA Framework. Integration tests verify the interaction between multiple components and real services.

## Structure

Integration tests are organized by component interactions:

1. **mtproto_miniapp_api.md** - Integration between UserTelegramClient and MiniAppApi
2. **mtproto_miniapp_ui.md** - Integration between UserTelegramClient and MiniAppUI
3. **end_to_end.md** - End-to-end workflows (full user journeys)
4. **external_services.md** - Integration with external services (Telegram API, HTTP endpoints)

## Test Categories

### 1. Component Integration Tests
Tests that verify interaction between two or more components:
- UserTelegramClient ↔ MiniAppApi
- UserTelegramClient ↔ MiniAppUI
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
