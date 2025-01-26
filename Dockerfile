FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl \
                                        gpg && apt clean

COPY ./code .

RUN pip install -r requirements.txt

RUN chmod +x ngrok_install.sh
RUN ./ngrok_install.sh

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
