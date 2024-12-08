import os
import httpx
from io import BytesIO
from httpx import HTTPStatusError, ConnectError
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from db.mongo_db import mongo_db
from config import IMGBB_API_KEY

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
            traceback.print_exc()
            return None

# Upload to IMGBB
async def upload_file_to_imbb(file_content: BytesIO):
    imgbb_api_key = IMGBB_API_KEY  # Ensure the key is in environment variables
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
            traceback.print_exc()
            return None

@Client.on_message(filters.photo)
async def handle_photo(client: Client, message: Message):
    try:
        temp_message = await message.reply("<b><i>Uploading your photo ⚡</i></b>")
        photo_file_path = await message.download()
 
        with open(photo_file_path, 'rb') as f:
            photo_bytes = BytesIO(f.read())
            photo_bytes.seek(0)  # Reset pointer to the beginning
 
        response_data = await upload_file_to_envs(photo_bytes)
 
        if response_data:
            formatted_link = f"🔗 <b>Link:</b> {response_data}\n<b>Click to copy:</b> `{response_data}`\n\n"
            credit_message = "🤴 <b>Bot by:</b> <i>@Neko_Drive</i>"
            final_message = f"✘ <b><i>Your image uploaded successfully 🙃.</i></b>\n\n{formatted_link}{credit_message}"
            await temp_message.edit(final_message, disable_web_page_preview=True)
            await mongo_db.insert_upload(response_data)
        else:
            await temp_message.edit("Failed to get the URL from envs.sh. Invalid response format.")
 
    except ConnectError:
        await message.reply("Network error occurred. Please check your connection.")
    except Exception as e:
        await message.reply("An error occurred while processing your request.")
        print("Error:", str(e))
        
    if os.path.exists(photo_file_path):
      os.remove(photo_file_path)
    
        
       