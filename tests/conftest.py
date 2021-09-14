import torch

import random
import pytest
import tempfile

from pathlib import Path
import numpy as np

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
def fake_dataset(size=256, nfiles=5, fname="data.tsv", alpha=0.4):
    with tempfile.TemporaryDirectory() as dirname:
        path = Path(dirname)
        dataset = path / fname
        with dump_list(dataset) as files:
            for i in range(nfiles):
                # Circle with parameters
                circle = make_blob(0.5, 0.5, 0.5, 0.5)
                circle = blob2image(circle)
                circle_path = path / 'circles' / f"{i}.png"
                write(circle, circle_path)
                files.append({"image": circle_path, 'label': 0})

                ellipsis = make_blob(0.5, 0.5, 0.5 - alpha, 0.5 + alpha)
                ellipsis = blob2image(ellipsis)
                ellipsis_path = path / 'ellipses' / f"{i}.png"
                write(ellipsis, ellipsis_path)
                files.append({"image": ellipsis_path, 'label': 1})
        yield dataset
