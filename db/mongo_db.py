import os
from motor.motor_asyncio import AsyncIOMotorClient
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

MONGODB_URL = os.getenv('MONGODB_URL')
if not MONGODB_URL:
    raise ValueError("MONGODB_URL environment variable is not set.")

class MongoDB:
    def __init__(self, url):
        try:
            self.client = AsyncIOMotorClient(url)
            self.db = self.client['imagehost_db']  
            self.uploads_collection = self.db['uploads']  
            self.users_collection = self.db['users']  
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {e}")

    async def close_connection(self):
        """Close the MongoDB connection."""
        self.client.close()

    async def insert_upload(self, file_url):
        try:
            await self.uploads_collection.insert_one({"file_url": file_url})
        except Exception as e:
            logger.error(f"Error inserting upload: {e}")

    async def get_all_uploads(self):
        try:
            return await self.uploads_collection.find({}, {"_id": 0, "file_url": 1}).to_list(length=None)
        except Exception as e:
            logger.error(f"Error fetching uploads: {e}")
            return []

    async def count_uploads(self):
        try:
            return await self.uploads_collection.count_documents({})
        except Exception as e:
            logger.error(f"Error counting uploads: {e}")
            return 0

    async def insert_user(self, user_id):
        try:
            await self.users_collection.insert_one({"user_id": user_id})
        except Exception as e:
            logger.error(f"Error inserting user: {e}")

    async def add_or_update_user(self, user_data):
        try:
            await self.users_collection.update_one(
                {"user_id": user_data["user_id"]},
                {"$set": user_data},
                upsert=True
            )
        except Exception as e:
            logger.error(f"Error updating user data: {e}")

    async def count_users(self):
        try:
            return await self.users_collection.count_documents({})
        except Exception as e:
            logger.error(f"Error counting users: {e}")
            return 0

    async def get_all_user_ids(self):
        try:
            cursor = self.users_collection.find({}, {"_id": 0, "user_id": 1})
            user_ids = await cursor.to_list(length=None)
            return [user['user_id'] for user in user_ids]
        except Exception as e:
            logger.error(f"Error fetching user IDs: {e}")
            return []

# MongoDB instance
mongo_db = MongoDB(MONGODB_URL)

async def connect_to_mongodb():
    """Connect to MongoDB and return the MongoDB instance."""
    return MongoDB(MONGODB_URL)
