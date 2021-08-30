import tqdm
import click
import logging
import pandas as pd

from click import Path as cpth
from pathlib import Path

from data.base import telegram, dump_list, width, height

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@click.command()
@click.option("--target", type=cpth(exists=True), default="data/targets.txt")
@click.option("--output", type=cpth(exists=False),
              default="data/positive/data.tsv")
@click.option("--images", type=cpth(), default="data/images/positive")
@click.option("--limit", type=int, default=None)
def main(target, output, images, limit):
    df = pd.read_csv(target, names=["title"])
    with telegram('test') as client, dump_list(output) as metadata:
        for idx, (title,) in df.iterrows():
            logger.info("Processing source %s", title)
            lpath = Path(images) / title
            entity = client.get_entity(title)
            messages = client.iter_messages(
                entity=entity,
                reverse=True,
                # filter=InputMessagesFilterimages(), # This doesn't work
                limit=limit,
            )

            filtered = [m for m in messages if m.photo is not None and m.out]
            for message in tqdm.tqdm(filtered, total=limit):
                # Only outgouing photos
                if message.photo is None or not message.out:
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
