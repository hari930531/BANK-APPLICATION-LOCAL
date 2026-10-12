# ==============================================================================
# Dockerfile: Transfer Service
# Purpose: Builds the container image for processing fund transfers between
#          accounts running on port 5002.
# ==============================================================================

# Step 1: Use lightweight base Python image
FROM python:3.11-slim

# Step 2: Set working directory inside the container
WORKDIR /app

# Step 3: Copy dependencies specification
COPY requirements.txt .

# Step 4: Install runtime dependencies (Flask, requests, flask-cors)
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy transaction logic code into container image
COPY app.py .

# Step 6: Expose Transfer Service listening port
EXPOSE 5002

# Step 7: Start the transfer microservice
CMD ["python", "app.py"]