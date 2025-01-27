#!/bin/bash

NGROK_TOKEN=$(jq -r --arg env "$ENVIRONMENT" '.[$env].NGROK_TOKEN' /secrets/secrets.json)

ngrok config add-authtoken $NGROK_TOKEN
ngrok http 3000 &

echo "Waiting for ngrok to initialize..."
sleep 5

NGROK_URL=$(curl --silent http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')

echo $NGROK_URL

python3 slack_bot.py