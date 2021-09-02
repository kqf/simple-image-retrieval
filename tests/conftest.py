import cv2

import pytest
import tempfile

from pathlib import Path

from model.mc import make_blob, blob2image


@pytest.fixture
def size():
    return 256


def write(img, imgpath):
    # _, png = cv2.imencode(".png", img)
    imgpath.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(imgpath), img)


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
