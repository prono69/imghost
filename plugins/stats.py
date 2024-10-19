# plugins/stats.py

from pyrogram import Client, filters
from config import ADMIN_ID

async def stats_command(client: Client, message):
    if message.from_user.id == ADMIN_ID:
        # Replace these values with actual statistics
        total_users = 100  # Example: Fetch from your database
        total_uploads = 50  # Example: Fetch from your database
        
        await message.reply(
            f"**Bot Statistics:**\n"
            f"Total Users: {total_users}\n"
            f"Total Uploads: {total_uploads}",
            parse_mode="Markdown"
        )
    else:
        await message.reply("You are not authorized to use this command.")
