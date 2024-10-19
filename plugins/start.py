# plugins/start.py

from pyrogram import Client, filters
from config import BOT_IMAGE_URL  # Import the BOT_IMAGE_URL from config.py

async def start_handler(client: Client, message):  # Change this to start_handler
    # Use the bot's image URL from config.py
    bot_image_url = BOT_IMAGE_URL

    # Inline buttons
    buttons = [
        [
            ("Updates", "https://t.me/Thealphabotz"),
            ("Support", "https://t.me/thealphabotz")
        ],
        [
            ("Help", "help"),
            ("Source", "https://github.com/utkarshdubey2008/imagehost")
        ]
    ]
    
    # Send the message with the image and buttons
    await message.reply_photo(
        photo=bot_image_url,
        caption=(
            "Welcome to ImageHost Bot! Send me an image, and I'll upload it for you.\n\n"
            "I can help you host your images and provide you with a shareable link.\n"
            "Feel free to reach out if you have any questions!"
        ),
        reply_markup={"inline_keyboard": buttons}
    )
