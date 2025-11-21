# Сопоставление тест-кейсов с юнит-тестами

## MiniAppApi - Сопоставление

### 1. Initialization Tests

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-API-001 | Initialize MiniAppApi with URL and config | `test_init_with_url_and_config` | ✅ |
| TC-API-002 | Initialize MiniAppApi with config=None raises error | `test_init_with_config_none_raises_error` | ✅ |
| TC-API-003 | Verify AsyncClient is initialized with correct timeout | `test_init_creates_async_client_with_timeout` | ✅ |
| TC-API-004 | Verify AsyncClient limits are set correctly | `test_init_creates_async_client_with_limits` | ✅ |

**Примечание**: TC-API-002 был обновлен - теперь проверяет, что config=None вызывает TypeError.

### 2. Close Method Tests

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-API-005 | Close MiniAppApi client | `test_close_calls_client_aclose` | ✅ |
| TC-API-006 | Close MiniAppApi multiple times | `test_close_multiple_times` | ✅ |

**Примечание**: TC-API-006 теперь полностью покрыт тестом на множественные вызовы.

### 3. validate_init_data() Tests

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-API-007 | Validate valid init_data | `test_validate_init_data_valid` | ✅ |
| TC-API-008 | Reject invalid init_data (wrong hash) | `test_validate_init_data_invalid_hash` | ✅ |
| TC-API-009 | Reject init_data without hash parameter | `test_validate_init_data_without_hash` | ✅ |
| TC-API-010 | Reject empty init_data | `test_validate_init_data_empty_init_data` | ✅ |
| TC-API-011 | Reject empty bot_token | `test_validate_init_data_empty_bot_token` | ✅ |
| TC-API-012 | Reject both empty init_data and bot_token | `test_validate_init_data_both_empty` | ✅ |
| TC-API-013 | Handle hash at beginning of init_data | `test_validate_init_data_hash_at_beginning` | ✅ |
| TC-API-014 | Handle hash in middle of init_data | `test_validate_init_data_hash_in_middle` | ✅ |
| TC-API-015 | Handle hash at end of init_data | `test_validate_init_data_hash_at_end` | ✅ |
| TC-API-016 | Verify validate_init_data uses compare_digest | `test_validate_init_data_uses_compare_digest` | ✅ |
| TC-API-017 | Handle exception in validate_init_data | `test_validate_init_data_logs_error_on_exception` | ✅ |
| TC-API-018 | Validate init_data with unicode characters | `test_validate_init_data_unicode` | ✅ |
| TC-API-019 | Validate init_data with special characters | `test_validate_init_data_with_ampersand_in_values`, `test_validate_init_data_bot_token_special_chars` | ✅ |

**Дополнительные тесты** (не в тест-кейсах):
- `test_validate_init_data_invalid_token` - проверка неверного токена
- `test_validate_init_data_logs_success` - логирование успеха
- `test_validate_init_data_logs_invalid` - логирование невалидности
- `test_validate_init_data_parametrized` - параметризованный тест
- `test_validate_init_data_very_long` - очень длинные данные

### 4. make_request() Tests

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-API-020 | Make GET request to relative endpoint | `test_make_request_relative_url_with_slash` | ✅ |
| TC-API-021 | Make GET request to absolute URL | `test_make_request_absolute_url` | ✅ |
| TC-API-022 | Make GET request with relative URL starting with slash | `test_make_request_relative_url_with_slash` | ✅ |
| TC-API-023 | Make GET request with relative URL without slash | `test_make_request_relative_url_without_slash` | ✅ |
| TC-API-024 | Make GET request and verify response | `test_make_request_status_200` | ✅ |
| TC-API-025 | Make POST request with data | `test_make_request_post_with_data` | ✅ |
| TC-API-026 | Make request with custom headers | `test_make_request_with_headers` | ✅ |
| TC-API-027 | Make request and verify response_time is recorded | `test_make_request_response_time` | ✅ |
| TC-API-028 | Make request and verify response data is extracted to immutable fields | `test_make_request_extracts_response_data` | ✅ |
| TC-API-029 | Handle request exception | `test_make_request_network_error`, `test_make_request_timeout_error` | ✅ |
| TC-API-030 | Verify make_request logs request | `test_make_request_logs_request` | ✅ |
| TC-API-031 | Verify make_request logs response | `test_make_request_logs_response` | ✅ |
| TC-API-032 | Verify make_request logs error on exception | `test_make_request_logs_error` | ✅ |
| TC-API-033 | Make request with different HTTP methods | `test_make_request_put_method`, `test_make_request_delete_method` | ✅ |
| TC-API-034 | Make request and verify status code flags | `test_make_request_status_200`, `test_make_request_status_301`, `test_make_request_status_404`, `test_make_request_status_500`, `test_make_request_status_101` | ✅ |
| TC-API-035 | Make request with base URL containing query params | `test_make_request_removes_query_params_from_base_url` | ✅ |
| TC-API-036 | Make request with very long endpoint | `test_make_request_very_long_endpoint` | ✅ |
| TC-API-037 | Make request with unicode in endpoint | `test_make_request_unicode_endpoint` | ✅ |
| TC-API-038 | Handle response_time when elapsed is unavailable | `test_make_request_response_time_unavailable`, `test_make_request_response_time_runtime_error` | ✅ |

