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

## Улучшение 6: Расширить Config для поддержки bot_token и language_code

### Файл: `tma_test_framework/config.py`

```python
class Config(msgspec.Struct, frozen=True):
    """Configuration for TMA test framework."""
    
    # ... существующие поля ...
    
    # Добавить новые поля:
    bot_token: Optional[str] = None
    language_code: str = "ru"
    
    @classmethod
    def from_env(cls) -> "Config":
        """
        Create config from environment variables.
        
        Returns:
            Config instance with values from environment
        """
        return cls(
            # ... существующие поля ...
            bot_token=os.getenv("TELEGRAM_BOT_TOKEN"),
            language_code=os.getenv("TMA_LANGUAGE_CODE", "ru"),
        )
```

**Преимущества:**
- Централизованное хранение конфигурации
- Упрощение использования в тестах
- Не нужно передавать `bot_token` и `language_code` отдельно

## Улучшение 7: Добавить методы в UserTelegramClient для работы с TMA пользователями

### Файл: `tma_test_framework/mtproto_client.py`

```python
class UserTelegramClient:
    # ... существующие методы ...
    
    def to_tma_user_data(self) -> Dict[str, Any]:
        """
        Convert UserInfo to TMA user data format for API.
        
        Returns:
            Dictionary with user data in format expected by /v1/create/tma/ endpoint
            
        Raises:
            ValueError: If user is not authorized (get_me() not called)
        """
        if not self._me:
            raise ValueError("User not authorized. Call get_me() first.")
        
        return {
            "telegram_id": str(self._me.id),
            "telegram_username": self._me.username or "",
            "first_name": self._me.first_name or "",
            "last_name": self._me.last_name or "",
        }
    
    async def generate_init_data(
        self,
        config: Config,
        is_premium: bool = False,
    ) -> str:
        """
        Generate Telegram init_data from current user info.
        
        Args:
            config: Config object with bot_token and language_code
            is_premium: Whether user has premium
            
        Returns:
            Valid Telegram init data string
            
        Raises:
            ValueError: If user is not authorized or bot_token is missing
        """
        if not self._me:
            raise ValueError("User not authorized. Call get_me() first.")
        
        if not config.bot_token:
            raise ValueError("bot_token is required in config")
        
        return generate_telegram_init_data(
            user_id=self._me.id,
            username=self._me.username or "",
            first_name=self._me.first_name or "",
            last_name=self._me.last_name or "",
            bot_token=config.bot_token,
            language_code=config.language_code,
            is_premium=is_premium or self._me.is_premium,
        )
```

**Преимущества:**
- Упрощает получение данных пользователя в нужном формате
- Автоматическая генерация init_data из реальных данных пользователя
- Меньше ручной работы в тестах

## Улучшение 8: Добавить утилиту для преобразования UserInfo в user_data

### Файл: `tma_test_framework/utils.py`

```python
def user_info_to_tma_data(user_info: UserInfo) -> Dict[str, Any]:
    """
    Convert UserInfo to TMA user data format for API.
    
    Args:
        user_info: UserInfo object from UserTelegramClient
        
    Returns:
        Dictionary with user data in format expected by /v1/create/tma/ endpoint
    """
    return {
        "telegram_id": str(user_info.id),
        "telegram_username": user_info.username or "",
        "first_name": user_info.first_name or "",
        "last_name": user_info.last_name or "",
    }
```

## Улучшение 9: Добавить метод в MiniAppApi для автоматической настройки TMA аутентификации

### Файл: `tma_test_framework/mini_app/api.py`

