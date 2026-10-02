"""Dataset class for loading and transforming images."""

from torch.utils.data import Dataset
from PIL import Image
from torchvision import transforms


class DataLoader(Dataset):
    """Load images, apply transformations, and return image-label pairs."""

    def __init__(self, image_paths, labels, preprocessor=None):
        """Initialize the dataset."""
        self.image_paths = image_paths
        self.labels = labels
        self.preprocessor = preprocessor

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.5, 0.5, 0.5],
                std=[0.5, 0.5, 0.5]
            )
        ])

    def __len__(self):
        """Return the number of images in the dataset."""
        return len(self.image_paths)

    def __getitem__(self, idx):
        """Load and return one image and its label."""
        image = Image.open(self.image_paths[idx]).convert("RGB")
        image = self.transform(image)

        if self.preprocessor is not None:
            image = image.numpy()
            image = self.preprocessor.transform(
                image.reshape(1, -1)
            )

        label = self.labels[idx]

        return image, label
    