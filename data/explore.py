from telethon import TelegramClient


def main():
    api_id = 1
    api_hash = 'lol'
    username = 'lol'
    picture = 'pepe.jpg'

    client = TelegramClient('session_name', api_id, api_hash)
    client.start()

    print(client.get_me().stringify())

    client.send_message(username, 'Hello world!')
    client.send_file(username, picture)

    client.download_profile_photo('me')
    messages = client.get_messages(username)
    messages[0].download_media()

    # @client.on(events.NewMessage(pattern='(?i)hi|hello'))
    # async def handler(event):
    #     await event.respond('Hey!')


if __name__ == '__main__':
    main()
