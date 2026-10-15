\# Training Report



\## Project

AutoPilot\_AI



\## Week 5 Review



\### Training Configuration

\- Model: AutoPilotModel (ResNet50 backbone)

\- Optimizer: Adam

\- Initial Learning Rate: 0.001

\- Scheduler: ReduceLROnPlateau

\- Scheduler Mode: min

\- Scheduler Patience: 3 epochs

\- Scheduler Factor: 0.5

\- Batch Size: 2

\- Epochs: 10

\- Loss Function: MSELoss



\## Training Results



\### Validation Loss



| Epoch | Validation Loss |

|---|---:|

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



\*Note: These results are from the previously recorded run. They have not been verified as results from the updated ReduceLROnPlateau scheduler.\*



\## Saved Models

\- `checkpoints/best\_model.pth`

\- `models/final\_model.pth`



\## Checkpoints

\- `epoch\_0.pth`

\- `epoch\_1.pth`

\- `epoch\_2.pth`

\- `epoch\_3.pth`

\- `epoch\_4.pth`

\- `epoch\_5.pth`

\- `epoch\_6.pth`

\- `epoch\_7.pth`

\- `epoch\_8.pth`

\- `epoch\_9.pth`



\## Observations

\- A training run and checkpoint saving were recorded.

\- Validation loss increased sharply in early epochs and decreased afterward.

\- The lowest value in the listed validation results was 0.100554 at Epoch 1.

\- TensorBoard logging was previously observed working.

\- The current training script uses ReduceLROnPlateau, which adjusts the learning rate based on validation loss.



\## Loss Analysis

Loss curve: `reports/loss\_curve.png`



The difference between training and validation loss warrants further investigation. Overfitting cannot be conclusively assessed from these results alone because the current pipeline uses zero-valued targets rather than real driving labels.



\## Conclusion

The training pipeline has been implemented, but the model's driving performance has not been established. Meaningful evaluation requires real driving targets, a suitable validation strategy, and a fresh evaluation run.



Potential next improvements:

\- Use real driving data and labels.

\- Increase the dataset size where appropriate.

\- Explore data augmentation.

\- Tune hyperparameters.

\- Evaluate on a separate validation dataset.

