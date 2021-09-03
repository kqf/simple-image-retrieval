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
    files = []
    with tempfile.TemporaryDirectory() as dirname:
        path = Path(dirname)
        for i in range(nfiles):
            circle = make_blob(size, size)
            circle = blob2image(circle)
            circle_path = path / 'circles' / f"{i}.png"
            write(circle, circle_path)
            files.append({"image": circle_path, 'label': 0})

            ellipsis = make_blob(size, size)
            ellipsis = blob2image(ellipsis)
            ellipsis_path = path / 'ellipses' / f"{i}.png"
            write(ellipsis, path / 'ellipses' / f"{i}.png")
            files.append({"image": ellipsis_path, 'label': 1})

        yield path
