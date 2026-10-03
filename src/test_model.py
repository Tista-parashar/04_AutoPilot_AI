import torch

from model import AutoPilotModel


def test_model_initialization():
    model = AutoPilotModel()
    assert model is not None


model = AutoPilotModel()

dummy = torch.randn(8, 3, 256, 256)

output = model(dummy)

assert output.shape == (8, 3)

print("Output shape:", output.shape)
print("Min value:", output.min().item())
print("Max value:", output.max().item())
