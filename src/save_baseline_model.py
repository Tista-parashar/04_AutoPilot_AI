
"""Save an unpruned baseline model for comparison."""

from pathlib import Path

import torch

from model import AutoPilotModel


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "models" / "baseline_model.pth"


def main():
    model = AutoPilotModel()
    torch.save(model.state_dict(), OUTPUT_PATH)

    size_mb = OUTPUT_PATH.stat().st_size / (1024 * 1024)
    print(f"Baseline model saved: {OUTPUT_PATH}")
    print(f"Baseline checkpoint size: {size_mb:.2f} MB")


if __name__ == "__main__":
    main()
