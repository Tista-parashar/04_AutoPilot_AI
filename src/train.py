import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from data_loader import DataLoader as ImageDataset
from model import AutoPilotModel

import os


def train_epoch(model, dataloader, optimizer, criterion):
    model.train()

    for batch_idx, (images, labels) in enumerate(dataloader):

        targets = torch.zeros(images.size(0), 3)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, targets)

        loss.backward()

        optimizer.step()

        if batch_idx % 10 == 0:
            print(f"Batch {batch_idx} | Loss: {loss.item():.6f}")


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

optimizer = optim.Adam(
    model.parameters(),
    lr=0.001
)

print("Starting training...")

for epoch in range(1):
    print(f"Epoch {epoch + 1}")
    train_epoch(model, loader, optimizer, criterion)

print("Training completed!")

