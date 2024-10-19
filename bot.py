import os
from pyrogram import Client, filters
from dotenv import load_dotenv
from handlers.photo_handler import handle_photo
from plugins.start import start
from plugins.help import help_command

# Load environment variables
load_dotenv()

API_ID = os.getenv('API_ID', 'your_api_id')
API_HASH = os.getenv('API_HASH', 'your_api_hash')
BOT_TOKEN = os.getenv('BOT_TOKEN', 'your_bot_token')
ADMIN_ID = os.getenv('ADMIN_ID', 'your_admin_id')  # Add your admin ID here

app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.photo)
async def photo_handler(client: Client, message):
    await handle_photo(client, message)

@app.on_message(filters.command("start"))
async def start_command(client: Client, message):
    await start(client, message)

@app.on_message(filters.command("help"))
async def help_cmd(client: Client, message):
    await help_command(client, message)

@app.on_message(filters.command("return"))
async def return_command(client: Client, message):
    await start(client, message)

@app.on_message(filters.command("stats") & filters.user(ADMIN_ID))
async def stats_command(client: Client, message):
    # Implement stats logic here
    total_users = 0  # Example: Replace with your actual logic to get total users
    await message.reply(f"Total users: {total_users}")

@app.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def broadcast_command(client: Client, message):
    # Check if the user has replied to a message
    if message.reply_to_message:
        # Get the content of the replied message
        reply_message = message.reply_to_message
        content = reply_message.caption if reply_message.caption else reply_message.text
        media = reply_message.photo if reply_message.photo else None

        # Implement broadcasting logic here
        # For example, sending the message to a specific chat or all users
        # Replace 'your_chat_id' with the actual chat ID where you want to broadcast
        # await client.send_photo(chat_id='your_chat_id', photo=media.file_id, caption=content)

        await message.reply("Broadcasting message...")  # Confirmation message
    else:
        await message.reply("Please reply to the message you want to broadcast.")

# Run the bot
if __name__ == "__main__":
    app.run()
