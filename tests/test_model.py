import pytest
import numpy as np
import pandas as pd

from irmetrics.topk import recall

from model.model import build_model
from model.dataset import SimilarityDataset
from model.augmentations import transform
from model.search import ImageFinder


@pytest.fixture
def max_epochs(request):
    return request.config.getoption("--max-epochs")


def test_model(fake_dataset, max_epochs, deterministic, n_dims=100):
    df = pd.read_table(fake_dataset)
    dataset = SimilarityDataset(df.iloc, transform=transform(train=True))
    model = build_model(n_outputs=n_dims, max_epochs=max_epochs)
    model.fit(dataset, None)
    assert model.predict(dataset).shape == (len(df), n_dims)

    finder = ImageFinder(model, dataset, df["label"].to_dict())
    df["predicted_label"] = finder.search(dataset, k=3)
    rc = recall(
        df["label"].values.reshape(-1, 1).astype(int),
        np.stack(df["predicted_label"].values).astype(int),
        k=1
    )

    print(f"The recalls {rc}")
    print(f"The mean recall {rc.mean()}")
