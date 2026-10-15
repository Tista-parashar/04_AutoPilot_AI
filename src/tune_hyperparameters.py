
"""Optuna hyperparameter tuning for AutoPilot_AI.

Requires meaningful driving-control labels before trials can run.
"""

import json
from pathlib import Path

import optuna
import torch
import torch.nn as nn
import torch.optim as optim

from data_loader import DataLoader as ImageDataset
from model import AutoPilotModel


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = PROJECT_ROOT / "config"
PARAMS_PATH = CONFIG_DIR / "best_params.json"


def objective(trial):
    """Tune hyperparameters after valid driving labels are available."""

    # Do not tune a model using fabricated targets.
    raise RuntimeError(
        "Tuning paused: provide real driving-control labels "
        "and update the dataset loading code before running trials."
    )


def main():
    """Check prerequisites and run Optuna when data is ready."""

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    print("AutoPilot_AI hyperparameter tuning")
    print(f"Optuna version: {optuna.__version__}")
    print(f"PyTorch version: {torch.__version__}")
    print(f"Dataset directory: {DATA_DIR}")
    print(f"Output file: {PARAMS_PATH}")

    print(
        "\nTrials have not been started. Real driving labels "
        "must be connected before hyperparameters can be evaluated."
    )


if __name__ == "__main__":
    main()
