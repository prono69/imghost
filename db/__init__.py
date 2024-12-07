from .mongo_db import mongo_db, connect_to_mongodb
import logging

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
async def save_image_url(file_url):
    """Save an image URL to the database."""
    try:
        await mongo_db.insert_upload(file_url)  # Await the async method
        logger.info(f"Image URL saved successfully: {file_url}")
    except Exception as e:
        logger.error(f"Error saving image URL: {e}")