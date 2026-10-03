import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from data_loader import DataLoader as ImageDataset
from model import AutoPilotModel
import os

image_paths = [
    os.path.join("data/cleaned", f)
    for f in os.listdir("data/cleaned")
]

labels = [0] * len(image_paths)

dataset = ImageDataset(image_paths, labels)

loader = DataLoader(
    dataset,
    batch_size=2,
    shuffle=True,
    num_workers=0
)

model = AutoPilotModel()

criterion = nn.MSELoss()

for images, labels in loader:

    targets = torch.zeros(images.size(0), 3)

    outputs = model(images)

    loss = criterion(outputs, targets)

    loss.backward()

    print("Output shape:", outputs.shape)
    print("Loss:", loss.item())

    break

print("Backward pass successful!")
