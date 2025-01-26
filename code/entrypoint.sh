#!/bin/bash

NGROK_TOKEN=$(jq -r --arg env "$ENVIRONMENT" '.[$env].NGROK_TOKEN' /secrets/secrets.json)

ngrok config add-authtoken $NGROK_TOKEN
ngrok http 3000 &

python3 slack_bot.py