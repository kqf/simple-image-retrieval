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

fields = [
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


def to_dict(dialog, fields):
    dump = {}
    for field in fields:
        try:
            dump[field] = attrgetter(field)(dialog)
        except AttributeError:
            dump[field] = None

    return dump


def main():
    # username = env("USERNAME")
    # picture = 'pepe.jpg'

    with TelegramClient('test', env("API_ID"), env("API_HASH")) as client:
        dialogs = [to_dict(d, fields) for d in client.get_dialogs()]
        print(dialogs)
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
