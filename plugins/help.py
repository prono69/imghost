# plugins/help.py

from pyrogram import Client, filters

async def help_command(client: Client, message):
    await message.reply(
        "Here are some commands you can use:\n"
        "/start - Start the bot\n"
        "Send me a photo to upload it.\n",
        reply_markup={"inline_keyboard": [[("Return", "return")]]}
    )
