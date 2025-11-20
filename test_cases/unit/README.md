# Unit Test Cases Documentation

This directory contains detailed test case specifications for all unit tests in the TMA Framework.

## Structure

Each module has its own test case documentation file:

- `config.md` - Configuration management (Config class)
- `mini_app_base.md` - Base Mini App class (BaseMiniApp)
- `mini_app_api.md` - Mini App API client (MiniAppApi)
- `mini_app_models.md` - Data models (MiniAppInfo, ApiResult)
- `mini_app_ui.md` - Mini App UI client (MiniAppUI)
- `mtproto_client.md` - MTProto client and models (UserTelegramClient, UserInfo, ChatInfo, MessageInfo)

## Test Case Format

Each test case includes:
- **Test Name**: Descriptive name of the test
- **Purpose**: What the test verifies
- **Preconditions**: Required setup before test execution
- **Test Steps**: Detailed steps to execute
- **Expected Result**: Expected outcome
- **Coverage**: Which code paths/methods are covered

## Coverage Goals

- **100% code coverage** for all modules
- **All edge cases** covered
- **Error handling** paths tested
- **Boundary conditions** verified
- **Type validation** tested
