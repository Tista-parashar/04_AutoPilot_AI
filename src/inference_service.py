"""Local HTTP inference service for the AutoPilot AI ONNX model."""

import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
from pathlib import Path

import numpy as np
import onnxruntime as ort
from PIL import Image

MODEL_PATH = Path("models/model.onnx")
HOST = "0.0.0.0"
PORT = 8000
MAX_IMAGE_BYTES = 10 * 1024 * 1024

session = None
request_count = 0
error_count = 0
inference_seconds = 0.0


def load_model():
    global session
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")
    session = ort.InferenceSession(
        str(MODEL_PATH),
        providers=["CPUExecutionProvider"],
    )


def preprocess_image(image_bytes):
    """Apply the project's RGB, resize, and normalization pipeline."""
    with Image.open(BytesIO(image_bytes)) as image:
        image = image.convert("RGB")
        image = image.resize(
            (224, 224),
            resample=Image.Resampling.BILINEAR,
        )

        array = np.asarray(image, dtype=np.float32) / 255.0
        array = (array - 0.5) / 0.5
        array = np.transpose(array, (2, 0, 1))
        return np.expand_dims(array, axis=0).astype(np.float32)


class InferenceHandler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            if session is None:
                self.send_json(503, {"status": "not_ready"})
            else:
                self.send_json(200, {"status": "ready", "model": "ONNX"})
            return

        if self.path == "/metrics":
            metrics = (
                "# HELP autopilot_inference_requests_total Total prediction requests\n"
                "# TYPE autopilot_inference_requests_total counter\n"
                f"autopilot_inference_requests_total {request_count}\n"
                "# HELP autopilot_inference_errors_total Failed prediction requests\n"
                "# TYPE autopilot_inference_errors_total counter\n"
                f"autopilot_inference_errors_total {error_count}\n"
                "# HELP autopilot_inference_seconds_total Total inference time in seconds\n"
                "# TYPE autopilot_inference_seconds_total counter\n"
                f"autopilot_inference_seconds_total {inference_seconds:.6f}\n"
            ).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4")
            self.send_header("Content-Length", str(len(metrics)))
            self.end_headers()
            self.wfile.write(metrics)
            return

        self.send_json(404, {"error": "Not found"})

    def do_POST(self):
        global request_count, error_count, inference_seconds

        if self.path != "/predict":
            self.send_json(404, {"error": "Not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_IMAGE_BYTES:
                self.send_json(400, {"error": "Invalid image size"})
                return

            image_bytes = self.rfile.read(length)
            if len(image_bytes) != length:
                self.send_json(400, {"error": "Incomplete image upload"})
                return

            image_batch = preprocess_image(image_bytes)

            start = time.perf_counter()
            input_name = session.get_inputs()[0].name
            output_name = session.get_outputs()[0].name
            result = session.run(
                [output_name],
                {input_name: image_batch},
            )[0][0]
            elapsed = time.perf_counter() - start

            request_count += 1
            inference_seconds += elapsed

            self.send_json(200, {
                "outputs": {
                    f"output_{index + 1}": float(value)
                    for index, value in enumerate(result)
                },
                "inference_time_seconds": elapsed,
                "note": "Raw model outputs; their driving meaning is not validated."
            })

        except Exception as exc:
            error_count += 1
            self.send_json(400, {
                "error": "Image processing or inference failed",
                "detail": str(exc),
            })

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")


if __name__ == "__main__":
    load_model()
    print(f"ONNX model loaded. Starting service on {HOST}:{PORT}")
    HTTPServer((HOST, PORT), InferenceHandler).serve_forever()
