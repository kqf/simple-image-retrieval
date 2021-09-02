import pytest
import tempfile

from pathlib import Path

from models.preprocess import write
from models.mc import make_blob, blob2image


@pytest.fixture
def size():
    return 256


@pytest.fixture
def fake_dataset(size=256, nfiles=5):
    with tempfile.TemporaryDirectory() as dirname:
        path = Path(dirname)
        for i in range(nfiles):
            circle = make_blob(size, size)
            circle = blob2image(circle)
            write(circle, path / 'circles' / f"{i}.png")

            ellipsis = make_blob(size, size)
            ellipsis = blob2image(ellipsis)
            write(ellipsis, path / 'ellipses' / f"{i}.png")

        yield path
