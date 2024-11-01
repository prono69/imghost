import asyncio
from .mongo_db import mongo_db, connect_to_mongodb

async def initialize_db():
    """Connect to MongoDB when the module is loaded."""
    await connect_to_mongodb()

# Call the async initialize_db function at startup
asyncio.run(initialize_db())

def save_image_url(file_url):
    """Save an image URL to the database."""
    try:
        # Use the insert method on mongo_db to save the URL
        mongo_db.insert_upload({"file_url": file_url})
        print(f"Image URL saved successfully: {file_url}")
    except Exception as e:
        print(f"Error saving image URL: {e}")
