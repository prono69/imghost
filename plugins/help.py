from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("help"))
async def command_help(client: Client, message):
    # Create help menu buttons
    buttons = [
        [InlineKeyboardButton("Close", callback_data="close")]
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)

    # Send help menu message
    await message.reply(
        "Here are some commands you can use:\n"
        "/start - Start the bot\n"
        "/help - Get help with commands\n"
        "/stats - View bot statistics (Admin only)\n"
        "/broadcast - Broadcast a message to all users (Admin only)\n"
        "Send me a photo to upload it and I'll provide a shareable link.\n",
        reply_markup=reply_markup
    )
