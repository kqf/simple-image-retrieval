import cv2
import numpy as np

from pathlib import Path


def make_blob(x=0.5, y=0.5, a=0.5, b=0.5, h=480, w=640, **kwargs):
    Y, X = np.ogrid[:h, :w]

    cx = h * x
    cy = w * y

    xx = (X[..., None] - cx)
    yy = (Y[..., None] - cy)
    dists = np.sqrt((xx / (a * w)) ** 2 + (yy / (b * h)) ** 2)

    mask = dists <= 1. / 2.
    return mask.sum(axis=-1).astype(np.uint8)


def blob2image(blob, channels=3, epsilon=0.1):
    h, w = blob.shape

    extended = blob[..., None]
    return extended + 255

    # Add a small term to add noise to the empty regions
    # noise = np.random.poisson(extended + epsilon, size=(h, w, channels))

    # Convet to image scale
    # return (extended + noise * 255).astype(np.uint8)


def generate_to_directory(annotations, dirname, image_col="image_id"):
    path = Path(dirname)
    for image_id, blobs in annotations.groupby(image_col):

        blobs = []
        for row in annotations.to_dict(orient="records"):
            blobs.append(make_blob(**row))
        blob = np.stack(blobs, axis=-1).any(-1)

        img = blob2image(blob)
        ifile = f"{image_id}.png"
        cv2.imwrite(str(path / ifile), img)
    annotations.to_csv(path / "train.csv", index=False)
