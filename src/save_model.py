import torch

from model import AutoPilotModel

model = AutoPilotModel()

torch.save(model.state_dict(), "models/model_v1.pth")

print("Model saved successfully!")
