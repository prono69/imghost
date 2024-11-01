import asyncio
import logging
from .mongo_db import connect_to_mongodb

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global MongoDB instance
mongo_db = None

async def initialize_db():
    """Connect to MongoDB when the module is loaded."""
    global mongo_db
    mongo_db = await connect_to_mongodb()
    logger.info("MongoDB connection established.")

# Call the async initialize_db function at startup
def setup_db():
    """Initialize the database connection in the event loop."""
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # If the event loop is already running (like in a web server), use ensure_future
        asyncio.ensure_future(initialize_db())
    else:
        asyncio.run(initialize_db())

setup_db()

async def save_image_url(file_url):
    """Save an image URL to the database."""
    try:
        await mongo_db.insert_upload(file_url)  # Await the async method
        logger.info(f"Image URL saved successfully: {file_url}")
    except Exception as e:
        logger.error(f"Error saving image URL: {e}")
