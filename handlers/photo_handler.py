import os
import httpx
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from db.mongo_db import mongo_db  # MongoDB handler

# Upload to Envs.sh
async def upload_file_to_envs(file_content: BytesIO):
    async with httpx.AsyncClient() as client:
        files = {'file': ('image.jpg', file_content, 'image/jpeg')}
        try:
            response = await client.post('https://envs.sh', files=files)
            response.raise_for_status()
            return response.text.strip()
        except HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Upload to IMGBB
async def upload_file_to_imbb(file_content: BytesIO):
    imgbb_api_key = os.getenv("IMGBB_API_KEY")  # Retrieve your IMGBB API key from environment variables
    async with httpx.AsyncClient() as client:
        files = {'image': file_content.getvalue()}
        try:
            response = await client.post(f'https://api.imgbb.com/1/upload?key={imgbb_api_key}', files=files)
            response.raise_for_status()
            return response.json().get("data", {}).get("url")
        except HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Photo handler with hosting options
@Client.on_message(filters.photo)
async def handle_photo(client: Client, message: Message):
    buttons = [
        [InlineKeyboardButton("Envs", callback_data="upload_envs")],
        [InlineKeyboardButton("IMGBB", callback_data="upload_imbb")]
    ]
    await message.reply("Choose the hosting provider:", reply_markup=InlineKeyboardMarkup(buttons))

# Callback query handler
@Client.on_callback_query(filters.regex("upload_"))
async def on_callback_query(client: Client, callback_query):
    user_choice = callback_query.data
    await callback_query.answer()
    
    # Download the photo file
    photo_file_path = await callback_query.message.reply_to_message.download()
    with open(photo_file_path, 'rb') as f:
        photo_bytes = BytesIO(f.read())
    
    temp_message = await callback_query.message.reply("⚡ Uploading your image...")
    if user_choice == "upload_envs":
        response_data = await upload_file_to_envs(photo_bytes)
    elif user_choice == "upload_imbb":
        response_data = await upload_file_to_imbb(photo_bytes)

    if response_data:
        formatted_link = f"Link: {response_data}\nClick to copy: `{response_data}`\n\n"
        credit_message = "> Bot by: @thealphabotz"
        final_message = f"Your image uploaded successfully 🙃.\n\n{formatted_link}{credit_message}"
        await temp_message.edit(final_message)

        # Insert the uploaded file's URL into MongoDB
        await mongo_db.insert_upload(response_data)
    else:
        await temp_message.edit("Failed to upload the image. Please try again.")

    # Clean up downloaded file
    os.remove(photo_file_path)
