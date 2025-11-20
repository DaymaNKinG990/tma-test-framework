# MiniAppUI Class - Unit Test Cases

## Overview
Tests for `src.mini_app.ui.MiniAppUI` class - UI testing client using Playwright.

## Test Categories

### 1. Initialization Tests

#### TC-UI-001: Initialize MiniAppUI with URL and config
- **Purpose**: Verify MiniAppUI can be initialized
- **Preconditions**: Valid URL and Config
- **Test Steps**:
  1. Create MiniAppUI(url, config)
  2. Verify url, config, browser=None, page=None
- **Expected Result**: MiniAppUI created with browser and page as None
- **Coverage**: `__init__` method

#### TC-UI-002: Initialize MiniAppUI with config=None raises error
- **Purpose**: Verify MiniAppUI rejects None config with ValueError
- **Preconditions**: Valid URL, config=None
- **Test Steps**:
  1. Create MiniAppUI(url, config=None)
  2. Verify ValueError is raised with message "config is required"
- **Expected Result**: ValueError raised (Config is required)
- **Coverage**: `__init__` validation

### 2. setup_browser() Tests

#### TC-UI-003: Setup browser for first time
- **Purpose**: Verify setup_browser() launches browser and creates page
- **Preconditions**: MiniAppUI instance, browser not setup
- **Test Steps**:
  1. Call await ui.setup_browser()
  2. Verify browser is created
  3. Verify page is created
  4. Verify user agent is set
- **Expected Result**: Browser and page created, user agent set, returns self
- **Coverage**: `setup_browser()` first call

#### TC-UI-004: Setup browser when already setup
- **Purpose**: Verify setup_browser() is idempotent
- **Preconditions**: Browser already setup
- **Test Steps**:
  1. Call setup_browser() twice
  2. Verify browser is not recreated
  3. Verify debug log "Browser already setup"
- **Expected Result**: No new browser created, returns self
- **Coverage**: `setup_browser()` idempotency

#### TC-UI-005: Verify setup_browser returns Self
- **Purpose**: Verify method chaining works
- **Preconditions**: MiniAppUI instance
- **Test Steps**:
  1. Call ui.setup_browser()
  2. Verify returns self
  3. Verify can chain: ui.setup_browser().click_element(...)
- **Expected Result**: Returns self for method chaining
- **Coverage**: `setup_browser()` return value

#### TC-UI-042: Reject setup_browser with empty or invalid URL
- **Purpose**: Verify setup_browser() rejects empty, None, or invalid URL
- **Preconditions**: MiniAppUI with empty/None/invalid URL
- **Test Steps**:
  1. Create MiniAppUI with url="" or url=None or url="   "
  2. Call await ui.setup_browser()
  3. Verify ValueError is raised with message about URL not set
- **Expected Result**: ValueError raised: "URL is not set or is empty. Cannot setup browser without a valid URL."
- **Coverage**: `setup_browser()` URL validation

#### TC-UI-043: Handle navigation error in setup_browser
- **Purpose**: Verify setup_browser() handles navigation failures gracefully
- **Preconditions**: Browser setup, page.goto() raises exception
- **Test Steps**:
  1. Setup browser
  2. Mock page.goto() to raise exception (e.g., TimeoutError, NetworkError)
  3. Call await ui.setup_browser()
  4. Verify RuntimeError is raised with error message
  5. Verify error is logged
- **Expected Result**: RuntimeError raised: "Failed to navigate to {url}: {error}", error logged
- **Coverage**: `setup_browser()` navigation error handling

### 3. close() Tests

#### TC-UI-006: Close browser when open
- **Purpose**: Verify close() closes browser
- **Preconditions**: Browser is open
- **Test Steps**:
  1. Setup browser
  2. Call await ui.close()
  3. Verify browser.close() was called
- **Expected Result**: Browser closed successfully
- **Coverage**: `close()` method

#### TC-UI-007: Close browser when not open
- **Purpose**: Verify close() handles no browser gracefully
- **Preconditions**: Browser not setup
- **Test Steps**:
  1. Call await ui.close()
  2. Verify no errors
- **Expected Result**: No errors, graceful handling
- **Coverage**: `close()` when browser=None

### 4. Element Interaction Tests

