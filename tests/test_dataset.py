import pandas as pd
from model.dataset import SimilarityDataset


def test_reads(fake_dataset):
    df = pd.read_table(fake_dataset)
    dataset = SimilarityDataset(df.loc)
    print(dataset)