**Дополнительные тесты** (не в тест-кейсах):
- `test_make_request_get_method` - явная проверка GET метода

### 5. Edge Cases

Все edge cases покрыты тестами.

### 6. Authentication Token Management Tests

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-API-039 | Initialize MiniAppApi with default auth token values | `test_init_sets_default_auth_token_values` | ✅ |
| TC-API-040 | Set authentication token with default type | `test_set_auth_token` | ✅ |
| TC-API-041 | Set authentication token with custom type | `test_set_auth_token_with_custom_type` | ✅ |
| TC-API-042 | Clear authentication token | `test_clear_auth_token` | ✅ |
| TC-API-043 | Make request automatically adds auth token to headers | `test_make_request_adds_auth_token_automatically` | ✅ |
| TC-API-044 | Make request without token does not add Authorization header | `test_make_request_without_token_no_auth_header` | ✅ |
| TC-API-045 | Make request uses custom token type | `test_make_request_custom_token_type` | ✅ |
| TC-API-046 | Make request allows overriding Authorization header | `test_make_request_headers_override_auth_token` | ✅ |
| TC-API-047 | Make request merges custom headers with auth token | `test_make_request_merges_headers_with_token` | ✅ |
| TC-API-048 | Make request sets Content-Type for requests with data | `test_make_request_sets_content_type_for_data` | ✅ |
| TC-API-049 | Make request preserves custom Content-Type header | `test_make_request_preserves_custom_content_type` | ✅ |

### 6. Query Parameters Tests

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-API-050 | Make request with query parameters | `test_make_request_with_query_params` | ✅ |
| TC-API-051 | Make request with query params and existing query string | `test_make_request_with_query_params_and_existing_query` | ✅ |
| TC-API-052 | Make request with empty params dict | `test_make_request_with_empty_params` | ✅ |

**Дополнительные тесты** (не в тест-кейсах):
- `test_make_request_timeout_respected` - проверка таймаута

### 7. Inheritance and Context Manager

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| - | Context manager calls close | `test_context_manager_calls_close` | ✅ |
| - | Logger bound to class name | `test_logger_bound_to_class_name` | ✅ |
| - | Inherits from BaseMiniApp | `test_inherits_from_base_miniapp` | ✅ |

## MiniAppUI - Сопоставление

### 1. Initialization Tests

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-UI-001 | Initialize MiniAppUI with URL and config | `test_init_with_url_and_config` | ✅ |
| TC-UI-002 | Initialize MiniAppUI with config=None raises error | `test_init_with_config_none_raises_value_error` | ✅ |
| - | Browser and page initially None | `test_init_sets_browser_and_page_to_none` | ✅ |

**Примечание**: TC-UI-002 был обновлен - теперь проверяет, что config=None вызывает ValueError.

### 2. setup_browser() Tests

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-UI-003 | Setup browser for first time | `test_setup_browser_first_call_launches_chromium`, `test_setup_browser_creates_new_page`, `test_setup_browser_sets_user_agent` | ✅ |
| TC-UI-004 | Setup browser when already setup | `test_setup_browser_second_call_logs_already_setup`, `test_setup_browser_second_call_does_not_create_new_browser` | ✅ |
| TC-UI-005 | Verify setup_browser returns Self | `test_setup_browser_returns_self`, `test_setup_browser_returns_self_for_fluent_interface` | ✅ |

