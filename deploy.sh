#!/bin/bash

# Push code to GitHub
git add .
git commit -m "Update code"
git push origin main

# Build and push Docker image to Docker Hub
docker build -t anchalshivank/iam-service .
docker push anchalshivank/iam-service

# SSH into your VM and redeploy the Docker container
ssh -i projectuser projectuser@34.131.181.137 << 'EOF'
sudo docker pull anchalshivank/iam-service
sudo docker stop iam-container
sudo docker rm iam-container
sudo docker run -d -p 8000:8000 --name iam-container anchalshivank/iam-service
EOF
