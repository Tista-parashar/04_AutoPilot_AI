# AutoPilot AI - User Guide

## 1. Introduction

AutoPilot AI is a computer vision and machine learning project that demonstrates image-based inference using an ONNX model.

The project includes:
- Image preprocessing
- ONNX model inference
- A local HTTP inference API
- Docker deployment
- Prometheus metrics
- Grafana monitoring

**Important:** This project is an experimental software demonstration. Its model outputs have not been validated for real-world vehicle control. Do not connect it to or use it to control a real vehicle.

## 2. Requirements

- Windows 10/11
- Python 3.12 (for the local development environment)
- Docker Desktop with Docker Compose
- Git
- Project files and the ONNX model at `models/model.onnx`

## 3. Starting the Application

Open PowerShell in the project root:

```powershell
cd D:\04_AutoPilot_AI
```

Start the Docker services:

```powershell
docker compose up -d
```

Check the running containers:

```powershell
docker compose ps
```

## 4. Accessing the Services

The application and monitoring tools are available locally:

| Service | Address |
|---|---|
| Inference API | http://localhost:8001 |
| Health check | http://localhost:8001/health |
| Prometheus metrics | http://localhost:8001/metrics |
| Prometheus dashboard | http://localhost:9090 |
| Grafana dashboard | http://localhost:3000 |

Grafana's initial development login is:
- Username: `admin`
- Password: `admin`

Change the default password before continued use.

## 5. Checking Application Health

Run:

```powershell
Invoke-RestMethod http://localhost:8001/health
```

A successful response looks like:

```json
{
  "status": "ready",
  "model": "ONNX"
}
```

## 6. Making an Image Prediction

The API accepts an image through the `/predict` endpoint.

Example using an existing project image:

```powershell
Invoke-RestMethod -Uri http://localhost:8001/predict -Method Post -ContentType "image/jpeg" -InFile "data/cleaned/t14.jpg" | ConvertTo-Json -Depth 5
```

The response contains:
- Three raw model outputs
- Inference time in seconds
- A note explaining that the driving meaning of the outputs is not validated

The input image must be valid and no larger than 10 MB.

## 7. Monitoring

Open Grafana:

http://localhost:3000

Open the **AutoPilot AI Monitoring** dashboard.

The dashboard displays:
- Total inference requests
- Failed inference requests
- Total inference time

Prometheus collects metrics from the inference service.

## 8. Stopping the Application

To stop the Docker services:

```powershell
docker compose down
```

To start them again:

```powershell
docker compose up -d
```

## 9. Troubleshooting

### Application is not responding
Check the containers:

```powershell
docker compose ps
```

View application logs:

```powershell
docker compose logs autopilot-ai
```

### Model not found
Check that `models/model.onnx` exists in the project directory.

### Grafana is unavailable
Check the Grafana container:

```powershell
docker compose logs grafana
```

### Prometheus is not collecting metrics
Check the Prometheus target at:

http://localhost:9090/targets

The AutoPilot AI target should show as UP.

## 10. Limitations and Safety

- Model accuracy has not been established using labelled evaluation data.
- The model's driving outputs have not been validated.
- CARLA end-to-end vehicle simulation has not been completed.
- The HTTP service is a basic local demonstration, not a hardened production API.
- The project must not be used for real-world autonomous vehicle control.

## 11. Support

For technical details, setup instructions, API endpoints, and project architecture, refer to the Developer Guide and API Reference in the `docs` directory.
