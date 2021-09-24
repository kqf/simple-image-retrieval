import logging

from telethon import events
from scripts.base import telegram

logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO)


def main():
    with telegram('test') as client:
        @client.on(events.NewMessage)
        async def my_replier(event):
            await event.reply('🔥')
        client.run_until_disconnected()


if __name__ == '__main__':
    main()
