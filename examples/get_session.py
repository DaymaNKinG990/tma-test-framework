"""
Example of how to get a session string for TMA Framework.
This script helps you get a session string that can be used in your application.
"""

import asyncio
import getpass
import re
from telethon import TelegramClient
from telethon.sessions import StringSession


async def get_session_string():
    """Get session string for TMA Framework."""

    print("TMA Framework - Session String Generator")
    print("=" * 50)
    print("This script will help you get a session string for TMA Framework.")
    print("You need to authenticate once to get the session string.")
    print()

    # Get API credentials
    api_id = input("Enter your API ID: ").strip()
    api_hash = getpass.getpass("Enter your API Hash: ").strip()
    phone_number = input(
        "Enter your phone number (with country code, e.g., +1234567890): "
    ).strip()

    # Validate API ID: must be a positive integer
    if not api_id:
        print("❌ API ID is required!")
        return

    try:
        api_id_int = int(api_id)
        if api_id_int <= 0:
            print("❌ API ID must be a positive number!")
            return
        # Use api_id_int for client creation
    except ValueError:
        print("❌ API ID must be a valid number!")
        return

    # Validate API Hash: must be non-empty after stripping
    if not api_hash:
        print("❌ API Hash is required!")
        return

    # Validate phone number: must match regex pattern
    phone_pattern = r"^\+\d{7,15}$"
    if not phone_number:
        print("❌ Phone number is required!")
        return

    if not re.match(phone_pattern, phone_number):
        print(
            "❌ Invalid phone number format! Must start with + and contain 7-15 digits (e.g., +1234567890)"
        )
        return

    # Create client with StringSession
    session = StringSession()
    client = TelegramClient(session, api_id_int, api_hash)

    try:
        # Connect and authenticate
        await client.connect()
        print("✅ Connected to Telegram")

        if not await client.is_user_authorized():
            print("🔐 Authenticating...")
            await client.send_code_request(phone_number)
            code = getpass.getpass("Enter the verification code: ").strip()

            try:
                await client.sign_in(phone_number, code)
                print("✅ Successfully authenticated!")
            except Exception as e:
                if "password" in str(e).lower():
                    password = getpass.getpass("Enter your 2FA password: ").strip()
                    await client.sign_in(password=password)
                    print("✅ Successfully authenticated with 2FA!")
                else:
                    print(f"❌ Authentication failed: {e}")
                    return
        else:
            print("✅ Already authenticated!")

        # Get session string
        session_string = client.session.save()

        print("\n" + "=" * 50)
        print("🎉 SUCCESS! Your session string:")
        print("=" * 50)
        print(session_string)
        print("=" * 50)
        print()
        print("📝 How to use this session string:")
        print("1. Save this string securely")
        print("2. Use it in your TMA Framework config:")
        print()
        print("```python")
        print(
            "from tma_test_framework.clients.mtproto_client import UserTelegramClient"
        )
        print("from tma_test_framework.config import Config")
        print()
        print("config = Config(")
        print(f"    api_id={api_id},")
        print("    api_hash='***',  # Replace with your actual API hash")
        print(f"    session_string='{session_string}'")
        print(")")
        print()
        print("async with UserTelegramClient(config) as client:")
        print("    user = await client.get_me()")
        print("    print(f'Logged in as: {user.first_name}')")
        print("```")
        print()
        print(
            "🔒 Keep this session string secure - it provides access to your Telegram account!"
        )

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.disconnect()


async def main():
    """Main function."""
    try:
        await get_session_string()
    except KeyboardInterrupt:
        print("\n👋 Cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
