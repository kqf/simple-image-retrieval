import click
import pandas as pd

from pathlib import Path
from environs import Env
from telethon.sync import TelegramClient
from contextlib import contextmanager

env = Env()
env.read_env()


@contextmanager
def dump_data(ofile):
    data = []
    yield data
    df = pd.DataFrame(data)
    print(df)
    df.to_csv(ofile)


@click.command()
@click.option("--target", type=click.Path(exists=True), default="titles.txt")
@click.option("--output", type=click.Path(exists=False), default="output.txt")
@click.option("--photos", type=click.Path(), default="photos")
def main(target, output, photos):
    df = pd.read_csv(target, sep="\t")
    df["entity.date"] = pd.to_datetime(df["entity.date"])
    candidates = df[["title", "entity.date"]]

    with TelegramClient('test', env("API_ID"), env("API_HASH")) as client, \
            dump_data(output) as metadata:
        for idx, (title, date) in candidates.iterrows():
            lpath = Path(photos) / title
            entity = client.get_entity(title)
            messages = client.iter_messages(
                entity=entity,
                offset_date=date,
                reverse=True,
            )
            for i, message in enumerate(messages):
                if i > 5:
                    break
                download_path = lpath / str(message.photo.access_hash)
                fname = message.download_media(download_path)
                print(fname)
                metadata.append({
                    "file": fname,
                    "source": title,
                })


if __name__ == '__main__':
    main()
