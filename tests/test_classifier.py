import torch
import pytest
from model.model import Classifier


@pytest.fixture
def batch_size():
    return 4


@pytest.fixture
def batch(batch_size, channels=3, width=480, height=640):
    return torch.ones((batch_size, channels, width, height))


def test_classifier(batch, batch_size):
    clf = Classifier()
    predictions = clf(batch)

    # For now it's binary classification problem
    assert predictions.shape == (batch_size, 2)
