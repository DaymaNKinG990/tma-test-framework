# Python imports
from pytest import fixture


@fixture
def valid_user_info_data() -> dict[str, int | str | bool]:
    """
    Valid user info data.

    Returns:
        dict[str, int | str | bool]: Valid user info data.
    """
    return {
        "id": 123456789,
        "first_name": "Test User",
        "username": "test_user",
        "last_name": "Test",
        "phone": "+1234567890",
        "is_bot": False,
        "is_verified": True,
        "is_premium": False,
    }


@fixture
def bot_user_info_data() -> dict[str, int | str | bool | None]:
    """
    Bot user info data.

    Returns:
        dict[str, int | str | bool | None]: Bot user info data.
    """
    return {
        "id": 987654321,
        "first_name": "Test Bot",
        "username": "test_bot",
        "last_name": None,
        "phone": None,
        "is_bot": True,
        "is_verified": False,
        "is_premium": False,
    }


@fixture
def minimal_user_info_data() -> dict[str, int | str | bool | None]:
    """
    Minimal user info data.

    Returns:
        dict[str, int | str | bool | None]: Minimal user info data.
    """
    return {
        "id": 111222333,
        "first_name": "Minimal User",
        "username": None,
        "last_name": None,
        "phone": None,
        "is_bot": False,
        "is_verified": False,
        "is_premium": False,
    }


@fixture
def edge_case_user_info_data() -> dict[str, int | str | bool]:
    """
    Edge case user info data.

    Returns:
        dict[str, int | str | bool]: Edge case user info data.
    """
    return {
        "id": 0,
        "first_name": "",
        "username": "a" * 100,
        "last_name": "a" * 100,
        "phone": "a" * 20,
        "is_bot": False,
        "is_verified": False,
        "is_premium": False,
    }


@fixture
def unicode_user_info_data() -> dict[str, int | str | bool]:
    """
    Unicode user info data.

    Returns:
        dict[str, int | str | bool]: Unicode user info data.
    """
    return {
        "id": 123456789,
        "first_name": "Тест Пользователь",
        "username": "test_用户",
        "last_name": "テスト",
        "phone": "+1234567890",
        "is_bot": False,
        "is_verified": True,
        "is_premium": False,
    }
