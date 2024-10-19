# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install NTP to keep the time synchronized
RUN apt-get update && apt-get install -y ntp && service ntp start

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Expose the port for the web server (change 8080 if needed)
EXPOSE 8080

# Health check for Koyeb: Flask server listens on port 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
 CMD curl --fail http://localhost:8080/health || exit 1

# Command to run both the bot and Flask health check server
CMD ["python", "bot.py"]
