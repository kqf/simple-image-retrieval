import pytest
import pandas as pd
from model.model import build_model
from model.dataset import SimilarityDataset
from model.augmentations import transform


@pytest.fixture
def max_epochs(request):
    return request.config.getoption("--max-epochs")


def test_model(fake_dataset, max_epochs, deterministic):
    df = pd.read_table(fake_dataset)
    dataset = SimilarityDataset(df.iloc, transform=transform(train=True))
    model = build_model(max_epochs=max_epochs)
    model.fit(dataset, None)
