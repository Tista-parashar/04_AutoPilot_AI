# Day 46: Debugging and Tuning Report

## 1. PID Controller Tuning

Updated the steering PID controller in `src/carla_bridge.py`.

| Parameter | Previous value | Updated value |
|---|---:|---:|
| Kp | 0.5 | 0.5 |
| Ki | 0.01 | 0.01 |
| Kd | 0.05 | 0.1 |

The updated values follow the mentor's recommended starting parameters.

## 2. Inference Performance Benchmark

Benchmarked model inference on the CPU using random input tensors of shape `(1, 3, 224, 224)`.

| Model | Latency (ms) | Estimated FPS |
|---|---:|---:|
| Baseline | 159.30 | 6.28 |
| Pruned | 145.11 | 6.89 |
| Dynamic INT8 | 141.56 | 7.06 |
| ONNX | 84.37 | 11.85 |

The ONNX model achieved the lowest measured latency. Its latency was approximately 47.0% lower than the baseline in this benchmark run.

Results are hardware- and workload-dependent. These measurements do not represent full camera-to-control response time.

## 3. Camera Resolution

 Camera preprocessing remains at 224 x 224 pixels to match the model input dimensions.No resolution reduction comparison was performed.

## 4. Validation

- Python compilation passed for `src/carla_bridge.py` and `src/controller.py`.
- The model benchmark completed successfully.
- Benchmark results were saved to `reports/benchmark.csv`.
- Deprecation warnings appeared, but they did not prevent the benchmark from completing.

## 5. Limitations and Next Steps

CARLA was unavailable at `localhost:2000` during the previous simulation test. Therefore, sharp-turn testing, driving smoothness, collision rates, and route completion were not measured.

The project does not yet have verified evidence that the PID change reduces collisions. Future work requires a working CARLA simulator, a functioning vehicle-control loop, and meaningful driving labels for model evaluation.

## Conclusion

Day 46 made progress on steering PID tuning and measured local inference performance. Real-world or simulated driving improvements remain unverified until CARLA testing is operational.