import httpx
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import Message
from httpx import ConnectError
from db.mongo_db import mongo_db

async def upload_file_to_envs(file_content: BytesIO):
    try:
        async with httpx.AsyncClient() as client:
            files = {'file': ('image.jpg', file_content, 'image/jpeg')}
            response = await client.post('https://envs.sh', files=files)

            # Check if the response is successful
            if response.status_code == 200:
                try:
                    return response.json()  # Try to parse the JSON response
                except ValueError:
                    print("Error: Received invalid JSON from envs.sh")
                    return None
            else:
                print(f"Error: Failed to upload file. Status code: {response.status_code}")
                print(f"Response: {response.text}")  # Print the raw response for debugging
                return None

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
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

# Add the handler to Pyrogram
@Client.on_message(filters.photo)
async def photo_handler(client, message):
    await handle_photo(client, message)
