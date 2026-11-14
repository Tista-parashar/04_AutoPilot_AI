

"""Benchmark baseline, pruned, INT8, and ONNX model variants."""

import gc
import os
import time
from pathlib import Path

import onnxruntime as ort
import pandas as pd
import psutil
import torch
import torch.nn as nn
from torch.ao.quantization import quantize_dynamic

from model import AutoPilotModel


ROOT = Path(__file__).resolve().parent.parent
MODELS = ROOT / "models"
REPORTS = ROOT / "reports"

WARMUP_RUNS = 5
BENCHMARK_RUNS = 1000
INPUT_SHAPE = (1, 3, 224, 224)

PROCESS = psutil.Process(os.getpid())


def get_memory_mb():
    """Return current process RAM usage in MB."""
    return PROCESS.memory_info().rss / (1024 * 1024)


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
    """Return average inference latency in milliseconds."""
    with torch.inference_mode():
        for _ in range(WARMUP_RUNS):
            model(sample)

        start = time.perf_counter()

        for _ in range(BENCHMARK_RUNS):
            model(sample)

        elapsed = time.perf_counter() - start

    return elapsed * 1000 / BENCHMARK_RUNS


def measure_onnx(session, sample):
    """Return average ONNX Runtime latency in milliseconds."""
    input_name = session.get_inputs()[0].name
    feed = {input_name: sample.numpy()}

    for _ in range(WARMUP_RUNS):
        session.run(None, feed)

    start = time.perf_counter()

    for _ in range(BENCHMARK_RUNS):
        session.run(None, feed)

    elapsed = time.perf_counter() - start

    return elapsed * 1000 / BENCHMARK_RUNS


def add_result(results, name, path, latency_ms,
               memory_before_mb, memory_after_mb):
    """Store benchmark metrics."""
    size_mb = path.stat().st_size / (1024 * 1024)

    results.append({
        "model": name,
        "latency_ms": round(latency_ms, 2),
        "fps": round(1000 / latency_ms, 2),
        "memory_mb": round(memory_after_mb, 2),
        "memory_increase_mb": round(
            memory_after_mb - memory_before_mb, 2
        ),
        "size_mb": round(size_mb, 2),
        "accuracy": "N/A - labelled data required",
    })


def main():
    REPORTS.mkdir(parents=True, exist_ok=True)

    torch.manual_seed(42)
    sample = torch.randn(*INPUT_SHAPE)

    results = []

    print("AUTOPILOT AI PERFORMANCE BENCHMARK")
    print("=" * 65)
    print(f"Warm-up runs: {WARMUP_RUNS}")
    print(f"Benchmark iterations per model: {BENCHMARK_RUNS}")
    print(f"Input shape: {INPUT_SHAPE}")
    print("Execution device: CPU")
    print()

    # Baseline and pruned models.
    for name, filename in [
        ("Baseline", "baseline_model.pth"),
        ("Pruned", "pruned_model.pth"),
    ]:
        gc.collect()
        memory_before = get_memory_mb()

        model = load_pytorch_model(filename)
        latency = measure_pytorch(model, sample)

        memory_after = get_memory_mb()

        add_result(
            results,
            name,
            MODELS / filename,
            latency,
            memory_before,
            memory_after,
        )

        print(f"{name} benchmark completed: {latency:.2f} ms")

        del model
        gc.collect()

    # Dynamic INT8 model.
    gc.collect()
    memory_before = get_memory_mb()

    int8_model = load_pytorch_model(
        "model_int8.pth",
        quantized=True,
    )
    int8_latency = measure_pytorch(int8_model, sample)

    memory_after = get_memory_mb()

    add_result(
        results,
        "Dynamic INT8",
        MODELS / "model_int8.pth",
        int8_latency,
        memory_before,
        memory_after,
    )

    print(f"Dynamic INT8 benchmark completed: {int8_latency:.2f} ms")

    del int8_model
    gc.collect()

    # ONNX Runtime CPU model.
    gc.collect()
    memory_before = get_memory_mb()

    onnx_path = MODELS / "model.onnx"

    session = ort.InferenceSession(
        str(onnx_path),
        providers=["CPUExecutionProvider"],
    )

    onnx_latency = measure_onnx(session, sample)
    memory_after = get_memory_mb()

    add_result(
        results,
        "ONNX",
        onnx_path,
        onnx_latency,
        memory_before,
        memory_after,
    )

    print(f"ONNX benchmark completed: {onnx_latency:.2f} ms")

    del session
    gc.collect()

    # Save CSV comparison.
    table = pd.DataFrame(results).sort_values("latency_ms")

    output_path = REPORTS / "benchmark.csv"
    table.to_csv(output_path, index=False)

    print("\nBENCHMARK RESULTS")
    print("=" * 65)
    print(table.to_string(index=False))

    print("\nPERFORMANCE SUMMARY")
    print("=" * 65)

    fastest = table.iloc[0]

    print(f"Fastest model: {fastest['model']}")
    print(f"Average latency: {fastest['latency_ms']} ms")
    print(f"FPS: {fastest['fps']}")
    print(f"Process RAM usage: {fastest['memory_mb']} MB")

    print(f"\nCSV report saved: {output_path}")
    print(
        "\nNotes:"
        "\n- Measurements are CPU benchmarks using random input."
        "\n- RAM is process RSS measured after inference."
        "\n- Memory increase is the difference from before model loading."
        "\n- Accuracy requires labelled evaluation data."
        "\n- No explicit inference performance acceptance target "
        "was found in the project documentation."
        "\n- These results do not establish real-world driving performance."
    )


if __name__ == "__main__":
    main()
