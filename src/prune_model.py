
"""Apply magnitude pruning to the AutoPilot ResNet-50 model."""

from pathlib import Path

import torch
import torch.nn.utils.prune as prune

from model import AutoPilotModel


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_ROOT / "models"
OUTPUT_PATH = MODEL_DIR / "pruned_model.pth"


def main():
    """Prune the final fully connected layer and report the results."""

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    model = AutoPilotModel()
    model.eval()

    # Count original parameters in the final layer.
    layer = model.backbone.fc
    total_weights = layer.weight.numel()
    original_zeros = torch.count_nonzero(layer.weight == 0).item()

    # Remove 30% of the smallest-magnitude weights.
    prune.l1_unstructured(layer, name="weight", amount=0.3)

    zeros_after_pruning = torch.count_nonzero(
        layer.weight == 0
    ).item()

    print(f"Final layer weights: {total_weights}")
    print(f"Zeros before pruning: {original_zeros}")
    print(f"Zeros after pruning: {zeros_after_pruning}")
    print(
        f"Zero-weight percentage: "
        f"{100 * zeros_after_pruning / total_weights:.2f}%"
    )

    # Make pruning permanent before saving.
    prune.remove(layer, "weight")

    torch.save(model.state_dict(), OUTPUT_PATH)
    print(f"Pruned model saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
