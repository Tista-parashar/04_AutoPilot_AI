# Week 7: Integration Report

## 1. Project Overview

AutoPilot AI is a Python-based autonomous-driving project intended to process camera images, predict model outputs, and calculate vehicle-control suggestions.

## 2. Integration Components

- Image preprocessing using NumPy and Pillow.
- ONNX model inference using ONNX Runtime.
- PID controllers for steering and speed-control suggestions.
- Docker packaging using a Python 3.10 base image.

## 3. Model Deployment Metrics

| Metric | Recorded Value |
|---|---|
| Model format | ONNX |
| Model size | 89.62 MB |
| Inference latency | 80.85 ms |
| Approximate inference speed | 12.37 FPS |
| Accuracy | Not measured |

These metrics are recorded in the project README. They should not be interpreted as proof of successful autonomous driving.

## 4. Testing Results

A previous automated test run reported 10 passed tests and 8 warnings. The tests must be rerun after the latest changes to `src/carla_bridge.py` before these results can be treated as current validation.

The ONNX model was previously loaded for inference testing. This does not establish that its predictions are accurate for real driving.

## 5. Demo Video

Demo video: [Open the project demo](demo.mp4)

Note: The existing demo video is a placeholder and is not verified CARLA simulation footage.

## 6. Docker Integration Status

The Docker build context was reduced from approximately 3.57 GB to around 20 KB by adding exclusions to `.dockerignore`.

The Docker build has not yet completed successfully. Package downloads repeatedly timed out from inside Docker. Linux-compatible dependencies have subsequently been downloaded into the local `wheelhouse` directory, but an offline Docker build has not yet been completed or tested.

## 7. Known Limitations

- CARLA server connectivity has not been verified.
- The bridge calculates control suggestions but does not itself demonstrate a vehicle completing a driving task.
- The model was trained using zero-valued targets, so meaningful driving performance has not been established.
- Accuracy has not been measured against labelled driving data.
- The latest bridge changes still require automated testing and inference validation.

## 8. Conclusion

The project has an ONNX inference component, image-preprocessing utilities, PID control utilities, and initial Docker packaging work. However, successful container execution and end-to-end CARLA simulation remain outstanding validation tasks.

The system should be described as partially integrated and not yet verified as simulation-ready.
