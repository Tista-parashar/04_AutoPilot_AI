# AutoPilot AI

An experimental computer vision and machine learning project for image-based autonomous driving research. The project includes image preprocessing, ONNX inference, a local HTTP API, Docker deployment, and monitoring with Prometheus and Grafana.

> **Safety notice:** This project is an experimental software demonstration. Model accuracy and driving performance have not been validated. It must not be used to control real vehicles.

## Documentation

| Document | Description |
|---|---|
| [User Guide](docs/user_guide.md) | Installation, running the application, predictions, and monitoring |
| [Developer Guide](docs/developer_guide.md) | Development setup, architecture, testing, and deployment |
| [API Reference](docs/api_reference.md) | HTTP endpoints, request formats, responses, and metrics |
## Project Features

- Image cleaning and preprocessing
- Dataset exploration and preparation
- Deep learning model development using PyTorch
- ONNX model export and CPU inference
- Image-based inference through a local HTTP API
- Docker containerization and Docker Compose
- Prometheus metrics collection
- Grafana monitoring dashboard
- Automated testing and regression checks

## Technology Stack

- Python
- PyTorch and Torchvision
- NumPy and Pandas
- Scikit-learn
- OpenCV and Pillow
- ONNX and ONNX Runtime
- Docker and Docker Compose
- Prometheus and Grafana
- Git and GitHub

## Project Structure

```text
04_AutoPilot_AI/
├── config/
│   ├── grafana/
│   │   ├── dashboards/
│   │   └── provisioning/
│   └── prometheus.yml
├── data/
├── docs/
│   ├── research/
│   ├── user_guide.md
│   ├── developer_guide.md
│   └── api_reference.md
├── models/
├── notebooks/
├── reports/
├── src/
├── tests/
├── web/
│   └── index.html
├── Dockerfile
├── docker-compose.yml
├── requirements-docker.txt
└── README.md
```

## Getting Started

### Requirements

- Python 3.12 for local development
- Docker Desktop with Docker Compose
- Git
- The project ONNX model at `models/model.onnx`

### Clone the Repository

```powershell
git clone https://github.com/Tista-parashar/04_AutoPilot_AI.git
cd 04_AutoPilot_AI
```

### Run with Docker Compose

Build and start the application and monitoring services:

```powershell
docker compose up -d --build
```

Check service status:

```powershell
docker compose ps
```

### Service URLs

| Service | URL |
|---|---|
| Inference API | http://localhost:8001 |
| Health check | http://localhost:8001/health |
| Metrics | http://localhost:8001/metrics |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

Grafana's initial development credentials are `admin` / `admin`. Change the default password before continued use.

## Running Automated Tests

Activate the Python virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Set the Python import path:

```powershell
$env:PYTHONPATH = "src"
```

Run tests:

```powershell
python -m pytest -q
```

Some simulator-related tests may be skipped when CARLA is unavailable.

## Model and Inference

The ONNX model is stored at:

`models/model.onnx`

The inference service is implemented in `src/inference_service.py`.

It accepts image bytes through `POST /predict`, preprocesses the image, and returns three raw model outputs with inference time.

The outputs do not represent validated steering, braking, or throttle commands.

## Monitoring

The project uses:

- **Prometheus** to collect inference request, error, and timing metrics.
- **Grafana** to display the monitoring dashboard.

The monitoring configuration is stored in `config/`.

## Deployment and Reports

Docker deployment instructions are provided in the User Guide and Developer Guide.

Additional project reports and experimental results are stored in `reports/`.

## Known Limitations

- Model accuracy has not been established using labelled evaluation data.
- Training targets used during development do not establish meaningful driving performance.
- Real-world autonomous driving performance is unvalidated.
- CARLA end-to-end vehicle simulation is incomplete.
- The HTTP inference service is a basic local demonstration, not a hardened production API.

## License

Add the appropriate project license before distributing this repository publicly.




