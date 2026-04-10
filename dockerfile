FROM python:3.9-slim

# Instalacja zależności systemowych dla Chrome
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl \
    && curl -sSL https://google.com | apt-key add - \
    && echo "deb [arch=amd64] http://google.com stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Instalacja bibliotek Python
RUN pip install selenium webdriver-manager requests

WORKDIR /app
COPY bot_legimi.py .

CMD ["python", "bot_legimi.py"]
