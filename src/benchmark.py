
"""Benchmark baseline, pruned, INT8, and ONNX model variants."""

import copy
import time
from pathlib import Path

import numpy as np
import onnxruntime as ort
import pandas as pd
import torch
import torch.nn as nn
from torch.ao.quantization import quantize_dynamic

from model import AutoPilotModel


ROOT = Path(__file__).resolve().parent.parent
MODELS = ROOT / "models"
REPORTS = ROOT / "reports"

WARMUP_RUNS = 5
BENCHMARK_RUNS = 20
INPUT_SHAPE = (1, 3, 224, 224)


def load_pytorch_model(checkpoint, quantized=False):
    """Build the correct architecture and load its state dictionary."""
    model = AutoPilotModel().cpu().eval()

    if quantized:
        model = quantize_dynamic(
            model, {nn.Linear}, dtype=torch.qint8
        )

    state = torch.load(
        MODELS / checkpoint,
        map_location="cpu",
        weights_only=True,
    )
    model.load_state_dict(state)
    return model.eval()


def measure_pytorch(model, sample):
    """Return mean latency in milliseconds."""
    with torch.inference_mode():
        for _ in range(WARMUP_RUNS):
            model(sample)

        start = time.perf_counter()
        for _ in range(BENCHMARK_RUNS):
            model(sample)
        elapsed = time.perf_counter() - start

    return elapsed * 1000 / BENCHMARK_RUNS


def measure_onnx(session, sample):
    """Return mean ONNX Runtime latency in milliseconds."""
    input_name = session.get_inputs()[0].name
    feed = {input_name: sample.numpy()}

    for _ in range(WARMUP_RUNS):
        session.run(None, feed)

    start = time.perf_counter()
    for _ in range(BENCHMARK_RUNS):
        session.run(None, feed)
    elapsed = time.perf_counter() - start

    return elapsed * 1000 / BENCHMARK_RUNS


def add_result(results, name, path, latency_ms):
    """Record benchmark metrics without inventing accuracy."""
    size_mb = path.stat().st_size / (1024 * 1024)

    results.append({
        "model": name,
        "latency_ms": round(latency_ms, 2),
        "fps": round(1000 / latency_ms, 2),
        "size_mb": round(size_mb, 2),
        "accuracy": "N/A - labelled data required",
    })


def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    torch.manual_seed(42)
    sample = torch.randn(*INPUT_SHAPE)

    results = []

    # Baseline and pruned state dictionaries.
    for name, filename in [
        ("Baseline", "baseline_model.pth"),
        ("Pruned", "pruned_model.pth"),
    ]:
        model = load_pytorch_model(filename)
        latency = measure_pytorch(model, sample)
        add_result(results, name, MODELS / filename, latency)
        print(f"{name}: {latency:.2f} ms")

    # Reconstruct the dynamic INT8 architecture before loading its weights.
    int8_model = load_pytorch_model(
        "model_int8.pth", quantized=True
    )
    int8_latency = measure_pytorch(int8_model, sample)
    add_result(
        results,
        "Dynamic INT8",
        MODELS / "model_int8.pth",
        int8_latency,
    )
    print(f"Dynamic INT8: {int8_latency:.2f} ms")

    # ONNX Runtime CPU inference.
    onnx_path = MODELS / "model.onnx"
    session = ort.InferenceSession(
        str(onnx_path),
        providers=["CPUExecutionProvider"],
    )
    onnx_latency = measure_onnx(session, sample)
    add_result(results, "ONNX", onnx_path, onnx_latency)
    print(f"ONNX: {onnx_latency:.2f} ms")

    table = pd.DataFrame(results).sort_values("latency_ms")
    output_path = REPORTS / "benchmark.csv"
    table.to_csv(output_path, index=False)

    print("\nBenchmark comparison:")
    print(table.to_string(index=False))
    print(f"\nCSV saved: {output_path}")
    print(
        "\nNote: timings use random inputs and are CPU benchmarks. "
        "Accuracy is unavailable without labelled evaluation data. "
        "Fastest inference does not automatically mean best model."
    )


if __name__ == "__main__":
    main()
