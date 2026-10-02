import torch

from model import AutoPilotModel


model = AutoPilotModel()

x = torch.randn(1, 3, 256, 256)

out = model(x)

print(out.shape)
