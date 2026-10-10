
import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from data_loader import DataLoader as ImageDataset
from model import AutoPilotModel


image_paths = [
    os.path.join("data/cleaned", f)
    for f in os.listdir("data/cleaned")
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

if not image_paths:
    raise RuntimeError("No supported images found in data/cleaned")

labels = [0] * len(image_paths)
dataset = ImageDataset(image_paths, labels)

loader = DataLoader(dataset, batch_size=4, shuffle=False)
images, labels = next(iter(loader))

model = AutoPilotModel()
criterion = nn.MSELoss()

# Temporary targets only for testing the pipeline.
targets = torch.zeros(images.size(0), 3)

outputs = model(images)
loss = criterion(outputs, targets)

print("Input shape:", images.shape)
print("Output shape:", outputs.shape)
print("Loss:", loss.item())

loss.backward()

has_gradients = any(
    parameter.grad is not None
    for parameter in model.parameters()
    if parameter.requires_grad
)

print("Gradients calculated:", has_gradients)

assert outputs.shape == (images.size(0), 3)
assert torch.isfinite(loss).item()
assert has_gradients

print("Day 28 integration test passed!")

