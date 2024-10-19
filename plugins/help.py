from pyrogram import Client, filters

async def help_handler(client: Client, message):
    await message.reply(
        "Here are some commands you can use:\n"
        "/start - Start the bot\n"
        "/help - Get help with commands\n"
        "/stats - View bot statistics (Admin only)\n"
        "/broadcast - Broadcast a message to all users (Admin only)\n"
        "Send me a photo to upload it and I'll provide a shareable link.\n",
        reply_markup={
            "inline_keyboard": [
                [("Return", "return")],
                [("Close", "close")]
            ]
        }
    )
