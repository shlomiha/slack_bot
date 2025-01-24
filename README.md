PhoneBook Slack Bot

A Python-based Slack bot that integrates with AWS S3 to manage a CSV file containing contact details. The bot supports adding, retrieving, and downloading records through Slack slash commands.

Features:
Add Record: Add a new contact record to the phonebook.
Retrieve Record: Fetch contact details by name.
Download PhoneBook: Download the complete phonebook as a CSV file.

Requirements:
Python Requirements
The project uses the following Python libraries:

boto3: AWS SDK for Python.
python-decouple: Securely handle environment variables.
slack-sdk: Slack API integration.
Flask: Web framework for handling Slack events.

Install dependencies using:
pip install -r requirements.txt

System Requirements:
Python 3.9 or later.
AWS S3 bucket with appropriate permissions.
Slack workspace and app configured with slash commands.

Setup

Environment Variables:
Create a .env file in the project root with the following variables:

Variable	            Description
AWS_ACCESS_KEY_ID	    Your AWS IAM access key ID.
AWS_SECRET_ACCESS_KEY	Your AWS IAM secret access key.
SLACK_API_KEY	        Your Slack bot's OAuth token.
S3_BUCKET_NAME	        Name of the S3 bucket storing the phonebook CSV file.
S3_OBJECT_KEY	        Key (path) of the phonebook CSV file in the S3 bucket.
ENVIRONMENT	            development or production (default is development).

Example .env file:

AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
SLACK_API_KEY=xoxb-your-slack-bot-token
S3_BUCKET_NAME=devopsedge-s3-bucket-for-excersice
S3_OBJECT_KEY=user2.csv
ENVIRONMENT=development

Usage

Running Locally
Install Dependencies:

pip install -r requirements.txt

Run the Flask App:

python slack_bot.py

Expose the App to Slack: Use ngrok to expose your local app to the internet:

ngrok http 3000
Configure Slack Slash Commands:

Go to your Slack app configuration and set the Request URL for slash commands (e.g., /add, /get, /download) to the ngrok HTTPS URL:

https://<your-ngrok-id>.ngrok.io/slack/events

Test Slash Commands in Slack:

/add John Doe,1234567890,john@example.com
/get John Doe
/download

Docker Setup

Dockerfile
The project includes a Dockerfile to containerize the application.

Build the Docker Image:

docker build -t phonebook-slack-bot .

Run the Container:

docker run -e AWS_ACCESS_KEY_ID=your-aws-access-key-id \
           -e AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key \
           -e SLACK_API_KEY=xoxb-your-slack-bot-token \
           -e S3_BUCKET_NAME=devopsedge-s3-bucket-for-excersice \
           -e S3_OBJECT_KEY=user2.csv \
           -e ENVIRONMENT=production \
           -p 3000:3000 phonebook-slack-bot

Docker Build Arguments
Build Argument	        Description

AWS_ACCESS_KEY_ID	    AWS access key ID for S3 operations.
AWS_SECRET_ACCESS_KEY	AWS secret access key for S3 operations.
SLACK_API_KEY	        Slack bot OAuth token.

Build the image with build arguments if needed:

docker build --build-arg AWS_ACCESS_KEY_ID=your-aws-access-key-id \
             --build-arg AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key \
             --build-arg SLACK_API_KEY=xoxb-your-slack-bot-token \
             -t phonebook-slack-bot .

Slash Commands

Command	Description	Example Usage:

/add	Adds a new record to the phonebook.	/add John,1234567890,john@example.com
/get	Retrieves details of a specific record by name.	/get John
/download	Downloads the phonebook CSV file and uploads it to Slack.	/download

Testing

Unit Tests
Unit tests are located in the tests directory. Run them using:

python -m unittest discover -s tests

Project Structure:

Slack_Bot/
├── python_library/
│   ├── __init__.py              # Library initialization
│   ├── s3_operations.py         # S3 operations (add, retrieve, download)
│   └── credentials.py           # Credential management
├── tests/
│   ├── __init__.py              # Test initialization
│   └── test_s3_operations.py    # Unit tests for S3 operations
├── slack_bot.py                 # Main Flask app for Slack integration
├── Dockerfile                   # Docker container configuration
├── requirements.txt             # Python dependencies
├── pyproject.toml               # Project metadata and packaging
└── README.md                    # Project documentation

Known Issues:
ngrok Free Tier: Public URLs change every time ngrok is restarted. Use a paid plan for a fixed subdomain.
Timeouts on Large Files: Ensure your CSV file is reasonably sized for efficient operations.
