#!/bin/bash

# Change directory to 'backend' directory
if [! -d "backend"]; then
    mkdir backened
fi

cd backened

# Check if the repository exists, if not, clone it
if [ ! -d "fc-iam-service" ]; then
    git clone https://github.com/frozenmafia/fc-iam-service.git
fi

# Change directory to the cloned repository
cd fc-iam-service

# Pull the latest changes from the repository
git pull

# Build the new Docker image for fc-iam-service
sudo docker build -t fc-iam-service-new .

# Check if the container exists
if sudo docker ps -a --format '{{.Names}}' | grep -Eq '^fc-iam-service$'; then
    # Stop the existing container
    sudo docker stop fc-iam-service

    # Remove the existing container
    sudo docker rm fc-iam-service
fi

# Run the new Docker container for fc-iam-service with restart options
sudo docker run -d --restart=always --name fc-iam-service -p 8001:8001 fc-iam-service-new
