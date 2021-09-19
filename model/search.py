import faiss                   # make faiss available
import numpy as np


def l2(a, b):
    return np.sum((a - b) ** 2, -1)


def ip(a, b):
    return np.sum(a * b, -1)


def linear(query, base, model, distance=l2, k=5):
    base_ = model.predict(base)
    query_ = model.predict(query)

    # query_[n_query, n], base_[n_base, n]
    distances = distance(query_[:, None], base_)

    # Take top k vectors as answers
    return (np.argsort(distances, -1))[..., :k]


def approximate(query, base, model, k=5):
    base_ = model.predict(base)
    query_ = model.predict(query)
    index = faiss.IndexFlatL2(base_.shape[-1])
    index.add(base_)
    _, indices = index.search(query_, k)
    return indices
