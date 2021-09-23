import click
import numpy as np
import pandas as pd

from irmetrics.topk import recall

from model.model import build_model
from model.dataset import SimilarityDataset
from model.augmentations import transform
from model.search import ImageFinder


@click.command()
@click.option("--train-path", type=click.Path(exists=True))
@click.option("--valid-path", type=click.Path(exists=True))
def main(train_path, valid_path):
    df = pd.read_table(train_path)
    train = SimilarityDataset(df.iloc, transform=transform(train=True))
    model = build_model()
    model.fit(train, None)

    val_df = pd.read_table(valid_path)
    valid = SimilarityDataset(val_df.iloc, transform=transform(train=False))

    finder = ImageFinder(model, valid, df["label"].to_dict())
    df["predicted_label"] = finder.search(valid, k=1)
    rc = recall(
        df["label"].values.reshape(-1, 1).astype(int),
        np.stack(df["predicted_label"].values).astype(int),
        k=1
    )

    print(f"The recalls {rc}")
    print(f"The mean recall {rc.mean()}")
