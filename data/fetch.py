import click
import pandas as pd

from environs import Env
from telethon.sync import TelegramClient

env = Env()
env.read_env()


@click.command()
@click.option("--target", type=click.Path(exists=True), default="titles.txt")
@click.option("--output", type=click.Path(exists=False), default="output.txt")
def main(target, output):
    df = pd.read_csv(target, sep="\t")
    df["entity.date"] = pd.to_datetime(df["entity.date"])
    candidates = df[["title", "entity.date"]]
    with TelegramClient('test', env("API_ID"), env("API_HASH")) as client:
        for idx, (title, date) in candidates.iterrows():
            entity = client.get_entity(title)
            messages = client.iter_messages(
                entity=entity,
                offset_date=date,
                reverse=True,
            )
            for message in messages:
                pass


if __name__ == '__main__':
    main()
