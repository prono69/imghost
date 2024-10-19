# plugins/start.py

from pyrogram import Client, filters

async def start(client: Client, message):
    buttons = [
        [("Support", "support"), ("Owner Channel", "owner_channel")],
        [("Updates Channel", "updates_channel"), ("Help", "help")]
    ]
    await message.reply(
        "Welcome to ImageHost Bot! Send me an image, and I'll upload it for you.\n\n"
        "I can help you host your images and provide you with a shareable link.\n"
        "Feel free to reach out if you have any questions!",
        reply_markup={"inline_keyboard": buttons}
    )
