# HTML Test Fixtures

This directory contains static HTML fixtures for browser integration testing.

## Purpose

These fixtures provide stable, reproducible test pages for browser automation tests, avoiding fragile dependencies on external websites that may change or become unavailable.

## Fixtures

### `test_page.html`
Basic test page for navigation and page loading tests.
- **Use case**: TC-INTEGRATION-EXT-012 (Navigate to real URL)
- **Elements**: `#page-status` - status indicator

### `interactive_page.html`
Interactive page with form elements for interaction testing.
- **Use case**: TC-INTEGRATION-EXT-013 (Interact with real web page)
- **Elements**:
  - `#test-input` - text input field
  - `#test-button` - clickable button
  - `#submit-button` - submit button
  - `#output` - output div element

### `error_page.html`
Page with intentional errors for error handling tests.
- **Use case**: TC-INTEGRATION-EXT-014 (Handle browser errors)
- **Elements**:
  - `#error-button` - button that triggers errors
  - `#error-output` - error output div
- **Errors**: Contains intentional JavaScript errors and missing resource references

### `no_js_page.html`
Page that works without JavaScript (pure HTML/CSS).
- **Use case**: TC-INTEGRATION-EXT-015 (Test browser with JavaScript disabled)
- **Elements**:
  - `#test-input` - text input field
  - `#test-button` - submit button
  - `#test-form` - HTML form element
  - `#output` - output div element

## Usage

### Local File Access
Access fixtures using `file://` protocol:
```python
url = f"file://{os.path.abspath('tests/data/html_fixtures/test_page.html')}"
```

### HTTP Server (Recommended for CI/CD)
Serve fixtures via a local HTTP server:
```python
import http.server
import socketserver
import threading
import os

def start_test_server(port=8000):
    os.chdir('tests/data/html_fixtures')
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    return f"http://localhost:{port}"

# Use in tests
base_url = start_test_server()
url = f"{base_url}/test_page.html"
```

## Location

Fixtures are located at: `tests/data/html_fixtures/`

## Maintenance

- Keep fixtures simple and stable
- Avoid external dependencies in fixtures
- Document all test elements with IDs/classes
- Update fixtures when test requirements change
- Ensure fixtures work in both headless and headed browser modes