### 3. close() Tests

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-UI-006 | Close browser when open | `test_close_closes_browser_if_set` | ✅ |
| TC-UI-007 | Close browser when not open | `test_close_does_nothing_if_browser_none` | ✅ |

### 4. Element Interaction Tests

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-UI-008 | Click element successfully | `test_click_element_success` | ✅ |
| TC-UI-009 | Click element with exception | `test_click_element_exception_handled` | ✅ |
| TC-UI-010 | Fill input field | `test_fill_input_success` | ✅ |
| TC-UI-011 | Fill input with exception | `test_fill_input_exception_handled` | ✅ |
| TC-UI-012 | Wait for element to appear | `test_wait_for_element_success` | ✅ |
| TC-UI-013 | Wait for element timeout | `test_wait_for_element_timeout` | ✅ |
| TC-UI-014 | Get element text | `test_get_element_text_success` | ✅ |
| TC-UI-015 | Get element text when element doesn't exist | `test_get_element_text_element_not_found` | ✅ |
| TC-UI-016 | Get element attribute value | `test_get_element_attribute_value_success` | ✅ |
| TC-UI-017 | Get element attribute when element doesn't exist | `test_get_element_attribute_value_element_not_found` | ✅ |
| TC-UI-018 | Scroll to element | `test_scroll_to_element_success` | ✅ |
| TC-UI-019 | Scroll to element with exception | `test_scroll_to_element_error_handled` | ✅ |
| TC-UI-020 | Hover over element | `test_hover_element_success` | ✅ |
| TC-UI-021 | Double click element | `test_double_click_element_success` | ✅ |
| TC-UI-022 | Right click element | `test_right_click_element_success` | ✅ |
| TC-UI-023 | Select option from dropdown | `test_select_option_success` | ✅ |
| TC-UI-024 | Check checkbox | `test_check_checkbox_success` | ✅ |
| TC-UI-025 | Uncheck checkbox | `test_uncheck_checkbox_success` | ✅ |
| TC-UI-026 | Upload file | `test_upload_file_success` | ✅ |

**Дополнительные тесты** (не в тест-кейсах):
- `test_hover_element_exception_handled` - обработка ошибок hover
- `test_double_click_element_exception_handled` - обработка ошибок double click
- `test_right_click_element_exception_handled` - обработка ошибок right click
- `test_check_checkbox_exception_handled` - обработка ошибок check
- `test_uncheck_checkbox_exception_handled` - обработка ошибок uncheck
- `test_select_option_exception_handled` - обработка ошибок select
- `test_get_element_text_exception_handled` - обработка ошибок get text
- `test_get_element_attribute_value_exception_handled` - обработка ошибок get attribute
- `test_upload_file_error_handled` - обработка ошибок upload

### 5. Keyboard Tests

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-UI-027 | Press key | `test_press_key_success` | ✅ |
| TC-UI-028 | Type text | `test_type_text_success` | ✅ |

**Дополнительные тесты**:
- `test_press_key_invalid_key_handled` - обработка неверного ключа
- `test_type_text_error_handled` - обработка ошибок ввода

### 6. Navigation and Page State Tests

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-UI-029 | Wait for navigation | `test_wait_for_navigation_success` | ✅ |
| TC-UI-030 | Wait for navigation timeout | `test_wait_for_navigation_timeout` | ✅ |
| TC-UI-031 | Get page title | `test_get_page_title_success` | ✅ |
| TC-UI-032 | Get page title with exception | `test_get_page_title_exception_handled` | ✅ |
| TC-UI-033 | Get page URL | `test_get_page_url_success` | ✅ |
| TC-UI-034 | Get page URL with exception | `test_get_page_url_exception_handled` | ✅ |

### 7. Screenshot and Script Tests

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-UI-035 | Take screenshot | `test_take_screenshot_success` | ✅ |
| TC-UI-036 | Take screenshot with exception | `test_take_screenshot_error_handled` | ✅ |
| TC-UI-037 | Execute JavaScript script | `test_execute_script_success` | ✅ |
| TC-UI-038 | Execute script with exception | `test_execute_script_error_handled` | ✅ |

