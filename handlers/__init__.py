# handlers/photo_handler.py

from db import save_image_url  # Importing the save_image_url function

async def handle_photo(client, message):
    # Your photo handling logic
    file_url = "example_file_url"  # Replace with actual file URL logic
    save_image_url(file_url)  # Use save_image_url to insert the upload
