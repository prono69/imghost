import httpx
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import Message
from httpx import ConnectError
from db.mongo_db import mongo_db

async def upload_file_to_envs(file_content: BytesIO):
    async with httpx.AsyncClient() as client:
        files = {'file': ('image.jpg', file_content, 'image/jpeg')}
        try:
            response = await client.post('https://envs.sh', files=files)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()  # Attempt to parse JSON response
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            print(f"Error occurred during upload: {str(e)}")
            return None

async def handle_photo(client: Client, message: Message):
    try:
        # Get the largest available photo size and download it
        largest_photo = message.photo[-1]  # Get the last item for the highest resolution
        photo_file_path = await largest_photo.download()  # Downloading the largest photo

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
