import pytest
import pandas as pd
from model.model import build_model
from model.dataset import SimilarityDataset
from model.augmentations import transform


@pytest.fixture
def max_epochs(request):
    return request.config.getoption("--max-epochs")


def test_model(fake_dataset, max_epochs, deterministic, n_dims=100):
    df = pd.read_table(fake_dataset)
    dataset = SimilarityDataset(df.iloc, transform=transform(train=True))
    model = build_model(n_outputs=n_dims, max_epochs=max_epochs)
    model.fit(dataset, None)
    vectors = model.predict(dataset)

    # TODO: Check why is it len(df) - 1?
    assert vectors.shape == (len(df) - 1, n_dims)
