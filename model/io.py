import pandas as pd
from contextlib import contextmanager


@contextmanager
def dump_list(ofile):
    data = []
    yield data
    df = pd.DataFrame(data)
    df.to_csv(ofile, sep="\t", index=False)
