# bot.py

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

app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.photo)
async def photo_handler(client: Client, message):
    await handle_photo(client, message)

@app.on_message(filters.command("start"))
async def start_command(client: Client, message):
    await start(client, message)

@app.on_message(filters.command("help"))
async def help_command(client: Client, message):
    await help_command(client, message)

@app.on_message(filters.command("return"))
async def return_command(client: Client, message):
    await start(client, message)

# Run the bot
app.run()
