import pandas as pd
import matplotlib.pyplot as plt

from model.dataset import SimilarityDataset


def test_reads(fake_dataset):
    df = pd.read_table(fake_dataset)
    dataset = SimilarityDataset(df.iloc)
    for i, (image, label) in enumerate(dataset):
        assert label in {0, 1}
        assert image.shape[0] == 3, "Dataset should contain 3 channel images"
        plt.imshow(image.transpose(1, 2, 0), interpolation='nearest')
        plt.show()
