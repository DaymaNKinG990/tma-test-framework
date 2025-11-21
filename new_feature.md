# Предложения по улучшению tma-test-framework

## Проблема
Сейчас для работы с токенами аутентификации нужно создавать обертки или вручную добавлять токен в headers каждого запроса.

## Решение: Встроить поддержку токенов в MiniAppApi

### Файл: `tma_test_framework/mini_app/api.py`

#### 1. Добавить атрибуты для хранения токена в `__init__`:

```python
def __init__(self, url: str, config: Optional[Config] = None) -> None:
    """
    Initialize Mini App API client.

    Args:
        url: Mini App URL
        config: Configuration object
    """
    super().__init__(url, config)
    self.client = AsyncClient(
        timeout=self.config.timeout,
        limits=Limits(max_keepalive_connections=5, max_connections=10),
    )
    # Добавить эти строки:
    self._auth_token: Optional[str] = None
    self._auth_token_type: str = "Bearer"
```

#### 2. Добавить метод для установки токена:

```python
def set_auth_token(self, token: str, token_type: str = "Bearer") -> None:
    """
    Set authentication token for all subsequent requests.

    Args:
        token: Authentication token (JWT, API key, etc.)
        token_type: Token type (default: "Bearer")
    
    Example:
        >>> client = MiniAppApi("http://api.example.com", config)
        >>> result = await client.make_request("v1/login/", method="POST", data=credentials)
        >>> token_data = json.loads(result.body)
        >>> client.set_auth_token(token_data["access"])
        >>> # Все последующие запросы автоматически включают токен
        >>> result = await client.make_request("v1/users/", method="GET")
    """
    self._auth_token = token
    self._auth_token_type = token_type
    self.logger.debug(f"Authentication token set (type: {token_type})")

def clear_auth_token(self) -> None:
    """Clear authentication token."""
    self._auth_token = None
    self._auth_token_type = "Bearer"
    self.logger.debug("Authentication token cleared")
```

#### 3. Модифицировать `make_request` для автоматического добавления токена:

```python
async def make_request(
    self,
    endpoint: str,
    method: str = "GET",
    data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
) -> ApiResult:
    """
    Make request to Mini App API endpoint.

    Args:
        endpoint: API endpoint to test
        method: HTTP method (GET, POST, PUT, DELETE)
        data: Request data
        headers: Request headers (will be merged with auth token if set)

    Returns:
        ApiResult with request result
    """
    try:
        if endpoint.startswith("http"):
            url = endpoint
        else:
            # Assume endpoint is relative to Mini App URL
            base_url = self.url.split("?")[0]  # Remove query params
            url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        # Подготовить headers с автоматическим добавлением токена
        request_headers = {}
        if headers:
            request_headers.update(headers)
        
        # Автоматически добавить токен, если он установлен
        if self._auth_token:
            auth_header = f"{self._auth_token_type} {self._auth_token}"
            request_headers["Authorization"] = auth_header
        
        # Установить Content-Type по умолчанию, если не указан
        if "Content-Type" not in request_headers:
            request_headers["Content-Type"] = "application/json"
        
        self.logger.info(f"Making request: {method} {url}")
        response = await self.client.request(
            method=method, url=url, json=data, headers=request_headers
        )
        # ... остальной код без изменений
```

## Улучшение 2: Добавить поддержку query params в make_request

### Файл: `tma_test_framework/mini_app/api.py`

```python
async def make_request(
    self,
    endpoint: str,
    method: str = "GET",
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,  # Добавить параметр
    headers: Optional[Dict[str, str]] = None,
) -> ApiResult:
    """
    Make request to Mini App API endpoint.

    Args:
        endpoint: API endpoint to test
        method: HTTP method (GET, POST, PUT, DELETE)
        data: Request data (for POST, PUT, PATCH)
        params: Query parameters (for GET requests)
        headers: Request headers

    Returns:
        ApiResult with request result
    """
    # ... код построения URL ...
    
    # Добавить query params к URL
    if params:
        from urllib.parse import urlencode
        query_string = urlencode(params)
        if query_string:
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}{query_string}"
    
    # ... остальной код ...
```

## Улучшение 3: Добавить методы в ApiResult для работы с JSON

### Файл: `tma_test_framework/mini_app/models.py`

