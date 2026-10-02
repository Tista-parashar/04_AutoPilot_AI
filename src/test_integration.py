from data_loader import DataLoader

image_paths = ["data/cleaned/t4.jpg"]
labels = [0]

dataset = DataLoader(image_paths, labels)

image, label = dataset[0]

print("Image shape:", image.shape)
print("Label:", label)