from telethon.sync import TelegramClient
from environs import Env
import logging
logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO)


env = Env()
env.read_env()

fields = [
    'date',
    'entity',
    'folder_id',
    'id',
    'is_channel',
    'is_group',
    'is_user',
    'name',
    'title',
    'to_dict',
    'unread_count',
    'unread_mentions_count'
]


def main():
    # username = env("USERNAME")
    # picture = 'pepe.jpg'

    with TelegramClient('test', env("API_ID"), env("API_HASH")) as client:
        dialogs = client.get_dialogs()
        print(dialogs)

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
