# 1. Starting with a node base image
FROM python:3.9-slim

# 2. Setting the main application directory
WORKDIR /app

# Environment variables
# Ensures output is sent straight to the terminal
ENV PYTHONUNBUFFERED=1

# 3. Copying the dependency list 
COPY requirements.txt .

# 4. Install libraries and dependencies in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copying weather tool script and json data file
COPY weather.py .
COPY weather_codes.json .

# Start the app using serve command
CMD [ "python", "weather.py" ]