#### TC-UI-008: Click element successfully
- **Purpose**: Verify click_element() clicks element
- **Preconditions**: Browser setup, element exists
- **Test Steps**:
  1. Setup browser and navigate to page
  2. Call await ui.click_element("#button")
  3. Verify page.click() was called
  4. Verify debug log
- **Expected Result**: Element clicked, logged
- **Coverage**: `click_element()` success

#### TC-UI-009: Click element with exception
- **Purpose**: Verify click_element() handles errors
- **Preconditions**: Element doesn't exist
- **Test Steps**:
  1. Setup browser
  2. Call click_element() with non-existent selector
  3. Verify error is logged
- **Expected Result**: Error logged, no exception raised
- **Coverage**: `click_element()` exception handling

#### TC-UI-010: Fill input field
- **Purpose**: Verify fill_input() fills input
- **Preconditions**: Browser setup, input exists
- **Test Steps**:
  1. Setup browser
  2. Call await ui.fill_input("#input", "text")
  3. Verify page.fill() was called
  4. Verify debug log
- **Expected Result**: Input filled, logged
- **Coverage**: `fill_input()` method

#### TC-UI-011: Fill input with exception
- **Purpose**: Verify fill_input() handles errors
- **Preconditions**: Input doesn't exist
- **Test Steps**:
  1. Call fill_input() with non-existent selector
  2. Verify error is logged
- **Expected Result**: Error logged
- **Coverage**: `fill_input()` exception handling

#### TC-UI-012: Wait for element to appear
- **Purpose**: Verify wait_for_element() waits for element
- **Preconditions**: Browser setup
- **Test Steps**:
  1. Setup browser
  2. Call await ui.wait_for_element("#element", timeout=5000)
  3. Verify page.wait_for_selector() was called
- **Expected Result**: Element wait completed, logged
- **Coverage**: `wait_for_element()` method

#### TC-UI-013: Wait for element timeout
- **Purpose**: Verify wait_for_element() handles timeout
- **Preconditions**: Element never appears
- **Test Steps**:
  1. Call wait_for_element() with short timeout
  2. Verify timeout error is logged
- **Expected Result**: Timeout error logged
- **Coverage**: `wait_for_element()` timeout

#### TC-UI-014: Get element text
- **Purpose**: Verify get_element_text() returns text
- **Preconditions**: Element exists with text
- **Test Steps**:
  1. Setup browser
  2. Call await ui.get_element_text("#element")
  3. Verify text is returned
- **Expected Result**: Element text returned, logged
- **Coverage**: `get_element_text()` method

#### TC-UI-015: Get element text when element doesn't exist
- **Purpose**: Verify get_element_text() returns None
- **Preconditions**: Element doesn't exist
- **Test Steps**:
  1. Call get_element_text() with non-existent selector
  2. Verify returns None
- **Expected Result**: Returns None, error logged
- **Coverage**: `get_element_text()` not found

#### TC-UI-016: Get element attribute value
- **Purpose**: Verify get_element_attribute_value() returns attribute
- **Preconditions**: Element exists with attribute
- **Test Steps**:
  1. Setup browser
  2. Call await ui.get_element_attribute_value("#element", "href")
  3. Verify attribute value returned
- **Expected Result**: Attribute value returned, logged
- **Coverage**: `get_element_attribute_value()` method

#### TC-UI-017: Get element attribute when element doesn't exist
- **Purpose**: Verify get_element_attribute_value() returns None
- **Preconditions**: Element doesn't exist
- **Test Steps**:
  1. Call get_element_attribute_value() with non-existent selector
  2. Verify returns None
- **Expected Result**: Returns None, error logged
- **Coverage**: `get_element_attribute_value()` not found

#### TC-UI-018: Scroll to element
- **Purpose**: Verify scroll_to_element() scrolls
- **Preconditions**: Browser setup, element exists
- **Test Steps**:
  1. Setup browser
  2. Call await ui.scroll_to_element("#element")
  3. Verify scroll_into_view_if_needed() was called
- **Expected Result**: Scrolled to element, logged
- **Coverage**: `scroll_to_element()` method

#### TC-UI-019: Scroll to element with exception
- **Purpose**: Verify scroll_to_element() handles errors
- **Preconditions**: Element doesn't exist
- **Test Steps**:
  1. Call scroll_to_element() with non-existent selector
  2. Verify error is logged
