from model.dataset import Dataset


def test_reads(fake_dataset):
    dataset = Dataset(fake_dataset)
    print(dataset)
