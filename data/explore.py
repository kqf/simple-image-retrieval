import click
import logging
import pandas as pd
from operator import attrgetter

from data.schema import TARGET_FIELDS
from data.base import telegram

logger = logging.getLogger(__name__)


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
    logger.info("Processing source %s", targets)

    with telegram("test") as client:
        dialogs = dump(client, TARGET_FIELDS)
        raw = pd.DataFrame(dialogs)
        df = pd.merge(raw, targets, on=["title"])
        logging.info('Processing dialogues %', df)
        df.to_csv(output, sep="\t", index=False)


if __name__ == '__main__':
    main()
