# db/__init__.py

from .mongo_db import mongo_db  # Import the mongo_db instance

def save_image_url(file_url):
    """Save an image URL to the database."""
    mongo_db.insert_upload(file_url)
