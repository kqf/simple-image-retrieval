import pytest
import pandas as pd
from model.model import build_model
from model.dataset import SimilarityDataset
from model.augmentations import transform
from model.search import linear
from irmetrics.topk import recall


@pytest.fixture
def max_epochs(request):
    return request.config.getoption("--max-epochs")


def test_model(fake_dataset, max_epochs, deterministic, n_dims=100):
    df = pd.read_table(fake_dataset)
    dataset = SimilarityDataset(df.iloc, transform=transform(train=True))
    model = build_model(n_outputs=n_dims, max_epochs=max_epochs)
    model.fit(dataset, None)
    vectors = model.predict(dataset)

    assert vectors.shape == (len(df), n_dims)

    df["predictions"] = list(linear(dataset, dataset, model))
    idx2label = df["label"].to_dict()

    df["predictions"] = df["predictions"].apply(
        lambda preds: [idx2label[i] for i in preds]
    )
    print(sum(df["predictions"].str[0] == df["label"]))
    print(recall(df["label"], df["predictions"]))

