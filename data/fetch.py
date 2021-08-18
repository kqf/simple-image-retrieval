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


@click.command()
@click.option("--target", type=click.Path(exists=True), default="titles.txt")
@click.option("--output", type=click.Path(exists=False), default="output.txt")
@click.option("--photos", type=click.Path(), default="photos")
def main(target, output, photos):
    df = pd.read_csv(target, sep="\t")
    df["entity.date"] = pd.to_datetime(df["entity.date"])
    candidates = df[["title", "entity.date"]]

    with telegram('test') as client, dump_list(output) as metadata:
        for idx, (title, date) in candidates.iterrows():
            lpath = Path(photos) / title
            entity = client.get_entity(title)
            messages = client.iter_messages(
                entity=entity,
                offset_date=date,
                reverse=True,
            )
            for i, message in enumerate(messages):
                if message.photo is None:
                    continue

                if i > 20:
                    break
                imgpath = lpath / str(message.photo.access_hash)
                fname = message.download_media(imgpath)
                print(fname)
                metadata.append({
                    "file": fname,
                    "source": title,
                    "date": message.date,
                })


if __name__ == '__main__':
    main()
