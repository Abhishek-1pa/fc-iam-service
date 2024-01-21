git add .
git commit -m "update code"
git push origin main

docker build -t iam-service .
docker push anchalshivank/iam-service

ssh -i shivajay295 shivajay295@34.131.181.137
docker pull anchalshivank/fc-iam-service
docker stop iam-container
docker rm iam-container
docker run -d -p 8000:8000 --name iam-container anchalshivank/fc-iam-service