import faiss


class ImageFinder:
    def __init__(self, model, base, index):
        self.model = model
        base_ = model.predict(base)
        index = faiss.IndexFlatL2(base_.shape[-1])
        index.add(base_)
        self.index = index

    def search(self, query, k):
        query_ = self.model.predict(query)
        _, indices = self.index.search(query_, k)
        return indices
