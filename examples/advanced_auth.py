"""
Advanced authentication example for TMA Framework.
Demonstrates session-based authorization with proper error handling.
"""

import asyncio
import os
import sys
import traceback
from tma_test_framework.clients.mtproto_client import UserTelegramClient
from tma_test_framework.config import Config

# Import telethon authorization-related exceptions
try:
    from telethon.errors import (
        SessionPasswordNeededError,
        AuthKeyUnregisteredError,
        AuthKeyInvalidError,
        SessionRevokedError,
        UserDeactivatedError,
        PhoneNumberInvalidError,
    )
except ImportError:
    # Fallback if telethon is not available
    SessionPasswordNeededError = type("SessionPasswordNeededError", (Exception,), {})
    AuthKeyUnregisteredError = type("AuthKeyUnregisteredError", (Exception,), {})
    AuthKeyInvalidError = type("AuthKeyInvalidError", (Exception,), {})
    SessionRevokedError = type("SessionRevokedError", (Exception,), {})
    UserDeactivatedError = type("UserDeactivatedError", (Exception,), {})
    PhoneNumberInvalidError = type("PhoneNumberInvalidError", (Exception,), {})


def get_required_env(var_name: str) -> str:
    """Get required environment variable or raise clear error."""
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(
            f"Required environment variable '{var_name}' is not set. "
            f"Please set it before running this script."
        )
    return value


async def step_by_step_auth():
    """Step-by-step session-based authorization process."""

    # Validate required environment variables
    api_id_str = get_required_env("TMA_API_ID")
    api_hash = get_required_env("TMA_API_HASH")
    session_string = get_required_env("TMA_SESSION_STRING")

    # Configuration with session string
    config = Config(
        api_id=int(api_id_str), api_hash=api_hash, session_string=session_string
    )

    try:
        # Step 1: Initialize client
        print("Step 1: Initializing client...")
        async with UserTelegramClient(config) as client:
            # Step 2: Check authorization
            print("Step 2: Checking authorization...")
            user = await client.get_me()
            print("✅ Successfully authorized!")
            print(f"Logged in as: {user.first_name} (@{user.username})")

            # Step 3: Test basic functionality
            print("Step 3: Testing basic functionality...")
            message = await client.send_message("me", "Hello from TMA Framework!")
            print(f"Message sent with ID: {message.id}")

    except ValueError as e:
        error_msg = str(e)
        # Check if ValueError is actually an authorization error
        if "not authorized" in error_msg.lower() or "session" in error_msg.lower():
            print(f"❌ Authorization failed: {e}")
            print(
                "Please run 'python examples/get_session.py' to generate a valid session string."
            )
        else:
            print(f"❌ Configuration error: {e}")
            print("Please check your API credentials and session string.")
    except (
        SessionPasswordNeededError,
        AuthKeyUnregisteredError,
        AuthKeyInvalidError,
        SessionRevokedError,
        UserDeactivatedError,
        PhoneNumberInvalidError,
    ) as e:
        # Authorization-specific errors from telethon
        print(f"❌ Authorization failed: {e}")
        print(
            "Please run 'python examples/get_session.py' to generate a valid session string."
        )
    except (ConnectionError, TimeoutError, OSError) as e:
        # Network/connection errors
        print(f"❌ Network error: {e}")
        print("Full error details:")
        traceback.print_exc()
        raise
    except Exception as e:
        # Other runtime errors - log full traceback for debugging
        print(f"❌ Runtime error: {type(e).__name__}: {e}")
        print("Full error traceback:")
        traceback.print_exc()
        raise


