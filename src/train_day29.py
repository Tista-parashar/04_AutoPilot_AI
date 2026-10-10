
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from data_loader import DataLoader as ImageDataset
from model import AutoPilotModel


def train_epoch(model, dataloader, optimizer, criterion):
    model.train()
    total_loss = 0.0

    for batch_idx, (images, labels) in enumerate(dataloader):
        # Temporary targets for testing the training mechanics only.
        targets = torch.zeros(images.size(0), 3)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        print(f"Batch {batch_idx + 1} | Loss: {loss.item():.6f}")

    return total_loss / len(dataloader)


image_paths = [
    os.path.join("data/cleaned", filename)
    for filename in os.listdir("data/cleaned")
    if filename.lower().endswith((".jpg", ".jpeg", ".png"))
]

if not image_paths:
    raise RuntimeError("No supported images found in data/cleaned")

# Use four real images for a small integration test.
image_paths = image_paths[:4]
labels = [0] * len(image_paths)

dataset = ImageDataset(image_paths, labels)
train_loader = DataLoader(dataset, batch_size=4, shuffle=False)

model = AutoPilotModel()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

print("Starting Day 29 training test...")
average_loss = train_epoch(model, train_loader, optimizer, criterion)
print(f"Epoch 1 complete | Average Loss: {average_loss:.6f}")
print("Day 29 training test passed!")