### 8. Edge Cases

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-UI-039 | Use methods before browser setup | `test_methods_before_browser_setup` | ✅ |
| TC-UI-040 | Use methods with unicode selectors | `test_click_element_unicode_selector`, `test_fill_input_unicode_selector` | ✅ |
| TC-UI-041 | Use methods with very long selectors | `test_click_element_very_long_selector`, `test_fill_input_very_long_selector` | ✅ |

### 9. Context Manager and Inheritance

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| - | Context manager __aenter__ returns self | `test_aenter_returns_self` | ✅ |
| - | Context manager __aexit__ calls close | `test_aexit_calls_close` | ✅ |
| - | Context manager usage | `test_context_manager_usage` | ✅ |
| - | Can be inherited | `test_can_be_inherited` | ✅ |
| - | Logger bound to class name | `test_logger_bound_to_class_name` | ✅ |
| - | No exceptions propagated | `test_no_exceptions_propagated` | ✅ |
| - | Browser closed in close | `test_browser_closed_in_close` | ✅ |
| - | Logs contain context | `test_logs_contain_context` | ✅ |

## ApiResult Methods - Сопоставление

### 1. JSON and Text Methods

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-MODEL-API-022 | ApiResult.json() parses valid JSON | `test_api_result_json_method` | ✅ |
| TC-MODEL-API-023 | ApiResult.json() raises ValueError for invalid JSON | `test_api_result_json_method_invalid_json` | ✅ |
| TC-MODEL-API-024 | ApiResult.text() returns decoded body | `test_api_result_text_method` | ✅ |
| TC-MODEL-API-025 | ApiResult.text() handles decode errors gracefully | `test_api_result_text_method_with_errors` | ✅ |

### 2. Status Code Assertion Methods

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-MODEL-API-026 | ApiResult.raise_for_status() does not raise for success | `test_api_result_raise_for_status_success` | ✅ |
| TC-MODEL-API-027 | ApiResult.raise_for_status() raises for 4xx status | `test_api_result_raise_for_status_client_error` | ✅ |
| TC-MODEL-API-028 | ApiResult.raise_for_status() raises for 5xx status | `test_api_result_raise_for_status_server_error` | ✅ |
| TC-MODEL-API-029 | ApiResult.assert_status_code() with matching code | `test_api_result_assert_status_code_success` | ✅ |
| TC-MODEL-API-030 | ApiResult.assert_status_code() raises for mismatch | `test_api_result_assert_status_code_failure` | ✅ |
| TC-MODEL-API-031 | ApiResult.assert_success() for successful request | `test_api_result_assert_success` | ✅ |
| TC-MODEL-API-032 | ApiResult.assert_success() raises for failed request | `test_api_result_assert_success_failure` | ✅ |
| TC-MODEL-API-033 | ApiResult.assert_has_fields() with all fields present | `test_api_result_assert_has_fields_success` | ✅ |
| TC-MODEL-API-034 | ApiResult.assert_has_fields() raises for missing fields | `test_api_result_assert_has_fields_missing` | ✅ |

## Utility Functions - Сопоставление

### 1. parse_json() Tests

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-UTILS-001 | Parse valid JSON | `test_parse_json_valid` | ✅ |
| TC-UTILS-002 | Parse invalid JSON returns empty dict | `test_parse_json_invalid` | ✅ |
| TC-UTILS-003 | Parse empty body returns empty dict | `test_parse_json_empty` | ✅ |
| TC-UTILS-004 | Parse JSON with unicode characters | `test_parse_json_unicode` | ✅ |

### 2. validate_response_structure() Tests

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-UTILS-005 | Validate structure with all fields present | `test_validate_response_structure_all_fields_present` | ✅ |
| TC-UTILS-006 | Validate structure with missing fields | `test_validate_response_structure_missing_fields` | ✅ |
| TC-UTILS-007 | Validate structure with empty expected fields | `test_validate_response_structure_empty_fields` | ✅ |

### 3. extract_pagination_info() Tests

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-UTILS-008 | Extract complete pagination info | `test_extract_pagination_info_complete` | ✅ |
| TC-UTILS-009 | Extract partial pagination info | `test_extract_pagination_info_partial` | ✅ |
| TC-UTILS-010 | Extract pagination info from empty data | `test_extract_pagination_info_empty` | ✅ |

