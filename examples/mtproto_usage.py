"""
Example usage of TMA Framework with MTProto user client.
Demonstrates full user simulation capabilities.

REQUIREMENTS FOR ACTIVATION:
1. Get API credentials from https://my.telegram.org:
   - Go to "API development tools"
   - Create new application
   - Copy api_id and api_hash

2. Get session string (one-time setup):
   - Run: python examples/get_session.py
   - Enter your API credentials and phone number
   - Complete authentication (SMS code + 2FA if needed)
   - Copy the generated session string

3. Environment variables:
   export API_ID="your_api_id"
   export API_HASH="your_api_hash"
   export SESSION_STRING="your_session_string"

4. Usage:
   - No authentication needed - just use the session string
   - Session string provides full access to your Telegram account
"""

import asyncio
import os
from src.mtproto_client import UserTelegramClient
from src.config import Config


async def main():
    """Example of using TMA Framework for full user simulation."""

    # Configuration with session string
    config = Config(
        api_id=int(os.getenv("API_ID", "12345")),
        api_hash=os.getenv("API_HASH", "your_api_hash"),
        session_string=os.getenv("SESSION_STRING", "your_session_string"),
    )

    # Initialize TMA Framework client
    async with UserTelegramClient(config) as client:
        # Get current user info
        me = await client.get_me()
        print(f"Logged in as: {me.first_name} (@{me.username})")

        # Example 1: Interact with a bot
        bot_username = "example_bot"  # Replace with actual bot username

        try:
            # Send /start command to bot
            response = await client.interact_with_bot(
                bot_username=bot_username,
                command="/start",
                wait_for_response=True,
                timeout=30,
            )

            if response:
                print(f"Bot response: {response.text}")
            else:
                print("No response from bot")

        except Exception as e:
            print(f"Error interacting with bot: {e}")

        # Example 2: Get Mini App from bot
        try:
            mini_app = await client.get_mini_app_from_bot(
                bot_username=bot_username, start_param="test_param"
            )

            if mini_app:
                print(f"Mini App URL: {mini_app.url}")
                # Now you can interact with the Mini App
                # mini_app.open_in_browser()
            else:
                print("No Mini App found")

        except Exception as e:
            print(f"Error getting Mini App: {e}")

        # Example 3: Send message to another user/chat
        try:
            # Send message to yourself (saved messages)
            message = await client.send_message(
                entity="me",  # or use username/phone/ID
                text="Hello from TMA Framework!",
            )
            print(f"Message sent with ID: {message.id}")

        except Exception as e:
            print(f"Error sending message: {e}")

        # Example 4: Get messages from a chat
        try:
            messages = await client.get_messages(
                entity="me",  # or use username/phone/ID
                limit=5,
            )

            print(f"Last {len(messages)} messages:")
            for msg in messages:
                print(f"- {msg.date}: {msg.text}")

        except Exception as e:
            print(f"Error getting messages: {e}")

        # Example 5: Get entity information
        try:
            entity_info = await client.get_entity("me")
            if hasattr(entity_info, "first_name"):  # UserInfo
                print(
                    f"Entity info: {entity_info.first_name} (@{entity_info.username})"
                )
            else:  # ChatInfo
                print(f"Entity info: {entity_info.title} (@{entity_info.username})")

        except Exception as e:
            print(f"Error getting entity info: {e}")

        # Example 6: Event handling (optional)
        def message_handler(event):
            """Handle incoming messages."""
            print(f"New message: {event.text}")

        # Add event handler
        client.add_event_handler(message_handler)

        # Start listening (this will run indefinitely)
        # Uncomment to start listening for messages
        # await client.start_listening()


async def session_management_example():
    """Example of session management for MTProto."""

    # First time: authenticate and save session
    config = Config(
        api_id=int(os.getenv("TMA_API_ID", "12345")),
        api_hash=os.getenv("TMA_API_HASH", "your_api_hash"),
        session_string=os.getenv("TMA_SESSION_STRING"),
        session_file="my_session.session",  # Save to file
    )

    async with UserTelegramClient(config) as client:
        # After first authentication, session is saved
        me = await client.get_me()
        print(f"Session saved for: {me.first_name}")

    # Later: use saved session
    config_with_session = Config(
        api_id=int(os.getenv("TMA_API_ID", "12345")),
        api_hash=os.getenv("TMA_API_HASH", "your_api_hash"),
        session_file="my_session.session",  # Load from file
    )

    async with UserTelegramClient(config_with_session) as client:
        # No need to authenticate again
        me = await client.get_me()
        print(f"Logged in with saved session: {me.first_name}")


if __name__ == "__main__":
    # Run the main example
    asyncio.run(main())
