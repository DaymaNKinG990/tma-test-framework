# External Services Integration Test Cases

## Overview
Tests for integration with external services: Telegram MTProto API, HTTP endpoints, and browser automation.

## Test Categories

### 1. Telegram MTProto API Integration

**Note on Test Implementation**: All Telegram integration tests use mocked Telethon/UserTelegramClient interactions to ensure deterministic, secure, and CI-friendly test execution. Tests use `pytest-mock` or `unittest.mock` to stub `connect()`, `is_connected()`, `get_me()`, `send_message()`, and `get_entity()` methods, returning controlled test data from fixtures instead of making real API calls. No real Telegram credentials are required.

#### TC-INTEGRATION-EXT-001: Connect to Telegram API (Mocked)
- **Purpose**: Verify connection logic to Telegram MTProto API using mocked client
- **Preconditions**:
  - Test fixtures: `user_telegram_client`, `mock_telegram_client_authorized`, `mock_telegram_user`
  - Mocked `TelegramClient` instance
- **Test Steps**:
  1. Create `UserTelegramClient` with test config (using `user_telegram_client` fixture)
  2. Mock `client.connect()` to return successfully (no exception)
  3. Mock `client.is_user_authorized()` to return `True`
  4. Mock `client.get_me()` to return `mock_telegram_user` fixture
  5. Call `connect()` on `UserTelegramClient`
  6. Verify `connect()` completes without exception
  7. Verify `is_connected()` returns `True`
  8. Verify `get_me()` returns `UserInfo` object matching `mock_telegram_user` data:
     - `id = 123456789`
     - `username = "test_user"`
     - `first_name = "Test User"`
     - `last_name = "Test"`
     - `phone = "+1234567890"`
     - `is_bot = False`
     - `is_verified = True`
     - `is_premium = False`
- **Expected Result**: Connection logic succeeds, `is_connected()` returns `True`, `get_me()` returns expected `UserInfo`
- **Coverage**: Telegram API connection logic (mocked)
- **Required Mocks/Fixtures**:
  - `user_telegram_client` fixture (from `tests/fixtures/mtproto_client.py`)
  - `mock_telegram_client_authorized` fixture (mocked `TelegramClient` with `connect()`, `is_user_authorized()`, `get_me()` stubbed)
  - `mock_telegram_user` fixture (mock `User` object with test data)
- **Test Data**: Test-only sample data from fixtures, no real credentials needed

#### TC-INTEGRATION-EXT-002: Send message to bot (Mocked)
- **Purpose**: Verify sending message logic using mocked bot interaction
- **Preconditions**:
  - Test fixtures: `user_telegram_client_connected`, `mock_telegram_client_authorized`, `mock_telegram_bot`, `mock_telegram_message`
  - Mocked `TelegramClient` with `send_message()` and `get_messages()` stubbed
- **Test Steps**:
  1. Use `user_telegram_client_connected` fixture (already connected)
  2. Mock `client.send_message("@test_bot", "/start")` to return `mock_telegram_message` fixture
  3. Mock `client.get_entity("@test_bot")` to return `mock_telegram_bot` fixture
  4. Call `send_message("@test_bot", "/start")` on `UserTelegramClient`
  5. Verify `send_message()` returns `MessageInfo` object with:
     - `id = 111222333`
     - `text = "Test message"`
     - `chat` matches bot entity data
     - `from_user` matches current user info
  6. Mock `client.get_messages("@test_bot", limit=5)` to return list with bot response message
  7. Call `get_messages("@test_bot", limit=5)`
  8. Verify returned messages list contains bot response
- **Expected Result**: Message sending logic works, `send_message()` returns `MessageInfo`, `get_messages()` returns bot response
- **Coverage**: Message sending logic (mocked)
- **Required Mocks/Fixtures**:
  - `user_telegram_client_connected` fixture
  - `mock_telegram_client_authorized` with `send_message()`, `get_entity()`, `get_messages()` stubbed
  - `mock_telegram_bot` fixture (mock bot `User` object)
  - `mock_telegram_message` fixture (mock `Message` object)
- **Test Data**: Test-only sample data from fixtures, no real bot required

#### TC-INTEGRATION-EXT-003: Get entity from Telegram (Mocked)
- **Purpose**: Verify entity retrieval logic using mocked entity data
- **Preconditions**:
  - Test fixtures: `user_telegram_client_connected`, `mock_telegram_client_authorized`, `mock_telegram_channel`, `mock_telegram_chat`
  - Mocked `TelegramClient` with `get_entity()` stubbed
- **Test Steps**:
  1. Use `user_telegram_client_connected` fixture
  2. Mock `client.get_entity("@test_channel")` to return `mock_telegram_channel` fixture
  3. Call `get_entity("@test_channel")` on `UserTelegramClient`
  4. Verify `ChatInfo` is returned with:
     - `id = 444555666`
     - `title = "Test Channel"`
     - `username = "test_channel"`
     - `type = "channel"`
     - `is_bot = False`
     - `is_verified = True`
  5. Mock `client.get_entity("@test_chat")` to return `mock_telegram_chat` fixture
  6. Call `get_entity("@test_chat")`
  7. Verify `ChatInfo` is returned with:
     - `id = 987654321`
     - `title = "Test Chat"`
     - `username = "test_chat"`
     - `type = "group"`
     - `is_bot = False`
     - `is_verified = False`
- **Expected Result**: Entity retrieval logic works, `get_entity()` returns correct `ChatInfo` for channel and chat
- **Coverage**: Entity retrieval logic (mocked)
- **Required Mocks/Fixtures**:
  - `user_telegram_client_connected` fixture
  - `mock_telegram_client_authorized` with `get_entity()` stubbed
  - `mock_telegram_channel` fixture (mock `Channel` object)
  - `mock_telegram_chat` fixture (mock `Chat` object)
- **Test Data**: Test-only sample data from fixtures, no real Telegram entities required

#### TC-INTEGRATION-EXT-004: Handle Telegram rate limits (Mocked with explicit sequence)
- **Purpose**: Verify handling of Telegram rate limits with explicit rapid operation sequence and mocked FloodWaitError
- **Preconditions**:
  - Test fixtures: `user_telegram_client_connected`, `mock_telegram_client_authorized`
  - Mocked `TelegramClient` with `send_message()` stubbed
  - `telethon.errors.FloodWaitError` available for mocking