### 4. get_error_detail() Tests

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-UTILS-011 | Extract error detail from 'detail' field | `test_get_error_detail_with_detail` | ✅ |
| TC-UTILS-012 | Extract error detail from 'error' field | `test_get_error_detail_with_error` | ✅ |
| TC-UTILS-013 | Extract error detail fallback to string representation | `test_get_error_detail_fallback` | ✅ |

### 5. generate_telegram_init_data() Tests

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-UTILS-014 | Generate init data with default parameters | `test_generate_telegram_init_data_default` | ✅ |
| TC-UTILS-015 | Generate init data with custom parameters | `test_generate_telegram_init_data_custom` | ✅ |
| TC-UTILS-016 | Generate init data with valid hash format | `test_generate_telegram_init_data_hash_format` | ✅ |
| TC-UTILS-017 | Generate init data can be validated | `test_generate_telegram_init_data_validates` | ✅ |

## UserTelegramClient - Сопоставление

### 12. Session Management Tests

| Тест-кейс | Описание | Соответствующий тест | Статус |
|-----------|----------|---------------------|--------|
| TC-CLIENT-053 | Get session_string from connected client | `test_session_string_returns_string` | ✅ |
| TC-CLIENT-054 | Get session_string raises when not connected | `test_session_string_not_connected` | ✅ |
| TC-CLIENT-055 | Get session_string raises with SQLiteSession | `test_session_string_with_sqlite_session` | ✅ |
| TC-CLIENT-056 | Create session with api_id and api_hash | `test_create_session_with_params` | ✅ |
| TC-CLIENT-057 | Create session with Config object | `test_create_session_with_config` | ✅ |
| TC-CLIENT-058 | Create session interactive mode | `test_create_session_interactive` | ✅ |
| TC-CLIENT-059 | Create session non-interactive mode | `test_create_session_non_interactive` | ✅ |
| TC-CLIENT-060 | Create session with 2FA password | `test_create_session_with_2fa` | ✅ |
| TC-CLIENT-061 | Create session validates api_id | `test_create_session_invalid_api_id` | ✅ |
| TC-CLIENT-062 | Create session validates phone number format | `test_create_session_invalid_phone` | ✅ |
| TC-CLIENT-063 | Create session requires phone_number when non-interactive | `test_create_session_missing_phone_non_interactive` | ✅ |
| TC-CLIENT-064 | Create session requires api_id and api_hash | `test_create_session_missing_params` | ✅ |
| TC-CLIENT-065 | Create session handles already authorized user | `test_create_session_already_authorized` | ✅ |
| TC-CLIENT-066 | Create session disconnects client after use | `test_create_session_disconnects` | ✅ |

## Выводы

### Покрытие тест-кейсов

**MiniAppApi**:
- Всего тест-кейсов: 52 (было 37, добавлено 15 новых)
- Покрыто тестами: 52 (100%)
- Новые тест-кейсы: TC-API-050, TC-API-051, TC-API-052 (query params)

**MiniAppUI**:
- Всего тест-кейсов: 41
- Покрыто тестами: 40 (98%)
- Не покрыто: 1 (некоторые edge cases частично)

**ApiResult Methods**:
- Всего тест-кейсов: 13 (TC-MODEL-API-022 до TC-MODEL-API-034)
- Покрыто тестами: 13 (100%)

**Utility Functions**:
- Всего тест-кейсов: 17 (TC-UTILS-001 до TC-UTILS-017)
- Покрыто тестами: 17 (100%)

**UserTelegramClient Session Management**:
- Всего тест-кейсов: 14 (TC-CLIENT-053 до TC-CLIENT-066)
- Покрыто тестами: 14 (100%)

### Рекомендации

1. **TC-API-002** и **TC-UI-002**: ✅ Обновлены - теперь проверяют, что config=None вызывает ошибку. Тесты соответствуют обновленным тест-кейсам.

2. **TC-API-006**: ✅ Добавлен тест на множественные вызовы close().

3. **Ссылки на тест-кейсы**: ✅ Все тесты теперь имеют ссылки на соответствующие тест-кейсы в docstring для лучшей трассируемости.

4. **Обновление тест-кейсов**: Некоторые тесты покрывают сценарии, не описанные в тест-кейсах (например, обработка исключений для всех методов UI). Рекомендуется обновить документацию тест-кейсов для полного соответствия.
