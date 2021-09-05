import torch
import pytest
from model.model import classifier


@pytest.fixture
def batch_size():
    return 4


@pytest.fixture
def batch(batch_size, channels=3, width=480, height=640):
    return torch.ones((batch_size, channels, width, height))


def test_builds(batch, batch_size):
    clf = classifier()
    predictions = clf(batch)
    print(predictions.shape)
