"""Functions for cleaning and validating image data."""

import os
from PIL import Image
from torchvision import transforms

resize = transforms.Resize((256, 256))

def clean_images(input_folder, output_folder):
    """Clean images, validate them, and save resized copies.

    Args:
        input_folder: Folder containing raw images.
        output_folder: Folder where cleaned images are saved.

    Returns:
        None.
    """

    removed = 0
    processed = 0

    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)

        if not os.path.exists(file_path):
            removed += 1
            continue

        try:
            image = Image.open(file_path)
            image.verify()

            image = Image.open(file_path)
            image = resize(image)

            save_path = os.path.join(output_folder, filename)
            image.save(save_path)

            processed += 1

        except (OSError, ValueError):
            removed += 1

    print("Processed:", processed)
    print("Removed:", removed)
