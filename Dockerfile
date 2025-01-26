FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV ENVIRONMENT="development"
ENV S3_BUCKET_NAME="devopsedge-s3-bucket-for-excersice"
ENV S3_OBJECT_KEY="user2.csv"
ENV S3_REGION="us-east-2"

EXPOSE 3000

CMD ["python3", "slack_bot.py"]
