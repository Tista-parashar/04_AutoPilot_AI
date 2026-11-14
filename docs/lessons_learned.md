\# Lessons Learned: AutoPilot\_AI



\## 1. Project Overview

AutoPilot\_AI is a prototype AI-based autonomous driving project. It uses a ResNet-50 model, ONNX inference, Docker deployment, and monitoring tools.



\## 2. What Went Well

\- Organized the project into separate modules.

\- Implemented image preprocessing and data loading.

\- Explored model training and evaluation.

\- Exported the model to ONNX format.

\- Created an inference API.

\- Deployed the application using Docker Compose.

\- Configured Prometheus and Grafana for monitoring.

\- Prepared project documentation and a final presentation.



\## 3. Challenges Faced

\- Setting up Python environments and dependencies.

\- Managing datasets and preprocessing images.

\- Handling model export and ONNX compatibility.

\- Troubleshooting Docker configuration and deployment.

\- Working with limited hardware resources.

\- CARLA simulator integration could not be fully validated because of hardware and configuration limitations.



\## 4. Technical Skills Learned

\- Python and PyTorch

\- Image preprocessing and computer vision

\- ResNet-50 architecture

\- ONNX model export and inference

\- REST API development

\- Docker and Docker Compose

\- Prometheus and Grafana

\- Git and GitHub

\- Testing and project documentation



\## 5. What Could Be Improved

\- Train the model using meaningful steering, throttle, and braking labels.

\- Perform proper model evaluation using real validation metrics.

\- Improve model accuracy and generalization.

\- Complete CARLA simulation integration.

\- Add more comprehensive automated tests.

\- Conduct controlled testing before any real-world application.



\## 6. Important Limitations



- The current model was trained using zero-valued targets, so meaningful driving accuracy has not been established.
- CARLA integration was not successfully validated.
- Model outputs are raw predictions and have not been verified as safe driving controls.
- This project is a prototype, not a production-ready autonomous driving system.

## 7. Future Recommendations
- Collect a properly labelled driving dataset.
- Retrain and evaluate the model using meaningful targets.
- Complete simulator integration.
- Perform extensive testing in a controlled environment.
- Improve error handling, monitoring, and documentation.

## 8. Conclusion
This project provided practical experience in machine learning, computer vision, model deployment, API development, monitoring, and software project management.

The development process also highlighted the importance of reliable datasets, proper evaluation, hardware compatibility, and realistic project validation.
