from decouple import config
import boto3
import json

def get_secret_from_aws(secret_name):
    """
    Fetch secrets from AWS Secrets Manager.
    """
    try:
        client = boto3.client("secretsmanager")
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response["SecretString"])
        return secret
    except Exception as e:
        raise RuntimeError(f"Error fetching secret: {e}")

def load_credentials():
    """
    Load credentials, prioritizing AWS Secrets Manager for production.
    """
    # Use environment variable to determine environment
    environment = config("ENVIRONMENT", default="development")

    if environment == "production":
        # Fetch secrets from AWS Secrets Manager
        secret_name = config("AWS_SECRET_NAME")
        secrets = get_secret_from_aws(secret_name)
        return {
            "AWS_ACCESS_KEY_ID": secrets["AWS_ACCESS_KEY_ID"],
            "AWS_SECRET_ACCESS_KEY": secrets["AWS_SECRET_ACCESS_KEY"],
            "SLACK_API_KEY": secrets["SLACK_API_KEY"]
        }
    else:
        # Load from .env file for local development
        return {
            "AWS_ACCESS_KEY_ID": config("AWS_ACCESS_KEY_ID"),
            "AWS_SECRET_ACCESS_KEY": config("AWS_SECRET_ACCESS_KEY"),
            "SLACK_API_KEY": config("SLACK_API_KEY")
        }


