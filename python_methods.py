import boto3
import csv
import io
from botocore.exceptions import NoCredentialsError, ClientError

# Initialize S3 client
s3_client = boto3.client('s3')

def add_record(bucket_name, object_key, new_row):
    """
    Add a new row to the CSV file stored in S3.
    Args:
        bucket_name (str): The S3 bucket name.
        object_key (str): The S3 object key (file path).
        new_row (list): The new row to append.
    """
    try:
        # Fetch the existing file
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        csv_content = response['Body'].read().decode('utf-8')

        # Read existing rows
        existing_rows = list(csv.reader(io.StringIO(csv_content)))

        # Append the new row
        existing_rows.append(new_row)

        # Write updated content back to S3
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerows(existing_rows)
        output.seek(0)

        s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=output.getvalue())
        print("Record added successfully!")
    except NoCredentialsError:
        print("AWS credentials are missing.")
    except ClientError as e:
        print(f"Failed to add record: {e}")

def retrieve_record(bucket_name, object_key, name):
    """
    Retrieve a record by name from the CSV file stored in S3.
    Args:
        bucket_name (str): The S3 bucket name.
        object_key (str): The S3 object key (file path).
        name (str): The name to search for.
    Returns:
        list: The matching record or None if not found.
    """
    try:
        # Fetch the existing file
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        csv_content = response['Body'].read().decode('utf-8')

        # Read existing rows
        existing_rows = list(csv.reader(io.StringIO(csv_content)))

        # Search for the record by name
        for row in existing_rows:
            if row[0].strip().lower() == name.strip().lower():  # Assuming name is in the first column
                return row

        print("Record not found.")
        return None
    except NoCredentialsError:
        print("AWS credentials are missing.")
    except ClientError as e:
        print(f"Failed to retrieve record: {e}")

def download_db(bucket_name, object_key, local_file):
    """
    Download the CSV file from S3 to the local system.
    Args:
        bucket_name (str): The S3 bucket name.
        object_key (str): The S3 object key (file path).
        local_file (str): Path to save the downloaded file locally.
    """
    try:
        s3_client.download_file(Bucket=bucket_name, Key=object_key, Filename=local_file)
        print(f"File downloaded successfully to {local_file}")
    except NoCredentialsError:
        print("AWS credentials are missing.")
    except ClientError as e:
        print(f"Failed to download file: {e}")
