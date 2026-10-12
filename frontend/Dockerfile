# ==============================================================================
# Dockerfile: Web Frontend (Static Server)
# Purpose: Serves the single-page application (index.html) using a high-performance
#          Nginx web server on HTTP port 80.
# ==============================================================================

# Step 1: Use standard lightweight Nginx Alpine base image
FROM nginx:alpine

# Step 2: Remove default placeholder Nginx webpage
RUN rm -rf /usr/share/nginx/html/*

# Step 3: Copy the banking application frontend file into the Nginx public directory
COPY index.html /usr/share/nginx/html/index.html

# Step 4: Expose default web traffic HTTP port
EXPOSE 80

# Step 5: Launch Nginx web server in the foreground
CMD ["nginx", "-g", "daemon off;"]