from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("help"))
async def help_handler(client: Client, message):  # Change function name to help_handler
    # Create help menu buttons
    buttons = [
        [InlineKeyboardButton("Close", callback_data="close")]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)

    # Send help menu message
    help_message = await message.reply(
        "Here are some commands you can use:\n"
        "/start - Start the bot\n"
        "/help - Get help with commands\n"
        "/stats - View bot statistics (Admin only)\n"
        "/broadcast - Broadcast a message to all users (Admin only)\n"
        "Send me a photo to upload it and I'll provide a shareable link.\n",
        reply_markup=reply_markup
    )

    # Listen for the callback query to close the help menu
    @Client.on_callback_query(filters.regex("close"))
    async def close_help(_, callback_query):
        await callback_query.message.delete()  # Delete the help menu message
        await callback_query.answer()  # Acknowledge the callback query
