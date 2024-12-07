from .mongo_db import mongo_db, connect_to_mongodb
 
def save_image_url(file_url):
    """Save an image URL to the database."""
    try:
        mongo_db.insert_upload(file_url)
    except Exception as e:
        print(f"Error saving image URL: {e}")