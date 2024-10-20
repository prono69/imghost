import httpx
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import Message
from httpx import ConnectError, HTTPStatusError
from db.mongo_db import mongo_db  # MongoDB handler

async def upload_file_to_envs(file_content: BytesIO):
    async with httpx.AsyncClient() as client:
        files = {'file': ('image.jpg', file_content, 'image/jpeg')}
        try:
            response = await client.post('https://envs.sh', files=files)
            response.raise_for_status()
            print("Raw response:", response.text)
            return response.text.strip()

        except HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

@Client.on_message(filters.photo)
async def handle_photo(client: Client, message: Message):
    try:
        temp_message = await message.reply("⚡")
        photo_file_path = await message.download()

        with open(photo_file_path, 'rb') as f:
            photo_bytes = BytesIO(f.read())

        response_data = await upload_file_to_envs(photo_bytes)

        if response_data:
            formatted_link = f"Link: {response_data}\nClick to copy: `{response_data}`\n\n"
            credit_message = "```Bot by: @thealphabotz```"
            final_message = f"Your image uploaded successfully .\n\n{formatted_link}{credit_message}"
            await temp_message.edit(final_message)
            await mongo_db.insert_upload(response_data)
        else:
            await temp_message.edit("Failed to get the URL from envs.sh. Invalid response format.")

    except ConnectError:
        await message.reply("Network error occurred. Please check your connection.")
    except Exception as e:
        await message.reply("An error occurred while processing your request.")
        print("Error:", str(e))
