import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

from data_loader import DataLoader as ImageDataset
from model import AutoPilotModel

import os


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
scheduler = StepLR(
    optimizer,
    step_size=1,
    gamma=0.5
)

writer = SummaryWriter("runs/day30")

print("Starting training...")


for epoch in range(2):
    print(f"Epoch {epoch + 1}")

    train_epoch(
        model,
        loader,
        optimizer,
        criterion,
        writer,
        epoch
    )

    torch.save(
        {
            "epoch": epoch,
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
        },
        f"checkpoints/epoch_{epoch}.pth"
    )

    print(f"Checkpoint saved: checkpoints/epoch_{epoch}.pth")
    scheduler.step()

writer.add_scalar(
    "LR",
    optimizer.param_groups[0]["lr"],
    epoch
)

print("Current LR:", optimizer.param_groups[0]["lr"])

print("Training completed!")
writer.close()