```python
async def setup_tma_auth(
    self,
    user_info: Optional[UserInfo] = None,
    config: Optional[Config] = None,
    create_user: bool = True,
    create_user_endpoint: str = "v1/create/tma/",
) -> None:
    """
    Setup TMA authentication: create user and set init_data token.
    
    Args:
        user_info: UserInfo object (if None, will try to get from UserTelegramClient)
        config: Config object (required if user_info is None)
        create_user: Whether to create user via API (default: True)
        create_user_endpoint: Endpoint for creating user (default: "v1/create/tma/")
        
    Raises:
        ValueError: If user_info and config are both None
        Exception: If user creation fails (unless user already exists)
    """
    if user_info is None:
        if config is None:
            raise ValueError("Either user_info or config must be provided")
        
        # Try to get user info from UserTelegramClient
        try:
            async with UserTelegramClient(config) as tg_client:
                user_info = await tg_client.get_me()
        except Exception as e:
            raise ValueError(f"Failed to get user info from Telegram: {e}") from e
    
    # Prepare user data
    user_data = user_info_to_tma_data(user_info)
    
    # Create user if needed
    if create_user:
        result = await self.make_request(
            create_user_endpoint,
            method="POST",
            data=user_data,
        )
        # 400 means user already exists, which is fine
        if result.status_code not in [HTTPStatus.CREATED, HTTPStatus.BAD_REQUEST]:
            result.raise_for_status()
    
    # Generate init_data
    if config is None:
        raise ValueError("config is required for generating init_data")
    
    init_data = generate_telegram_init_data(
        user_id=user_info.id,
        username=user_info.username or "",
        first_name=user_info.first_name or "",
        last_name=user_info.last_name or "",
        bot_token=config.bot_token or "",
        language_code=config.language_code,
        is_premium=user_info.is_premium,
    )
    
    # Set auth token
    self.set_auth_token(init_data, token_type="tma")
```

**Преимущества:**
- Один метод для полной настройки TMA аутентификации
- Автоматическая обработка создания пользователя
- Упрощает код в фикстурах

## Пример использования после улучшения

```python
# До улучшения (текущий код в conftest.py):
async def authenticated_tma_client(api_client: MiniAppApi, api_config: Config) -> MiniAppApi:
    async with UserTelegramClient(api_config) as tg_client:
        me = await tg_client.get_me()
    user_data = {
        "telegram_id": str(me.id),
        "telegram_username": me.username or "",
        "first_name": me.first_name or "",
        "last_name": me.last_name or "",
    }
    
    result = await api_client.make_request("v1/create/tma/", method="POST", data=user_data)
    if result.status_code not in [HTTPStatus.CREATED, HTTPStatus.BAD_REQUEST]:
        result.raise_for_status()
    
    bot_token = api_config.bot_token  # Может не существовать
    init_data = generate_telegram_init_data(
        user_id=telegram_id,  # Переменная не определена!
        username=telegram_username,  # Переменная не определена!
        first_name=first_name,  # Переменная не определена!
        last_name=last_name,  # Переменная не определена!
        bot_token=bot_token,
        language_code=api_config.language_code,  # Может не существовать
        is_premium=False,
    )
    api_client.set_auth_token(init_data, token_type="tma")
    return api_client

# После улучшения:
async def authenticated_tma_client(api_client: MiniAppApi, api_config: Config) -> MiniAppApi:
    """Create authenticated TMA client with init_data in Authorization header"""
    # Один метод делает всё: получает данные пользователя, создаёт пользователя, генерирует init_data
    await api_client.setup_tma_auth(config=api_config)
    return api_client

# Или более явный вариант:
async def authenticated_tma_client(api_client: MiniAppApi, api_config: Config) -> MiniAppApi:
    """Create authenticated TMA client with init_data in Authorization header"""
    async with UserTelegramClient(api_config) as tg_client:
        me = await tg_client.get_me()
        # Удобные методы для преобразования данных
        user_data = tg_client.to_tma_user_data()
        
        # Создать пользователя
        result = await api_client.make_request("v1/create/tma/", method="POST", data=user_data)
        if result.status_code not in [HTTPStatus.CREATED, HTTPStatus.BAD_REQUEST]:
            result.raise_for_status()
        
        # Генерация init_data из данных пользователя
        init_data = await tg_client.generate_init_data(api_config)
        api_client.set_auth_token(init_data, token_type="tma")
    
    return api_client
```

## Резюме всех улучшений

1. **Управление токенами** - автоматическое добавление токенов в запросы
2. **Query параметры** - поддержка params в make_request
3. **Методы ApiResult** - удобные методы для работы с ответами
4. **Утилиты** - встроенные функции для валидации и парсинга
5. **Генерация init_data** - функция для создания валидных Telegram init data
6. **Расширенный Config** - поддержка bot_token и language_code
7. **Методы UserTelegramClient** - преобразование UserInfo в нужные форматы
8. **Утилита преобразования** - user_info_to_tma_data
9. **Автоматическая настройка TMA** - setup_tma_auth для полной настройки аутентификации
