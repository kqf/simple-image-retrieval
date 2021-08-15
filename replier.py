import logging

from telethon import TelegramClient, events
from environs import Env

logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO)


env = Env()
env.read_env()


def main():
    with TelegramClient('test', env("API_ID"), env("API_HASH")) as client:
        @client.on(events.NewMessage)
        async def my_replier(event):
            await event.reply('🔥')
        client.run_until_disconnected()


if __name__ == '__main__':
    main()
