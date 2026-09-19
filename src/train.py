import time
from torch.utils.data import DataLoader
from data_loader import DataLoader as ImageDataset

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
    num_workers=0,
    pin_memory=True
)

start = time.time()

for images, labels in loader:
    pass

end = time.time()

print("Time taken:", end - start, "seconds")
print("Dataset size:", len(dataset))
