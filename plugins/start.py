from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_IMAGE_URL

# Global variable to keep track of the original message ID
original_message_id = None

async def start_handler(client: Client, message):
    global original_message_id
    bot_image_url = BOT_IMAGE_URL

    # Create the start message with buttons
    buttons = [
        [
            InlineKeyboardButton("Updates", url="https://t.me/Thealphabotz"),
            InlineKeyboardButton("Support", url="https://t.me/thealphabotz")
        ],
        [
            InlineKeyboardButton("Help", callback_data="help"),
            InlineKeyboardButton("Source", url="https://github.com/utkarshdubey2008/imagehost")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)

    # Send the start message and save the message ID
    original_message = await message.reply_photo(
        photo=bot_image_url,
        caption=(
            "Welcome to ImageHost Bot! Send me an image, and I'll upload it for you.\n\n"
            "I can help you host your images and provide you with a shareable link.\n"
            "Feel free to reach out if you have any questions!"
        ),
        reply_markup=reply_markup
    )
    original_message_id = original_message.message_id  # Save the ID for future reference


@Client.on_callback_query(filters.regex("help"))
async def help_handler(client: Client, callback_query):
    await callback_query.answer()  # Acknowledge the callback query

    # Create help menu buttons
    buttons = [
        [InlineKeyboardButton("Close", callback_data="close")]
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)

    # Edit the original message to show help information
    await client.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=original_message_id,
        caption=(
            "Here are some commands you can use:\n"
            "/start - Start the bot\n"
            "/help - Get help with commands\n"
            "/stats - View bot statistics (Admin only)\n"
            "/broadcast - Broadcast a message to all users (Admin only)\n"
            "Send me a photo to upload it and I'll provide a shareable link.\n"
        ),
        reply_markup=reply_markup  # Update the reply markup to show help button
    )


@Client.on_callback_query(filters.regex("close"))
async def close_handler(client: Client, callback_query):
    await callback_query.answer("Closing help menu...")

    # Delete the help message (which is actually the start message)
    await client.delete_messages(
        chat_id=callback_query.message.chat.id,
        message_ids=original_message_id
    )
