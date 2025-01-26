from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bot.credentials import load_credentials
from slack_bot.s3_operations import add_record, retrieve_record, download_db
import os

# Load credentials
credentials = load_credentials()
SLACK_API_KEY = credentials["SLACK_API_KEY"]

# Initialize Slack client
slack_client = WebClient(token=SLACK_API_KEY)

# Flask app for handling Slack events
app = Flask(__name__)

# Bucket and file configuration
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
OBJECT_KEY = os.getenv("S3_OBJECT_KEY")

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.form
    command = data.get("command")
    text = data.get("text")
    response_url = data.get("response_url")

    try:
        if command == "/add":
            name, phone, email = text.split(",")
            add_record(BUCKET_NAME, OBJECT_KEY, [name.strip(), phone.strip(), email.strip()])
            response_message = f"Record added: {name}, {phone}, {email}"

        elif command == "/get":
            name = text.strip()
            record = retrieve_record(BUCKET_NAME, OBJECT_KEY, name)
            if record:
                response_message = f"Record found: Name: {record[0]}, Phone: {record[1]}, Email: {record[2]}"
            else:
                response_message = f"No record found for name: {name}"

        elif command == "/download":
            local_file_path = download_db(BUCKET_NAME, OBJECT_KEY)

            if not os.path.exists(local_file_path):
                raise FileNotFoundError(f"File not found: {local_file_path}")

            slack_client.files_upload_v2(
                channels=data.get("channel_id"),
                file=local_file_path,
                title="PhoneBook.csv",
                request_timeout=300
            )
            response_message = "PhoneBook file uploaded successfully."

        else:
            response_message = "Invalid command."

        # Send response back to Slack
        return jsonify({"response_type": "in_channel", "text": response_message})

    except SlackApiError as e:
        return jsonify({"response_type": "ephemeral", "text": f"Slack API Error: {e.response['error']}"})
    except Exception as e:
        return jsonify({"response_type": "ephemeral", "text": f"Error: {str(e)}"})

# Run the Flask app
if __name__ == "__main__":
    app.run(port=3000)
