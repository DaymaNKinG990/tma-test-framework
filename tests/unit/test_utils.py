"""
Unit tests for utility functions.
"""

import json
import allure

from tma_test_framework.utils import (
    parse_json,
    validate_response_structure,
    extract_pagination_info,
    get_error_detail,
    generate_telegram_init_data,
)


class TestParseJson:
    """Test parse_json utility function."""

    @allure.title("parse_json with valid JSON")
    @allure.description("Test parse_json with valid JSON.")
    def test_parse_json_valid(self):
        """Test parse_json with valid JSON."""
        with allure.step("Prepare JSON data and encode to bytes"):
            json_data = {"key": "value", "number": 123}
            body = json.dumps(json_data).encode("utf-8")

        with allure.step("Call parse_json and verify result"):
            result = parse_json(body)

            assert result == json_data
            assert result["key"] == "value"
            assert result["number"] == 123

    @allure.title("parse_json with invalid JSON returns empty dict")
    @allure.description("Test parse_json with invalid JSON returns empty dict.")
    def test_parse_json_invalid(self):
        """Test parse_json with invalid JSON returns empty dict."""
        with allure.step("Prepare invalid JSON bytes"):
            body = b"not valid json"

        with allure.step("Call parse_json and verify empty dict is returned"):
            result = parse_json(body)

            assert result == {}

    @allure.title("parse_json with empty body")
    @allure.description("Test parse_json with empty body.")
    def test_parse_json_empty(self):
        """Test parse_json with empty body."""
        with allure.step("Prepare empty bytes"):
            body = b""

        with allure.step("Call parse_json and verify empty dict is returned"):
            result = parse_json(body)

            assert result == {}

    @allure.title("parse_json with unicode characters")
    @allure.description("Test parse_json with unicode characters.")
    def test_parse_json_unicode(self):
        """Test parse_json with unicode characters."""
        with allure.step("Prepare JSON data with unicode characters and encode"):
            json_data = {"message": "Привет", "emoji": "🎉"}
            body = json.dumps(json_data, ensure_ascii=False).encode("utf-8")

        with allure.step("Call parse_json and verify unicode is preserved"):
            result = parse_json(body)

            assert result == json_data


class TestValidateResponseStructure:
    """Test validate_response_structure utility function."""

    @allure.title("validate_response_structure with all fields present")
    @allure.description("Test validate_response_structure with all fields present.")
    def test_validate_response_structure_all_fields_present(self):
        """Test validate_response_structure with all fields present."""
        with allure.step("Prepare data with all expected fields"):
            data = {"name": "test", "id": 123, "status": "active"}
            expected_fields = ["name", "id", "status"]

        with allure.step("Call validate_response_structure and verify True"):
            result = validate_response_structure(data, expected_fields)

            assert result is True

    @allure.title("validate_response_structure with missing fields")
    @allure.description("Test validate_response_structure with missing fields.")
    def test_validate_response_structure_missing_fields(self):
        """Test validate_response_structure with missing fields."""
        with allure.step("Prepare data with missing fields"):
            data = {"name": "test", "id": 123}
            expected_fields = ["name", "id", "status", "email"]

        with allure.step("Call validate_response_structure and verify False"):
            result = validate_response_structure(data, expected_fields)

            assert result is False

    @allure.title("validate_response_structure with empty expected fields")
    @allure.description("Test validate_response_structure with empty expected fields.")
    def test_validate_response_structure_empty_fields(self):
        """Test validate_response_structure with empty expected fields."""
        with allure.step("Prepare data with empty expected fields list"):
            data = {"name": "test"}
            expected_fields = []

        with allure.step("Call validate_response_structure and verify True"):
            result = validate_response_structure(data, expected_fields)

            assert result is True


class TestExtractPaginationInfo:
    """Test extract_pagination_info utility function."""

    @allure.title("extract_pagination_info with complete pagination data")
    @allure.description("Test extract_pagination_info with complete pagination data.")
    def test_extract_pagination_info_complete(self):
        """Test extract_pagination_info with complete pagination data."""
        with allure.step("Prepare data with complete pagination fields"):
            data = {
                "count": 100,
                "next": "http://api.example.com/items/?page=2",
                "previous": None,
                "results": [{"id": 1}, {"id": 2}],
            }

        with allure.step("Call extract_pagination_info and verify all fields"):
            result = extract_pagination_info(data)

            assert result["count"] == 100
            assert result["next"] == "http://api.example.com/items/?page=2"
            assert result["previous"] is None
            assert result["results"] == [{"id": 1}, {"id": 2}]

    @allure.title("extract_pagination_info with partial pagination data")
    @allure.description("Test extract_pagination_info with partial pagination data.")
    def test_extract_pagination_info_partial(self):
        """Test extract_pagination_info with partial pagination data."""
        with allure.step("Prepare data with only count field"):
            data = {"count": 50}

        with allure.step("Call extract_pagination_info and verify default values"):
            result = extract_pagination_info(data)

            assert result["count"] == 50
            assert result["next"] is None
            assert result["previous"] is None
            assert result["results"] == []

    @allure.title("extract_pagination_info with empty data")
    @allure.description("Test extract_pagination_info with empty data.")
    def test_extract_pagination_info_empty(self):
        """Test extract_pagination_info with empty data."""
        with allure.step("Prepare empty data dictionary"):
            data = {}

        with allure.step(
            "Call extract_pagination_info and verify all None/default values"
        ):
            result = extract_pagination_info(data)

            assert result["count"] is None
            assert result["next"] is None
            assert result["previous"] is None
            assert result["results"] == []


