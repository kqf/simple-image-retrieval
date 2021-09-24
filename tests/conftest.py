import torch

import random
import pytest
import tempfile
import numpy as np

from pathlib import Path

from model.mc import make_blob, blob2image
from model.cv import write
from model.io import dump_list


@pytest.fixture
def deterministic(seed=137):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True


@pytest.fixture
def size():
    return 256


def pytest_addoption(parser):
    parser.addoption(
        "--max-epochs",
        action="store",
        default=2,
        type=int,
        help="Number of epochs to run the tests",
    )


def sigmoid_space(start, stop, n_points, sigmoid_start=-10, sigmoid_stop=10):
    # Define the
    x = np.linspace(sigmoid_start, sigmoid_stop, n_points)

    # The sigmoid range is (0, 1)
    sigmoid = 1. / (1. + np.exp(-x))

    # Convert it to (stop, start)
    return sigmoid * (stop - start) + start


@pytest.fixture
def fake_dataset(size=256, nfiles=10, fname="data.tsv", max_alpha=0.4):
    with tempfile.TemporaryDirectory() as dirname:
        path = Path(dirname)
        dataset = path / fname

        with dump_list(dataset) as files:
            for i in range(nfiles):
                alpha = max_alpha if i > nfiles // 2 else 0
                example = make_blob(0.5, 0.5, 0.5 - alpha, 0.5 + alpha)
                image = blob2image(example)
                example_path = path / f"{i}.png"
                write(image, example_path)
                files.append({
                    "image": example_path,
                    'label': alpha > max_alpha / 2.,
                    "distance": alpha,
                })

        yield dataset
