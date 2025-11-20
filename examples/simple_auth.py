"""
Simple authentication example showing the difference between first run and subsequent runs.
"""

import asyncio
import os
from src.mtproto_client import UserTelegramClient
from src.config import Config


async def main():
    """Simple example showing session-based authorization."""

    # Validate required environment variables
    session_string = os.getenv("SESSION_STRING")
    api_id_str = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")

    # Check if session string is provided
    if not session_string:
        print("❌ No session string provided!")
        print(
            "Please run 'python examples/get_session.py' first to generate a session string."
        )
        return

    # Validate API_ID is present and can be parsed to int
    if not api_id_str:
        print("❌ API_ID environment variable is not set!")
        print(
            "Please set API_ID environment variable or run 'python examples/get_session.py' to configure."
        )
        return

    try:
        api_id = int(api_id_str)
    except ValueError:
        print(f"❌ API_ID must be a valid integer, got: {api_id_str}")
        print(
            "Please set a valid API_ID environment variable or run 'python examples/get_session.py' to configure."
        )
        return

    # Validate API_HASH is present
    if not api_hash:
        print("❌ API_HASH environment variable is not set!")
        print(
            "Please set API_HASH environment variable or run 'python examples/get_session.py' to configure."
        )
        return

    # All validations passed, construct Config
    print("🔄 Using session string (no authentication needed)")
    config = Config(api_id=api_id, api_hash=api_hash, session_string=session_string)

    # Use the client
    async with UserTelegramClient(config) as client:
        user = await client.get_me()
        # Normalize first_name: handle None and trim whitespace
        first_name = (user.first_name or "Unknown").strip()
        # Build display string with conditional username formatting
        if user.username:
            display_name = f"{first_name} (@{user.username})"
        else:
            display_name = f"{first_name} (no username)"
        print(f"✅ Logged in as: {display_name}")
        print("📱 Using pre-authenticated session!")


if __name__ == "__main__":
    print("TMA Framework - Simple Authentication Example")
    print("=" * 50)

    # Show what environment variables are needed
    print("\nEnvironment variables needed:")
    print("Required: API_ID, API_HASH, SESSION_STRING")
    print("Get SESSION_STRING by running: python examples/get_session.py")

    asyncio.run(main())
