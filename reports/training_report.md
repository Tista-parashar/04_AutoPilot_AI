\# Training Report



\## Project

AutoPilot\_AI



\## Week 5 Review



\### Training Configuration



\- Model: AutoPilotModel (ResNet50 backbone)

\- Optimizer: Adam

\- Learning Rate: 0.001

\- Scheduler: StepLR

\- Scheduler Gamma: 0.5

\- Batch Size: 2

\- Epochs: 10

\- Loss Function: MSELoss



\---



\## Training Results



\### Validation Loss



| Epoch | Validation Loss |

|---------|---------|

| 1 | 0.100554 |

| 2 | 0.170217 |

| 3 | 4.815784 |

| 4 | 4.689034 |

| 5 | 2.736627 |

| 6 | 1.642652 |

| 7 | 1.087461 |

| 8 | 0.773344 |

| 9 | 0.600291 |

| 10 | 0.491504 |



\---



\## Saved Models



\- checkpoints/best\_model.pth

\- models/final\_model.pth



\---



\## Checkpoints



\- epoch\_0.pth

\- epoch\_1.pth

\- epoch\_2.pth

\- epoch\_3.pth

\- epoch\_4.pth

\- epoch\_5.pth

\- epoch\_6.pth

\- epoch\_7.pth

\- epoch\_8.pth

\- epoch\_9.pth



\---



\## Observations



\- Training completed successfully.

\- Validation loss increased sharply during early epochs.

\- Validation loss gradually decreased afterwards.

\- Best validation loss achieved: 0.100554.

\- Learning rate scheduler reduced learning rate each epoch.

\- TensorBoard logging worked successfully.

\- Checkpoint saving worked successfully.



\---



\## Loss Analysis



Loss curve saved in:



reports/loss\_curve.png



No severe overfitting observed.



\---



\## Conclusion



Week 5 training pipeline is complete.



The model can be further improved by:



\- Increasing dataset size

\- Using real driving data

\- Data augmentation

\- Hyperparameter tuning

\- Better validation strategy



Current model is ready for future optimisation experiments.

