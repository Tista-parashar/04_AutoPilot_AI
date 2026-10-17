# Week 6: Model Optimisation Report

## 1. Objective

The objective is to compare the performance of four model variants and select the best candidate for further integration testing.

## 2. Benchmark Results

| Model | Latency (ms) | FPS | Size (MB) | Accuracy |
|---|---:|---:|---:|---|
| ONNX | 80.85 | 12.37 | 89.62 | N/A |
| Pruned | 112.90 | 8.86 | 90.00 | N/A |
| Dynamic INT8 | 113.98 | 8.77 | 89.99 | N/A |
| Baseline | 131.57 | 7.60 | 90.00 | N/A |

Accuracy could not be measured because labelled evaluation data was unavailable.

## 3. Results

- ONNX achieved the lowest latency at 80.85 ms.
- ONNX achieved the highest throughput at 12.37 FPS.
- Pruned and Dynamic INT8 were slower than ONNX in this benchmark.
- The model sizes were similar, at approximately 90 MB.

ONNX reduced latency by approximately 38.5% compared with the baseline.

## 4. Selected Model

**Selected model: ONNX**

ONNX is selected for further integration testing because it performed best in the recorded CPU benchmark.

This selection is based on speed, not driving accuracy or safety.

## 5. Limitations

- Labelled data is required to evaluate accuracy.
- Performance may differ on other hardware.
- The model has not been validated for real-world autonomous driving.
- Further testing is required before drawing conclusions about driving performance.

## 6. Integration Plan

1. Load the ONNX model using ONNX Runtime.
2. Check that the input and output formats match the integration pipeline.
3. Compare ONNX outputs with PyTorch outputs.
4. Evaluate accuracy when suitable labelled data becomes available.
5. Record integration issues and benchmark results.

## 7. Conclusion

ONNX is the current performance winner in the recorded benchmark. It will be used as the candidate for further integration testing, subject to output validation and additional evaluation.