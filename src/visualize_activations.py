
import os
import sys

import matplotlib.pyplot as plt
import torch
from torchvision import transforms
from PIL import Image

from model import AutoPilotModel


def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_path = os.path.join(
        project_root, "data", "raw", "color_0041C3_t4.jpg"
    )
    report_dir = os.path.join(project_root, "reports")
    os.makedirs(report_dir, exist_ok=True)

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    model = AutoPilotModel()
    model.eval()

    activations = {}

    def capture_activation(module, inputs, output):
        activations["conv1"] = output.detach().cpu()

    hook = model.backbone.conv1.register_forward_hook(capture_activation)

    preprocess = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
    ])

    image = Image.open(image_path).convert("RGB")
    input_tensor = preprocess(image).unsqueeze(0)

    try:
        with torch.no_grad():
            model(input_tensor)
    finally:
        hook.remove()

    feature_maps = activations["conv1"][0]
    count = min(16, feature_maps.shape[0])

    fig, axes = plt.subplots(4, 4, figsize=(10, 10))
    for i, ax in enumerate(axes.flat):
        if i < count:
            ax.imshow(feature_maps[i], cmap="viridis")
            ax.set_title(f"Channel {i + 1}")
        ax.axis("off")

    plt.tight_layout()
    output_path = os.path.join(report_dir, "layer_activations.png")
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
