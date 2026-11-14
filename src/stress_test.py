from pathlib import Path
import time
import logging
import psutil
import numpy as np
import onnxruntime as ort
from PIL import Image

DURATION_SECONDS = 3600
LOG_INTERVAL = 60
IMAGE_DIR = Path("data/cleaned")
LOG_PATH = Path("logs/stress_test.log")

LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

images = sorted(
    p for p in IMAGE_DIR.iterdir()
    if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".avif"}
)

session = ort.InferenceSession(
    "models/model.onnx",
    providers=["CPUExecutionProvider"]
)

input_name = session.get_inputs()[0].name
process = psutil.Process()

def preprocess_image(path):
    with Image.open(path) as image:
        image = image.convert("RGB").resize((224, 224))
        array = np.asarray(image, dtype=np.float32) / 255.0

    array = (array - 0.5) / 0.5
    array = np.transpose(array, (2, 0, 1))
    return np.expand_dims(array, axis=0).astype(np.float32)

logging.info("===== DAY 53 IMAGE-BASED STRESS TEST STARTED =====")
logging.info("Available images: %d", len(images))
logging.info("Target duration: 60 minutes")

start_time = time.monotonic()
next_log = start_time + LOG_INTERVAL
image_count = 0
image_index = 0

try:
    while time.monotonic() - start_time < DURATION_SECONDS:
        tensor = preprocess_image(images[image_index])
        session.run(None, {input_name: tensor})

        image_count += 1
        image_index = (image_index + 1) % len(images)

        now = time.monotonic()
        if now >= next_log:
            elapsed = now - start_time
            ram_mb = process.memory_info().rss / (1024 * 1024)

            logging.info(
                "Elapsed: %.1f min | Images: %d | RAM: %.2f MB",
                elapsed / 60, image_count, ram_mb
            )
            next_log = now + LOG_INTERVAL

except KeyboardInterrupt:
    logging.warning("Test stopped manually.")

finally:
    elapsed = time.monotonic() - start_time
    final_ram = process.memory_info().rss / (1024 * 1024)

    logging.info("===== STRESS TEST FINISHED =====")
    logging.info("Duration: %.2f minutes", elapsed / 60)
    logging.info("Images processed: %d", image_count)
    logging.info("Final RAM: %.2f MB", final_ram)
