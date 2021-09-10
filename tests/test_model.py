import pytest
import pandas as pd
from model.model import build_model
from model.dataset import SimilarityDataset


@pytest.fixture
def max_epochs(request):
    return request.config.getoption("--max-epochs")


def test_model(fake_dataset, max_epochs):
    print(max_epochs)
    df = pd.read_table(fake_dataset)
    dataset = SimilarityDataset(df.iloc)
    model = build_model(max_epochs=max_epochs)
    model.fit(dataset, None)
