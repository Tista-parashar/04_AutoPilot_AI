import os

import torch
import torch.nn as nn
import torch.optim as optim

from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader, random_split
from torch.utils.tensorboard import SummaryWriter

from data_loader import DataLoader as ImageDataset
from model import AutoPilotModel


def train_epoch(model, dataloader, optimizer, criterion, writer, epoch):
    model.train()

    for batch_idx, (images, labels) in enumerate(dataloader):

        targets = torch.zeros(images.size(0), 3)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, targets)

        loss.backward()

        optimizer.step()

        writer.add_scalar(
            "Loss/train",
            loss.item(),
            epoch * len(dataloader) + batch_idx
        )

        if batch_idx % 10 == 0:
            print(f"Batch {batch_idx} | Loss: {loss.item():.6f}")


def validate(model, dataloader, criterion):
    model.eval()

    total_loss = 0.0

    with torch.no_grad():

        for images, labels in dataloader:

            targets = torch.zeros(images.size(0), 3)

            outputs = model(images)

            loss = criterion(outputs, targets)

            total_loss += loss.item()

    return total_loss / len(dataloader)


image_paths = [
    os.path.join("data/cleaned", f)
    for f in os.listdir("data/cleaned")
]

labels = [0] * len(image_paths)

dataset = ImageDataset(image_paths, labels)

train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size

train_dataset, val_dataset = random_split(
    dataset,
    [train_size, val_size]
)

train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True,
    num_workers=0
)

val_loader = DataLoader(
    val_dataset,
    batch_size=32,
    shuffle=False,
    num_workers=0
)

model = AutoPilotModel()

criterion = nn.MSELoss()

optimizer = optim.Adam(
    model.parameters(),
    lr=0.001
)

scheduler = ReduceLROnPlateau(
    optimizer,
    mode="min",
    patience=3,
    factor=0.5
)

writer = SummaryWriter("runs/day32")

best_loss = float("inf")

print("Starting training...")

for epoch in range(10):

    print(f"Epoch {epoch + 1}")

    train_epoch(
        model,
        train_loader,
        optimizer,
        criterion,
        writer,
        epoch
    )

    val_loss = validate(
        model,
        val_loader,
        criterion
    )

    print(f"Validation Loss: {val_loss:.6f}")

    writer.add_scalar(
        "Loss/val",
        val_loss,
        epoch
    )

    if val_loss < best_loss:

        best_loss = val_loss

        torch.save(
            model.state_dict(),
            "checkpoints/best_model.pth"
        )

        print("Best model saved!")

    torch.save(
        {
            "epoch": epoch,
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
        },
        f"checkpoints/epoch_{epoch}.pth"
    )

    print(f"Checkpoint saved: checkpoints/epoch_{epoch}.pth")

    scheduler.step(val_loss)

    writer.add_scalar(
        "LR",
        optimizer.param_groups[0]["lr"],
        epoch
    )

    print("Current LR:", optimizer.param_groups[0]["lr"])

print("Training completed!")

writer.close()
