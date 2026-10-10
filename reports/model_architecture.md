

\# AutoPilot\_AI Model Architecture



\## Overview



The AutoPilotModel uses a ResNet-50 backbone with a

modified final fully connected layer that produces three outputs.



```mermaid

flowchart TD

&#x20;   A\["Input Image<br/>3 × 256 × 256"] --> B\["Conv1 + BatchNorm + ReLU"]

&#x20;   B --> C\["Max Pooling"]

&#x20;   C --> D\["ResNet Layer 1<br/>256 channels"]

&#x20;   D --> E\["ResNet Layer 2<br/>512 channels"]

&#x20;   E --> F\["ResNet Layer 3<br/>1024 channels"]

&#x20;   F --> G\["ResNet Layer 4<br/>2048 channels"]

&#x20;   G --> H\["Global Average Pooling"]

&#x20;   H --> I\["Fully Connected Layer<br/>2048 → 3"]

&#x20;   I --> J\["Output: 3 values"]

```



\## Visualisation files



\- `model\_summary.txt`: Layer-by-layer model summary.

\- `filter\_visualization.png`: First convolution layer filters.

\- `layer\_activations.png`: First convolution layer activations.



