import asyncio
import logging
from .mongo_db import connect_to_mongodb

# Set up logging
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global MongoDB instance
mongo_db = None

async def initialize_db():
    """Connect to MongoDB when the module is loaded."""
    global mongo_db
    if mongo_db is None:
        mongo_db = await connect_to_mongodb()
        logger.info("MongoDB connection established.")
    else:
        logger.info("MongoDB connection already established.")

def setup_db():
    """Initialize the database connection in the event loop."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:  # No running event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    if loop.is_running():
        asyncio.ensure_future(initialize_db())
    else:
        loop.run_until_complete(initialize_db())

setup_db()

async def save_image_url(file_url):
    """Save an image URL to the database."""
    try:
        if mongo_db is None:
            logger.error("MongoDB is not initialized. Ensure setup_db() was called.")
            return
        await mongo_db.insert_upload(file_url)  # Await the async method
        logger.info(f"Image URL saved successfully: {file_url}")
    except Exception as e:
        logger.error(f"Error saving image URL: {e}")
