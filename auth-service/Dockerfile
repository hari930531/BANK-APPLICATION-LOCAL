# ==============================================================================
# Dockerfile: Authentication Service
# Purpose: Builds the container image for user authentication, registration,
#          and JWT handling running on port 5003.
# ==============================================================================

# Step 1: Use official lightweight Python 3.11 slim image as base
FROM python:3.11-slim

# Step 2: Set working directory inside the container filesystem
WORKDIR /app

# Step 3: Copy only dependency definitions first to leverage Docker layer caching
COPY requirements.txt .

# Step 4: Install required Python libraries without caching wheel files to save space
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the Flask application source code into the container
COPY app.py .

# Step 6: Inform Docker that the container listens on port 5003 at runtime
EXPOSE 5003

# Step 7: Specify the default command to start the microservice
CMD ["python", "app.py"]