async def interactive_auth():
    """Interactive session-based authorization with retry logic."""

    try:
        # Validate required environment variables
        api_id_str = get_required_env("TMA_API_ID")
        api_hash = get_required_env("TMA_API_HASH")
        session_string = get_required_env("TMA_SESSION_STRING")

        config = Config(
            api_id=int(api_id_str), api_hash=api_hash, session_string=session_string
        )

        try:
            async with UserTelegramClient(config) as client:
                print("✅ Successfully authorized!")
                user = await client.get_me()
                print(f"Logged in as: {user.first_name} (@{user.username})")

                # Test basic functionality
                print("\nTesting basic functionality...")

                # Send message to yourself
                message = await client.send_message("me", "Hello from TMA Framework!")
                print(f"Message sent with ID: {message.id}")

                # Get recent messages
                messages = await client.get_messages("me", limit=3)
                print(f"Recent messages: {len(messages)}")
                for msg in messages:
                    # Handle messages without text (media/service/deleted messages)
                    text = msg.text or "<no text>"
                    print(f"- {text}")
        except (ConnectionError, TimeoutError, OSError) as e:
            print(f"❌ Network error during authorization: {e}")
            print(f"Error type: {type(e).__name__}")
            print("\nFull traceback:")
            traceback.print_exc()
            return False
        except (
            SessionPasswordNeededError,
            AuthKeyUnregisteredError,
            AuthKeyInvalidError,
            SessionRevokedError,
            UserDeactivatedError,
            PhoneNumberInvalidError,
        ) as e:
            print(f"❌ Authorization-specific error during authorization: {e}")
            print(f"Error type: {type(e).__name__}")
            print("\nFull traceback:")
            traceback.print_exc()
            print(
                "Please run 'python examples/get_session.py' to generate a valid session string."
            )
            return False
        except ValueError as e:
            print(f"❌ Configuration error during authorization: {e}")
            print(f"Error type: {type(e).__name__}")
            print("\nFull traceback:")
            traceback.print_exc()
            return False
        except Exception as e:
            print(f"❌ Unexpected error during authorization: {e}")
            print(f"Error type: {type(e).__name__}")
            print("\nFull traceback:")
            traceback.print_exc()
            return False
    except ValueError as e:
        error_msg = str(e)
        # Check if ValueError is actually an authorization error
        if "not authorized" in error_msg.lower() or "session" in error_msg.lower():
            print(f"❌ Authorization failed: {e}")
            print(
                "Please run 'python examples/get_session.py' to generate a valid session string."
            )
        else:
            print(f"❌ Configuration error: {e}")
            print("Please check your API credentials and session string.")
        return False
    except (
        SessionPasswordNeededError,
        AuthKeyUnregisteredError,
        AuthKeyInvalidError,
        SessionRevokedError,
        UserDeactivatedError,
        PhoneNumberInvalidError,
    ) as e:
        # Authorization-specific errors from telethon
        print(f"❌ Authorization failed: {e}")
        print(
            "Please run 'python examples/get_session.py' to generate a valid session string."
        )
        return False
    except (ConnectionError, TimeoutError, OSError) as e:
        # Network/connection errors
        print(f"❌ Network error: {e}")
        print("Full error details:")
        traceback.print_exc()
        return False
    except Exception as e:
        # Other runtime errors - log full traceback for debugging
        print(f"❌ Runtime error: {type(e).__name__}: {e}")
        print("Full error traceback:")
        traceback.print_exc()
        return False

    return True


async def session_management_demo():
    """Demonstrate session management."""

    # Validate required environment variables
    api_id_str = get_required_env("TMA_API_ID")
    api_hash = get_required_env("TMA_API_HASH")
    session_string = get_required_env("TMA_SESSION_STRING")

    # Using session string
    print("=== Using session string ===")
    config = Config(
        api_id=int(api_id_str), api_hash=api_hash, session_string=session_string
    )

    async with UserTelegramClient(config) as client:
        user = await client.get_me()
        print(f"Logged in with session string: {user.first_name}")
        print("✅ No authentication required!")

    # Using session file
    print("\n=== Using session file ===")
    config_with_file = Config(
        api_id=int(api_id_str), api_hash=api_hash, session_file="demo_session.session"
    )

    async with UserTelegramClient(config_with_file) as client:
        user = await client.get_me()
        print(f"Logged in with session file: {user.first_name}")
        print("✅ Using cached session credentials — no re-authentication required")


async def error_handling_demo():
    """Demonstrate proper error handling."""

    # Validate required environment variables
    api_id_str = get_required_env("TMA_API_ID")
    api_hash = get_required_env("TMA_API_HASH")
    session_string = get_required_env("TMA_SESSION_STRING")

    config = Config(
        api_id=int(api_id_str), api_hash=api_hash, session_string=session_string
    )

    try:
        async with UserTelegramClient(config) as client:
            print("✅ Authorization successful!")

            # Test with invalid entity
            try:
                await client.get_entity("nonexistent_user_12345")
            except Exception as e:
                print(f"Expected error for invalid entity: {e}")

            # Test sending message to invalid user
            try:
                await client.send_message("invalid_user", "Test message")
            except Exception as e:
                print(f"Expected error for invalid user: {e}")

    except ValueError as e:
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    print("TMA Framework - Advanced Authentication Examples")
    print("=" * 50)

    # Choose example to run
    examples = {
        "1": ("Step-by-step authorization", step_by_step_auth),
        "2": ("Interactive authorization", interactive_auth),
        "3": ("Session management demo", session_management_demo),
        "4": ("Error handling demo", error_handling_demo),
    }

    print("Available examples:")
    for key, (name, _) in examples.items():
        print(f"{key}. {name}")

    choice = input("\nChoose example (1-4): ").strip()

    if choice in examples:
        name, func = examples[choice]
        print(f"\nRunning: {name}")
        print("-" * 30)
        result = asyncio.run(func())
        if result is False:
            print(
                "\n❌ The example encountered an error and may not have completed successfully."
            )
            sys.exit(1)
    else:
        print("Invalid choice. Running interactive authorization...")
        result = asyncio.run(interactive_auth())
        if result is False:
            print("\n❌ Error during interactive authorization.")
            print("The program encountered an error and will exit.")
            sys.exit(1)
