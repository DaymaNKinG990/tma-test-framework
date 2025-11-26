"""
Error handling examples for TMA Framework.
Shows proper error handling for authentication and configuration.
"""

import asyncio
import os
from tma_test_framework.clients.mtproto_client import UserTelegramClient
from tma_test_framework.config import Config


async def test_invalid_credentials():
    """Test with invalid credentials."""
    print("=== Testing Invalid Credentials ===")

    try:
        config = Config(
            api_id=12345,  # Invalid
            api_hash="invalid_hash",  # Invalid
            session_string="dummy_session",
        )

        async with UserTelegramClient(config) as client:
            await client.get_me()

    except ValueError as e:
        print(f"✅ Expected error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def test_missing_session():
    """Test without session when no session exists."""
    print("\n=== Testing Missing Session ===")

    try:
        config = Config(
            api_id=int(os.getenv("API_ID", "12345")),
            api_hash=os.getenv("API_HASH", "your_api_hash"),
            # session_string and session_file not provided
        )

        async with UserTelegramClient(config) as client:
            await client.get_me()

    except ValueError as e:
        print(f"✅ Expected error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def test_missing_api_credentials():
    """Test without API credentials."""
    print("\n=== Testing Missing API Credentials ===")

    try:
        _ = Config(  # type: ignore[call-arg]
            # api_id and api_hash not provided
            session_string="some_session_string"
        )

    except ValueError as e:
        print(f"✅ Expected error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def test_environment_variables():
    """Test environment variable loading."""
    print("\n=== Testing Environment Variables ===")

    # Clear environment variables
    old_api_id = os.environ.pop("TMA_API_ID", None)
    old_api_hash = os.environ.pop("TMA_API_HASH", None)

    try:
        _ = Config.from_env()

    except ValueError as e:
        print(f"✅ Expected error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        # Restore environment variables
        if old_api_id is not None:
            os.environ["TMA_API_ID"] = old_api_id
        if old_api_hash is not None:
            os.environ["TMA_API_HASH"] = old_api_hash


def test_valid_configuration():
    """Test with valid configuration."""
    print("\n=== Testing Valid Configuration ===")

    try:
        config = Config(
            api_id=int(os.getenv("API_ID", "12345")),
            api_hash=os.getenv("API_HASH", "your_api_hash"),
            session_string=os.getenv("SESSION_STRING", "test_session_string"),
        )

        print("✅ Configuration created successfully")
        # Note: Printing API hashes in examples is for demo only and should not be done in production
        print(f"API ID: {config.api_id}")
        print(f"API Hash: {config.api_hash}")
        # Check for None before slicing to avoid AttributeError
        session_display = (
            config.session_string[:20] + "..."
            if config.session_string is not None
            else "<none>"
        )
        print(f"Session string: {session_display}")

    except ValueError as e:
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def main():
    """Run all error handling tests."""
    print("TMA Framework - Error Handling Examples")
    print("=" * 50)

    await test_missing_api_credentials()
    await test_missing_session()
    await test_invalid_credentials()
    test_environment_variables()
    test_valid_configuration()

    print("\n" + "=" * 50)
    print("Error handling tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
