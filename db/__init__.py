# db/__init__.py

from .mongodb import connect_to_mongodb, mongo_db

def save_image_url(file_url):
    """Save an image URL to the database."""
    mongo_db.insert_upload(file_url)
