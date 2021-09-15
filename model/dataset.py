import pathlib

from torch.utils.data import Dataset
from model.cv import read
from model.augmentations import transform


class SimilarityDataset(Dataset):
    def __init__(self, samples, transofrm=transform(train=False)):
        super().__init__()
        self.samples = samples
        self.transform = transofrm

    def __len__(self):
        return self.samples[-1].name

    def __getitem__(self, idx):
        sample = pathlib.Path(self.samples[idx]["image"])

        image = read(sample)
        label = self.samples[idx]["label"]

        if self.transform is not None:
            image = image.transpose(1, 2, 0)
            transformed = self.transform(image=image)["image"]
            return transformed.numpy(), label

        return image, label
