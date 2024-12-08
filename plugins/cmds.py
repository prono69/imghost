import os
import time
import asyncio
from pyrogram import Client, filters
from handlers.photo_handler import handle_photo
from plugins.start import start_handler
from plugins.help import help_handler
from db.mongo_db import mongo_db
from config import ADMIN_ID, LOG_GROUP_ID
import logging

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def log_new_user(user_id, username):
    message = f"New user 😗\nId: {user_id}\nUsername: {username}\n#new_user"
    try:
        await Client.send_message(LOG_GROUP_ID, message)
    except Exception as e:
        logger.error("Error sending log message:", e)

@Client.on_message(filters.photo)
async def photo_handler(client: Client, message):
    response_data = await handle_photo(client, message)
    await mongo_db.insert_upload(response_data)

@Client.on_message(filters.command("start"))
async def start_command(client: Client, message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"

    user_data = {
        "user_id": user_id,
        "username": username,
    }
    
    try:
        existing_user = await mongo_db.users_collection.find_one({"user_id": user_id})
        
        if existing_user is None:
            await mongo_db.insert_user(user_id)
            logger.info("User data updated:", user_data)
            await log_new_user(user_id, username)
        else:
            logger.info("User already exists in the database:", user_data)

    except Exception as e:
        logger.error("Error updating user data:", e)
    
    await start_handler(client, message)

@Client.on_message(filters.command("help"))
async def help_cmd(client: Client, message):
    await help_handler(client, message)

@Client.on_message(filters.command("return"))
async def return_command(client: Client, message):
    await start_handler(client, message)

@Client.on_message(filters.command("stats") & filters.user(ADMIN_ID))
async def stats_cmd(client: Client, message):
    try:
        total_users = await mongo_db.count_users()
        total_uploads = await mongo_db.get_all_uploads()

        await message.reply(
            f"<b><i>✘ Bot Statistics:</i></b>\n\n"
            f"🙎‍♂️ **Total Users:** `{total_users}`\n"
            f"⏫ **Total Uploads:** `{len(total_uploads)}`"
        )
    except Exception as e:
        await message.reply("An error occurred while fetching statistics.")
        logger.error(f"Error fetching stats: {e}")

@Client.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def broadcast_cmd(client: Client, message):
    if message.reply_to_message:
        reply_message = message.reply_to_message
        content = reply_message.caption if reply_message.caption else reply_message.text
        media = reply_message.photo if reply_message.photo else None
        
        await message.reply("Broadcasting message...")
        
        user_ids = await mongo_db.get_all_user_ids()

        for user_id in user_ids:
            try:
                if media:
                    await client.send_photo(user_id, media.file_id, caption=content)
                else:
                    await client.send_message(user_id, content)
            except Exception as e:
                logger.error(f"Failed to send message to {user_id}: {e}")

