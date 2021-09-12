import torch


def l2(a):
    return (a ** 2).sum(-1).view(-1, 1)


def dist(a, b):
    return -2 * a @ b.T + l2(a) + l2(b)


class RetrievalLoss(torch.nn.Module):
    def __init__(self, sim=dist, delta=1.0):
        super().__init__()
        self.delta = delta
        self.sim = sim

    def forward(self, queries, targets):
        with torch.no_grad():
            distances = self.sim(queries, queries)

            # exploit the broadcasting
            same_idx = targets.view(-1, 1) == targets.view(1, -1)
            pos = queries[(distances * same_idx).argmax(-1)]

            neg_idx = (distances * ~same_idx).argmax(-1)
            neg = queries[neg_idx]

        loss = self.delta - l2(queries - pos) + l2(queries - neg)
        return torch.nn.functional.relu(loss).mean()
