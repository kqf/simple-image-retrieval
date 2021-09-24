import tqdm
import click
import logging
import pandas as pd

from click import Path as cpth
from pathlib import Path

from data.base import telegram, width, height
from model.io import dump_list

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def candidates(df):
    df["entity.date"] = pd.to_datetime(df["entity.date"])
    candidates = df[["title", "entity.date"]]
    return candidates.iterrows()


@click.command()
@click.option("--target", type=cpth(exists=True), default="data/explored.tsv")
@click.option("--output", type=cpth(exists=False),
              default="data/images/anchors/data.tsv")
@click.option("--images", type=cpth(), default="data/images/anchors")
@click.option("--limit", type=int, default=None)
def main(target, output, images, limit):
    df = pd.read_csv(target, sep="\t")

    with telegram('test') as client, dump_list(output) as metadata:
        for idx, (title, date) in candidates(df):
            logger.info("Processing source %s", title)
            lpath = Path(images) / title
            entity = client.get_entity(title)
            messages = client.iter_messages(
                entity=entity,
                offset_date=date,
                reverse=True,
                # filter=InputMessagesFilterimages(), # This doesn't work
                limit=limit,
            )

            filtered = [m for m in messages if m.photo is not None]
            for message in tqdm.tqdm(filtered, total=limit):
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
                    "width": width(sizes),
                    "height": height(sizes),
                })


if __name__ == '__main__':
    main()
