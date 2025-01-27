# Slack Bot

A Python-based Slack bot designed to integrate with AWS S3, facilitating seamless interactions between Slack and S3 storage.

## Table of Contents

- [Features]
- [Prerequisites]
- [Installation]
- [Configuration]
- [Usage]

## Features

- **AWS S3 Integration**: Add and retrieve records from an S3 bucket.
- **Slack Commands**: Execute commands within Slack to interact with the bot.
- **Containerized Deployment**: Run the bot in a Docker container for consistency and ease of setup.

## Prerequisites

Before setting up the Slack Bot, ensure you have the following installed on your host machine:

- **Docker Runtime**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)
- **Slack Workspace**: [Create a Slack workspace](https://slack.com/get-started)
- **ngrok Account**: To expose your local server to the internet.
- **Python 3.8 or Higher** (Optional): If you prefer to run the bot locally without Docker.

## Installation

1. Clone the Repository

    git clone https://github.com/shlomiha/slack_bot.git
    cd slack_bot

2. Create a Slack App

    Create the App:
        Navigate to the Slack API Apps page.
        Click "Create New App".
        Choose "From scratch" and provide an app name and select your workspace.

    Set Up Slash Commands:
        In your app settings, go to "Slash Commands".
        Click "Create New Command".
        Set the command (e.g., /yourcommand) and the request URL (this will be your ngrok URL plus the endpoint, e.g., https://your-ngrok-id.ngrok.io/your-endpoint).

    Enable Event Subscriptions:
        Go to "Event Subscriptions".
        Enable events and set the request URL to your ngrok URL.
        Subscribe to bot events as needed.

    Install the App:
        Go to "OAuth & Permissions".
        Configure the following Bot Token Scopes:
            commands
            chat:write
            files:read
            files:write
            channels:history
        Install the app to your workspace and note down the Bot User OAuth Token.

## Configurations

        1. Environment Variables

        Create a .env file in the root directory with the following variables:

        # S3 Bucket and Object Details
        S3_BUCKET_NAME="your-s3-bucket-name"
        S3_OBJECT_KEY="your-s3-filename"
        S3_REGION="your-s3-aws-region"

        # Application Environment
        ENVIRONMENT="your-chosen-environment"

        Replace the placeholder values with your actual credentials.

        2. Create a secrets.json file under /secrets/ directory with the following values:

            {
                "production": {
                    "AWS_ACCESS_KEY_ID": "your-aws-access-key-id-for-production",
                    "AWS_SECRET_ACCESS_KEY": "your-aws-secret-access-key-for-production",
                    "SLACK_API_KEY": "your-slack-api-key-for-production",
                    "NGROK_TOKEN": "your-ngrok-auth-token-for-production"
                },

                "development": {
                    "AWS_ACCESS_KEY_ID": "your-aws-access-key-id-for-production",
                    "AWS_SECRET_ACCESS_KEY": "your-aws-secret-access-key-for-development",
                    "SLACK_API_KEY": "your-slack-api-key-for-development",
                    "NGROK_TOKEN": "your-ngrok-auth-token-for-development"
                }
            }
        
 ## Usage:
   
        Start the Application:
            - Build and run the container:
                docker-compose up --build
            - Retrieve the ngrok URL from the containers output
            - Update the Slack app's request URL as follows  `https://<ngrok-url>/slack/events`.
	
        Slack Workspace:
            - Invite the bot to your Slack workspace in the designated application channel: `/invite @slack_bot`.
            - Use slash commands:
                - `/add <name>, <email>, <phone>` to add a contact.
                - `/get <name>` to retrieve contact details.
                - `/download to download the entire phonebook.
            - View responses directly in Slack.

Have Fun!
