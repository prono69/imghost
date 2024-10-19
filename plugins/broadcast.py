# plugins/broadcast.py

from pyrogram import Client, filters
from config import ADMIN_ID

async def broadcast_command(client: Client, message):
    if message.from_user.id == ADMIN_ID:
        # Get the message content to broadcast
        content = message.text.split(None, 1)
        if len(content) < 2:
            await message.reply("Please provide a message to broadcast.")
            return

        broadcast_message = content[1]
        # Here you should implement the logic to send the message to your users or groups
        # For demonstration, we are just sending a confirmation
        await message.reply(f"Broadcasting the message: {broadcast_message}")
        
        # Example: Loop through a list of user IDs and send the broadcast message
        user_ids = []  # This should be replaced with actual user IDs from your database
        for user_id in user_ids:
            try:
                await client.send_message(user_id, broadcast_message)
            except Exception as e:
                print(f"Failed to send message to {user_id}: {e}")
    else:
        await message.reply("You are not authorized to use this command.")
