from decouple import config
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _load_secrets_json_(filepath: str="secrets.json") -> dict:
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise 
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON file: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error loading JSON file: {e}")
        raise

def load_credentials():
    """
    Load credentials from json file.
    """
    # Use environment variable to determine environment
    environment = config("ENVIRONMENT", default="development")
    secrets = _load_secrets_json_().get(environment, {})

    if not secrets:
        logger.error(f"No secrets found for environment: {environment}")
        raise ValueError(f"Invalid environment {environment} please check spelling.")

    return secrets
    
    



