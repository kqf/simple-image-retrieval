import click
import pandas as pd

from pathlib import Path
from environs import Env
from telethon.sync import TelegramClient

env = Env()
env.read_env()


@click.command()
@click.option("--target", type=click.Path(exists=True), default="titles.txt")
@click.option("--output", type=click.Path(exists=False), default="output.txt")
@click.option("--photos", type=click.Path(), default="photos")
def main(target, output, photos):
    df = pd.read_csv(target, sep="\t")
    df["entity.date"] = pd.to_datetime(df["entity.date"])
    candidates = df[["title", "entity.date"]]

    metadata = []
    with TelegramClient('test', env("API_ID"), env("API_HASH")) as client:
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

    odf = pd.DataFrame(metadata)
    print(odf)
    odf.to_csv(output)


if __name__ == '__main__':
    main()
