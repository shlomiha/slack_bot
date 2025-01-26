from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bot.credentials import load_credentials
from slack_bot.s3_operations import add_record, retrieve_record, download_db
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Load credentials
credentials = load_credentials()
SLACK_API_KEY = credentials["SLACK_API_KEY"]

# Initialize Slack client
slack_client = WebClient(token=SLACK_API_KEY, timeout=120)

# Flask app for handling Slack events
app = Flask(__name__)

# Bucket and file configuration
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
OBJECT_KEY = os.getenv("S3_OBJECT_KEY")

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.form
    command = data.get("command")
    text = data.get("text", "").strip()
    channel_id = data.get("channel_id")

    logging.debug(f"Received Slack event: {data}")

    if not command:
        logging.error("No command received.")
        return jsonify({"response_type": "ephemeral", "text": "No command received. Please provide a valid command."})

    try:
        if command == "/add":
            # Add a record to S3
            try:
                name, phone, email = map(str.strip, text.split(","))
                if not (name and phone and email):
                    raise ValueError("Empty fields are not allowed.")
                add_record(BUCKET_NAME, OBJECT_KEY, [name, phone, email])
                response_message = f"Record added: Name: {name}, Phone: {phone}, Email: {email}"
            except ValueError:
                logging.error("Invalid format for /add command. Expected: Name, Phone, Email.")
                response_message = "Invalid format. Use: `Name, Phone, Email`."

        elif command == "/get":
            # Retrieve a record from S3
            if not text:
                response_message = "Please provide a name to search for."
            else:
                record = retrieve_record(BUCKET_NAME, OBJECT_KEY, text)
                if record:
                    response_message = f"Record found:\n- Name: {record[0]}\n- Phone: {record[1]}\n- Email: {record[2]}"
                else:
                    response_message = f"No record found for the name: {text}"

        elif command == "/download":
            # Download the database from S3
            try:
                local_file_path = download_db(BUCKET_NAME, OBJECT_KEY)
                logging.info(f"File downloaded to {local_file_path}")

                # Check if file exists before uploading
                if os.path.exists(local_file_path):
                    with open(local_file_path, "rb") as file_content:
                        try:
                            response = slack_client.files_upload_v2(
                                channels=channel_id,
                                file=file_content,
                                title="PhoneBook.csv",
                                filetype="csv",  # Explicitly set filetype
                                request_timeout=1200  # Increased timeout
                            )
                            logging.info(f"File uploaded successfully: {response}")
                            response_message = "PhoneBook file uploaded successfully."
                        except SlackApiError as e:
                            logging.error(f"Slack API Error during file upload: {e.response.get('error', 'Unknown error')}")
                            response_message = f"Slack API Error: {e.response.get('error', 'Unknown error')}"
                else:
                    logging.error("File does not exist. Unable to upload.")
                    response_message = "File not found. Unable to upload."
            except Exception as e:
                logging.error(f"Error during file download or upload: {e}")
                response_message = f"Error: {str(e)}"

        else:
            logging.warning(f"Invalid command received: {command}")
            response_message = "Invalid command. Supported commands: `/add`, `/get`, `/download`."

        # Send response back to Slack
        return jsonify({"response_type": "in_channel", "text": response_message})

    except Exception as e:
        logging.error(f"Unhandled error: {e}")
        return jsonify({"response_type": "ephemeral", "text": f"An error occurred: {str(e)}"})

# Run the Flask app
if __name__ == "__main__":
    app.run(port=3000)
