import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGODB_URL = os.getenv('MONGODB_URL')

if not MONGODB_URL:
    logger.error("MONGODB_URL environment variable not set.")
    raise ValueError("MONGODB_URL environment variable must be set.")

class MongoDB:
    def __init__(self, url):
        self.client = AsyncIOMotorClient(url)
        self.db = self.client['imagehost_db']
        self.uploads_collection = self.db['uploads']
        self.users_collection = self.db['users']

    async def insert_upload(self, file_url):
        """Insert uploaded file URL into the database."""
        try:
            await self.uploads_collection.insert_one({"file_url": file_url})
            logger.info(f"Inserted upload: {file_url}")
        except Exception as e:
            logger.error(f"Error inserting upload: {e}")

    async def get_all_uploads(self):
        """Get all uploaded file URLs from the database."""
        try:
            uploads = await self.uploads_collection.find({}, {"_id": 0, "file_url": 1}).to_list(length=None)
            logger.info("Fetched all uploads.")
            return uploads
        except Exception as e:
            logger.error(f"Error fetching uploads: {e}")
            return []

    async def count_uploads(self):
        """Get the total count of uploads."""
        try:
            count = await self.uploads_collection.count_documents({})
            logger.info(f"Total uploads count: {count}")
            return count
        except Exception as e:
            logger.error(f"Error counting uploads: {e}")
            return 0

    async def insert_user(self, user_id):
        """Insert a new user into the users collection."""
        try:
            await self.users_collection.insert_one({"user_id": user_id})
            logger.info(f"Inserted user: {user_id}")
        except Exception as e:
            logger.error(f"Error inserting user: {e}")

    async def add_or_update_user(self, user_data):
        """Add a new user or update existing user data."""
        try:
            await self.users_collection.update_one(
                {"user_id": user_data["user_id"]},
                {"$set": user_data},
                upsert=True
            )
            logger.info(f"User data updated or inserted: {user_data['user_id']}")
        except Exception as e:
            logger.error(f"Error updating user data: {e}")

    async def count_users(self):
        """Get the total count of users."""
        try:
            count = await self.users_collection.count_documents({})
            logger.info(f"Total users count: {count}")
            return count
        except Exception as e:
            logger.error(f"Error counting users: {e}")
            return 0

    async def get_total_users(self):
        """Get the total number of users."""
        try:
            return await self.count_users()
        except Exception as e:
            logger.error(f"Error fetching total users: {e}")
            return 0

    async def get_all_user_ids(self):
        """Get all user IDs from the users collection."""
        try:
            cursor = self.users_collection.find({}, {"_id": 0, "user_id": 1})
            user_ids = await cursor.to_list(length=None)
            logger.info("Fetched all user IDs.")
            return [user['user_id'] for user in user_ids]
        except Exception as e:
            logger.error(f"Error fetching user IDs: {e}")
            return []

async def connect_to_mongodb():
    """Connect to MongoDB and return the MongoDB instance."""
    return MongoDB(MONGODB_URL)
