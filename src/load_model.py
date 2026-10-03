import torch

from model import AutoPilotModel

# Create first model and load saved weights
model1 = AutoPilotModel()
model1.load_state_dict(torch.load("models/model_v1.pth"))

# Create dummy input
dummy = torch.randn(1, 3, 256, 256)

# First output
out1 = model1(dummy)

# Create second model and load same weights
model2 = AutoPilotModel()
model2.load_state_dict(torch.load("models/model_v1.pth"))

# Second output
out2 = model2(dummy)

# Compare outputs
print("Outputs equal:", torch.allclose(out1, out2))