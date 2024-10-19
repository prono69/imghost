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

# Expose the port (change 8080 to the correct port if needed)
EXPOSE 8080

# Command to run the bot
CMD ["python", "bot.py"]
