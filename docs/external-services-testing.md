# External Services Integration Tests - Requirements

## Overview

24 tests from the **External Services** category require real external services to execute. These tests verify integration with real services rather than mocks.

---

## Category 1: Telegram MTProto API Integration (5 tests)

### TC-INTEGRATION-EXT-001: Connect to real Telegram API
**Required Real Services:**
- **Telegram MTProto API** (official Telegram API)
- **Active Telegram account** with valid credentials

**Specific Requirements:**
- `api_id` and `api_hash` from [my.telegram.org](https://my.telegram.org)
- Valid session (`session_string` or `session_file`)
- Active internet access to Telegram servers
- Account not blocked or restricted

**Why Real Service is Needed:**
- Verify real connection to Telegram API
- Validate authentication
- Check retrieval of real user data

---

### TC-INTEGRATION-EXT-002: Send message to real bot
**Required Real Services:**
- **Telegram MTProto API**
- **Real Telegram bot** (created via @BotFather)

**Specific Requirements:**
- Bot must be active and respond to commands
- Bot must have `/start` command
- Bot must be accessible to test account
- Test account must be able to send messages to bot

**Why Real Service is Needed:**
- Verify real message sending
- Check receiving responses from bot
- Validate full interaction cycle

---

### TC-INTEGRATION-EXT-003: Get entity from real Telegram
**Required Real Services:**
- **Telegram MTProto API**
- **Real Telegram entity** (user, chat, channel)

**Specific Requirements:**
- Public channel or group
- Or private chat with access
- Or user with contact

**Why Real Service is Needed:**
- Verify retrieval of real entity data
- Validate data structure from Telegram API
- Check handling of different entity types

---

### TC-INTEGRATION-EXT-004: Handle Telegram rate limits
**Required Real Services:**
- **Telegram MTProto API**
- **Operations that trigger rate limits**

**Specific Requirements:**
- Need to perform many operations in short time
- Telegram must return `FloodWaitError`
- Requires real rate limiting from Telegram API

**Why Real Service is Needed:**
- Rate limits are Telegram API protection
- Cannot simulate real limitations
- Testing `FloodWaitError` handling requires real API response

---

### TC-INTEGRATION-EXT-005: Handle Telegram connection errors
**Required Real Services:**
- **Telegram MTProto API**
- **Controlled network issues**

**Specific Requirements:**
- Ability to interrupt network connection
- Or use invalid credentials
- Or simulate API problems

**Why Real Service is Needed:**
- Real network errors differ from mocks
- Verify handling of real exceptions
- Validate reconnection mechanisms

---

## Category 2: HTTP API Integration (5 tests)

### TC-INTEGRATION-EXT-006: Test real HTTP endpoint
**Required Real Services:**
- **Real HTTP server** with accessible endpoint

**Specific Requirements:**
- Public HTTP endpoint (e.g., `http://httpbin.org/get`)
- Or local server for testing
- Endpoint must respond to GET requests
- Endpoint must be accessible from test environment

**Why Real Service is Needed:**
- Verify real HTTP requests
- Validate handling of real responses
- Check network stack

**Example Services:**
- httpbin.org (for testing)
- jsonplaceholder.typicode.com
- Own test server

---

### TC-INTEGRATION-EXT-007: Test HTTPS endpoint
**Required Real Services:**
- **Real HTTPS server** with valid SSL certificate

**Specific Requirements:**
- HTTPS endpoint with valid SSL/TLS certificate
- Endpoint must support TLS handshake
- Certificate must be valid and not expired

**Why Real Service is Needed:**
- Verify SSL/TLS handshake
- Validate certificates
- Check secure connection

**Example Services:**
- https://httpbin.org/get
- https://api.github.com
- Any HTTPS endpoint with valid certificate

---

### TC-INTEGRATION-EXT-008: Test HTTP endpoint with authentication
**Required Real Services:**
- **HTTP/HTTPS server** with authentication

**Specific Requirements:**
- Endpoint requiring authentication (Bearer token, API key, Basic Auth)
- Valid credentials for access
- Endpoint must reject unauthorized requests

**Why Real Service is Needed:**
- Verify real authentication
- Validate handling of 401/403 errors
- Check credential transmission

**Example Services:**
- GitHub API (requires token)
- Any API with OAuth/Bearer token
- Own protected endpoint

---

### TC-INTEGRATION-EXT-009: Handle HTTP errors (4xx, 5xx)
**Required Real Services:**
- **HTTP servers** returning errors

**Specific Requirements:**
- Endpoint returning 404 (Not Found)
- Endpoint returning 500 (Internal Server Error)
- Or server configured to return errors

**Why Real Service is Needed:**
- Verify handling of real HTTP errors
- Validate status codes
- Check error response structure

**Example Services:**
- httpbin.org/status/404
- httpbin.org/status/500
- Own server with error endpoints

---

### TC-INTEGRATION-EXT-010: Handle HTTP timeouts
**Required Real Services:**
- **Slow or non-responding HTTP server**

**Specific Requirements:**
- Endpoint with large response delay
- Or endpoint that doesn't respond
- Ability to control timeout

**Why Real Service is Needed:**
- Verify real timeout situations
- Validate handling of network delays
- Check timeout mechanisms

**Example Services:**
- httpbin.org/delay/10 (10 second delay)
- Own slow endpoint
- Unavailable server

---

## Category 3: Browser Automation Integration (5 tests)

### TC-INTEGRATION-EXT-011: Launch real browser
**Required Real Services:**
- **Playwright** with installed browsers

**Specific Requirements:**
- Playwright installed (`playwright install`)
- Browsers (Chromium, Firefox, WebKit) installed
- Access to graphical environment (Xvfb needed on Linux for headless)

**Why Real Service is Needed:**
- Verify real browser launch
- Validate Playwright functionality
- Check system dependencies

**Note:**
- Can work in headless mode
- Requires browser installation via Playwright

---

### TC-INTEGRATION-EXT-012: Navigate to real URL
**Required Real Services:**
- **Real website** with accessible URL

**Specific Requirements:**
- Public website (e.g., example.com)
- Or local web server
- URL must be accessible from test environment

**Why Real Service is Needed:**
- Verify real navigation
- Validate page loading
- Check browser functionality with real content

**Example Services:**
- https://example.com
- https://httpbin.org/html
- Own web server

---

### TC-INTEGRATION-EXT-013: Interact with real web page
**Required Real Services:**
- **Real web page** with interactive elements

**Specific Requirements:**
- Page with buttons, forms, input fields
- Elements must be accessible for interaction
- Page must respond to actions

**Why Real Service is Needed:**
- Verify real interactions
- Validate DOM work
- Check event handling

**Example Services:**
- https://httpbin.org/forms/post (form)
- Own test page
- Any page with interactive elements

---

### TC-INTEGRATION-EXT-014: Handle browser errors
**Required Real Services:**
- **Web page** causing browser errors

**Specific Requirements:**
- Page with invalid JavaScript
- Or page with unavailable resources
- Or page causing console errors

**Why Real Service is Needed:**
- Verify handling of real browser errors
- Validate error logging
- Check error resilience

**Example Services:**
- Page with JavaScript syntax errors
- Page with unavailable resources (404)
- Own page with errors

---

### TC-INTEGRATION-EXT-015: Test browser with JavaScript disabled
**Required Real Services:**
- **Web page** working without JavaScript

**Specific Requirements:**
- Page must work without JavaScript
- Elements must be accessible via HTML
- Forms must work without JS

**Why Real Service is Needed:**
- Verify work without JavaScript
- Validate fallback behavior
- Check compatibility

**Example Services:**
- Static HTML pages
- Simple forms without JS
- Own page without JavaScript

---

## Category 4: Network Integration (3 tests)

### TC-INTEGRATION-EXT-016: Handle network interruptions
**Required Real Services:**
- **Controlled network connection**

**Specific Requirements:**
- Ability to interrupt network connection
- Ability to restore connection
- Control over network interface

**Why Real Service is Needed:**
- Verify handling of real network errors
- Validate recovery mechanisms
- Check failure resilience

**Implementation Methods:**
- Disable network interface
- Use firewall for blocking
- Use network emulation tools

---

### TC-INTEGRATION-EXT-017: Test with proxy
**Required Real Services:**
- **Proxy server**

**Specific Requirements:**
- Working proxy server (HTTP/HTTPS/SOCKS)
- Access to proxy from test environment
- Valid credentials (if required)

**Why Real Service is Needed:**
- Verify work through proxy
- Validate proxy configuration
- Check traffic routing

**Examples:**
- Local proxy (e.g., mitmproxy)
- Public proxy server
- SOCKS proxy

---

### TC-INTEGRATION-EXT-018: Test with different network conditions
**Required Real Services:**
- **Tools for emulating network conditions**

**Specific Requirements:**
- Ability to emulate slow network
- Ability to emulate high latency
- Ability to emulate packet loss

**Why Real Service is Needed:**
- Verify work in various network conditions
- Validate timeout mechanisms
- Check performance

**Tools:**
- `tc` (traffic control) on Linux
- Network Link Conditioner (macOS)
- Clumsy (Windows)
- Playwright network throttling

---

## Category 5: Security Integration (2 tests)

### TC-INTEGRATION-EXT-019: Verify SSL certificate validation
**Required Real Services:**
- **HTTPS servers** with valid and invalid certificates

**Specific Requirements:**
- HTTPS endpoint with valid SSL certificate
- HTTPS endpoint with invalid/expired certificate
- Or self-signed certificate

**Why Real Service is Needed:**
- Verify SSL certificate validation
- Validate handling of certificate errors
- Check connection security

**Examples:**
- https://example.com (valid)
- Own server with invalid certificate
- badssl.com (test certificates)

---

### TC-INTEGRATION-EXT-020: Test with different user agents
**Required Real Services:**
- **Web page** checking user agent

**Specific Requirements:**
- Page that reads and responds to user agent
- Ability to verify set user agent

**Why Real Service is Needed:**
- Verify user agent setting
- Validate work with various UAs
- Check compatibility

**Examples:**
- httpbin.org/user-agent
- Own page checking UA
- Any page showing UA

---

## Category 6: Performance Integration (2 tests)

### TC-INTEGRATION-EXT-021: Measure API response times
**Required Real Services:**
- **HTTP/HTTPS API endpoint**

**Specific Requirements:**
- API endpoint with measurable response time
- Endpoint must be stable
- Ability to make multiple requests

**Why Real Service is Needed:**
- Verify real response times
- Validate performance measurement
- Check work in real conditions

**Examples:**
- httpbin.org/delay/1
- Any stable API endpoint
- Own test API

---

### TC-INTEGRATION-EXT-022: Measure page load times
**Required Real Services:**
- **Web page** with measurable load time

**Specific Requirements:**
- Page with various resources (CSS, JS, images)
- Ability to measure load time
- Stable page availability

**Why Real Service is Needed:**
- Verify real load times
- Validate performance metrics
- Check optimization

**Examples:**
- Any web page
- Own test page
- Page with controlled load time

---

## Category 7: Compatibility Integration (2 tests)

### TC-INTEGRATION-EXT-023: Test with different browsers
**Required Real Services:**
- **Multiple browsers** via Playwright

**Specific Requirements:**
- Chromium installed
- Firefox installed
- WebKit installed
- All browsers accessible via Playwright

**Why Real Service is Needed:**
- Verify compatibility with various browsers
- Validate engine functionality
- Check cross-browser compatibility

**Note:**
- Requires installation of all browsers via `playwright install`
- Can work in headless mode

---

### TC-INTEGRATION-EXT-024: Test with different Telegram API versions
**Required Real Services:**
- **Telegram MTProto API** with various versions

**Specific Requirements:**
- Access to current Telegram API version
- Ability to test with various versions (if available)
- Or test compatibility with API updates

**Why Real Service is Needed:**
- Verify compatibility with API versions
- Validate work with updates
- Check backward compatibility

**Note:**
- Telegram API usually has one active version
- Test may check compatibility when updating Telethon library

---

## Summary of Requirements

### Critical Real Services (Required):
1. **Telegram MTProto API** - for 5 tests
2. **Real Telegram Account** - for all Telegram tests
3. **Real Telegram Bot** - for message sending test

### Optional Real Services (Can use test services):
1. **HTTP/HTTPS Servers** - can use httpbin.org or own
2. **Web Pages** - can use public or own
3. **Playwright Browsers** - require installation, but work locally

### Emulation Tools:
1. **Network emulation tools** - for network condition tests
2. **Proxy servers** - can use local
3. **SSL certificates** - can use test certificates

---

## Implementation Recommendations

### For CI/CD:
- Use test services (httpbin.org, example.com)
- Use headless browsers
- Use mocks for Telegram API (or test account)

### For Local Testing:
- Use real services for full validation
- Set up test Telegram bot
- Use local web servers

### For Production Testing:
- Use staging environment
- Use test accounts
- Isolate from production data
