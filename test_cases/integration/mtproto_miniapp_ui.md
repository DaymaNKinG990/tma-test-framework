# MTProto + UiClient Integration Test Cases

## Overview
Tests for integration between `UserTelegramClient` and `UiClient` (aliased as `MiniAppUI`) components.

## Test Categories

### 1. Get Mini App and Test UI

#### TC-INTEGRATION-MTUI-001: Get Mini App from bot and test UI
- **Purpose**: Verify complete flow: get Mini App from bot, then test its UI
- **Preconditions**:
  - Valid Telegram session
  - Bot that responds with Mini App URL
  - Mini App with accessible UI
- **Test Steps**:
  1. Create UserTelegramClient with valid config
  2. Connect to Telegram
  3. Call `get_mini_app_from_bot(bot_username)`
  4. Verify `UiClient` is returned with correct URL
  5. Setup browser using `setup_browser()`
  6. Navigate to Mini App URL
  7. Test UI elements (click, fill, etc.)
- **Expected Result**: Mini App retrieved and UI tested successfully
- **Coverage**: `get_mini_app_from_bot()`, `UiClient` methods (or `MiniAppUI` methods)
- **Dependencies**: Real Telegram bot, Mini App with UI

#### TC-INTEGRATION-MTUI-002: Get Mini App with start_param and test UI
- **Purpose**: Verify Mini App retrieval with start parameter and UI testing
- **Preconditions**: Bot that accepts start parameters
- **Test Steps**:
  1. Connect UserTelegramClient
  2. Call `get_mini_app_from_bot(bot_username, start_param="123")`
  3. Verify Mini App URL contains start parameter
  4. Setup browser and navigate
  5. Verify UI reflects start parameter
- **Expected Result**: Mini App retrieved with start param, UI works
- **Coverage**: `get_mini_app_from_bot()` with start_param, UI navigation
- **Dependencies**: Bot supporting start parameters

#### TC-INTEGRATION-MTUI-003: Get Mini App from media and test UI
- **Purpose**: Verify Mini App retrieval from message media and UI testing
- **Preconditions**: Bot that sends Mini App in media
- **Test Steps**:
  1. Connect UserTelegramClient
  2. Get messages from bot
  3. Find message with web_app media
  4. Extract Mini App URL from media
  5. Create `UiClient` (or use `MiniAppUI` alias) and test UI
- **Expected Result**: Mini App extracted from media, UI tested
- **Coverage**: `get_mini_app_from_bot()` media extraction, UI testing
- **Dependencies**: Bot with web_app media

### 2. UI Interaction Scenarios

#### TC-INTEGRATION-MTUI-004: Complete form submission flow
- **Purpose**: Verify complete form submission in Mini App
- **Preconditions**: Mini App with form
- **Test Steps**:
  1. Get Mini App from bot
  2. Setup browser and navigate
  3. Fill form fields using `fill_input()`
  4. Click submit button using `click_element()`
  5. Wait for response using `wait_for_navigation()`
  6. Verify success message
- **Expected Result**: Form submitted successfully
- **Coverage**: Form interaction flow
- **Dependencies**: Mini App with form

#### TC-INTEGRATION-MTUI-005: Test button interactions
- **Purpose**: Verify various button interactions
- **Preconditions**: Mini App with multiple buttons
- **Test Steps**:
  1. Get Mini App from bot
  2. Setup browser and navigate
  3. Click primary button
  4. Click secondary button
  5. Double-click action button
  6. Right-click context button
  7. Verify all interactions work
- **Expected Result**: All button interactions work
- **Coverage**: Button interaction methods
- **Dependencies**: Mini App with buttons

#### TC-INTEGRATION-MTUI-006: Test dropdown and selection
- **Purpose**: Verify dropdown and option selection
- **Preconditions**: Mini App with dropdown
- **Test Steps**:
  1. Get Mini App from bot
  2. Setup browser and navigate
  3. Click dropdown to open
  4. Select option using `select_option()`
  5. Verify selection is applied
- **Expected Result**: Dropdown selection works
- **Coverage**: `select_option()` method
- **Dependencies**: Mini App with dropdown

#### TC-INTEGRATION-MTUI-007: Test checkbox interactions
- **Purpose**: Verify checkbox check/uncheck
- **Preconditions**: Mini App with checkboxes
- **Test Steps**:
  1. Get Mini App from bot
  2. Setup browser and navigate
  3. Check checkbox using `check_checkbox()`
  4. Verify checkbox is checked
  5. Uncheck using `uncheck_checkbox()`
  6. Verify checkbox is unchecked
- **Expected Result**: Checkbox interactions work
- **Coverage**: `check_checkbox()`, `uncheck_checkbox()`
- **Dependencies**: Mini App with checkboxes

### 3. Navigation and Page State

#### TC-INTEGRATION-MTUI-008: Test page navigation
- **Purpose**: Verify navigation between pages
- **Preconditions**: Mini App with multiple pages
- **Test Steps**:
  1. Get Mini App from bot
  2. Setup browser and navigate
  3. Click navigation link
  4. Wait for navigation using `wait_for_navigation()`
  5. Verify new page URL using `get_page_url()`
  6. Verify page title using `get_page_title()`
- **Expected Result**: Navigation works correctly
- **Coverage**: Navigation methods
- **Dependencies**: Mini App with navigation

#### TC-INTEGRATION-MTUI-009: Test scrolling and element visibility
- **Purpose**: Verify scrolling to elements
- **Preconditions**: Mini App with scrollable content
- **Test Steps**:
  1. Get Mini App from bot
  2. Setup browser and navigate
  3. Scroll to element using `scroll_to_element()`
  4. Verify element is visible
  5. Get element text using `get_element_text()`
