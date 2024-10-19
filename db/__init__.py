# database/__init__.py

from .mongodb import connect_to_mongodb, save_image_url  # Example functions

__all__ = ['connect_to_mongodb', 'save_image_url']  # Specifies what should be imported
