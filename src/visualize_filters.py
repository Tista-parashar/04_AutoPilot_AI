import torch
from torchvision.utils import make_grid
import matplotlib.pyplot as plt

from model import AutoPilotModel

model = AutoPilotModel()

# First convolution layer weights
filters = model.backbone.conv1.weight.data.clone()

# Normalize for display
filters = (filters - filters.min()) / (filters.max() - filters.min())

# Take first 16 filters
grid = make_grid(filters[:16], nrow=4)

plt.figure(figsize=(8, 8))
plt.imshow(grid.permute(1, 2, 0))
plt.axis("off")

plt.savefig("reports/filter_visualization.png")
print("Filter visualization saved!")
