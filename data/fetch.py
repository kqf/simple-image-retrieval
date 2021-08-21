import click
import pandas as pd

from pathlib import Path
from environs import Env
from telethon.sync import TelegramClient
from contextlib import contextmanager
from functools import partial


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
    print(df)
    df.to_csv(ofile, index=False)


def candidates(df):
    df["entity.date"] = pd.to_datetime(df["entity.date"])
    candidates = df[["title", "entity.date"]]
    return candidates.iterrows()


@click.command()
@click.option("--target", type=click.Path(exists=True), default="titles.txt")
@click.option("--output", type=click.Path(exists=False), default="output.txt")
@click.option("--images", type=click.Path(), default="images")
@click.option("--limit", type=int, default=20)
def main(target, output, images, limit):
    df = pd.read_csv(target, sep="\t")

    with telegram('test') as client, dump_list(output) as metadata:
        for idx, (title, date) in candidates(df):
            lpath = Path(images) / title
            entity = client.get_entity(title)
            messages = client.iter_messages(
                entity=entity,
                offset_date=date,
                reverse=True,
                # filter=InputMessagesFilterimages(), # This doesn't work
                limit=limit,
            )
            for i, message in enumerate(messages):
                if message.photo is None:
                    continue

                imgpath = lpath / str(message.photo.access_hash)
                fname = message.download_media(imgpath)
                metadata.append({
                    "file": fname,
                    "source": title,
                    "date": message.date,
                })


if __name__ == '__main__':
    main()
