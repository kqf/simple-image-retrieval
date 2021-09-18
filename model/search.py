import numpy as np


def l2(a, b):
    return (a - b) ** 2


def linear_search(query, base, model, distance=l2, k=5):
    base_ = model.predict(base)
    query_ = model.predict(query)

    # query_[n_query, n], base_[n_base, n]
    distances = distance(query_[:, None], base_)

    # Take top k vectors as answers
    return (-np.arsort(distances, -1))[..., :k]