- **Expected Result**: Error logged
- **Coverage**: `scroll_to_element()` exception handling

#### TC-UI-020: Hover over element
- **Purpose**: Verify hover_element() hovers
- **Preconditions**: Browser setup, element exists
- **Test Steps**:
  1. Setup browser
  2. Call await ui.hover_element("#element")
  3. Verify page.hover() was called
- **Expected Result**: Element hovered, logged
- **Coverage**: `hover_element()` method

#### TC-UI-021: Double click element
- **Purpose**: Verify double_click_element() double clicks
- **Preconditions**: Browser setup, element exists
- **Test Steps**:
  1. Setup browser
  2. Call await ui.double_click_element("#element")
  3. Verify page.dblclick() was called
- **Expected Result**: Element double clicked, logged
- **Coverage**: `double_click_element()` method

#### TC-UI-022: Right click element
- **Purpose**: Verify right_click_element() right clicks
- **Preconditions**: Browser setup, element exists
- **Test Steps**:
  1. Setup browser
  2. Call await ui.right_click_element("#element")
  3. Verify page.click(button="right") was called
- **Expected Result**: Element right clicked, logged
- **Coverage**: `right_click_element()` method

#### TC-UI-023: Select option from dropdown
- **Purpose**: Verify select_option() selects option
- **Preconditions**: Browser setup, select element exists
- **Test Steps**:
  1. Setup browser
  2. Call await ui.select_option("#select", "value")
  3. Verify page.select_option() was called
- **Expected Result**: Option selected, logged
- **Coverage**: `select_option()` method

#### TC-UI-024: Check checkbox
- **Purpose**: Verify check_checkbox() checks checkbox
- **Preconditions**: Browser setup, checkbox exists
- **Test Steps**:
  1. Setup browser
  2. Call await ui.check_checkbox("#checkbox")
  3. Verify page.check() was called
- **Expected Result**: Checkbox checked, logged
- **Coverage**: `check_checkbox()` method

#### TC-UI-025: Uncheck checkbox
- **Purpose**: Verify uncheck_checkbox() unchecks checkbox
- **Preconditions**: Browser setup, checkbox exists
- **Test Steps**:
  1. Setup browser
  2. Call await ui.uncheck_checkbox("#checkbox")
  3. Verify page.uncheck() was called
- **Expected Result**: Checkbox unchecked, logged
- **Coverage**: `uncheck_checkbox()` method

#### TC-UI-026: Upload file
- **Purpose**: Verify upload_file() uploads file
- **Preconditions**: Browser setup, file input exists
- **Test Steps**:
  1. Setup browser
  2. Call await ui.upload_file("#file-input", "path/to/file")
  3. Verify page.set_input_files() was called
- **Expected Result**: File uploaded, logged
- **Coverage**: `upload_file()` method

### 5. Keyboard Tests

#### TC-UI-027: Press key
- **Purpose**: Verify press_key() presses key
- **Preconditions**: Browser setup
- **Test Steps**:
  1. Setup browser
  2. Call await ui.press_key("Enter")
  3. Verify page.keyboard.press() was called
- **Expected Result**: Key pressed, logged
- **Coverage**: `press_key()` method

#### TC-UI-028: Type text
- **Purpose**: Verify type_text() types text
- **Preconditions**: Browser setup
- **Test Steps**:
  1. Setup browser
  2. Call await ui.type_text("Hello")
  3. Verify page.keyboard.type() was called
- **Expected Result**: Text typed, logged
- **Coverage**: `type_text()` method

### 6. Navigation and Page State Tests

#### TC-UI-029: Wait for navigation
- **Purpose**: Verify wait_for_navigation() waits
- **Preconditions**: Browser setup
- **Test Steps**:
  1. Setup browser
  2. Call await ui.wait_for_navigation(timeout=5000)
  3. Verify page.wait_for_load_state() was called
- **Expected Result**: Navigation wait completed, logged
- **Coverage**: `wait_for_navigation()` method

#### TC-UI-030: Wait for navigation timeout
- **Purpose**: Verify wait_for_navigation() handles timeout
- **Preconditions**: Navigation never completes
- **Test Steps**:
  1. Call wait_for_navigation() with short timeout
  2. Verify timeout error is logged
