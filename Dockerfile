FROM python:3.11.9-slim

WORKDIR /app

COPY . /app/

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 5000

CMD ["python3", "/app/Server.py"]