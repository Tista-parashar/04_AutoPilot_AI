@'
# AutoPilot AI - Comprehensive Test Report

## 1. Project Overview
**Project:** AutoPilot AI  
**Purpose:** Image-based autonomous-driving model and vehicle-control suggestions.  
**Report:** Day 54 - Test Documentation

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

## 4. Test Execution Results

### Previously Recorded Full Test Run
- Passed: 13
- Skipped: 4
- Failed: 0

### Latest Test Attempt
- Command: pytest -v
- Tests collected: 0
- Execution time: 258.91 seconds
- Result: Interrupted using KeyboardInterrupt
- This attempt did not complete and is not counted as a successful test run.

### Additional Verification
- 56 cleaned images validated successfully.
- ONNX model loaded successfully.
- Model input and output shapes verified.
- Image-based stress test completed without a recorded crash.
- RAM remained approximately 166-170 MB during recorded observations.

## 5. Test Evidence and Screenshots

Available evidence:
- Test source files in the tests/ directory.
- Previously recorded pytest results.
- ONNX model verification output.
- logs/stress_test.log
- reports/day53_stress_test_report.md
- reports/benchmark_report.txt
- reports/benchmark.csv

Screenshots:
No separate screenshots were captured for this report. Existing terminal outputs and log files are retained as test evidence.

## 6. Known Issues and Limitations

1. CARLA simulator could not be executed because of hardware limitations.
2. Live CARLA camera and maximum sensor-load testing remain unverified.
3. Four tests were skipped in the previously recorded full test run.
4. The latest pytest attempt was interrupted during collection.
5. Model accuracy on real driving data has not been established.
6. The training targets used during earlier model training were zero-valued, so successful inference does not establish driving accuracy.
7. Continuous one-hour stress-test execution was not verified because the log contains a long interruption.

## 7. Overall Assessment

The project contains data, model, preprocessing and system-level test modules. Previous test records show 13 passed, 4 skipped and 0 failed.

Additional ONNX loading, image validation and benchmarking checks have also been performed.

However, live CARLA integration, real sensor-load testing and model accuracy validation remain limitations.

## 8. Conclusion

AutoPilot AI has a documented testing structure covering its major software components. Existing test results and supporting logs provide evidence of software-level verification.

Further testing with a compatible CARLA environment and representative labelled driving data is required before claiming complete autonomous-driving system validation.
'@ | Set-Content -Path reports/test_report.md -Encoding UTF8
