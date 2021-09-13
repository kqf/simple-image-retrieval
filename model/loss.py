import torch


def l2(a):
    return (a ** 2).sum(-1).view(-1, 1)


def dist(a, b):
    return -2 * a @ b.T + l2(a) + l2(b)


def dist2(a, b):
    return torch.sum((a - b) ** 2, dim=-1)


def mask_distances(distances, mask, fill_value=float("-inf")):
    masked_distances = distances * mask
    masked_distances.fill_diagonal_(fill_value)
    return masked_distances


class RetrievalLoss(torch.nn.Module):
    def __init__(self, sim=dist2, delta=1.0):
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

            neg_idx = (-mask_distances(distances, ~same_idx)).argmin(-1)
            neg = queries[neg_idx]

        loss = self.delta - l2(queries - pos) + l2(queries - neg)
        return torch.nn.functional.relu(loss).mean()
