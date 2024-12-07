import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

API_ID = int(os.getenv('API_ID', 'your_api_id'))
API_HASH = os.getenv('API_HASH', 'your_api_hash')  
BOT_TOKEN = os.getenv('BOT_TOKEN', 'your_bot_token')  
MONGODB_URL = os.getenv('MONGODB_URL', 'your_mongodb_url')  # MongoDB URL
ADMIN_ID = int(os.getenv('ADMIN_ID', 'your_admin_id'))  # Add admin ID
BOT_IMAGE_URL = os.getenv('BOT_IMAGE_URL', 'https://envs.sh/WKQ.jpg')  # Bot's image URL
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "d8271e879cd79d8a20948f1b7c48c4b5")
LOG_GROUP_ID = -1001684936508