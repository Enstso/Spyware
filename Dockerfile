# Utilisez une image de base légère avec Python
FROM python:3.10-slim-bullseye
WORKDIR /app
COPY . .
# Install necessary development dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libudev-dev \
    libevdev-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pynput
RUN pip3 install pynput
RUN pip3 freeze > reqirements.txt
RUN pip install --no-cache-dir -r requirements.txt
#docker build -t spyware .
#docker run -it --rm -v $(pwd):/app spyware bash
