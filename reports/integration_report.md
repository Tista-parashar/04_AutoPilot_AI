# Week 7: Integration Report

## 1. Project Overview

AutoPilot AI is a Python-based autonomous-driving project designed to process camera images, generate model predictions, and calculate vehicle-control suggestions.

## 2. Integration Components

- Image preprocessing using NumPy and Pillow.
- ONNX model inference using ONNX Runtime.
- PID controllers for steering and speed-control suggestions.
- Docker packaging using a Python 3.10 base image.
- Git and GitHub for version control.

## 3. Model Deployment Metrics

| Metric | Recorded Value |
|---|---|
| Model format | ONNX |
| Model size | 89.62 MB (approximately 90 MB) |
| Inference latency | 80.85 ms |
| Approximate inference speed | 12.37 FPS |
| Accuracy | Not measured |

These metrics are recorded in the project README and optimization report. They should not be interpreted as proof of successful autonomous driving.

## 4. Testing Results

The latest automated test run produced:

- 13 tests passed.
- 4 tests skipped.
- 0 test failures.

Tests were executed using:

```powershell
$env:PYTHONPATH = "src"
python -m pytest -q
```

The ONNX model was also tested inside Docker. The model loaded successfully and completed an inference operation.

The inference smoke test used a zero-filled input tensor of shape `(1, 3, 224, 224)` and returned an output of shape `(1, 3)`.

This verifies model execution, not prediction accuracy.

## 5. Demo Video

Demo video: [Open the project demo](demo.mp4)

Note: The existing demo video is a placeholder and is not verified CARLA simulation footage.

## 6. Docker Integration Status

Docker packaging and inference verification were completed successfully.

Verified results:

- Docker image built successfully using `docker build -t autopilot:latest .`.
- Python 3.10 base image used.
- Required dependencies installed successfully.
- ONNX model included in the Docker image.
- ONNX Runtime successfully loaded the model.
- Inference executed successfully inside the container.

### Docker Build Optimization

The `.dockerignore` file was updated to exclude unnecessary development and training folders.

| Metric | Before | After |
|---|---:|---:|
| Docker build context | 3.62 GB | 5.24 KB |
| Docker build | Successful | Successful |

The optimized Docker image was rebuilt and tested successfully.

## 7. Known Limitations

- CARLA server connectivity has not been verified.
- The bridge calculates control suggestions but does not yet demonstrate a vehicle completing a driving task.
- The model was trained using zero-valued targets, so meaningful driving performance has not been established.
- Accuracy has not been measured against labelled driving data.
- End-to-end autonomous driving in CARLA remains unverified.
- The existing demo video is not verified simulation footage.

## 8. Conclusion

The project now includes ONNX model inference, image-preprocessing utilities, PID control utilities, automated tests, and successfully verified Docker packaging.

The Docker container can load the ONNX model and execute inference successfully. Automated testing also reports 13 passed tests and 4 skipped tests.

However, end-to-end CARLA simulation and real autonomous-driving performance have not been verified.

The system should therefore be described as partially integrated, with Docker packaging and model inference verified, but not yet confirmed as simulation-ready.