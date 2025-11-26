"""
Example: Using only MiniAppApi for Telegram WebApp API testing.

This example demonstrates how to use MiniAppApi class independently
for testing Telegram WebApp API functionality.
"""

import asyncio
import os
from tma_test_framework.clients.api_client import ApiClient as MiniAppApi
from tma_test_framework.config import Config


async def test_mini_app_api_only():
    """Test Mini App using only API functionality."""

    # Create config
    config = Config(
        api_id=int(os.getenv("TMA_API_ID", "12345678")),
        api_hash=os.getenv("TMA_API_HASH", "0123456789abcdef0123456789abcdef"),
        session_string=os.getenv("TMA_SESSION_STRING"),
        log_level="INFO",
    )
    bot_token = os.getenv("TMA_BOT_TOKEN", "123456789:ABCdefGHIjklMNOpqrsTUVwxyz")

    # Initialize API client
    api = MiniAppApi("https://example.com/mini-app", config)

    try:
        print("=== MiniAppApi Testing ===")

        # 1. Test HTTP API endpoints
        print("\n1. Testing HTTP API endpoints...")

        # Test GET endpoint
        get_result = await api.make_request("/api/status", "GET")
        print(
            f"   GET /api/status: {'[OK]' if get_result.success else '[ERROR]'} "
            f"({get_result.status_code}) - {get_result.response_time:.3f}s"
        )

        # Test POST endpoint
        post_result = await api.make_request(
            "/api/data",
            "POST",
            data={"key": "value"},
            headers={"Content-Type": "application/json"},
        )
        print(
            f"   POST /api/data: {'[OK]' if post_result.success else '[ERROR]'} "
            f"({post_result.status_code}) - {post_result.response_time:.3f}s"
        )

        # 2. Validate initData (example)
        print("\n2. Testing initData validation...")
        sample_init_data = "user=%7B%22id%22%3A123%2C%22first_name%22%3A%22Test%22%7D&auth_date=1234567890&hash=test_hash"
        is_valid = await api.validate_init_data(sample_init_data, bot_token)
        print(
            f"   InitData validation: {'[OK] Valid' if is_valid else '[ERROR] Invalid'}"
        )

        print("\n=== API Testing Complete ===")

    except Exception as e:
        print(f"[ERROR] Error during API testing: {e}")

    finally:
        # Clean up
        await api.close()


async def test_api_with_context_manager():
    """Test MiniAppApi using context manager."""

    config = Config(
        api_id=int(os.getenv("TMA_API_ID", "12345678")),
        api_hash=os.getenv("TMA_API_HASH", "0123456789abcdef0123456789abcdef"),
        session_string=os.getenv("TMA_SESSION_STRING"),
        log_level="INFO",
    )

    print("\n=== Context Manager Testing ===")

    async with MiniAppApi("https://example.com/mini-app", config) as api:
        # Quick API test
        result = await api.make_request("/api/health", "GET")
        print(
            f"Health check: {'[OK]' if result.success else '[ERROR]'} "
            f"({result.status_code}) - {result.response_time:.3f}s"
        )

    print("Context manager cleanup completed")


async def main():
    """Main function to run all examples."""
    print("MiniAppApi Examples")
    print("==================")

    # Run API-only testing
    await test_mini_app_api_only()

    # Run context manager testing
    await test_api_with_context_manager()

    print("\nAll examples completed!")


if __name__ == "__main__":
    asyncio.run(main())
