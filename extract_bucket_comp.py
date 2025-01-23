import os

# Extract bucket name and key from S3 URL
def parse_s3_url(s3_url):
    if not s3_url.startswith("s3://"):
        raise ValueError("Invalid S3 URL. Expected format: s3://<bucket-name>/<object-key>")
    
    # Remove the 's3://' prefix and split into bucket name and key
    path_parts = s3_url.replace("s3://", "").split("/", 1)
    bucket_name = path_parts[0]
    key = path_parts[1] if len(path_parts) > 1 else None
    
    if not bucket_name or not key:
        raise ValueError("Invalid S3 URL. Both bucket name and object key must be specified.")
    
    return bucket_name, key

s3_url = "s3://devopsedge-s3-bucket-for-excersice/user2.csv"
bucket_name, key = parse_s3_url(s3_url)

