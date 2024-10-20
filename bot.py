import os
import json
import time
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from dotenv import load_dotenv
from handlers.photo_handler import handle_photo
from plugins.start import start_handler
from plugins.help import help_handler
from db import mongo_db  # Import your mongo_db instance for database access

# Load environment variables
load_dotenv()

# Retrieve bot credentials and admin ID from environment variables
API_ID = os.getenv('API_ID', 'your_api_id')
API_HASH = os.getenv('API_HASH', 'your_api_hash')
BOT_TOKEN = os.getenv('BOT_TOKEN', 'your_bot_token')
ADMIN_ID = int(os.getenv('ADMIN_ID', 'your_admin_id'))

# Create Pyrogram client
app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# Flask app for health check
health_app = Flask(__name__)

@health_app.route('/health', methods=['GET'])
def health_check():
    return "Bot is running", 200

def run_flask():
    health_app.run(host="0.0.0.0", port=8080)

# Run Flask server in a separate thread
Thread(target=run_flask, daemon=True).start()

# File to store user data
USER_DATA_FILE = "userdata.json"

def load_user_data():
    """Load user data from a JSON file."""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_user_data(data):
    """Save user data to a JSON file."""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Load existing user data
user_data = load_user_data()

# Photo handler
@app.on_message(filters.photo)
async def photo_handler(client: Client, message):
    await handle_photo(client, message)
    user_id = message.from_user.id
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {'uploads': 0}
        save_user_data(user_data)
    user_data[str(user_id)]['uploads'] += 1  # Increment upload count
    save_user_data(user_data)

# Start command handler
@app.on_message(filters.command("start"))
async def start_command(client: Client, message):
    await start_handler(client, message)
    user_id = message.from_user.id
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {'uploads': 0}
        save_user_data(user_data)

# Help command handler
@app.on_message(filters.command("help"))
async def help_cmd(client: Client, message):
    await help_handler(client, message)

# Return command handler
@app.on_message(filters.command("return"))
async def return_command(client: Client, message):
    await start_handler(client, message)

# Stats command handler
@app.on_message(filters.command("stats") & filters.user(ADMIN_ID))
async def stats_cmd(client: Client, message):
    try:
        total_users = len(user_data)
        total_uploads = sum(user['uploads'] for user in user_data.values())

        await message.reply(
            f"<b>Bot Statistics:</b>\n"
            f"Total Users: {total_users}\n"
            f"Total Uploads: {total_uploads}",
            parse_mode="HTML"
        )
    except Exception as e:
        await message.reply("An error occurred while fetching statistics.")
        print(f"Error fetching stats: {e}")

# Broadcast command handler
@app.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def broadcast_cmd(client: Client, message):
    if message.reply_to_message:
        reply_message = message.reply_to_message
        content = reply_message.caption if reply_message.caption else reply_message.text
        media = reply_message.photo if reply_message.photo else None
        
        await message.reply("Broadcasting message...")  # Confirmation message
        
        # Get all user IDs from user data
        user_ids = [int(user_id) for user_id in user_data.keys()]

        for user_id in user_ids:
            try:
                if media:
                    await client.send_photo(user_id, media.file_id, caption=content)
                else:
                    await client.send_message(user_id, content)
            except Exception as e:
                print(f"Failed to send message to {user_id}: {e}")

    else:
        await message.reply("Please reply to the message you want to broadcast.")

if __name__ == "__main__":
    # Add a delay before starting your bot
    time.sleep(10)

    retries = 5
    for attempt in range(retries):
        try:
            app.run()  # Start Pyrogram client
            break  # Exit loop if successful
        except Exception as e:
            print(f"Error: {e}. Attempt {attempt + 1} of {retries}")
            time.sleep(5)  # Wait before retrying
