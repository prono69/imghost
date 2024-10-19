# config.py

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

API_ID = os.getenv('API_ID', 'your_api_id')  
API_HASH = os.getenv('API_HASH', 'your_api_hash')  
BOT_TOKEN = os.getenv('BOT_TOKEN', 'your_bot_token')  
MONGODB_URL = os.getenv('MONGODB_URL', 'your_mongodb_url')  # MongoDB URL
