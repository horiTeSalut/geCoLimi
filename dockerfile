FROM python:3.9-slim

# Instalacja Chrome i sterowników
RUN apt-get update && apt-get install -y \
    wget gnupg unzip \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Instalacja bibliotek Python
RUN pip install selenium webdriver-manager

WORKDIR /app
COPY bot_legimi.py .

# Uruchomienie skryptu
CMD ["python", "bot_legimi.py"]
