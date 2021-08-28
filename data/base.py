import logging
import pandas as pd

from environs import Env
from telethon.sync import TelegramClient
from contextlib import contextmanager
from functools import partial

logger = logging.getLogger(__name__)

env = Env()
env.read_env()
telegram = partial(
    TelegramClient,
    api_id=env("API_ID"),
    api_hash=env("API_HASH")
)


@contextmanager
def dump_list(ofile):
    data = []
    yield data
    df = pd.DataFrame(data)
    logger.warning("Dumping the dataframe %s", df)
    df.to_csv(ofile, sep="\t", index=False)