- **Test Steps**:
  1. Use `user_telegram_client_connected` fixture
  2. Define explicit operation sequence: 50 sequential `send_message()` calls to `"@test_bot"` with text `f"Message {i}"` for `i` in range(1, 51)
  3. Configure mock `client.send_message()` behavior:
     - For calls 1-24: return `mock_telegram_message` fixture normally
     - For call 25: raise `FloodWaitError(seconds=5)` (simulate rate limit hit)
     - For calls 26-50: return `mock_telegram_message` fixture normally (after retry/backoff)
  4. Execute rapid sequence: call `send_message("@test_bot", f"Message {i}")` 50 times sequentially
  5. Verify `FloodWaitError` is raised on call 25
  6. Verify retry/backoff logic:
     - Framework catches `FloodWaitError`
     - Framework waits for `seconds` (5 seconds) or uses exponential backoff
     - Framework retries the failed operation
     - Framework logs error appropriately
  7. Verify all 50 operations complete successfully after retry
  8. Verify `send_message()` was called exactly 51 times (50 original + 1 retry for call 25)
- **Expected Result**: Rate limit handling works correctly, `FloodWaitError` is caught on call 25, retry/backoff logic executes, all 50 operations complete
- **Coverage**: Rate limit handling with explicit operation sequence (mocked)
- **Required Mocks/Fixtures**:
  - `user_telegram_client_connected` fixture
  - `mock_telegram_client_authorized` with `send_message()` stubbed using `side_effect` to raise `FloodWaitError(5)` on call 25
  - `mock_telegram_message` fixture for successful responses
  - `telethon.errors.FloodWaitError` imported for exception raising
- **Test Data**: Test-only sample data, explicit 50-operation sequence, no real rate limiting required
- **Notes**:
  - Operation sequence is explicitly defined: 50 sequential `send_message()` calls
  - `FloodWaitError` is raised on a specific call (call 25) using mock `side_effect`
  - Retry/backoff logic is verified through mock call counts and timing assertions

#### TC-INTEGRATION-EXT-005: Handle Telegram connection errors (Mocked with network interruption simulation)
- **Purpose**: Verify handling of connection errors with simulated network interruption
- **Preconditions**:
  - Test fixtures: `user_telegram_client`, `mock_telegram_client_authorized`
  - Mocked `TelegramClient` with `connect()` and transport methods stubbed
- **Test Steps**:
  1. Use `user_telegram_client` fixture (not connected)
  2. **Simulate network interruption Method A (ConnectionError from connect())**:
     - Patch `client.connect()` to raise `ConnectionError("Network unreachable")` on first call
     - Call `connect()` on `UserTelegramClient`
     - Verify `ConnectionError` is caught
     - Verify error is logged (check log output contains "Failed to connect" and error message)
     - Verify `_is_connected` remains `False`
  3. **Simulate network interruption Method B (ConnectionError from transport)**:
     - Patch `client.connect()` to succeed initially
     - Patch `client.is_connected()` to return `False` after initial connection (simulate connection loss)
     - Patch `client.send_message()` to raise `ConnectionError("Connection lost")` when called
     - Call `connect()` (should succeed)
     - Call `send_message("@test_bot", "test")` (should raise `ConnectionError`)
     - Verify `ConnectionError` is caught and logged
  4. **Verify retry behavior**:
     - Configure mock to raise `ConnectionError` on first 2 calls, succeed on 3rd call
     - Call `connect()` (should retry and eventually succeed)
     - Verify retry mechanism attempts connection multiple times
     - Verify connection succeeds after retries
  5. **Verify error logging**:
     - Assert log messages contain connection error details
     - Assert error messages are logged at appropriate level (ERROR)
- **Expected Result**: Connection errors handled gracefully, errors logged appropriately, retry mechanism works
- **Coverage**: Connection error handling with network interruption simulation (mocked)
- **Required Mocks/Fixtures**:
  - `user_telegram_client` fixture
  - `mock_telegram_client_authorized` with `connect()`, `is_connected()`, `send_message()` stubbed
  - `pytest-mock` or `unittest.mock.patch` for patching methods to raise `ConnectionError`
- **Test Data**: Test-only sample data, simulated network errors via mocks, no real network issues required
- **Notes**:
  - Network interruption is simulated by patching `client.connect()` or transport methods to raise `ConnectionError`
  - Error logging is verified through log capture (e.g., `caplog` fixture)
  - Retry behavior is verified through mock call counts and success after retries

### 2. HTTP API Integration

#### TC-INTEGRATION-EXT-006: Test real HTTP endpoint
- **Purpose**: Verify HTTP requests to real endpoints
- **Preconditions**:
  - Real HTTP endpoint URL (use httpbin.org or local mock server)
  - Endpoint is accessible
- **Test Steps**:
  1. Create MiniAppApi with base URL from fixture or environment variable
     - Default: `http://httpbin.org` (or `http://localhost:8000` for local mock server)
     - Use `MOCK_SERVER_URL` environment variable if available for CI
  2. Call `make_request("/get")` to httpbin.org/get endpoint
  3. Verify response is received
  4. Verify response status code is 200
  5. Verify response data matches expected schema:
     ```json
     {
       "url": "http://httpbin.org/get",
       "headers": {...},
       "args": {}
     }
     ```
     - Verify `url` field exists and matches request URL
     - Verify `headers` field exists and is a dictionary
- **Expected Result**: Real HTTP request succeeds with status 200 and valid JSON response
- **Coverage**: Real HTTP integration
- **Dependencies**: Real HTTP endpoint (httpbin.org or mock server)
- **Notes**:
  - For CI/CD, use `MOCK_SERVER_URL` environment variable to point to a provided mock server fixture
  - Local development can use httpbin.org or start a local mock server on port 8000

#### TC-INTEGRATION-EXT-007: Test HTTPS endpoint
- **Purpose**: Verify HTTPS requests work correctly
- **Preconditions**: HTTPS endpoint with valid SSL certificate
- **Test Steps**:
  1. Create MiniAppApi with HTTPS URL: `https://httpbin.org`
  2. Call `make_request("/get")` to https://httpbin.org/get endpoint
  3. Verify SSL/TLS handshake succeeds
  4. Verify response is received with status code 200
  5. Verify response contains valid JSON data
