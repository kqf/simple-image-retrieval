import logging

from environs import Env
from telethon.sync import TelegramClient
from telethon.tl.types import PhotoSize
from functools import partial

logger = logging.getLogger(__name__)

env = Env()
env.read_env()
telegram = partial(
    TelegramClient,
    api_id=env("API_ID"),
    api_hash=env("API_HASH")
)


def width(size):
    if not isinstance(size, PhotoSize):
        return None
    return size.w


def height(size):
    if not isinstance(size, PhotoSize):
        return None
    return size.h
