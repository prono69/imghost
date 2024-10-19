import httpx
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import Message
from httpx import ConnectError
from db.mongo_db import mongo_db

async def upload_file_to_envs(file_content: BytesIO):
    async with httpx.AsyncClient() as client:
        files = {'file': ('image.jpg', file_content, 'image/jpeg')}
        response = await client.post('https://envs.sh', files=files)

        if response.status_code == 200:
            return response.json()
        else:
            return None

async def handle_photo(client: Client, message: Message):
    try:
        # Download the photo and get the file path
        photo_file_path = await message.download()  # Downloading the photo

        # Read the photo content as bytes
        with open(photo_file_path, 'rb') as photo_file:
            photo_bytes = BytesIO(photo_file.read())

        # Upload the photo to envs.sh
        response_data = await upload_file_to_envs(photo_bytes)

        if response_data and 'url' in response_data:
            link = response_data['url']
            formatted_link = f"Link: {link}"
            await message.reply(formatted_link)

            # Insert the URL into MongoDB
            mongo_db.insert_upload(link)
        else:
            await message.reply("Failed to get the URL from envs.sh. Invalid response format.")

    except ConnectError:
        await message.reply("Network error occurred. Please check your connection.")
    except Exception as e:
        await message.reply("An error occurred while processing your request.")
        print("Error:", str(e))
