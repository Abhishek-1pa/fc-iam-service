#!/bin/bash
# Change directory to 'backend' directory
if [ ! -d "backend" ]; then
    mkdir backend
fi

cd backend

# Check if the repository exists, if not, clone it
if [ ! -d "fc-blog-service" ]; then
    git clone https://github.com/frozenmafia/fc-blog-service.git
fi

# Change directory to the cloned repository
cd fc-blog-service

# Pull the latest changes from the repository
git pull

# Build the new Docker image for fc-blog-service
sudo docker build -t fc-blog-service-new .

# Check if the container exists
if sudo docker ps -a --format '{{.Names}}' | grep -Eq '^fc-blog-service$'; then
    # Stop the existing container
    sudo docker stop fc-blog-service

    # Remove the existing container
    sudo docker rm fc-blog-service
fi

# Run the new Docker container for fc-blog-service with restart options
sudo docker run -d --restart=always --name fc-blog-service -p 8002:8002 fc-blog-service-new