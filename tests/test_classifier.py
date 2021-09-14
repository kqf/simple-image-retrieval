import torch
import pytest
import numpy as np
from model.model import Classifier


@pytest.fixture
def batch_size():
    return 4


@pytest.fixture
def batch(batch_size, channels=3, width=480, height=640):
    return torch.ones((batch_size, channels, width, height))


def init_with(f):
    def wrap(m):
        if 'weight' in dir(m) and m.weight is not None:
            f(m.weight)

        if 'bias' in dir(m) and m.bias is not None:
            f(m.bias)

    return wrap


def test_classifier(batch, batch_size):
    clf = Classifier()
    clf.apply(init_with(torch.nn.init.zeros_))
    preds = clf(batch)

    # Check if it's indeed convergent
    np.testing.assert_allclose(preds.detach(), 0.)

    # For now it's binary classification problem
    assert preds.shape == (batch_size, 2)

    clf.apply(init_with(torch.nn.init.ones_))
    preds = clf(batch)
    assert preds.shape == (batch_size, 2)
