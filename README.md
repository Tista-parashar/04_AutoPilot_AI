  # AutoPilot AI

## Project Objective

Build an autonomous driving system that can perceive the environment, make decisions, and control vehicle movement.

## System Architecture

### Perception
- Camera
- LiDAR
- GPS

### Decision
- RL Agent
- Path Planner

### Control
- Steering
- Brake
- Throttle

## Tech Stack

- Python
- PyTorch
- NumPy
- Pandas
- Matplotlib
- Scikit-Learn
- Git
- GitHub

## Hardware Constraints

- Limited processing power
- Sensor inaccuracies
- Memory limitations

## Software Constraints

- Python dependencies
- Training time requirements
- Dataset size limitations

## Folder Structure

04_AutoPilot_AI/
├── docs/
│   └── architecture.png
├── data/
├── models/
├── notebooks/
├── src/
└── README.md

## Data Preparation

The data preparation pipeline includes the following steps:

1. Load image data and labels.
2. Clean and validate images.
3. Resize images to the required dimensions.
4. Split the dataset into training, validation, and test sets.
5. Apply preprocessing and normalization.
6. Use data augmentation during training.
7. Analyse the dataset using EDA.
8. Calculate mean and standard deviation for normalization.

The dataset is split into:
- 70% training data
- 15% validation data
- 15% test data

The calculated mean and standard deviation are stored in `data/mean_std.json`.

## Preprocessing Pipeline

The preprocessing pipeline includes:

- Image cleaning and validation
- Image resizing to 256×256
- Feature engineering
- Feature normalization
- Data versioning with DVC
- Preprocessing pipeline using sklearn Pipeline
- Integration with DataLoader

Pipeline artifacts:

- models/preprocessor.joblib
- data/norm_params.json
- data/feature_scaler.pkl
