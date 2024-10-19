# plugins/start.py

from pyrogram import Client, filters

async def start(client: Client, message):
    # Path to your bot's image
    bot_image_url = "Link: https://envs.sh/pQp.jpg"  # Replace with your bot's image URL

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
