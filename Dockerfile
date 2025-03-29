# Utilisez une image de base légère avec Python
FROM python:3.10-slim-bullseye

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    build-essential \
    libudev-dev \
    libevdev-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pynput

# Si tu veux rajouter d'autres dépendances :
# RUN pip install --no-cache-dir cryptography psutil requests pyfiglet

# Optionnel : Sauvegarde des dépendances
RUN pip freeze > requirements.txt

CMD ["bash"]
