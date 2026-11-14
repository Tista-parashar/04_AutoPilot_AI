# AutoPilot AI - Deployment Documentation

## 1. Overview

This project provides a local Docker-based deployment of the AutoPilot AI ONNX inference service with Prometheus monitoring and Grafana dashboards.

This is a controlled software demonstration, not a production autonomous-driving deployment.

## 2. Architecture

The deployment contains three services:

- **AutoPilot AI:** Runs the ONNX model and provides HTTP inference.
- **Prometheus:** Collects inference metrics.
- **Grafana:** Displays monitoring dashboards.

## 3. Deployment Requirements

- Docker Desktop
- Docker Compose
- ONNX model: `models/model.onnx`
- Docker dependencies: `requirements-docker.txt`

## 4. Build and Start

Build and start all services:

```powershell
docker compose up -d --build
```

Check service status:

```powershell
docker compose ps
```

Validate configuration:

```powershell
docker compose config
```

## 5. Service URLs

| Service | URL |
|---|---|
| AutoPilot AI | http://localhost:8001 |
| Health Check | http://localhost:8001/health |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

## 6. API Endpoints

### Health Check

- Method: GET
- Endpoint: `/health`
- Checks whether the ONNX model is loaded.

### Prediction

- Method: POST
- Endpoint: `/predict`
- Accepts an image and returns three raw model outputs and inference time.

Example:

```powershell
Invoke-RestMethod -Uri http://localhost:8001/predict -Method Post -ContentType "image/jpeg" -InFile "data/cleaned/t14.jpg"
```

The outputs have not been validated as driving commands.

### Metrics

- Method: GET
- Endpoint: `/metrics`
- Exposes request count, error count and total inference time.

## 7. Monitoring

Prometheus collects metrics from the AutoPilot AI service every 5 seconds.

Grafana uses Prometheus as its default data source.

The **AutoPilot AI Monitoring** dashboard displays:

- Total inference requests
- Failed inference requests
- Total inference time

Dashboard URL:

http://localhost:3000/d/autopilot-monitor/autopilot-ai-monitoring

## 8. Verification Results

The following checks were completed:

- Docker image built successfully.
- Docker Compose services started successfully.
- Health endpoint returned `ready`.
- Image prediction request returned three outputs.
- Prometheus target reported `up`.
- Prometheus recorded one inference request.
- Error counter reported zero errors.
- Grafana health endpoint responded successfully.
- Prometheus data source was provisioned.
- Grafana dashboard was registered.

A test image was used to verify the API pipeline. It was not road-camera footage.

## 9. Security and Limitations

- Services are bound to localhost and are not intended for public exposure.
- Change the default Grafana admin password before further use.
- The inference service uses Python's basic HTTP server and lacks production-grade authentication, TLS, rate limiting and concurrency handling.
- Model accuracy and driving performance have not been validated.
- Training used zero-valued targets, so meaningful prediction quality cannot be established.
- CARLA simulator testing was skipped because of hardware and setup limitations.
- The system is not approved for autonomous-driving deployment.

## 10. Stop and Restart

Stop all services:

```powershell
docker compose down
```

Start services:

```powershell
docker compose up -d
```

Check logs:

```powershell
docker compose logs
```

## 11. Conclusion

The local Docker deployment and monitoring pipeline were successfully demonstrated. The inference API, Prometheus metrics collection and Grafana dashboard were verified.

Further model validation, realistic simulation testing and production security work are required before any real-world driving application.
