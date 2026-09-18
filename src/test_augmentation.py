from PIL import Image
import matplotlib.pyplot as plt

from augmentations import augmentation_pipeline

image = Image.open("data/cleaned/t2.png").convert("RGB")
augmented_image = augmentation_pipeline(image)

plt.figure(figsize=(8, 4))

plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title("Original")
plt.axis("off")

plt.figure(figsize=(8, 4))

plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title("Original")
plt.axis("off")