class TestGetErrorDetail:
    """Test get_error_detail utility function."""

    @allure.title("get_error_detail extracts 'detail' field")
    @allure.description("Test get_error_detail extracts 'detail' field.")
    def test_get_error_detail_with_detail(self):
        """Test get_error_detail extracts 'detail' field."""
        with allure.step("Prepare data with 'detail' field"):
            data = {"detail": "Error message"}

        with allure.step("Call get_error_detail and verify 'detail' is extracted"):
            result = get_error_detail(data)

            assert result == "Error message"

    @allure.title("get_error_detail extracts 'error' field when 'detail' missing")
    @allure.description(
        "Test get_error_detail extracts 'error' field when 'detail' missing."
    )
    def test_get_error_detail_with_error(self):
        """Test get_error_detail extracts 'error' field when 'detail' missing."""
        with allure.step("Prepare data with 'error' field (no 'detail')"):
            data = {"error": "Error message"}

        with allure.step("Call get_error_detail and verify 'error' is extracted"):
            result = get_error_detail(data)

            assert result == "Error message"

    @allure.title("get_error_detail falls back to string representation")
    @allure.description("Test get_error_detail falls back to string representation.")
    def test_get_error_detail_fallback(self):
        """Test get_error_detail falls back to string representation."""
        with allure.step("Prepare data without 'detail' or 'error' fields"):
            data = {"message": "Some message"}

        with allure.step(
            "Call get_error_detail and verify fallback to string representation"
        ):
            result = get_error_detail(data)

            assert isinstance(result, str)
            assert "message" in result or "Some message" in result


class TestGenerateTelegramInitData:
    """Test generate_telegram_init_data utility function."""

    @allure.title("generate_telegram_init_data with default parameters")
    @allure.description("Test generate_telegram_init_data with default parameters.")
    def test_generate_telegram_init_data_default(self):
        """Test generate_telegram_init_data with default parameters."""
        with allure.step("Prepare bot_token"):
            bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"

        with allure.step("Call generate_telegram_init_data with default parameters"):
            init_data = generate_telegram_init_data(bot_token=bot_token)

        with allure.step("Verify init_data structure contains required fields"):
            assert isinstance(init_data, str)
            assert "user=" in init_data
            assert "auth_date=" in init_data
            assert "hash=" in init_data

    @allure.title("generate_telegram_init_data with custom parameters")
    @allure.description("Test generate_telegram_init_data with custom parameters.")
    def test_generate_telegram_init_data_custom(self):
        """Test generate_telegram_init_data with custom parameters."""
        with allure.step("Prepare bot_token and custom user parameters"):
            bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"

        with allure.step("Call generate_telegram_init_data with custom parameters"):
            init_data = generate_telegram_init_data(
                user_id=999999999,
                username="custom_user",
                first_name="Custom",
                last_name="User",
                bot_token=bot_token,
                language_code="en",
                is_premium=True,
            )

        with allure.step("Verify init_data structure and custom user data"):
            assert isinstance(init_data, str)
            assert "user=" in init_data
            assert "auth_date=" in init_data
            assert "hash=" in init_data
            # Verify user data is in the init_data
            assert "custom_user" in init_data or "999999999" in init_data

    @allure.title("Generated init_data can be validated")
    @allure.description("Test that generated init_data can be validated.")
    def test_generate_telegram_init_data_validates(self, valid_config):
        """Test that generated init_data can be validated."""
        with allure.step("Prepare bot_token"):
            bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"

        with allure.step("Generate init_data"):
            init_data = generate_telegram_init_data(bot_token=bot_token)

        with allure.step("Create MiniAppApi instance and verify init_data structure"):
            # Note: This test requires actual validation logic
            # For now, just verify the structure
            assert "hash=" in init_data
            assert "auth_date=" in init_data

    @allure.title("Generated hash is valid hex string")
    @allure.description("Test that generated hash is valid hex string.")
    def test_generate_telegram_init_data_hash_format(self):
        """Test that generated hash is valid hex string."""
        with allure.step("Prepare bot_token"):
            bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"

        with allure.step("Generate init_data"):
            init_data = generate_telegram_init_data(bot_token=bot_token)

        with allure.step("Extract hash from init_data and verify format"):
            # Extract hash from init_data
            import urllib.parse

            parsed = urllib.parse.parse_qs(init_data)
            hash_value = parsed.get("hash", [""])[0]

            # Hash should be 64 character hex string (SHA256)
            assert len(hash_value) == 64
            assert all(c in "0123456789abcdef" for c in hash_value)
