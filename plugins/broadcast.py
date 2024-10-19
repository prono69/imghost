# plugins/broadcast.py

from pyrogram import Client, filters
from config import ADMIN_ID

async def broadcast_command(client: Client, message):
    if message.from_user.id == ADMIN_ID:
        # Check if the message is a reply
        if message.reply_to_message:
            # Get the message to broadcast
            reply_message = message.reply_to_message
            
            # If the reply is a photo
            if reply_message.photo:
                # Forward the photo to all users
                user_ids = []  # This should be replaced with actual user IDs from your database
                for user_id in user_ids:
                    try:
                        await client.send_photo(user_id, photo=reply_message.photo.file_id, caption=reply_message.caption or "")
                    except Exception as e:
                        print(f"Failed to send message to {user_id}: {e}")

            # If the reply is a text message
            elif reply_message.text:
                broadcast_text = reply_message.text
                user_ids = []  # This should be replaced with actual user IDs from your database
                for user_id in user_ids:
                    try:
                        await client.send_message(user_id, broadcast_text)
                    except Exception as e:
                        print(f"Failed to send message to {user_id}: {e}")

            # If the reply is a document or other media, you can handle it similarly
            else:
                await message.reply("This message type is not supported for broadcasting.")
        else:
            await message.reply("Please reply to a message to broadcast it.")
    else:
        await message.reply("You are not authorized to use this command.")
