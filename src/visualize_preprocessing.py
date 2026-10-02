import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

raw_image = "data/raw/color_0041C3_t4.jpg"
cleaned_image = "data/cleaned/t4.jpg"

original = np.array(Image.open(raw_image))
processed = np.array(Image.open(cleaned_image))

fig, axes = plt.subplots(2, 2, figsize=(10, 8))

axes[0, 0].imshow(original)
axes[0, 0].set_title("Original")

axes[0, 1].imshow(processed)
axes[0, 1].set_title("Preprocessed")

axes[1, 0].hist(original.flatten(), bins=50)
axes[1, 0].set_title("Original Pixel Distribution")

axes[1, 1].hist(processed.flatten(), bins=50)
axes[1, 1].set_title("Preprocessed Pixel Distribution")

plt.tight_layout()

os.makedirs("reports", exist_ok=True)

plt.savefig("reports/preprocess_report.png")

print("Saved: reports/preprocess_report.png")