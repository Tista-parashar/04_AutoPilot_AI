import os
import cv2
import numpy as np

INPUT_DIR = "data/raw"
OUTPUT_DIR = "data/features"

os.makedirs(OUTPUT_DIR, exist_ok=True)

image_extensions = (".jpg", ".jpeg", ".png")

for filename in os.listdir(INPUT_DIR):

    if not filename.lower().endswith(image_extensions):
        continue

    image_path = os.path.join(INPUT_DIR, filename)

    img = cv2.imread(image_path)

    if img is None:
        print(f"Skipping {filename}")
        continue

    img = cv2.resize(img, (256, 256))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Edge Detection
    edges = cv2.Canny(gray, 100, 200)

    # Dummy Optical Flow
    flow = np.zeros((256, 256, 2), dtype=np.float32)

    # Combine features
    combined = np.dstack([img, edges, flow])

    output_name = os.path.splitext(filename)[0] + ".npy"

    np.save(
        os.path.join(OUTPUT_DIR, output_name),
        combined
    )

    print(f"Saved: {output_name}")

print("Feature extraction completed.")
