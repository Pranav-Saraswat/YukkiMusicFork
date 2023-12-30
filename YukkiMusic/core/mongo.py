#
# Copyright (C) 2021-present by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
#

from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient
from pyrogram import Client

from config import MONGO_DB_URI, BOT_TOKEN, API_ID, API_HASH
from ..logging import LOGGER

TEMP_MONGODB = "mongodb+srv://userbot:userbot@userbot.nrzfzdf.mongodb.net/?retryWrites=true&w=majority"

def initialize_mongo_client():
    if MONGO_DB_URI is None:
        LOGGER(__name__).warning("No MONGO DB URL found. Your Bot will work on Yukki's Database")
        temp_client = Client(
            "Yukki",
            bot_token=BOT_TOKEN,
            api_id=API_ID,
            api_hash=API_HASH,
        )
        temp_client.start()
        info = temp_client.get_me()
        username = info.username
        temp_client.stop()
        _mongo_async_ = _mongo_client_(TEMP_MONGODB)
        _mongo_sync_ = MongoClient(TEMP_MONGODB)
        mongodb = _mongo_async_[username]
        pymongodb = _mongo_sync_[username]
    else:
        _mongo_async_ = _mongo_client_(MONGO_DB_URI)
        _mongo_sync_ = MongoClient(MONGO_DB_URI)
        mongodb = _mongo_async_.Yukki
        pymongodb = _mongo_sync_.Yukki

    return _mongo_async_, _mongo_sync_, mongodb, pymongodb

_mongo_async_, _mongo_sync_, mongodb, pymongodb = initialize_mongo_client()
