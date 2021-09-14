import pathlib

from torch.utils.data import Dataset
from model.cv import read


class SimilarityDataset(Dataset):
    def __init__(self, samples, transofrm=None):
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
            return self.transform(image), label

        return image, label
