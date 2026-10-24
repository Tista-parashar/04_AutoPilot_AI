# Day 50: System-Level Test Report

## Test Summary

- Date: October 24, 2026
- Test command: `python -m pytest tests/test_system.py -v -rs`
- Total tests collected: 7
- Passed: 3
- Failed: 0
- Skipped: 4

## Tests Passed

1. Camera image preprocessing
2. ONNX model inference
3. PID control output bounds

## Tests Skipped

1. Sunny weather
2. Rainy weather
3. Night conditions
4. Heavy traffic

## Issue Identified

The CARLA server was unavailable at `127.0.0.1:2000`.
The connection attempt timed out after 3 seconds.

## Resolution Status

The local component tests passed. The four CARLA integration
tests remain unverified because the simulator is unavailable.

## Limitations

Passing preprocessing and inference tests does not establish
real-world driving accuracy or successful end-to-end vehicle control.

## Next Actions

- Restore CARLA connectivity on compatible hardware.
- Run the weather and traffic tests against a live simulator.
- Record and address any failures from those tests.