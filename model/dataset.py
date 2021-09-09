import cv2
import pathlib

from torch.utils.data import Dataset


class SimilarityDataset(Dataset):
    def __init__(self, samples, transofrm=None):
        super().__init__()
        self.samples = samples
        self.transform = transofrm

    def __len__(self):
        return self.samples[-1].name

    def __getitem__(self, idx):
        sample = pathlib.Path(self.samples[idx]["image"])

        # By default OpenCV uses BGR color space for color images,
        # so we need to convert the image to RGB color space.
        image_channels_last = cv2.imread(str(sample), cv2.COLOR_BGR2RGB)
        image = image_channels_last.transpose(2, 0, 1)
        label = self.samples[idx]["image"]

        if self.transform is not None:
            return self.transform(image), label

        return image, label
