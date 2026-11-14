# AutoPilot AI - Comprehensive Test Report

## 1. Project Overview

**Project:** AutoPilot AI  
**Purpose:** Image-based autonomous-driving model and vehicle-control suggestions.  
**Report:** Day 54 - Test Documentation, updated with Day 55 Regression Testing

## 2. Test Environment

- Operating System: Windows
- Python: 3.12.10
- Virtual Environment: venv
- Testing Framework: pytest 9.1.1
- ONNX Runtime: CPU Execution Provider
- Model: models/model.onnx
- Model Input: [1, 3, 224, 224]
- Model Output: [1, 3]

## 3. Test Modules and Test Cases

### 3.1 Data Tests - tests/test_data.py

| Test Case | Purpose |
|---|---|
| test_train_split_exists | Checks training split availability |
| test_val_split_exists | Checks validation split availability |
| test_test_split_exists | Checks testing split availability |
| test_split_files_are_valid | Checks validity of split files |

### 3.2 Model Tests - tests/test_model.py

| Test Case | Purpose |
|---|---|
| test_model_initialization | Checks model initialization |
| test_forward_pass | Checks model forward pass |
| test_cuda_availability | Checks CUDA availability |

### 3.3 Preprocessing Tests - tests/test_preprocess.py

| Test Case | Purpose |
|---|---|
| test_preprocessed_shape | Checks preprocessed image dimensions |
| test_normalized_range | Checks normalized value range |

### 3.4 System Tests - tests/test_system.py

| Test Case | Purpose |
|---|---|
| test_camera_preprocessing | Checks camera image preprocessing |
| test_onnx_inference | Checks ONNX model inference |
| test_control_suggestions_are_bounded | Checks control output boundaries |
| test_carla_weather_scenario | Tests CARLA weather scenarios |
| test_carla_heavy_traffic_scenario | Tests heavy traffic scenarios |

The weather test is parameterized for sunny, rainy and night conditions.

## 4. Test Execution Results

### 4.1 Previously Recorded Full Test Run

- Passed: 13
- Skipped: 4
- Failed: 0

This is an earlier recorded result, separate from the Day 55 regression run.

### 4.2 Day 54 Latest Test Attempt

- Command: `pytest -v`
- Tests collected: 0
- Execution time: 258.91 seconds
- Result: Interrupted using KeyboardInterrupt
- This attempt did not complete and is not counted as a successful test run.

### 4.3 Day 55 Regression Test Run

**Command executed:**

`python -m pytest tests/ -v`

**Results:**

| Metric | Result |
|---|---:|
| Tests collected | 16 |
| Passed | 12 |
| Skipped | 4 |
| Failed | 0 |
| Execution time | 22.30 seconds |

**Passed test groups:**
- Data split availability and file validation
- Model initialization and forward pass
- CUDA availability check
- Image preprocessing shape and normalization
- Camera image preprocessing
- ONNX inference
- Bounded control suggestions

**Skipped tests:**
- Sunny weather scenario
- Rainy weather scenario
- Night weather scenario
- Heavy traffic scenario

The four skipped tests are CARLA-related scenarios. Live CARLA simulation was not available in the current environment, so these results must not be interpreted as successful live simulator tests.

**Regression test outcome:** All 12 tests that executed passed, with no failures. All 16 collected test cases were accounted for.

### 4.4 Pytest Invocation Note

The mentor-provided command `pytest tests/ --regression` was checked, but the installed pytest environment does not expose a `--regression` option.

The standalone `pytest` executable also encountered a collection import error for `src.carla_bridge`. The module imported successfully through the active Python interpreter, and running pytest with `python -m pytest` collected and executed the full test suite successfully.

The successful Day 55 result is therefore associated with the exact command `python -m pytest tests/ -v`.

### 4.5 Additional Verification

- 56 cleaned images validated successfully.
- ONNX model loaded successfully.
- Model input and output shapes verified.
- Image-based stress test completed, but uninterrupted one-hour execution was not established.
- RAM remained approximately 166-170 MB during recorded stress-test observations.

## 5. Test Evidence and Screenshots

Available evidence:
- Test source files in the tests/ directory.
- Day 55 terminal output showing 12 passed and 4 skipped.
- ONNX model verification output.
- logs/stress_test.log
- reports/day53_stress_test_report.md
- reports/benchmark_report.txt
- reports/benchmark.csv

Screenshots:
No separate screenshots were captured for this report. The terminal output and log files are retained as test evidence.

## 6. Known Issues and Limitations

1. CARLA simulator could not be executed because of hardware and environment limitations.
2. Live CARLA camera and maximum sensor-load testing remain unverified.
3. Four CARLA-related tests were skipped in the Day 55 regression run.
4. The Day 54 latest pytest attempt was interrupted during collection; it is not a successful test result.
5. The standalone pytest executable encountered an import-path issue. The active Python interpreter successfully ran the tests using `python -m pytest`.
6. Model accuracy on real driving data has not been established.
7. The training targets used during earlier model training were zero-valued, so successful inference does not establish driving accuracy.
8. Continuous one-hour stress-test execution was not verified because the stress-test log contains a long interruption.

## 7. Overall Assessment

The Day 55 regression run collected all 16 test cases. Twelve tests passed, four CARLA-related tests were skipped, and no tests failed.

The successful tests provide evidence of software-level verification for data handling, model operations, preprocessing, ONNX inference and bounded control suggestions.

However, skipped simulator scenarios, live CARLA integration, continuous sensor-load testing and real driving accuracy remain outstanding limitations.

## 8. Conclusion

The AutoPilot AI project has a documented test structure covering its major software components. The Day 55 regression run completed with 12 passed, 4 skipped and 0 failed.

The regression results support the stability of the tested software components in this environment. They do not establish complete autonomous-driving system validation because live CARLA scenarios and model accuracy on representative labelled driving data remain unverified.
