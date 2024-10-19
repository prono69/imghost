from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
from config import BOT_IMAGE_URL

async def start_handler(client: Client, message):
    bot_image_url = BOT_IMAGE_URL
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
    
    reply_markup = InlineKeyboardMarkup(buttons)

    await message.reply_photo(
        photo=bot_image_url,
        caption=(
            "Welcome to ImageHost Bot! Send me an image, and I'll upload it for you.\n\n"
            "I can help you host your images and provide you with a shareable link.\n"
            "Feel free to reach out if you have any questions!"
        ),
        reply_markup=reply_markup
    )