- **Expected Result**: Timeout error logged
- **Coverage**: `wait_for_navigation()` timeout

#### TC-UI-031: Get page title
- **Purpose**: Verify get_page_title() returns title
- **Preconditions**: Browser setup, page loaded
- **Test Steps**:
  1. Setup browser and navigate
  2. Call await ui.get_page_title()
  3. Verify page.title() was called
- **Expected Result**: Page title returned, logged
- **Coverage**: `get_page_title()` method

#### TC-UI-032: Get page title with exception
- **Purpose**: Verify get_page_title() handles errors
- **Preconditions**: Exception accessing title
- **Test Steps**:
  1. Mock page.title() to raise exception
  2. Call get_page_title()
  3. Verify returns empty string, error logged
- **Expected Result**: Returns "", error logged
- **Coverage**: `get_page_title()` exception handling

#### TC-UI-033: Get page URL
- **Purpose**: Verify get_page_url() returns URL
- **Preconditions**: Browser setup, page loaded
- **Test Steps**:
  1. Setup browser and navigate
  2. Call await ui.get_page_url()
  3. Verify page.url is accessed
- **Expected Result**: Page URL returned, logged
- **Coverage**: `get_page_url()` method

#### TC-UI-034: Get page URL with exception
- **Purpose**: Verify get_page_url() handles errors
- **Preconditions**: Exception accessing URL
- **Test Steps**:
  1. Mock page.url to raise exception
  2. Call get_page_url()
  3. Verify returns empty string, error logged
- **Expected Result**: Returns "", error logged
- **Coverage**: `get_page_url()` exception handling

### 7. Screenshot and Script Tests

#### TC-UI-035: Take screenshot
- **Purpose**: Verify take_screenshot() saves screenshot
- **Preconditions**: Browser setup, page loaded
- **Test Steps**:
  1. Setup browser
  2. Call await ui.take_screenshot("screenshot.png")
  3. Verify page.screenshot() was called
- **Expected Result**: Screenshot saved, logged
- **Coverage**: `take_screenshot()` method

#### TC-UI-036: Take screenshot with exception
- **Purpose**: Verify take_screenshot() handles errors
- **Preconditions**: Exception during screenshot
- **Test Steps**:
  1. Mock page.screenshot() to raise exception
  2. Call take_screenshot()
  3. Verify error is logged
- **Expected Result**: Error logged
- **Coverage**: `take_screenshot()` exception handling

#### TC-UI-037: Execute JavaScript script
- **Purpose**: Verify execute_script() executes script
- **Preconditions**: Browser setup
- **Test Steps**:
  1. Setup browser
  2. Call await ui.execute_script("return document.title")
  3. Verify page.evaluate() was called
  4. Verify result is returned
- **Expected Result**: Script executed, result returned, logged
- **Coverage**: `execute_script()` method

#### TC-UI-038: Execute script with exception
- **Purpose**: Verify execute_script() handles errors
- **Preconditions**: Script causes exception
- **Test Steps**:
  1. Mock page.evaluate() to raise exception
  2. Call execute_script()
  3. Verify returns None, error logged
- **Expected Result**: Returns None, error logged
- **Coverage**: `execute_script()` exception handling

### 8. Edge Cases

#### TC-UI-039: Use methods before browser setup
- **Purpose**: Verify methods handle missing browser
- **Preconditions**: Browser not setup
- **Test Steps**:
  1. Call click_element() without setup_browser()
  2. Verify exception is raised or handled
- **Expected Result**: Appropriate error handling
- **Coverage**: Error handling for missing browser

#### TC-UI-040: Use methods with unicode selectors
- **Purpose**: Verify methods handle unicode in selectors
- **Preconditions**: Selector with unicode
- **Test Steps**:
  1. Call click_element() with unicode selector
  2. Verify works correctly
- **Expected Result**: Works with unicode
- **Coverage**: Unicode handling

#### TC-UI-041: Use methods with very long selectors
- **Purpose**: Verify methods handle long selectors
- **Preconditions**: Very long selector string
- **Test Steps**:
  1. Call click_element() with very long selector
  2. Verify works correctly
- **Expected Result**: Works with long selectors
- **Coverage**: Large data handling
