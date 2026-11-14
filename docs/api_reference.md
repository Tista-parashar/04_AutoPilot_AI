# AutoPilot AI - API Reference

## 1. Overview

The AutoPilot AI inference service provides HTTP endpoints for model health checks, image prediction, and Prometheus monitoring.

**Base URL:** `http://localhost:8001`

The service runs inside Docker on port 8000 and is exposed locally on port 8001.

## 2. Health Check

### GET /health

Checks whether the ONNX model has loaded successfully.

**Successful response:**

HTTP Status: `200 OK`

```json
{
  "status": "ready",
  "model": "ONNX"
}
```

If the model is not loaded:

HTTP Status: `503 Service Unavailable`

```json
{
  "status": "not_ready"
}
```

## 3. Image Prediction

### POST /predict

Accepts image bytes and performs ONNX model inference.

**Request headers:**

```text
Content-Type: image/jpeg
```

**Request body:**

Raw image file bytes.

**Example using PowerShell:**

```powershell
Invoke-RestMethod `
  -Uri http://localhost:8001/predict `
  -Method Post `
  -ContentType "image/jpeg" `
  -InFile "data/cleaned/t14.jpg"
```

**Image processing:**

1. Convert image to RGB.
2. Resize to 224 × 224 pixels.
3. Convert pixel values to float32.
4. Normalize using `(pixel / 255 - 0.5) / 0.5`.
5. Convert to NCHW format.
6. Run ONNX inference using CPU execution.

**Successful response:**

HTTP Status: `200 OK`

```json
{
  "outputs": {
    "output_1": 0.10,
    "output_2": 0.19,
    "output_3": 0.52
  },
  "inference_time_seconds": 0.14,
  "note": "Raw model outputs; their driving meaning is not validated."
}
```

The values above are illustrative response values, not guaranteed prediction results.

**Error responses:**

| Status | Meaning |
|---|---|
| 400 | Invalid image size |
| 400 | Incomplete image upload |
| 400 | Image processing or inference failed |
| 404 | Unknown endpoint |

The maximum accepted image size is 10 MB.

## 4. Prometheus Metrics

### GET /metrics

Returns metrics in Prometheus text exposition format.

**Example:**

```text
# HELP autopilot_inference_requests_total Total prediction requests
# TYPE autopilot_inference_requests_total counter
autopilot_inference_requests_total 1

# HELP autopilot_inference_errors_total Failed prediction requests
# TYPE autopilot_inference_errors_total counter
autopilot_inference_errors_total 0

# HELP autopilot_inference_seconds_total Total inference time in seconds
# TYPE autopilot_inference_seconds_total counter
autopilot_inference_seconds_total 0.145505
```

### Available metrics

| Metric | Description |
|---|---|
| `autopilot_inference_requests_total` | Successful prediction requests |
| `autopilot_inference_errors_total` | Failed prediction requests |
| `autopilot_inference_seconds_total` | Cumulative inference time in seconds |

These counters are maintained in application memory and reset when the service restarts.

## 5. Error Handling

The API returns JSON error messages when an invalid request or inference failure occurs.

Example:

```json
{
  "error": "Invalid image size"
}
```

Inference errors may also include a `detail` field describing the underlying exception.

## 6. Monitoring Integration

Prometheus scrapes the `/metrics` endpoint every five seconds using the configuration in:

`config/prometheus.yml`

Grafana visualizes the collected metrics using the provisioned AutoPilot AI dashboard.

## 7. Important Limitations

- The API accepts raw image bytes, not JSON or multipart form uploads.
- The service does not currently provide authentication or HTTPS.
- Request concurrency and rate limiting are not implemented.
- Metrics are held in memory and are not persistent.
- Model outputs have not been validated for real-world driving decisions.
- The API is intended for local experimental use, not production vehicle control.
