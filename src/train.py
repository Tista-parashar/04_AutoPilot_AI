import time
from torch.utils.data import DataLoader
from data_loader import DataLoader as ImageDataset

image_paths = [
    "data/cleaned/t2.png",
    "data/cleaned/test.png"
]

labels = [0, 1]

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
