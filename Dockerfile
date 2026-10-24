FROM python:3.10-slim
WORKDIR /app
COPY requirements-docker.txt .
RUN pip install --no-cache-dir --timeout=60 --retries=2 -r requirements-docker.txt
COPY . .