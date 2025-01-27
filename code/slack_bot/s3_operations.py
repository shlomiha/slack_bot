import boto3
import csv
import io
import os
from botocore.exceptions import NoCredentialsError, ClientError
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def add_record(bucket_name: str, object_key: str, new_row: list): 
    """
    Adds a new row to the CSV file stored in S3.
    Args:
        bucket_name (str): The S3 bucket name.
        object_key (str): The S3 object key (file path).
        new_row (list): The new row to append.
    """
    s3_client = boto3.client('s3', region_name=os.getenv("S3_REGION"))
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        csv_content = response['Body'].read().decode('utf-8')

        output = io.StringIO()
        writer = csv.writer(output)
        reader = csv.reader(io.StringIO(csv_content))
        for row in reader:
            writer.writerow(row)
        writer.writerow(new_row)

        s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=output.getvalue())
        logging.info("Record added successfully!")

    except (NoCredentialsError, ClientError) as e:
        logging.error(f"Error in add_record: {e}")
        raise

def retrieve_record(bucket_name: str, object_key: str, name: str) -> list:
    """
    Retrieve a record by name from the CSV file stored in S3.
    Args:
        bucket_name (str): The S3 bucket name.
        object_key (str): The S3 object key (file path).
        name (str): The name to search for.
    Returns:
        list: The matching record or None if not found.
    """
    s3_client = boto3.client('s3', region_name=os.getenv("S3_REGION"))
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        csv_content = response['Body'].read().decode('utf-8')

        reader = csv.reader(io.StringIO(csv_content))
        for row in reader:
            if row[0].strip().lower() == name.strip().lower():
                logging.info(f"Record found: {row}")
                return row

        logging.warning("Record not found.")
        return None

    except (NoCredentialsError, ClientError) as e:
        logging.error(f"Error in retrieve_record: {e}")
        raise

def download_db(bucket_name: str, object_key: str, local_file=None):
    """
    Download the CSV file from S3 to the local system.
    Args:
        bucket_name (str): The S3 bucket name.
        object_key (str): The S3 object key (file path).
        local_file (str, optional): Path to save the downloaded file locally. 
                                    If not provided, the object_key will be used as the filename.
    Returns:
        str: The local file path where the file was saved.
    """
    if not bucket_name or not object_key:
        raise ValueError("Both bucket_name and object_key must be provided.")

    s3_client = boto3.client('s3', region_name=os.getenv("S3_REGION"))
    try:
        local_file = local_file or os.path.basename(object_key)
        if os.path.exists(local_file):
            logging.warning(f"File {local_file} already exists. It will be overwritten.")

        s3_client.download_file(Bucket=bucket_name, Key=object_key, Filename=local_file)
        logging.info(f"File downloaded successfully to {local_file}")
        return local_file

    except (NoCredentialsError, ClientError) as e:
        logging.error(f"Error in download_db: {e}")
        raise
