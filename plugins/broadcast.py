from pyrogram import Client, filters
from config import ADMIN_ID
from db.mongo_db import mongo_db  # Import the MongoDB instance

async def broadcast_command(client: Client, message):
    if message.from_user.id == ADMIN_ID:
        # Check if the message is a reply
        if message.reply_to_message:
            # Get the message to broadcast
            reply_message = message.reply_to_message
            
            # Fetch user IDs from the database
            user_ids = [user['user_id'] for user in mongo_db.users_collection.find({}, {"user_id": 1})]  # Assuming user_id is stored in the 'users' collection
            
            # Handle photo broadcasts
            if reply_message.photo:
                for user_id in user_ids:
                    try:
                        await client.send_photo(user_id, photo=reply_message.photo.file_id, caption=reply_message.caption or "")
                    except Exception as e:
                        print(f"Failed to send photo to {user_id}: {e}")

            # Handle text message broadcasts
            elif reply_message.text:
                broadcast_text = reply_message.text
                for user_id in user_ids:
                    try:
                        await client.send_message(user_id, broadcast_text)
                    except Exception as e:
                        print(f"Failed to send message to {user_id}: {e}")

            # Handle documents or other media types
            elif reply_message.document:
                for user_id in user_ids:
                    try:
                        await client.send_document(user_id, document=reply_message.document.file_id, caption=reply_message.caption or "")
                    except Exception as e:
                        print(f"Failed to send document to {user_id}: {e}")

            else:
                await message.reply("This message type is not supported for broadcasting.")
        else:
            await message.reply("Please reply to a message to broadcast it.")
    else:
        await message.reply("You are not authorized to use this command.")
