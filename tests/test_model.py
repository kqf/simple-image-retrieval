import pandas as pd
from model.model import build_model
from model.dataset import SimilarityDataset


def test_model(fake_dataset):
    df = pd.read_table(fake_dataset)
    dataset = SimilarityDataset(df.iloc)
    model = build_model()
    model.fit(dataset)
