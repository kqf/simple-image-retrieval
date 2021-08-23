import tqdm
import click
import logging
import pandas as pd

from click import Path as cpth
from pathlib import Path
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
    df.to_csv(ofile, index=False)


@click.command()
@click.option("--target", type=cpth(exists=True), default="data/targets.txt")
@click.option("--output", type=cpth(exists=False), default="data/output.txt")
@click.option("--images", type=cpth(), default="data/images")
@click.option("--limit", type=int, default=None)
def main(target, output, images, limit):
    df = pd.read_csv(target, names=["title"])
    with telegram('test') as client, dump_list(output) as metadata:
        for idx, title in df.iterrows():
            logger.info("Processing source %s", title)
            lpath = Path(images) / title
            entity = client.get_entity(title)
            messages = client.iter_messages(
                entity=entity,
                reverse=True,
                # filter=InputMessagesFilterimages(), # This doesn't work
                limit=limit,
            )
            for message in tqdm.tqdm(messages):
                if message.photo is None:
                    continue

                imgpath = lpath / str(message.photo.access_hash)
                fname = message.download_media(imgpath)
                sizes = message.photo.sizes[-1]
                metadata.append({
                    "file": fname,
                    "source": title,
                    "date": message.date,
                    "photo_id": message.photo.id,
                    "reference": message.photo.file_reference,
                    "width": sizes.w,
                    "height": sizes.h,
                })


if __name__ == '__main__':
    main()
