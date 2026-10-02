import torch.nn as nn
from torchvision import models


class AutoPilotModel(nn.Module):
    """Autonomous driving model."""

    def __init__(self):
        super().__init__()

        self.backbone = models.resnet50(pretrained=True)
        self.backbone.fc = nn.Linear(2048, 3)

    def forward(self, x):
        return self.backbone(x)
