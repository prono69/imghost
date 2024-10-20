import os
from motor.motor_asyncio import AsyncIOMotorClient  # Use AsyncIOMotorClient for async operations

# Load environment variables
MONGODB_URL = os.getenv('MONGODB_URL', 'your_mongodb_url')

class MongoDB:
    def __init__(self, url):
        self.client = AsyncIOMotorClient(url)
        self.db = self.client['imagehost_db']  # Database name
        self.uploads_collection = self.db['uploads']  # Collection for uploads
        self.users_collection = self.db['users']      # Collection for users

    async def insert_upload(self, file_url):
        """Insert uploaded file URL into the database."""
        try:
            await self.uploads_collection.insert_one({"file_url": file_url})
        except Exception as e:
            print(f"Error inserting upload: {e}")

    async def get_all_uploads(self):
        """Get all uploaded file URLs from the database."""
        try:
            return await self.uploads_collection.find({}, {"_id": 0, "file_url": 1}).to_list(length=None)
        except Exception as e:
            print(f"Error fetching uploads: {e}")
            return []

    async def count_uploads(self):
        """Get the total count of uploads."""
        try:
            return await self.uploads_collection.count_documents({})
        except Exception as e:
            print(f"Error counting uploads: {e}")
            return 0

    async def insert_user(self, user_id):
        """Insert a new user into the users collection."""
        try:
            await self.users_collection.insert_one({"user_id": user_id})
        except Exception as e:
            print(f"Error inserting user: {e}")

    async def count_users(self):
        """Get the total count of users."""
        try:
            return await self.users_collection.count_documents({})
        except Exception as e:
            print(f"Error counting users: {e}")
            return 0

    async def get_total_users(self):
        """Get the total number of users."""
        try:
            return await self.count_users()  # Reuse the count_users method
        except Exception as e:
            print(f"Error fetching total users: {e}")
            return 0

    async def get_all_user_ids(self):
        """Get all user IDs from the users collection."""
        try:
            cursor = self.users_collection.find({}, {"_id": 0, "user_id": 1})  # Adjust according to your schema
            user_ids = await cursor.to_list(length=None)  # Convert cursor to a list
            return [user['user_id'] for user in user_ids]  # Extract user_ids
        except Exception as e:
            print(f"Error fetching user IDs: {e}")
            return []

async def connect_to_mongodb():
    """Connect to MongoDB and return the MongoDB instance."""
    return MongoDB(MONGODB_URL)

# Initialize MongoDB instance
mongo_db = MongoDB(MONGODB_URL)
