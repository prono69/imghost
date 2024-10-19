# db/mongodb.py

from pymongo import MongoClient
import os

# Load environment variables
MONGODB_URL = os.getenv('MONGODB_URL', 'your_mongodb_url')

class MongoDB:
    def __init__(self, url):
        self.client = MongoClient(url)
        self.db = self.client['imagehost_db']  # Database name
        self.collection = self.db['uploads']    # Collection name

    def insert_upload(self, file_url):
        """Insert uploaded file URL into the database."""
        self.collection.insert_one({"file_url": file_url})

    def get_all_uploads(self):
        """Get all uploaded file URLs from the database."""
        return list(self.collection.find({}, {"_id": 0, "file_url": 1}))

def connect_to_mongodb():
    """Connect to MongoDB and return the MongoDB instance."""
    return MongoDB(MONGODB_URL)

# Initialize MongoDB instance
mongo_db = MongoDB(MONGODB_URL)
