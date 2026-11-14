FROM python:3.10-slim

WORKDIR /app

COPY requirements-docker.txt .
RUN pip install --no-cache-dir --timeout=60 --retries=2 -r requirements-docker.txt

COPY src/ ./src/
COPY models/model.onnx ./models/model.onnx

EXPOSE 8000

CMD ["python", "-m", "src.inference_service"]
