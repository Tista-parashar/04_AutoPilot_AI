# Day 53: Stress Testing Report

## 1. Objective
Evaluate memory behavior during repeated image preprocessing and ONNX inference.

## 2. Test Environment
- Model: models/model.onnx
- Execution provider: ONNX Runtime CPU
- Input shape: 1 x 3 x 224 x 224
- Source: 56 validated images from data/cleaned
- Memory monitoring: psutil
- Log: logs/stress_test.log

## 3. Results
- Total images processed: 13,749
- First 20 minutes: 13,600 images processed
- Reported elapsed time: 97.12 minutes
- Final RAM: 168.87 MB
- Observed RAM range: approximately 166–170 MB
- No crash or inference error was recorded.

## 4. Observations
Memory usage remained broadly stable during the observed processing period.

The log contains a large gap between minute 20 and minute 97. Only 149 additional images were processed during this interval. Therefore, continuous execution for one hour has not been verified.

## 5. Limitations
- Live CARLA simulation was unavailable because of hardware limitations.
- Maximum live sensor-load testing was not performed.
- Existing project images were used instead of live simulator camera frames.
- The test does not establish real-world autonomous-driving performance.

## 6. Conclusion
The image-based ONNX stress test completed without a recorded crash. RAM usage showed no obvious sustained increase in the available measurements.

However, the one-hour continuous stress-test requirement remains unverified because of the interruption in the log. A continuous one-hour run is still required for full completion.
