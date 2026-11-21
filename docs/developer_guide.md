# AutoPilot AI - Developer Guide

## 1. Project Overview

AutoPilot AI is an experimental computer vision and machine learning project. It uses an ONNX model for image-based inference and provides a local HTTP service with monitoring support.

## 2. Technology Stack

- Python 3.12 for development
- PyTorch and Torchvision for model development
- NumPy and Pandas for data processing
- Scikit-learn for preprocessing
- ONNX and ONNX Runtime for model inference
- Pillow and OpenCV for image processing
- Docker and Docker Compose for deployment
- Prometheus for metrics collection
- Grafana for monitoring
- Git and GitHub for version control

## 3. Project Structure

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
│   ├── model.onnx
│   └── preprocessor.joblib
├── notebooks/
├── reports/
├── src/
│   ├── inference_service.py
│   ├── carla_bridge.py
│   └── controller.py
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements-docker.txt
└── README.md
```

Additional files and directories may exist as the project develops.

## 4. Development Environment Setup

Clone the repository:

```powershell
git clone https://github.com/Tista-parashar/04_AutoPilot_AI.git
cd 04_AutoPilot_AI
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the project's development dependencies using the repository's dependency files.

Set the Python import path:

```powershell
$env:PYTHONPATH = "src"
```

Run the tests:

```powershell
python -m pytest -q
```

Some CARLA-related tests may be skipped when a compatible simulator is unavailable.

## 5. Model and Inference Architecture

The project uses an ONNX model stored at:

`models/model.onnx`

The inference service is implemented in:

`src/inference_service.py`

The service:
1. Loads the ONNX model using ONNX Runtime.
2. Receives image data through HTTP.
3. Converts the image to RGB.
4. Resizes it to 224 × 224 pixels.
5. Normalizes pixel values to the range [-1, 1].
6. Converts the image to NCHW format.
7. Runs inference using the CPU execution provider.
8. Returns three raw model outputs and inference time.

The driving meaning of these outputs has not been validated.

## 6. Docker Deployment

Build the Docker image:

```powershell
docker build -t autopilot-ai:day57 .
```

Start the application and monitoring services:

```powershell
docker compose up -d
```

Check services:

```powershell
docker compose ps
```

View logs:

```powershell
docker compose logs
```

Stop services:

```powershell
docker compose down
```

## 7. Monitoring Architecture

The monitoring setup includes:

### Prometheus
- Scrapes the inference service's `/metrics` endpoint.
- Collects request, error, and inference-time counters.
- Uses the configuration in `config/prometheus.yml`.

### Grafana
- Uses Prometheus as its data source.
- Loads dashboard configuration from `config/grafana/`.
- Displays inference request counts, errors, and total inference time.

## 8. Testing and Quality Assurance

Run automated tests:

```powershell
$env:PYTHONPATH = "src"
python -m pytest -q
```

The project also includes:
- Data preprocessing tests
- Model and integration tests
- Regression testing
- ONNX inference checks
- Docker health checks
- Prometheus metrics verification

CARLA end-to-end testing remains incomplete.

## 9. Version Control Workflow

Check repository changes:

```powershell
git status --short
```

Stage only the intended files:

```powershell
git add <file-path>
```

Commit changes:

```powershell
git commit -m "Describe your changes"
```

Push to GitHub:

```powershell
git push origin main
```

Avoid staging unrelated backup files.

## 10. Development Guidelines

- Keep code modular and readable.
- Use meaningful variable and function names.
- Add tests when changing functionality.
- Update documentation when APIs or configurations change.
- Do not commit virtual environments, temporary files, or generated cache files.
- Keep model and preprocessing configurations consistent.
- Validate changes locally before committing.