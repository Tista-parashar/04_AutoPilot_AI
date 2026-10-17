
"""Quantise and benchmark the AutoPilot model on CPU."""

import copy
import time
from pathlib import Path

import torch
import torch.nn as nn
from torch.ao.quantization import quantize_dynamic

from model import AutoPilotModel


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_ROOT / "models"
OUTPUT_PATH = MODEL_DIR / "model_int8.pth"

WARMUP_RUNS = 5
BENCHMARK_RUNS = 20


def benchmark(model, dummy_input):
    """Measure average CPU inference time."""

    model.eval()

    with torch.inference_mode():
        for _ in range(WARMUP_RUNS):
            model(dummy_input)

        start = time.perf_counter()

        for _ in range(BENCHMARK_RUNS):
            model(dummy_input)

        elapsed = time.perf_counter() - start

    return elapsed / BENCHMARK_RUNS * 1000


def main():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    torch.manual_seed(42)

    # Load the same pretrained architecture for a fair comparison.
    original_model = AutoPilotModel().cpu().eval()
    quantized_model = copy.deepcopy(original_model)

    dummy_input = torch.randn(1, 3, 224, 224)

    baseline_ms = benchmark(original_model, dummy_input)

    # Dynamic INT8 quantisation of supported Linear layers.
    quantized_model = quantize_dynamic(
        quantized_model,
        {nn.Linear},
        dtype=torch.qint8,
    )

    quantized_ms = benchmark(quantized_model, dummy_input)

    # Save the quantised model's state dictionary.
    torch.save(quantized_model.state_dict(), OUTPUT_PATH)

    baseline_size = sum(
        p.numel() * p.element_size()
        for p in original_model.parameters()
    )
    quantized_size = OUTPUT_PATH.stat().st_size

    print(f"Baseline inference: {baseline_ms:.2f} ms")
    print(f"Quantised inference: {quantized_ms:.2f} ms")
    print(f"Baseline parameter memory: {baseline_size / 1024**2:.2f} MiB")
    print(f"Quantised checkpoint: {quantized_size / 1024**2:.2f} MiB")
    print(f"Quantised checkpoint saved: {OUTPUT_PATH}")

    if quantized_ms > 0:
        print(f"Measured speedup: {baseline_ms / quantized_ms:.2f}x")

    print(
        "Note: accuracy has not been evaluated. "
        "Real driving-control validation labels are required."
    )


if __name__ == "__main__":
    main()
