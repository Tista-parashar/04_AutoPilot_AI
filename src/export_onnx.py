
"""Export AutoPilot ResNet-50 to ONNX and verify CPU inference."""

import time
from pathlib import Path

import numpy as np
import onnx
import onnxruntime as ort
import torch

from model import AutoPilotModel


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_ROOT / "models"
ONNX_PATH = MODEL_DIR / "model.onnx"


def main():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    torch.manual_seed(42)

    model = AutoPilotModel().cpu().eval()
    dummy = torch.randn(1, 3, 224, 224)

    # Export with names expected by ONNX Runtime.
    with torch.inference_mode():
        torch.onnx.export(
            model,
            dummy,
            str(ONNX_PATH),
            input_names=["input"],
            output_names=["output"],
            opset_version=17,
        )

        torch_output = model(dummy).numpy()

    # Check the exported ONNX graph.
    onnx_model = onnx.load(str(ONNX_PATH))
    onnx.checker.check_model(onnx_model)

    # Run inference using ONNX Runtime on CPU.
    session = ort.InferenceSession(
        str(ONNX_PATH),
        providers=["CPUExecutionProvider"],
    )

    ort_output = session.run(
        ["output"],
        {"input": dummy.numpy()},
    )[0]

    max_difference = float(
        np.max(np.abs(torch_output - ort_output))
    )

    print(f"ONNX file: {ONNX_PATH}")
    print(f"ONNX file size: {ONNX_PATH.stat().st_size / 1024**2:.2f} MiB")
    print(f"PyTorch output shape: {torch_output.shape}")
    print(f"ONNX output shape: {ort_output.shape}")
    print(f"Maximum absolute output difference: {max_difference:.8f}")
    print(f"Outputs close: {np.allclose(torch_output, ort_output, rtol=1e-3, atol=1e-4)}")

    # Warm up both runtimes before timing.
    with torch.inference_mode():
        for _ in range(5):
            model(dummy)

    for _ in range(5):
        session.run(["output"], {"input": dummy.numpy()})

    runs = 20

    start = time.perf_counter()
    with torch.inference_mode():
        for _ in range(runs):
            model(dummy)
    pytorch_ms = (time.perf_counter() - start) * 1000 / runs

    start = time.perf_counter()
    for _ in range(runs):
        session.run(["output"], {"input": dummy.numpy()})
    onnx_ms = (time.perf_counter() - start) * 1000 / runs

    print(f"PyTorch CPU inference: {pytorch_ms:.2f} ms")
    print(f"ONNX Runtime CPU inference: {onnx_ms:.2f} ms")
    print(f"ONNX speedup: {pytorch_ms / onnx_ms:.2f}x")


if __name__ == "__main__":
    main()
