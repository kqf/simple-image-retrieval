import torch

import random
import pytest
import tempfile
import numpy as np

from pathlib import Path

from model.mc import make_blob, blob2image
from model.cv import write
from data.base import dump_list


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


@pytest.fixture
def fake_dataset(size=256, nfiles=10, fname="data.tsv", max_alpha=0.4):
    with tempfile.TemporaryDirectory() as dirname:
        path = Path(dirname)
        dataset = path / fname
        lengths = np.linspace(0, max_alpha, nfiles)
        with dump_list(dataset) as files:
            for i, alpha in enumerate(lengths):
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
