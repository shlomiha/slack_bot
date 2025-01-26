#!/bin/bash

ngrok http 3000 &

python3 slack_bot.py