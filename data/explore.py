from telethon import TelegramClient


def main():
    api_id = 1
    api_hash = 'lol'

    client = TelegramClient('session_name', api_id, api_hash)
    client.start()


if __name__ == '__main__':
    main()
