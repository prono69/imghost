# database/__init__.py

from .mongodb import connect_to_mongodb, save_image_url  # Replace these with actual function names

__all__ = ['connect_to_mongodb', 'save_image_url']  # Specifies what should be imported
