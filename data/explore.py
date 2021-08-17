import click
import pandas as pd
from operator import attrgetter

from telethon.sync import TelegramClient
from environs import Env
from data.schema import TARGET_FIELDS


env = Env()
env.read_env()


def dump(client, fields):
    for dialog in client.get_dialogs():
        dialog_dict = {}
        for field in fields:
            try:
                dialog_dict[field] = attrgetter(field)(dialog)
            except AttributeError:
                dialog_dict[field] = None
        yield dialog_dict


@click.command()
@click.option("--titles", type=click.Path(exists=True), default="titles.txt")
@click.option("--output", type=click.Path(exists=False), default="output.txt")
def main(titles, output):
    targets = pd.read_csv(titles, names=["title"])
    print(targets)

    with TelegramClient('test', env("API_ID"), env("API_HASH")) as client:
        dialogs = dump(client, TARGET_FIELDS)
        raw = pd.DataFrame(dialogs)
        df = pd.merge(raw, targets, on=["title"])
        print(df)
        df.to_csv(output, sep="\t", index=False)


if __name__ == '__main__':
    main()
