from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("help"))
async def help_handler(client: Client, message):
    
    buttons = [
        [InlineKeyboardButton("Close", callback_data="close")]  # Close button to delete the message
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)

    # Send help menu message
    await message.reply(
        "**Here are some commands you can use:**\n"
        "/start - __Start the bot__\n"
        "/help - __Get help with commands__\n"
        "/stats - __View bot statistics (Admin only)__\n"
        "/broadcast - __Broadcast a message to all users (Admin only)__\n\n"
        "**Send me a photo to upload it and I'll provide a shareable link.**\n",
        reply_markup=reply_markup
    )

@Client.on_callback_query(filters.regex("close"))
async def close_help(client: Client, callback_query):
    await callback_query.message.delete()  # Delete the help menu message
    await callback_query.answer()  # Acknowledge the callback query
