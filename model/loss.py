import torch


def l2(a, b):
    return torch.sum((a - b) ** 2, dim=-1)


def ip(a, b):
    return torch.sum(a * b, dim=-1)


def mask_distances(distances, mask, fill_value=float("-inf")):
    masked_distances = distances * mask

    # Never take an example as it's own positive / negative
    masked_distances.fill_diagonal_(fill_value)
    return masked_distances


class RetrievalLoss(torch.nn.Module):
    def __init__(self, sim=l2, delta=1.0):
        super().__init__()
        self.delta = delta
        self.sim = sim

    def forward(self, queries, targets):
        with torch.no_grad():
            distances = self.sim(queries[None, :], queries[:, None])
            # exploit the broadcasting
            same_idx = (targets.view(-1, 1) == targets.view(1, -1))

            pos_idx = mask_distances(distances, same_idx).argmax(-1)
            pos = queries[pos_idx]

            neg_distances = mask_distances(
                distances, 1. / ~same_idx, float("inf"))
            neg_idx = neg_distances.argmin(-1)
            neg = queries[neg_idx]

        loss = self.delta - self.sim(queries, pos) + self.sim(queries, neg)
        return torch.nn.functional.relu(loss).mean()
