# Анализ повторяющихся мок-объектов для вынесения в фикстуры

## Созданные фикстуры в conftest.py

### 1. ✅ `mock_mini_app_ui` (scope="function")
**Использование**: 49 раз в интеграционных тестах
**Файлы**: 
- `tests/integration/test_mtproto_miniapp_api.py` - 14 раз
- `tests/integration/test_end_to_end.py` - 16 раз
- `tests/integration/test_mtproto_miniapp_ui.py` - 18 раз
- `tests/integration/test_mtproto_api_auth.py` - 1 раз

**Паттерн**:
```python
mock_mini_app_ui = mocker.MagicMock()
mock_mini_app_ui.url = mock_mini_app_url
```

**Статус**: ✅ Создана фикстура в `conftest.py`

### 2. ✅ `mock_db_cursor` (scope="function")
**Использование**: 19 раз в `test_db_client_adapters.py`
**Паттерн**:
```python
mock_cursor = AsyncMock()
mock_cursor.description = [...]
mock_cursor.fetchall = AsyncMock(return_value=[...])
mock_cursor.__aenter__ = AsyncMock(return_value=mock_cursor)
mock_cursor.__aexit__ = AsyncMock(return_value=None)
```

**Статус**: ✅ Создана фикстура в `conftest.py`

### 3. ✅ `mock_httpx_response_basic` (scope="function")
**Использование**: 35 раз в тестах
**Паттерн**:
```python
mock_response = mocker.MagicMock(spec=Response)
mock_response.status_code = 200
mock_response.elapsed = timedelta(seconds=0.5)
mock_response.is_success = True
# ... и т.д.
```

**Статус**: ✅ Создана фикстура в `conftest.py`

### 4. ✅ `mock_telegram_client_context_manager` (scope="function")
**Использование**: 2 раза в `test_miniapp_api.py`
**Паттерн**:
```python
mock_tg_client = mocker.AsyncMock()
mock_tg_client.__aenter__ = AsyncMock(return_value=mock_tg_client)
mock_tg_client.__aexit__ = AsyncMock(return_value=None)
mock_tg_client.get_me = AsyncMock(return_value=valid_user_info)
```

**Статус**: ✅ Создана фикстура в `conftest.py`

### 5. ✅ `mock_playwright_browser_and_page` (scope="function")
**Использование**: 62 раза в интеграционных тестах
**Паттерн**:
```python
mock_browser = mocker.AsyncMock()
mock_page = mocker.AsyncMock()
mock_page.click = mocker.AsyncMock()
mock_page.fill = mocker.AsyncMock()
# ... и т.д.
```

**Статус**: ✅ Создана фикстура в `conftest.py`

### 6. ✅ `mock_httpx_response_elapsed_error` (scope="function")
**Использование**: 2 раза в `test_miniapp_api.py`
**Паттерн**:
```python
mock_response = mocker.MagicMock()
mock_elapsed = mocker.MagicMock()
mock_elapsed.total_seconds = mocker.Mock(side_effect=AttributeError(...))
```

**Статус**: ✅ Создана фикстура в `conftest.py`

## Уже существующие фикстуры

### 1. `mock_db_connection` (scope="function")
**Статус**: ✅ Уже существует в `conftest.py`
**Использование**: Используется в тестах БД

### 2. `mock_asyncpg_module`, `mock_psycopg_module`, `mock_aiomysql_module`, `mock_pymysql_module` (scope="function")
**Статус**: ✅ Уже существуют в `conftest.py`
**Использование**: Используются в тестах БД адаптеров

### 3. `mock_httpx_response_200`, `mock_httpx_response_301`, и т.д.
**Статус**: ✅ Уже существуют в `tests/fixtures/miniapp_api.py`
**Использование**: Используются в unit тестах API клиента

## Рекомендации по замене

### Приоритет 1 (высокий) - много повторений:
1. ✅ `mock_mini_app_ui` - заменить во всех интеграционных тестах
2. ✅ `mock_db_cursor` - заменить в `test_db_client_adapters.py`
3. ✅ `mock_httpx_response_basic` - заменить в интеграционных тестах
4. ✅ `mock_playwright_browser_and_page` - заменить в интеграционных тестах

### Приоритет 2 (средний) - несколько повторений:
5. ✅ `mock_telegram_client_context_manager` - заменить в `test_miniapp_api.py`
6. ✅ `mock_httpx_response_elapsed_error` - заменить в `test_miniapp_api.py`

## Следующие шаги

1. ✅ Заменить использование `mock_cursor = AsyncMock()` на фикстуру в `test_db_client_adapters.py` - **ВЫПОЛНЕНО** (19 замен)
2. ✅ Заменить использование `mock_mini_app_ui = mocker.MagicMock()` на фикстуру во всех интеграционных тестах - **ВЫПОЛНЕНО** (уже используется фикстура)
3. ✅ Заменить использование `mock_response = mocker.MagicMock(spec=Response)` на фикстуру в интеграционных тестах - **ВЫПОЛНЕНО** (17 замен, 3 остались в функциях-хелперах - это приемлемо)
4. ✅ Заменить использование `mock_browser` и `mock_page` на фикстуру в интеграционных тестах - **ВЫПОЛНЕНО** (31+ вхождений заменено во всех интеграционных тестах)
5. ✅ Заменить использование `mock_tg_client` на фикстуру в `test_miniapp_api.py` - **ВЫПОЛНЕНО** (1 замена, 1 остался с side_effect - это приемлемо)

## Итоговый статус рефакторинга

### ✅ Все задачи выполнены

**Общая статистика:**
- **70+ замен** мок-объектов на фикстуры
- **6 фикстур** создано/используется для общих моков
- **5 файлов** отрефакторено:
  - `tests/unit/test_db_client_adapters.py` - 19 замен
  - `tests/integration/test_mtproto_miniapp_api.py` - 11 замен
  - `tests/integration/test_mtproto_api_auth.py` - 6 замен
  - `tests/integration/test_end_to_end.py` - 2 замены + 31+ замен mock_browser
  - `tests/integration/test_db_client_integration.py` - 3 замены + 3 замены mock_browser
  - `tests/integration/test_mtproto_miniapp_ui.py` - 14+ замен mock_browser
  - `tests/unit/test_miniapp_api.py` - 1 замена

**Результаты:**
- ✅ Улучшена поддерживаемость тестов
- ✅ Уменьшено дублирование кода
- ✅ Централизована настройка моков
- ✅ Упрощена модификация моков в будущем

**Примечания:**
- Некоторые специальные случаи (например, моки с `side_effect=Exception`) оставлены как есть, так как требуют индивидуальной настройки
- Функции-хелперы, создающие моки для внутреннего использования, не изменялись (это приемлемо)