```python
class ApiResult(msgspec.Struct, frozen=True):
    """Api request result."""
    
    # ... существующие поля ...
    
    def json(self) -> Dict[str, Any]:
        """
        Parse JSON from response body.
        
        Returns:
            Parsed JSON data as dictionary
            
        Raises:
            ValueError: If body is not valid JSON
        """
        import json
        try:
            return json.loads(self.body.decode('utf-8'))
        except (json.JSONDecodeError, ValueError, UnicodeDecodeError) as e:
            raise ValueError(f"Failed to parse JSON: {e}") from e
    
    def text(self) -> str:
        """
        Get response body as text.
        
        Returns:
            Response body decoded as UTF-8 string
        """
        return self.body.decode('utf-8', errors='replace')
    
    def raise_for_status(self) -> None:
        """
        Raise exception if status code indicates error.
        
        Raises:
            HTTPError: If status code is 4xx or 5xx
        """
        if 400 <= self.status_code < 600:
            error_msg = self.error_message or self.text()
            raise Exception(f"HTTP {self.status_code}: {error_msg}")
    
    def assert_status_code(self, expected_code: int) -> None:
        """
        Assert that status code matches expected value.
        
        Args:
            expected_code: Expected HTTP status code
            
        Raises:
            AssertionError: If status code doesn't match
        """
        assert self.status_code == expected_code, (
            f"Expected status code {expected_code}, got {self.status_code}. "
            f"Response: {self.text()}"
        )
    
    def assert_success(self) -> None:
        """Assert that request was successful (2xx status)."""
        assert self.success, (
            f"Request failed with status {self.status_code}. "
            f"Response: {self.text()}"
        )
    
    def assert_has_fields(self, *fields: str) -> None:
        """
        Assert that JSON response contains specified fields.
        
        Args:
            *fields: Field names that must be present in response
            
        Raises:
            AssertionError: If any field is missing
        """
        data = self.json()
        missing = [field for field in fields if field not in data]
        if missing:
            raise AssertionError(
                f"Missing required fields: {', '.join(missing)}. "
                f"Response: {data}"
            )
```

## Улучшение 4: Добавить утилиты для тестирования

### Файл: `tma_test_framework/utils.py` (новый файл)

```python
"""
Utility functions for API testing.
"""
import json
from typing import Dict, Any, List, Optional


def parse_json(body: bytes) -> Dict[str, Any]:
    """
    Parse JSON from response body.
    
    Args:
        body: Response body as bytes
        
    Returns:
        Parsed JSON data
    """
    try:
        return json.loads(body.decode('utf-8'))
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
        return {}


def validate_response_structure(data: Dict[str, Any], expected_fields: List[str]) -> bool:
    """
    Validate that response contains expected fields.
    
    Args:
        data: Response data dictionary
        expected_fields: List of expected field names
        
    Returns:
        True if all fields present, False otherwise
    """
    return all(field in data for field in expected_fields)


def extract_pagination_info(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract pagination information from response.
    
    Args:
        data: Response data dictionary
        
    Returns:
        Dictionary with pagination info
    """
    return {
        "count": data.get("count"),
        "next": data.get("next"),
        "previous": data.get("previous"),
        "results": data.get("results", []),
    }


def get_error_detail(data: Dict[str, Any]) -> str:
    """
    Extract error detail from response data.
    
    Args:
        data: Response data dictionary
        
    Returns:
        Error detail string
    """
    return data.get("detail", data.get("error", str(data)))
```

## Улучшение 5: Добавить генерацию Telegram init data

### Файл: `tma_test_framework/utils.py`

```python
import hashlib
import hmac
import json
import time
from urllib.parse import urlencode


def generate_telegram_init_data(
    user_id: int = 123456789,
    username: str = "test_user",
    first_name: str = "Test",
    last_name: str = "User",
    bot_token: str = "test_bot_token",
    language_code: str = "ru",
    is_premium: bool = False,
) -> str:
    """
    Generate valid Telegram init data for testing.
    
    Args:
        user_id: Telegram user ID
        username: Telegram username
        first_name: User first name
        last_name: User last name
        bot_token: Bot token for signature generation
        language_code: User language code
        is_premium: Whether user has premium
        
    Returns:
        Valid Telegram init data string
    """
    auth_date = int(time.time())
    user_data = {
        "id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "language_code": language_code,
        "is_premium": is_premium,
        "allows_write_to_pm": True,
    }
    
    data = {
        "user": json.dumps(user_data),
        "auth_date": str(auth_date),
    }
    
    # Generate hash
    check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
    secret = hmac.new("WebAppData".encode(), bot_token.encode(), hashlib.sha256).digest()
    signature = hmac.new(secret, check_string.encode(), hashlib.sha256).hexdigest()
    
    data["hash"] = signature
    return urlencode(data)
```

## Преимущества

1. **Упрощение кода тестов** - не нужно вручную добавлять токен в каждый запрос
2. **Автоматическое управление** - токен добавляется автоматически во все запросы
3. **Обратная совместимость** - если токен не установлен, поведение не меняется
4. **Гибкость** - можно переопределить headers в конкретном запросе
5. **Удобные методы** - `result.json()`, `result.assert_status_code()` вместо внешних функций
6. **Встроенные утилиты** - все необходимые функции в одном месте

## Пример использования после улучшения

```python
# До улучшения (текущий код):
from tests.framework.helpers import assert_status_code, _parse_json

client = MiniAppApi(base_url, config)
result = await client.make_request("v1/login/", method="POST", data=credentials)
token = _parse_json(result.body)["access"]
result = await client.make_request(
    "v1/users/", 
    method="GET",
    headers={"Authorization": f"Bearer {token}"}
)
assert_status_code(result, 200)
data = _parse_json(result.body)

# После улучшения:
from tma_test_framework import MiniAppApi, Config, generate_telegram_init_data

client = MiniAppApi(base_url, config)
result = await client.make_request("v1/login/", method="POST", data=credentials)
token = result.json()["access"]
client.set_auth_token(token)  # Установить один раз

# Токен автоматически добавляется, удобные методы для проверок
result = await client.make_request("v1/users/", method="GET", params={"page": 1})
result.assert_status_code(200)
result.assert_has_fields("results", "count")
data = result.json()
```
