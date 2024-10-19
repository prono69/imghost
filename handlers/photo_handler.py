import httpx
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import Message
from httpx import ConnectError, HTTPStatusError
from db.mongo_db import mongo_db  # MongoDB handler

# Function to upload file content to envs.sh
async def upload_file_to_envs(file_content: BytesIO):
    async with httpx.AsyncClient() as client:
        files = {'file': ('image.jpg', file_content, 'image/jpeg')}
        try:
            response = await client.post('https://envs.sh', files=files)
            response.raise_for_status()  # Check for HTTP errors
            
            # Debugging: Print the raw response
            print("Raw response:", response.text)
            return response.text.strip()  # Return the plain text response (URL)

        except HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")  # Log HTTP errors
            return None
        except Exception as e:
            print(f"An error occurred: {e}")  # Log other errors
            return None

# Function to handle photo upload
@Client.on_message(filters.photo)
async def handle_photo(client: Client, message: Message):
    try:
        # Download the photo that the user has sent
        photo_file_path = await message.download()  # Download the photo to local storage

        # Open and read the photo content as bytes
        with open(photo_file_path, 'rb') as f:
            photo_bytes = BytesIO(f.read())

        # Upload the photo to envs.sh
        response_data = await upload_file_to_envs(photo_bytes)

        if response_data:  # If a valid response is received
            formatted_link = f"Link: {response_data}"  # Format the link
            await message.reply(formatted_link)  # Send the link back to the user

            # Insert the uploaded file's URL into MongoDB
            mongo_db.insert_upload(response_data)
        else:
            await message.reply("Failed to get the URL from envs.sh. Invalid response format.")

    except ConnectError:
        await message.reply("Network error occurred. Please check your connection.")
    except Exception as e:
        await message.reply("An error occurred while processing your request.")
        print("Error:", str(e))

# Note: No need to define a start command or other unnecessary parts,
#       since it's already handled in your main bot file.
