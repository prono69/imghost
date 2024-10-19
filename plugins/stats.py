# plugins/stats.py

from pyrogram import Client, filters
from config import ADMIN_ID
from db import mongo_db  # Import your mongo_db instance for database access

async def stats_command(client: Client, message):
    if message.from_user.id == ADMIN_ID:
        try:
            # Fetch total users and uploads from the database
            total_users = await mongo_db.get_total_users()  # Should return the count of users
            total_uploads = await mongo_db.count_uploads()  # Should return the count of uploads
            
            await message.reply(
                f"**Bot Statistics:**\n"
                f"Total Users: {total_users}\n"
                f"Total Uploads: {total_uploads}",  # Directly use the count instead of list length
                parse_mode="Markdown"
            )
        except Exception as e:
            await message.reply("An error occurred while fetching statistics.")
            print(f"Error fetching stats: {e}")  # Log the error for debugging
    else:
        await message.reply("You are not authorized to use this command.")
