FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Ensure sensitive credentials are passed as environment variables
ENV ENVIRONMENT=production

# Expose port for communication with ngrok
EXPOSE 3000

CMD ["python", "slack_bot.py"]
