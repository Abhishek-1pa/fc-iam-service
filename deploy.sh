git add .
git commit -m "update code"
git push origin main

docker build -t iam-service .
docker push anchalshivank/iam-service

ssh -i projectuser projectuser@34.131.181.137
sudo docker pull anchalshivank/fc-iam-service
sudo docker stop iam-container
sudo docker rm iam-container
sudo docker run -d -p 8000:8000 --name iam-container anchalshivank/fc-iam-service