"""Functions for loading raw project data."""

import glob
import json
import os


def load_data(data_directory):
    """Load images, labels, and metadata from a data directory.

    Args:
        data_directory: Path to the directory containing raw data.

    Returns:
        A dictionary containing images, labels, and metadata.
    """
    image_patterns = [
        os.path.join(data_directory, "**", "*.jpg"),
        os.path.join(data_directory, "**", "*.jpeg"),
        os.path.join(data_directory, "**", "*.png"),
    ]

    images = []

    for pattern in image_patterns:
        images.extend(glob.glob(pattern, recursive=True))

    labels = {}
    metadata = {}

    json_files = glob.glob(
        os.path.join(data_directory, "**", "*.json"),
        recursive=True
    )

    for json_file in json_files:
        with open(json_file, "r", encoding="utf-8") as file:
            annotations = json.load(file)
            labels[json_file] = annotations

    return {
        "images": images,
        "labels": labels,
        "metadata": metadata,
    }
