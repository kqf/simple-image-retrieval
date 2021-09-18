import pytest
import numpy as np
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

    df["pred_label"] = df["predictions"].apply(
        lambda preds: [idx2label[i] for i in preds]
    )
    print(sum(df["pred_label"].str[0] == df["label"]))

    rc = recall(
        df["label"].values.reshape(-1, 1).astype(int),
        np.stack(df["pred_label"].values).astype(int),
        k=1
    )

    print(f"The recalls {rc}")
    print(f"The mean recall {rc.mean()}")
    import ipdb; ipdb.set_trace(); import IPython; IPython.embed()  # noqa
