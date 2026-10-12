# ==============================================================================
# Dockerfile: Account Service
# Purpose: Builds the container image for account management and balance queries
#          running on port 5001.
# ==============================================================================

# Step 1: Base Python runtime environment
FROM python:3.11-slim

# Step 2: Establish application root inside the container
WORKDIR /app

# Step 3: Copy requirements file to isolate dependency build layer
COPY requirements.txt .

# Step 4: Install Python packages (Flask, mysql-connector, flask-cors)
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy account service entrypoint script
COPY app.py .

# Step 6: Expose Account Service listening port
EXPOSE 5001

# Step 7: Launch the Flask service
CMD ["python", "app.py"]