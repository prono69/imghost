from pymongo import MongoClient
import os

# Load environment variables
MONGODB_URL = os.getenv('MONGODB_URL', 'your_mongodb_url')

class MongoDB:
    def __init__(self, url):
        self.client = MongoClient(url)
        self.db = self.client['imagehost_db']  # Database name
        self.uploads_collection = self.db['uploads']  # Collection for uploads
        self.users_collection = self.db['users']      # Collection for users

    def insert_upload(self, file_url):
        """Insert uploaded file URL into the database."""
        try:
            self.uploads_collection.insert_one({"file_url": file_url})
        except Exception as e:
            print(f"Error inserting upload: {e}")

    def get_all_uploads(self):
        """Get all uploaded file URLs from the database."""
        try:
            return list(self.uploads_collection.find({}, {"_id": 0, "file_url": 1}))
        except Exception as e:
            print(f"Error fetching uploads: {e}")
            return []

    def count_uploads(self):
        """Get the total count of uploads."""
        try:
            return self.uploads_collection.count_documents({})
        except Exception as e:
            print(f"Error counting uploads: {e}")
            return 0

    def insert_user(self, user_id):
        """Insert a new user into the users collection."""
        try:
            self.users_collection.insert_one({"user_id": user_id})
        except Exception as e:
            print(f"Error inserting user: {e}")

    def count_users(self):
        """Get the total count of users."""
        try:
            return self.users_collection.count_documents({})
        except Exception as e:
            print(f"Error counting users: {e}")
            return 0

    def get_total_users(self):
        """Get the total number of users."""
        try:
            return self.users_collection.count_documents({})
        except Exception as e:
            print(f"Error fetching total users: {e}")
            return 0

def connect_to_mongodb():
    """Connect to MongoDB and return the MongoDB instance."""
    return MongoDB(MONGODB_URL)

# Initialize MongoDB instance
mongo_db = MongoDB(MONGODB_URL)