- **Expected Result**: HTTPS request succeeds with status 200
- **Coverage**: HTTPS integration
- **Dependencies**: HTTPS endpoint (https://httpbin.org)
- **Notes**: Uses httpbin.org for testing SSL/TLS handshake

#### TC-INTEGRATION-EXT-008: Test HTTP endpoint with authentication
- **Purpose**: Verify authenticated HTTP requests
- **Preconditions**:
  - HTTP endpoint requiring authentication (use httpbin.org/bearer or mock server)
  - Valid auth token
- **Test Steps**:
  1. Create MiniAppApi with base URL: `https://httpbin.org`
  2. Call `make_request("/bearer")` with auth header:
     - Header name: `Authorization`
     - Header format: `Bearer {token}`
     - Sample token: `test_token_12345abcdef`
     - Full header value: `Bearer test_token_12345abcdef`
  3. Verify authenticated request succeeds with status 200
  4. Verify response contains `authenticated: true` in JSON body
  5. Try request without auth headers to `/bearer`
  6. Verify unauthenticated request returns status 401 or 403
- **Expected Result**:
  - Authenticated request succeeds (status 200, `authenticated: true`)
  - Unauthenticated request fails (status 401 or 403)
- **Coverage**: HTTP authentication
- **Dependencies**: Authenticated endpoint (httpbin.org/bearer or mock server with auth)
- **Notes**:
  - For CI/CD, use mock server fixture that supports Bearer token authentication
  - Token can be provided via `TEST_AUTH_TOKEN` environment variable

#### TC-INTEGRATION-EXT-009: Handle HTTP errors (4xx, 5xx)
- **Purpose**: Verify handling of HTTP error responses
- **Preconditions**: Endpoints that return specific error codes
- **Test Steps**:
  1. Create MiniAppApi with base URL: `https://httpbin.org`
  2. Call `make_request("/status/404")` to endpoint returning 404
  3. Verify ApiResult has:
     - `status_code = 404`
     - `client_error = True`
     - `success = False`
     - `server_error = False`
  4. Call `make_request("/status/500")` to endpoint returning 500
  5. Verify ApiResult has:
     - `status_code = 500`
     - `server_error = True`
     - `success = False`
     - `client_error = False`
  6. Optionally verify error response body structure:
     ```json
     {
       "status": 404,
       "message": "Not Found"
     }
     ```
- **Expected Result**:
  - 404 error correctly identified as client_error (status 404, client_error=True)
  - 500 error correctly identified as server_error (status 500, server_error=True)
- **Coverage**: HTTP error handling
- **Dependencies**: Endpoints returning errors (httpbin.org/status/{code} or mock server)
- **Notes**: httpbin.org provides `/status/{code}` endpoints for testing various status codes

#### TC-INTEGRATION-EXT-010: Handle HTTP timeouts
- **Purpose**: Verify handling of HTTP timeouts
- **Preconditions**: Slow or unresponsive endpoint
- **Test Steps**:
  1. Create MiniAppApi with timeout set to 2 seconds (2000ms)
  2. Call `make_request("/delay/5")` to httpbin.org/delay/5 endpoint (which delays 5 seconds)
  3. Verify timeout is detected within 2-3 seconds
  4. Verify ApiResult indicates timeout:
     - `success = False`
     - `error_message` contains "timeout" or "timed out"
     - `status_code` may be None or 408 (Request Timeout)
- **Expected Result**: HTTP timeout detected correctly within specified timeout period (2 seconds)
- **Coverage**: HTTP timeout handling
- **Dependencies**: Slow endpoint (httpbin.org/delay/{seconds} or mock server with delay)
- **Notes**:
  - Timeout threshold: 2 seconds (2000ms)
  - For CI/CD, use mock server fixture with configurable delay endpoint
  - Alternative: use httpbin.org/delay/{seconds} where seconds > timeout value

### 3. Browser Automation Integration

**Note on Test Fixtures**: Browser integration tests use local HTML fixtures located in `tests/data/html_fixtures/` to ensure reproducibility and avoid fragile external dependencies. These fixtures are served via a local HTTP server or accessed via `file://` protocol. For production-like testing, stable external URLs (e.g., `https://example.com`, `https://httpbin.org/html`) can be used as fallback, but local fixtures are preferred for CI/CD environments.

#### TC-INTEGRATION-EXT-011: Launch real browser
- **Purpose**: Verify Playwright browser launches correctly
- **Preconditions**: Playwright installed
- **Test Steps**:
  1. Create MiniAppUI
  2. Call `setup_browser()`
  3. Verify browser is launched
  4. Verify page is created
  5. Verify browser is accessible
- **Expected Result**: Browser launches successfully
- **Coverage**: Browser launch integration
- **Dependencies**: Playwright installation

#### TC-INTEGRATION-EXT-012: Navigate to real URL
- **Purpose**: Verify navigation to real web page
- **Preconditions**:
  - Test fixture URL or stable external URL (e.g., `file:///path/to/tests/data/html_fixtures/test_page.html` or `https://example.com`)
  - Browser setup
- **Test Steps**:
  1. Create MiniAppUI with test URL: `file:///path/to/tests/data/html_fixtures/test_page.html` (or `https://example.com` as fallback)
  2. Setup browser using `setup_browser()`
  3. Navigate to URL explicitly using `page.goto(url)`
  4. Wait for page load using `page.wait_for_load_state("domcontentloaded")`
  5. Verify page loads by checking `page.url` matches expected URL
  6. Verify page title using `page.title()` equals "Test Page for Browser Integration Tests"
- **Expected Result**: Navigation to URL succeeds, page loads correctly
- **Coverage**: Real URL navigation
- **Dependencies**: Local HTML fixture at `tests/data/html_fixtures/test_page.html` or stable external URL
- **Test Fixture**: `tests/data/html_fixtures/test_page.html`

#### TC-INTEGRATION-EXT-013: Interact with real web page
- **Purpose**: Verify interaction with real web page elements
- **Preconditions**:
  - Test fixture URL: `file:///path/to/tests/data/html_fixtures/interactive_page.html` (or `https://httpbin.org/forms/post` as fallback)
  - Browser setup
- **Test Steps**:
  1. Navigate to test page: `file:///path/to/tests/data/html_fixtures/interactive_page.html`
  2. Wait for element `#test-input` using `wait_for_element("#test-input")`
  3. Fill input field using `fill_input("#test-input", "test value")`
  4. Click button using `click_element("#test-button")`
  5. Wait for output element `#output` to appear
  6. Verify interactions work by checking `#output` element text contains "Button clicked!"
  7. Fill input again: `fill_input("#test-input", "form submission")`
  8. Click submit button: `click_element("#submit-button")`
  9. Verify output updated with submitted value
- **Expected Result**: Real page interactions work correctly
- **Coverage**: Real page interaction
- **Dependencies**: Local HTML fixture at `tests/data/html_fixtures/interactive_page.html` with elements:
  - `#test-input` - text input field
  - `#test-button` - clickable button
  - `#submit-button` - submit button
  - `#output` - output div element
- **Test Fixture**: `tests/data/html_fixtures/interactive_page.html`

#### TC-INTEGRATION-EXT-014: Handle browser errors
- **Purpose**: Verify handling of browser errors
- **Preconditions**:
  - Test fixture URL: `file:///path/to/tests/data/html_fixtures/error_page.html` (local fixture with intentional errors)
  - Browser setup
- **Test Steps**:
  1. Navigate to error test page: `file:///path/to/tests/data/html_fixtures/error_page.html`
  2. Wait for page load
  3. Verify JavaScript console errors are logged (check browser console)
  4. Try to interact with element `#error-button` using `click_element("#error-button")`
  5. Verify errors are caught and logged (check error logs)
  6. Verify test continues execution after error handling
  7. Verify page still accessible after errors
- **Expected Result**: Browser errors handled gracefully, errors logged, test continues
- **Coverage**: Browser error handling
- **Dependencies**: Local HTML fixture at `tests/data/html_fixtures/error_page.html` containing:
  - Intentional JavaScript errors (undefined function calls)
  - Missing resource references (404 errors)
  - Error button element `#error-button`
- **Test Fixture**: `tests/data/html_fixtures/error_page.html`

#### TC-INTEGRATION-EXT-015: Test browser with JavaScript disabled
- **Purpose**: Verify framework works without JavaScript
- **Preconditions**:
  - Test fixture URL: `file:///path/to/tests/data/html_fixtures/no_js_page.html` (page that works without JavaScript)
  - Browser setup with JavaScript disabled
- **Test Steps**:
  1. Setup browser context with JavaScript disabled using Playwright API:
     - Create browser context: `context = await browser.new_context(js_enabled=False)`
     - Create page from context: `page = await context.new_page()`
  2. Navigate to no-JS test page: `file:///path/to/tests/data/html_fixtures/no_js_page.html`
  3. Wait for page load using `page.wait_for_load_state("domcontentloaded")`
  4. Verify page loads (check page title equals "No JavaScript Test Page")
  5. Fill input field using `fill_input("#test-input", "test without js")`
  6. Verify input value was set correctly
  7. Click submit button using `click_element("#test-button")`
  8. Verify form interaction works without JavaScript
- **Expected Result**: Works without JavaScript, basic interactions succeed
- **Coverage**: JavaScript independence
- **Dependencies**:
  - Local HTML fixture at `tests/data/html_fixtures/no_js_page.html` (pure HTML form, no JS required)
  - Playwright browser context with `js_enabled=False` parameter
- **JavaScript Disable Method**: Use `browser.new_context(js_enabled=False)` to create a context without JavaScript, then create page from that context
- **Test Fixture**: `tests/data/html_fixtures/no_js_page.html`

### 4. Network Integration

#### TC-INTEGRATION-EXT-016: Handle network interruptions
- **Purpose**: Verify handling of network interruptions with retry mechanism
- **Preconditions**:
  - Network that can be interrupted
  - Docker installed (for network namespace control)
  - OR iptables available (Linux) / netsh (Windows)
  - OR pytest-httpx for HTTP client mocking
- **Test Steps**:
  1. Create MiniAppApi with test endpoint URL
  2. **Method A (Docker network namespace)**:
     - Start test container with network namespace
     - Create MiniAppApi inside container
     - Execute: `docker network disconnect bridge <container_id>` to interrupt
     - Attempt HTTP request via `make_request()`
     - Verify `ApiResult.error_message` contains network error (e.g., "Connection refused", "Network unreachable")
     - Execute: `docker network connect bridge <container_id>` to restore
     - Retry request within 5 seconds after restore
     - Verify request succeeds with `ApiResult.success=True`
  3. **Method B (iptables - Linux only)**:
     - Execute: `iptables -A OUTPUT -d <target_host> -j DROP` to block traffic
     - Attempt HTTP request via `make_request()`
     - Verify `ApiResult.error_message` contains network error
     - Execute: `iptables -D OUTPUT -d <target_host> -j DROP` to restore
     - Retry request within 5 seconds after restore
     - Verify request succeeds
  4. **Method C (pytest-httpx mock)**:
     - Use `httpx_mock` fixture to simulate `httpx.ConnectError` or `httpx.NetworkError`
     - Attempt HTTP request via `make_request()`
     - Verify `ApiResult.error_message` contains network error
     - Configure mock to return successful response on retry
     - Retry request (if framework implements automatic retry)
     - Verify request succeeds
- **Acceptance Criteria**:
  - Client reports network error in `ApiResult.error_message` within timeout period
  - After network restoration, client successfully retries within 3 attempts or 10 seconds
  - `ApiResult.success=True` on successful retry
  - Error is logged appropriately
- **Expected Result**: Network interruptions detected, logged, and retry succeeds after restoration
- **Coverage**: Network error handling and retry mechanism
- **Dependencies**: Docker OR iptables (Linux) OR pytest-httpx

#### TC-INTEGRATION-EXT-017: Test with proxy
- **Purpose**: Verify framework works with HTTP/HTTPS proxy server
- **Preconditions**:
  - Proxy server available (Squid or mitmproxy)
  - Proxy accessible from test environment
- **Proxy Server Setup**:
  - **Squid**: Default port 3128, URL: `http://localhost:3128` (or configured host)
  - **mitmproxy**: Default port 8080, URL: `http://localhost:8080`
  - Authentication (if required): Basic auth with username/password
- **Test Steps**:
  1. Start proxy server:
     - **Squid**: `docker run -d -p 3128:3128 ubuntu/squid:latest` OR local Squid service
     - **mitmproxy**: `mitmproxy -p 8080 --set confdir=~/.mitmproxy` OR `mitmdump -p 8080`
  2. Configure proxy in httpx client:
     - Modify `MiniAppApi.__init__()` to accept `proxy` parameter
     - Pass proxy to `AsyncClient(proxies=proxy)` where proxy format is:
       - `"http://proxy.example.com:3128"` (no auth)
       - `"http://user:pass@proxy.example.com:3128"` (with auth)
  3. Create MiniAppApi with proxy configuration:
     ```python
     api = MiniAppApi(
         url="https://example.com/mini-app",
         config=config,
         proxy="http://localhost:3128"  # or mitmproxy: "http://localhost:8080"
     )
     ```
  4. Make HTTP request via `make_request("/api/status")`
  5. **Verify request routed through proxy**:
     - **Squid**: Check access logs: `tail -f /var/log/squid/access.log` shows request
     - **mitmproxy**: Check mitmproxy UI or logs for intercepted request
     - Verify proxy headers in request (e.g., `Via: 1.1 proxy.example.com`)
     - OR verify proxy logs contain target URL and client IP
  6. **Verify response received**:
     - `ApiResult.success=True`
     - `ApiResult.status_code` matches expected (e.g., 200)
     - Response content is valid
  7. **Test with authentication** (if proxy requires auth):
     - Configure proxy URL with credentials: `"http://user:pass@localhost:3128"`
     - Repeat request and verify success
- **Acceptance Criteria**:
  - Request is routed through proxy (verified via proxy logs or headers)
  - Response is successfully returned through proxy
  - `ApiResult.success=True` and valid status code
  - Proxy authentication works if configured
  - Error handling works if proxy is unreachable
- **Expected Result**: Proxy integration works correctly, requests routed through proxy, responses received
- **Coverage**: Proxy support for HTTP/HTTPS requests
- **Dependencies**: Squid proxy server OR mitmproxy, Docker (optional for containerized Squid)

#### TC-INTEGRATION-EXT-018: Test with different network conditions
- **Purpose**: Verify framework behavior under various network conditions (bandwidth, latency, packet loss)
- **Preconditions**: Network throttling tool available
- **Throttling Tools**:
  - **Playwright**: Built-in network throttling via `context.set_extra_http_headers()` and `page.route()`
  - **tc (Linux)**: Traffic control via `tc qdisc` and `tc netem`
  - **Docker + netem**: Containerized network emulation
- **Network Profiles**:
  1. **Fast (baseline)**: No throttling, normal conditions
  2. **Slow 3G**: 400 Kbps down, 400 Kbps up, 400ms latency, 0% loss
  3. **Fast 3G**: 1.6 Mbps down, 750 Kbps up, 150ms latency, 0% loss
  4. **High Latency**: Normal bandwidth, 500ms latency, 0% loss
  5. **Packet Loss**: Normal bandwidth, 50ms latency, 5% packet loss
- **Test Steps**:
  1. **Baseline (Fast Network)**:
     - Make HTTP request via `make_request("/api/status")`
     - Measure `ApiResult.response_time`
     - Verify request completes within 2 seconds
     - Verify `ApiResult.success=True`
  2. **Method A (Playwright - for browser-based tests)**:
     - Setup browser context with throttling:
       ```python
       context = await browser.new_context()
       await context.set_extra_http_headers({"X-Throttle": "slow-3g"})
       ```
     - Navigate and make requests
     - Measure response times for each profile
  3. **Method B (tc - Linux only)**:
     - Apply slow 3G profile:
       ```bash
       tc qdisc add dev eth0 root handle 1: htb default 30
       tc class add dev eth0 parent 1: classid 1:1 htb rate 400kbit
       tc class add dev eth0 parent 1:1 classid 1:10 htb rate 400kbit ceil 400kbit
       tc qdisc add dev eth0 parent 1:10 netem delay 400ms
       tc filter add dev eth0 protocol ip parent 1:0 prio 1 u32 match ip dst <target_ip> flowid 1:10
       ```
     - Make HTTP request via `make_request()`
     - Measure response time
     - Remove throttling: `tc qdisc del dev eth0 root`
  4. **Method C (Docker + netem)**:
     - Use docker-compose with network emulation:
       ```yaml
       services:
         netem:
           image: gaiadocker/iproute2
           command: tc qdisc add dev eth0 root netem delay 500ms loss 5%
       ```
     - Run test container with network from netem service
     - Make requests and measure
  5. **Test each profile**:
     - **Slow 3G**: Request completes within 10 seconds OR triggers timeout/retry
     - **Fast 3G**: Request completes within 5 seconds
     - **High Latency (500ms)**: Request completes within 3 seconds (500ms base + processing)
     - **Packet Loss (5%)**: Request may require retry, completes within retry attempts
- **Acceptance Criteria**:
  - **Fast network**: Request completes within 2 seconds, `ApiResult.success=True`
  - **Slow 3G**: Request completes within 10 seconds OR timeout/retry triggered appropriately
  - **Fast 3G**: Request completes within 5 seconds, `ApiResult.success=True`
  - **High Latency (500ms)**: Request completes within 3 seconds (accounting for latency)
  - **Packet Loss (5%)**: Request succeeds after retry (if retry_count > 0) OR fails gracefully
  - Response times recorded in `ApiResult.response_time` reflect network conditions
  - Timeout behavior is appropriate for each condition
- **Expected Result**: Framework handles various network conditions correctly, with appropriate timeouts and retries
- **Coverage**: Network condition handling, timeout behavior, retry logic
- **Dependencies**:
  - Playwright (for browser-based throttling)
  - OR tc + iproute2 (Linux, for system-level throttling)
  - OR Docker + netem image (for containerized throttling)
  - Root/admin privileges (for tc method)

### 5. Security Integration

#### TC-INTEGRATION-EXT-019: Verify SSL certificate validation
- **Purpose**: Verify SSL certificate validation works with various certificate scenarios
- **Preconditions**:
  - HTTPS test server capability (e.g., local test server with certificate control)
  - Certificate fixtures prepared (see Setup section)
- **Certificate Fixtures to Test**:
  1. **Self-signed certificate**: Certificate not signed by a trusted CA
  2. **Expired certificate**: Certificate with `notAfter` date in the past
  3. **Revoked certificate (CRL)**: Certificate listed in Certificate Revocation List
  4. **Hostname mismatch**: Certificate issued for different hostname than requested
- **Setup Instructions**:
  - **Self-signed**: Generate using `openssl req -x509 -newkey rsa:2048 -keyout self-signed.key -out self-signed.crt -days 365 -nodes`
  - **Expired**: Generate with `-days -1` or manually set `notAfter` to past date
  - **Revoked**: Generate valid cert, then add to CRL using `openssl ca -gencrl -out revoked.crl`
  - **Hostname mismatch**: Generate cert with CN=wronghostname.example.com, serve on different hostname
  - Configure test server to serve each certificate fixture on separate port/endpoint
- **Test Steps**:
  1. Create MiniAppApi with default SSL validation enabled
  2. Make request to HTTPS endpoint with **valid certificate** (baseline)
     - **Assertion**: Request succeeds, status 200, no SSL errors
  3. Make request to endpoint with **self-signed certificate**
     - **Assertion**: Connection rejected with `SSL: CERTIFICATE_VERIFY_FAILED` error or equivalent
     - **Expected error code/message**: `ssl.SSLCertVerificationError` or `requests.exceptions.SSLError` with message containing "certificate verify failed" or "self-signed certificate"
  4. Make request to endpoint with **expired certificate**
     - **Assertion**: Connection rejected with certificate expiration error
     - **Expected error code/message**: `ssl.SSLCertVerificationError` with message containing "certificate has expired" or "notAfter"
  5. Make request to endpoint with **revoked certificate (CRL)**
     - **Assertion**: Connection rejected if CRL checking enabled, otherwise may succeed (implementation-dependent)
     - **Expected error code/message**: `ssl.SSLCertVerificationError` with message containing "certificate revoked" or "CRL" (if CRL checking enabled)
  6. Make request to endpoint with **hostname mismatch certificate**
     - **Assertion**: Connection rejected with hostname verification error
     - **Expected error code/message**: `ssl.SSLCertVerificationError` with message containing "hostname doesn't match" or "certificate verify failed" with hostname mismatch details
  7. (Optional) Test with SSL validation disabled
     - **Assertion**: All requests succeed regardless of certificate validity (security test)
- **Expected Result**:
  - Valid certificates accepted
  - Invalid certificates (self-signed, expired, revoked, hostname mismatch) rejected with appropriate error codes
  - Error messages clearly indicate certificate validation failure reason
- **Coverage**: SSL/TLS security with comprehensive certificate validation scenarios
- **Dependencies**: HTTPS test server with certificate fixture control

#### TC-INTEGRATION-EXT-020: Test with different user agents
- **Purpose**: Verify user agent handling with explicit verification methods
- **Preconditions**:
  - Browser setup (Playwright)
  - Test page/server that can verify user agent (see Verification Methods)
- **Verification Methods**:
  1. **Server-side header check**: Test server logs or returns `User-Agent` header value in response
  2. **Client-side JS check**: Page JavaScript reads `navigator.userAgent` and displays/returns value
  3. **Network request inspection**: Check actual HTTP request headers in browser DevTools or network logs
- **Test Steps**:
  1. Setup browser with custom user agent string (e.g., `"CustomTestAgent/1.0"`)
     - **Implementation**: Use Playwright's `browser_context.set_extra_http_headers({"User-Agent": "CustomTestAgent/1.0"})` or `browser.new_context(user_agent="CustomTestAgent/1.0")`
  2. Navigate to test page that verifies user agent
     - **Page should**: Log User-Agent header server-side OR execute JS to read `navigator.userAgent` and display in DOM
  3. **Verify user agent is set correctly (server-side)**:
     - **Method**: Check server logs or make request to endpoint that returns User-Agent header
     - **Assertion criteria**:
       - HTTP request header `User-Agent` equals `"CustomTestAgent/1.0"`
       - Server response contains expected User-Agent value (if page returns it)
     - **Test wiring**: Use `page.request.get()` or inspect network requests via `page.on("request")` event listener to capture request headers
  4. **Verify user agent is set correctly (client-side)**:
     - **Method**: Execute JavaScript in page context: `user_agent = await page.evaluate("() => navigator.userAgent")`
     - **Assertion criteria**:
       - `navigator.userAgent` equals `"CustomTestAgent/1.0"`
       - If page displays UA in DOM, verify DOM element contains expected value
     - **Test wiring**: Use `page.evaluate()` to read `navigator.userAgent` and assert value matches configured UA
  5. **Verify page responds to user agent**:
     - **Method**: Test page behavior based on user agent (e.g., different content, status codes, redirects)
     - **Assertion criteria**:
       - Page loads successfully (status 200) OR returns expected status code based on UA
       - Page content/behavior matches expected response for given user agent
       - No errors in browser console related to user agent
     - **Test wiring**:
       - Check `page.response.status` after navigation
       - Verify page content using `page.content()` or element selectors
       - Check console messages via `page.on("console")` event listener
- **Expected Result**:
  - User agent is correctly set in HTTP request headers
  - `navigator.userAgent` in browser context matches configured value
  - Page/server correctly receives and responds to user agent
  - All verification methods (server-side, client-side, network inspection) confirm correct UA value
- **Coverage**: User agent support with explicit verification across server, client, and network layers
- **Dependencies**: Test page/server with user agent verification capability

### 6. Performance Integration

#### TC-INTEGRATION-EXT-021: Measure API response times
- **Purpose**: Verify API response time measurement with concrete performance criteria
- **Preconditions**:
  - API endpoint accessible and stable
  - Network conditions are consistent
- **Test Steps**:
  1. Create MiniAppApi with target endpoint
  2. Execute 100 sequential HTTP requests to the same endpoint
  3. For each request, capture response time using `time.perf_counter()`:
     - Start timer before `make_request()` call
     - Stop timer after `ApiResult` is returned
     - Record elapsed time in milliseconds
  4. Calculate statistics from all 100 measurements:
     - Mean (arithmetic average)
     - Median (50th percentile)
     - 95th percentile (p95)
     - 99th percentile (p99)
  5. Verify all times are recorded in ApiResult objects
  6. Evaluate performance budget:
     - Pass if: p95 < 500ms AND mean < 300ms
     - Fail if: p95 >= 500ms OR mean >= 300ms
- **Expected Result**:
  - All 100 requests complete successfully
  - Response times are measured and recorded
  - Performance budget is met (p95 < 500ms and mean < 300ms)
- **Failure Conditions**:
  - Any request fails (non-2xx status)
  - p95 >= 500ms (95% of requests exceed 500ms)
  - mean >= 300ms (average response time exceeds 300ms)
  - Missing time measurements for any request
- **Coverage**: Performance measurement with deterministic criteria
- **Dependencies**: Stable API endpoint

#### TC-INTEGRATION-EXT-022: Measure page load times
- **Purpose**: Verify page load time measurement with concrete performance criteria
- **Preconditions**:
  - Web page URL accessible and stable
  - Browser environment is consistent
  - Network conditions are stable
- **Test Steps**:
  1. Setup browser (fresh instance for each run)
  2. Execute 10 navigation runs:
     - For each run:
       - Start timer using `time.perf_counter()` before `navigate()` or `setup_browser()` call
       - Wait for page load complete using Playwright's `page.wait_for_load_state("networkidle")` or equivalent
       - Stop timer after load state is reached
       - Record elapsed time in seconds
       - Close browser instance
  3. Calculate statistics from all 10 measurements:
     - Median (50th percentile)
     - Mean (arithmetic average)
     - Standard deviation
     - Coefficient of variation (CV) = (standard_deviation / mean) * 100%
  4. Evaluate acceptance criteria:
     - Pass if: median < 2.0s AND coefficient_of_variation < 10%
     - Fail if: median >= 2.0s OR coefficient_of_variation >= 10%
- **Expected Result**:
  - All 10 navigation runs complete successfully
  - Load times are measured consistently
  - Performance criteria are met (median < 2s and CV < 10%)
- **Failure Conditions**:
  - Any navigation fails or times out
  - Median load time >= 2.0s (more than half of runs exceed 2 seconds)
  - Coefficient of variation >= 10% (load times are too inconsistent)
  - Missing time measurements for any run
- **Coverage**: Page load performance with deterministic criteria
- **Dependencies**: Stable web page and consistent browser environment

### 7. Compatibility Integration

#### TC-INTEGRATION-EXT-023: Test with different browsers
- **Purpose**: Verify framework works correctly across different browser engines
- **Preconditions**:
  - Playwright installed with all browsers: `uv run playwright install chromium firefox webkit`
  - Test fixtures available: `tests/data/html_fixtures/test_page.html`, `tests/data/html_fixtures/interactive_page.html`
- **Browser Versions**:
  - **Chromium**: Version installed by Playwright (typically latest stable, e.g., 131.x or newer)
  - **Firefox**: Version installed by Playwright (typically latest stable, e.g., 135.x or newer)
  - **WebKit**: Version installed by Playwright (typically latest stable, e.g., 19.x or newer)
  - Verify installed versions: `uv run playwright --version` or check `playwright install` output
- **Test Suite to Execute**: Run the following browser automation test cases on each browser:
  - TC-INTEGRATION-EXT-011: Launch real browser
  - TC-INTEGRATION-EXT-012: Navigate to real URL
  - TC-INTEGRATION-EXT-013: Interact with real web page
  - TC-INTEGRATION-EXT-014: Handle browser errors
  - TC-INTEGRATION-EXT-015: Test browser with JavaScript disabled
- **Test Steps**:
  1. **For Chromium**:
     - Configure Playwright to use Chromium: `browser = await playwright.chromium.launch()`
     - Execute test suite TC-011 through TC-015 sequentially
     - Record results: test name, browser, pass/fail status, execution time, any errors
  2. **For Firefox**:
     - Configure Playwright to use Firefox: `browser = await playwright.firefox.launch()`
     - Execute the same test suite TC-011 through TC-015 sequentially
     - Record results: test name, browser, pass/fail status, execution time, any errors
  3. **For WebKit**:
     - Configure Playwright to use WebKit: `browser = await playwright.webkit.launch()`
     - Execute the same test suite TC-011 through TC-015 sequentially
     - Record results: test name, browser, pass/fail status, execution time, any errors
  4. **Compare Results**:
     - Create comparison matrix: Browser × Test Case × Result
     - Verify all test steps pass on each browser (5 tests × 3 browsers = 15 total test executions)
     - Compare execution times across browsers (document but do not fail on time differences)
     - Identify any browser-specific failures or behavioral differences
- **Acceptance Criteria**:
  - **Pass Condition**: All 5 test cases (TC-011 through TC-015) must pass successfully on all 3 browsers (Chromium, Firefox, WebKit)
  - **Failure Condition**: Test fails if any test case fails on any browser
  - **Result Comparison**: Results must be identical across browsers for:
    - Page navigation success (TC-012)
    - Element interaction success (TC-013)
    - Error handling behavior (TC-014)
    - JavaScript-disabled functionality (TC-015)
  - **Documentation**: Record browser versions, execution times, and any browser-specific notes
- **Expected Result**:
  - All 15 test executions pass (5 tests × 3 browsers)
  - Framework functionality is consistent across all browser engines
  - Results comparison matrix shows identical behavior across browsers
- **Coverage**: Browser compatibility across Chromium, Firefox, and WebKit engines
- **Dependencies**:
  - Playwright with all browsers installed
  - Test fixtures in `tests/data/html_fixtures/`
  - Browser versions as specified above

#### TC-INTEGRATION-EXT-024: Test with different Telegram API versions
- **Purpose**: Verify framework compatibility with different Telegram MTProto API versions via Telethon library versions
- **Preconditions**:
  - Valid Telegram API credentials (api_id, api_hash, session_string or session_file)
  - Ability to install and test with different Telethon library versions
  - Test environment supports virtual environments or dependency isolation
- **API Versions to Test**:
  - **Current Version**: Telethon >=1.42.0 (as specified in pyproject.toml)
  - **Previous Stable Version**: Telethon 1.41.x (last minor version before current)
  - **Older Compatible Version**: Telethon 1.40.x (for backward compatibility verification)
  - **Latest Available**: Telethon latest (from PyPI, e.g., 1.43.x or newer if available)
- **Version Installation Methods**:
  - **Method A (uv with dependency override)**:
    - Create isolated test environment: `uv venv test_env_telethon_1.41`
    - Install specific version: `uv pip install telethon==1.41.0` (or target version)
    - Install other dependencies: `uv pip install -e .` (excluding telethon)
  - **Method B (pytest with dependency injection)**:
    - Use `pytest-dependency` or `pytest-env` to manage Telethon versions per test
    - Install versions in separate virtual environments and switch between them
  - **Method C (Docker containers)**:
    - Create Dockerfile with specific Telethon version
    - Run tests in containerized environment
  - **Fallback**: If specific versions unavailable, test with:
    - Minimum supported version (1.42.0)
    - Latest available version from PyPI
    - Document actual versions tested
- **Test Operations to Verify**:
  - **Core Operations** (must work on all versions):
    1. Connect to Telegram API (`connect()`, `is_connected()`)
    2. Get user info (`get_me()`)
    3. Get entity (`get_entity("@test_channel")`)
    4. Send message (`send_message("@test_bot", "/start")`)
    5. Get messages (`get_messages("@test_bot", limit=5)`)
- **Test Steps**:
  1. **Setup for Version 1.42.0 (Current)**:
     - Install Telethon 1.42.0 in test environment
     - Create UserTelegramClient with test credentials
     - Execute all 5 core operations
     - Record results: operation name, version, success/failure, response data structure, execution time
  2. **Setup for Version 1.41.x (Previous)**:
     - Install Telethon 1.41.0 (or latest 1.41.x) in separate test environment
     - Create UserTelegramClient with same credentials
     - Execute the same 5 core operations
     - Record results: operation name, version, success/failure, response data structure, execution time
  3. **Setup for Version 1.40.x (Older)**:
     - Install Telethon 1.40.0 (or latest 1.40.x) in separate test environment
     - Create UserTelegramClient with same credentials
     - Execute the same 5 core operations
     - Record results: operation name, version, success/failure, response data structure, execution time
  4. **Setup for Latest Version**:
     - Install latest Telethon from PyPI: `uv pip install --upgrade telethon`
     - Create UserTelegramClient with same credentials
     - Execute the same 5 core operations
     - Record results: operation name, version, success/failure, response data structure, execution time
  5. **Compare Results Across Versions**:
     - Create comparison matrix: API Version × Operation × Result
     - Verify response data structures are compatible (same fields, compatible types)
     - Verify all operations succeed on all tested versions
     - Document any version-specific differences or deprecations
- **Acceptance Criteria**:
  - **Pass Condition**: All 5 core operations must succeed on all tested API versions
  - **Response Compatibility**:
    - `get_me()` returns UserInfo with identical or compatible field structure across versions
    - `get_entity()` returns ChatInfo with identical or compatible field structure across versions
    - `send_message()` and `get_messages()` return MessageInfo with identical or compatible field structure across versions
  - **Error Handling**: Framework must handle version-specific errors gracefully (e.g., deprecated methods, changed response formats)
  - **Backward Compatibility**: Framework must work with at least 2 previous minor versions (e.g., 1.42.x, 1.41.x, 1.40.x)
  - **Forward Compatibility**: Framework must work with latest available Telethon version
  - **Failure Condition**: Test fails if any core operation fails on any tested version without documented incompatibility
- **Expected Result**:
  - All core operations succeed on all tested Telegram API versions (via Telethon library versions)
  - Response data structures are compatible across versions
  - Framework maintains backward and forward compatibility
  - Version comparison matrix documents any differences
- **Coverage**: Telegram MTProto API version compatibility via Telethon library versions
- **Dependencies**:
  - Multiple Telethon versions (1.40.x, 1.41.x, 1.42.x, latest)
  - Valid Telegram API credentials
  - Test environments for version isolation
  - Access to test Telegram entities (bot, channel) for operations

## Dependencies and Setup

### Network Integration Tests (TC-016, TC-017, TC-018)

#### Required Tools

**For TC-INTEGRATION-EXT-016 (Network Interruptions)**:
- **Option 1 - Docker**:
  - Docker Engine installed and running
  - Docker CLI available in PATH
  - Test container image (e.g., `python:3.12-slim`)
- **Option 2 - iptables (Linux only)**:
  - `iptables` command available
  - Root/sudo privileges required
  - Network interface name (e.g., `eth0`, `ens33`)
- **Option 3 - pytest-httpx (Mocking)**:
  - `pytest-httpx` package: `uv add pytest-httpx --dev`
  - Python test environment

**For TC-INTEGRATION-EXT-017 (Proxy)**:
- **Squid Proxy**:
  - Docker: `docker pull ubuntu/squid:latest`
  - OR local Squid installation: `apt-get install squid` (Debian/Ubuntu) or `yum install squid` (RHEL/CentOS)
- **mitmproxy**:
  - Install: `uv add mitmproxy` OR `pip install mitmproxy`
  - OR Docker: `docker pull mitmproxy/mitmproxy:latest`
- Docker (optional, for containerized proxy)

**For TC-INTEGRATION-EXT-018 (Network Conditions)**:
- **Option 1 - Playwright**:
  - Playwright installed: `uv add playwright` and `playwright install`
- **Option 2 - tc (Linux)**:
  - `tc` command (part of `iproute2` package)
  - Install: `apt-get install iproute2` (Debian/Ubuntu) or `yum install iproute` (RHEL/CentOS)
  - Root/sudo privileges required
- **Option 3 - Docker + netem**:
  - Docker Engine installed
  - Docker image: `gaiadocker/iproute2` or `networkstatic/iproute2`

#### Setup Commands

**TC-016 Setup (Docker method)**:
```bash
# Pull test image
docker pull python:3.12-slim

# Start test container
docker run -d --name tma-network-test python:3.12-slim sleep 3600

# Get container ID
CONTAINER_ID=$(docker ps -q -f name=tma-network-test)
```

**TC-016 Teardown (Docker method)**:
```bash
# Restore network (if interrupted)
docker network connect bridge $CONTAINER_ID

# Cleanup
docker stop $CONTAINER_ID
docker rm $CONTAINER_ID
```

**TC-016 Setup (iptables method)**:
```bash
# Identify target host IP
TARGET_HOST="example.com"
TARGET_IP=$(getent hosts $TARGET_HOST | awk '{print $1}')

# Identify network interface
INTERFACE=$(ip route | grep default | awk '{print $5}' | head -1)
```

**TC-016 Teardown (iptables method)**:
```bash
# Remove blocking rule
iptables -D OUTPUT -d $TARGET_IP -j DROP

# Verify rule removed
iptables -L OUTPUT -n | grep $TARGET_IP
```

**TC-017 Setup (Squid via Docker)**:
```bash
# Start Squid proxy container
docker run -d --name squid-proxy -p 3128:3128 ubuntu/squid:latest

# Verify proxy is running
curl -x http://localhost:3128 http://www.example.com
```

**TC-017 Setup (Squid local)**:
```bash
# Install Squid
sudo apt-get install squid  # Debian/Ubuntu
# OR
sudo yum install squid      # RHEL/CentOS

# Start Squid service
sudo systemctl start squid
sudo systemctl enable squid

# Verify proxy is running
sudo systemctl status squid
```

**TC-017 Setup (mitmproxy)**:
```bash
# Install mitmproxy
uv add mitmproxy
# OR
pip install mitmproxy

# Start mitmproxy (interactive)
mitmproxy -p 8080

# OR start mitmdump (non-interactive)
mitmdump -p 8080 --set confdir=~/.mitmproxy
```

**TC-017 Teardown**:
```bash
# Docker Squid
docker stop squid-proxy
docker rm squid-proxy

# Local Squid
sudo systemctl stop squid

# mitmproxy
# Press Ctrl+C in terminal or kill process
pkill mitmproxy
```

**TC-018 Setup (tc method)**:
```bash
# Identify network interface
INTERFACE=$(ip route | grep default | awk '{print $5}' | head -1)

# Identify target IP
TARGET_HOST="example.com"
TARGET_IP=$(getent hosts $TARGET_HOST | awk '{print $1}')

# Verify tc is available
which tc
```

**TC-018 Teardown (tc method)**:
```bash
# Remove all qdisc rules
sudo tc qdisc del dev $INTERFACE root

# Verify rules removed
sudo tc qdisc show dev $INTERFACE
```

**TC-018 Setup (Docker + netem)**:
```bash
# Create docker-compose.yml for netem
cat > docker-compose.netem.yml <<EOF
version: '3'
services:
  netem:
    image: gaiadocker/iproute2
    network_mode: host
    cap_add:
      - NET_ADMIN
    command: >
      sh -c "
      tc qdisc add dev eth0 root handle 1: htb default 30 &&
      tc class add dev eth0 parent 1: classid 1:1 htb rate 400kbit &&
      tc class add dev eth0 parent 1:1 classid 1:10 htb rate 400kbit ceil 400kbit &&
      tc qdisc add dev eth0 parent 1:10 netem delay 400ms &&
      sleep infinity
      "
EOF

# Start netem service
docker-compose -f docker-compose.netem.yml up -d
```

**TC-018 Teardown (Docker + netem)**:
```bash
# Stop and remove netem service
docker-compose -f docker-compose.netem.yml down

# Remove network rules (if needed)
docker exec netem tc qdisc del dev eth0 root
```

#### Python Dependencies

Add to `pyproject.toml` or install via `uv`:
```bash
# For HTTP mocking (TC-016 Option 3)
uv add pytest-httpx --dev

# For mitmproxy (TC-017)
uv add mitmproxy

# For Playwright (TC-018 Option 1)
uv add playwright
playwright install
```

#### Environment Variables

For proxy configuration (TC-017):
```bash
export HTTP_PROXY="http://localhost:3128"
export HTTPS_PROXY="http://localhost:3128"
export NO_PROXY="localhost,127.0.0.1"
```

#### Verification Commands

**Verify Docker is running**:
```bash
docker ps
docker version
```

**Verify iptables is available**:
```bash
which iptables
sudo iptables -L -n
```

**Verify tc is available**:
```bash
which tc
tc -Version
```

**Verify proxy is accessible**:
```bash
# Squid
curl -x http://localhost:3128 http://www.example.com

# mitmproxy
curl -x http://localhost:8080 http://www.example.com
```
