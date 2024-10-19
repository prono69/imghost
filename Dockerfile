# Dockerfile

# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Set environment variables
ENV API_ID=your_api_id
ENV API_HASH=your_api_hash
ENV BOT_TOKEN=your_bot_token
ENV MONGODB_URL=your_mongodb_url  # MongoDB URL

# Command to run the bot
CMD ["python", "bot.py"]
