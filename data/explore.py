import logging
import pandas as pd
from operator import attrgetter

from telethon.sync import TelegramClient
from environs import Env
logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO)


env = Env()
env.read_env()

TARGET_FIELDS = [
    'entity.date',
    'folder_id',
    'id',
    'is_channel',
    'is_group',
    'is_user',
    'name',
    'title',
    'unread_count',
    'unread_mentions_count'
]


def dump(client, fields):
    for dialog in client.get_dialogs():
        dialog_dict = {}
        for field in fields:
            try:
                dialog_dict[field] = attrgetter(field)(dialog)
            except AttributeError:
                dialog_dict[field] = None
        yield dialog_dict


def main():
    # username = env("USERNAME")
    # picture = 'pepe.jpg'

    with TelegramClient('test', env("API_ID"), env("API_HASH")) as client:
        dialogs = dump(client, TARGET_FIELDS)
        df = pd.DataFrame(dialogs)
        print(df)

        # print(client.get_me().stringify())

        # client.send_message(username, 'Hello world!')
        # client.send_file(username, picture)

        # client.download_profile_photo('me')
        # messages = client.get_messages(username)
        # messages[0].download_media()

        # @client.on(events.NewMessage(pattern='(?i)hi|hello'))
        # async def handler(event):
        #     await event.respond('Hey!')


if __name__ == '__main__':
    main()