- **Expected Result**: Scrolling and element access work
- **Coverage**: Scrolling and element methods
- **Dependencies**: Mini App with scrollable content

### 4. Screenshots and Visual Testing

#### TC-INTEGRATION-MTUI-010: Take screenshot of Mini App
- **Purpose**: Verify screenshot capture
- **Preconditions**: Mini App with visual content
- **Test Steps**:
  1. Get Mini App from bot
  2. Setup browser and navigate
  3. Take screenshot using `take_screenshot()`
  4. Verify screenshot file is created
  5. Verify screenshot is not empty
- **Expected Result**: Screenshot captured successfully
- **Coverage**: `take_screenshot()` method
- **Dependencies**: Mini App with visual content

#### TC-INTEGRATION-MTUI-011: Take screenshot of specific element
- **Purpose**: Verify element-specific screenshot
- **Preconditions**: Mini App with identifiable elements
- **Test Steps**:
  1. Get Mini App from bot
  2. Setup browser and navigate
  3. Take screenshot of specific element
  4. Verify element screenshot is captured
- **Expected Result**: Element screenshot works
- **Coverage**: Element screenshot functionality
- **Dependencies**: Mini App with elements

### 5. JavaScript Execution

#### TC-INTEGRATION-MTUI-012: Execute JavaScript in Mini App
- **Purpose**: Verify JavaScript execution
- **Preconditions**: Mini App with JavaScript
- **Test Steps**:
  1. Get Mini App from bot
  2. Setup browser and navigate
  3. Execute JavaScript using `execute_script()`
  4. Verify script result is returned
- **Expected Result**: JavaScript executed successfully
- **Coverage**: `execute_script()` method
- **Dependencies**: Mini App with JavaScript

#### TC-INTEGRATION-MTUI-013: Get data via JavaScript
- **Purpose**: Verify data extraction via JavaScript
- **Preconditions**: Mini App with data in JavaScript
- **Test Steps**:
  1. Get Mini App from bot
  2. Setup browser and navigate
  3. Execute script to get data: `return window.appData`
  4. Verify data is returned correctly
- **Expected Result**: Data extracted via JavaScript
- **Coverage**: JavaScript data extraction
- **Dependencies**: Mini App with JavaScript data

### 6. Error Handling Integration

#### TC-INTEGRATION-MTUI-014: Handle Mini App not found
- **Purpose**: Verify error handling when Mini App not found
- **Preconditions**: Bot that doesn't provide Mini App
- **Test Steps**:
  1. Connect UserTelegramClient
  2. Call `get_mini_app_from_bot("bot_without_miniapp")`
  3. Verify returns None or handles gracefully
- **Expected Result**: Error handled, no crash
- **Coverage**: Error handling in `get_mini_app_from_bot()`
- **Dependencies**: Bot without Mini App

#### TC-INTEGRATION-MTUI-015: Handle UI element not found
- **Purpose**: Verify error handling for missing UI elements
- **Preconditions**: Mini App with missing elements
- **Test Steps**:
  1. Get Mini App from bot
  2. Setup browser and navigate
  3. Try to click non-existent element
  4. Verify error is handled gracefully
- **Expected Result**: Error handled, no crash
- **Coverage**: Error handling in UI methods
- **Dependencies**: Mini App with missing elements

#### TC-INTEGRATION-MTUI-016: Handle browser errors
- **Purpose**: Verify browser error handling
- **Preconditions**: Mini App that causes browser errors
- **Test Steps**:
  1. Get Mini App from bot
  2. Setup browser and navigate
  3. Trigger browser error (e.g., invalid JavaScript)
  4. Verify error is caught and handled
- **Expected Result**: Browser errors handled gracefully
- **Coverage**: Browser error handling
- **Dependencies**: Mini App causing errors

### 7. Context Manager Integration

#### TC-INTEGRATION-MTUI-017: Use context manager for full flow
- **Purpose**: Verify context manager usage in integration
- **Preconditions**: Valid config and bot
- **Test Steps**:
  1. Use `async with UserTelegramClient(config) as client:`
  2. Get Mini App from bot
  3. Use `async with UiClient(url, config) as ui:` (or `async with MiniAppUI(url, config) as ui:`)
  4. Setup browser and test UI
  5. Verify both close correctly on exit
- **Expected Result**: Both clients close properly
- **Coverage**: Context managers integration
- **Dependencies**: Valid setup

### 8. Performance Integration

#### TC-INTEGRATION-MTUI-018: Test UI loading performance
- **Purpose**: Verify Mini App UI loads in reasonable time
- **Preconditions**: Mini App with measurable load time
- **Test Steps**:
  1. Get Mini App from bot
  2. Setup browser
  3. Measure time to navigate and load
  4. Verify load time is acceptable
- **Expected Result**: UI loads in reasonable time
- **Coverage**: Performance measurement
- **Dependencies**: Mini App with load time

#### TC-INTEGRATION-MTUI-019: Test multiple UI interactions performance
- **Purpose**: Verify performance with multiple interactions
- **Preconditions**: Mini App with multiple interactive elements
- **Test Steps**:
  1. Get Mini App from bot
  2. Setup browser and navigate
  3. Perform 10 sequential UI interactions
  4. Measure total time
  5. Verify all interactions complete
- **Expected Result**: All interactions complete in reasonable time
- **Coverage**: Performance with multiple interactions
- **Dependencies**: Mini App with multiple elements
