from decouple import config

# Load AWS credentials
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")

# Load Slack API key
SLACK_API_KEY = config("SLACK_API_KEY")

# Load S3 bucket details
S3_BUCKET_NAME = config("S3_BUCKET_NAME")
S3_OBJECT_KEY = config("S3_OBJECT_KEY")

# Load application environment
ENVIRONMENT = config("ENVIRONMENT", default="development")
