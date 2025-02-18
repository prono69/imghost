from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_IMAGE_URL

async def start_handler(client, message):
    bot_image_url = BOT_IMAGE_URL
    buttons = [
        [
            InlineKeyboardButton("Updates🔊", url="https://t.me/Neko_Drive"),  
            InlineKeyboardButton("Support🧑‍🔧", url="https://t.me/NeoMatrix90")
        ],
        [
            InlineKeyboardButton("donate🥺", url="https://t.me/NeoMatrix90"),  
            InlineKeyboardButton("Source", url="https://t.me/Neko_Drive")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)  

    await message.reply_photo(
        photo=bot_image_url,
        caption=(
            "__Welcome to ImageHost Bot! Send me an image, and I'll upload it for you.__\n\n"
            "__I can help you host your images and provide you with a shareable link.__\n"
            "__Feel free to reach out if you have any questions!__"
        ),
        reply_markup=reply_markup  # Pass the properly structured reply markup
    )
