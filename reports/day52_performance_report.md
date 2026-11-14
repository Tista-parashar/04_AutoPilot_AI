# Day 52: Performance Benchmarking Report

## 1. Objective
Benchmark Baseline, Pruned, Dynamic INT8, and ONNX model variants.

## 2. Benchmark Configuration
- Device: CPU
- Input shape: (1, 3, 224, 224)
- Warm-up iterations: 5
- Benchmark iterations per model: 1000
- Metrics: Latency, FPS, process RAM, and model size

## 3. Results

| Model | Latency (ms) | FPS | Model Size (MB) |
|---|---:|---:|---:|
| Baseline | 141.76 | 7.05 | 90.00 |
| Pruned | 127.12 | 7.87 | 90.00 |
| Dynamic INT8 | 118.22 | 8.46 | 89.99 |
| ONNX | 58.24 | 17.17 | 89.62 |

## 4. Observations
- ONNX achieved the lowest average latency.
- ONNX achieved the highest measured throughput at 17.17 FPS.
- Highest reported process RAM snapshot was 521.67 MB.
- RAM measurements are process-level snapshots, not isolated per-model memory usage.

## 5. Limitations
- Benchmarks used random input and CPU execution.
- Model accuracy was not evaluated because labelled evaluation data was unavailable.
- No explicit inference performance acceptance target was found in the project documentation.
- CARLA live simulation was not performed due to hardware limitations.
- These results do not establish real-world driving performance.

## 6. Output Files
- reports/benchmark.csv
- reports/benchmark_report.txt

## 7. Conclusion
The ONNX model was the fastest variant in this CPU benchmark, with an average latency of 58.24 ms and throughput of 17.17 FPS. Compliance with a formal performance target cannot be determined because no explicit target was available.
