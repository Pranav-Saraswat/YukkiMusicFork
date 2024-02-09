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

import config

from ..logging import LOGGER

TEMP_MONGODB = "mongodb+srv://userbot:userbot@userbot.nrzfzdf.mongodb.net/?retryWrites=true&w=majority"

def setup_local_database():
    local_mongo_uri = input("Enter the local MongoDB URI (e.g., mongodb://localhost:27017): ")
    local_db_name = input("Enter the local database name: ")

    _mongo_async_ = _mongo_client_(local_mongo_uri)
    _mongo_sync_ = MongoClient(local_mongo_uri)

    mongodb = _mongo_async_[local_db_name]
    pymongodb = _mongo_sync_[local_db_name]

    return mongodb, pymongodb

if config.MONGO_DB_URI is None:
    LOGGER(__name__).warning(
        "No MONGO DB URL found. Your Bot will work on a local database."
    )

    use_local_db = input("Do you want to use a local database? (y/n): ").lower()
    if use_local_db == 'y':
        mongodb, pymongodb = setup_local_database()
    else:
        temp_client = Client(
            "Yukki",
            bot_token=config.BOT_TOKEN,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
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
    _mongo_async_ = _mongo_client_(config.MONGO_DB_URI)
    _mongo_sync_ = MongoClient(config.MONGO_DB_URI)
    mongodb = _mongo_async_.Yukki
    pymongodb = _mongo_sync_.Yukki
