import json
import logging
import sys
import os
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

def _load_secrets_json_(filepath: str="/secrets/secrets.json") -> dict:
    """
    Load secrets from a JSON file.
    
    Args:
        filepath (str, optional): _description_. Defaults to "/secrets/secrets.json".

    Returns:
        dict: _description_
    """
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
    Load credentials from json file and export them as environment variables.
    """
    environment = os.getenv("ENVIRONMENT")
    secrets = _load_secrets_json_()
    secrets = secrets.get(environment)
    
    if not secrets:
        logger.error(f"No secrets found for environment: {environment}")
        raise ValueError(f"Invalid environment {environment} please check spelling.")
    logger.debug(f"Secrets loaded successfully for environment: {environment}")

    for key, value in secrets.items():
        os.environ[key] = value
        logger.debug(f"Exported {key} as environment variable.")

    return secrets