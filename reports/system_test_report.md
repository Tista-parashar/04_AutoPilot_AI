# Day 50: System-Level Test Report

## 1. Test Summary

- Date: November 14, 2026
- Test command: `python -m pytest tests/test_system.py -v -rs`
- Total tests collected: 7
- Passed: 3
- Failed: 0
- Skipped: 4

## 2. Tests Passed

1. Camera image preprocessing
2. ONNX model inference
3. PID control output bounds

## 3. Tests Skipped

1. Sunny weather
2. Rainy weather
3. Night conditions
4. Heavy traffic

## 4. Issue Identified

The CARLA server was unavailable at `127.0.0.1:2000`.

All four CARLA integration tests were skipped because the connection attempt timed out after 3 seconds.

## 5. Resolution Status

- Local camera preprocessing test passed.
- ONNX model inference test passed.
- PID control output bounds test passed.
- CARLA weather and heavy-traffic scenarios remain unverified.

## 6. CARLA Hardware Limitation

Previous CARLA launch attempts on the available hardware resulted in an "Out of video memory" error.

- GPU: NVIDIA GeForce GTX 1650 Ti with 4 GB VRAM.
- CARLA server did not become available on port 2000.
- Low-quality settings and 800 x 600 resolution did not resolve the issue.

## 7. Limitations

- Actual CARLA weather testing has not been completed.
- Heavy-traffic simulation has not been verified.
- Passing local tests does not establish real-world driving accuracy.
- End-to-end autonomous vehicle control remains unverified.

## 8. Next Actions

- Run CARLA on compatible hardware with sufficient video memory.
- Repeat sunny, rainy, and night weather tests.
- Run the heavy-traffic scenario.
- Record and resolve any failures from live simulation testing.

## 9. Conclusion

The system-level test suite collected seven tests. Three local component tests passed, and four CARLA integration tests were skipped because the simulator was unavailable.

Image preprocessing, ONNX inference, and PID control output checks are verified. However, complete end-to-end autonomous driving and CARLA scenario validation remain outstanding.