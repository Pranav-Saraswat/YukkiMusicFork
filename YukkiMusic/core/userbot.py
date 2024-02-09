#
# Copyright (C) 2021-present by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
#

import sys
from pyrogram import Client
import config
from ..logging import LOGGER

assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self, session_string, assistant_number):
        super().__init__(
            f"YukkiString{assistant_number}",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(session_string),
            no_updates=True,
        )

    async def start(self, assistant_number):
        LOGGER(__name__).info(f"Starting Assistant {assistant_number}")
        if self.is_initialized():
            try:
                await self.join_common_channels()
                await self.send_message(config.LOG_GROUP_ID, "Assistant Started")
            except Exception as e:
                LOGGER(__name__).error(f"Assistant Account {assistant_number} failed to start: {e}")
                sys.exit()

            get_me = await self.get_me()
            self.username = get_me.username
            self.id = get_me.id
            assistantids.append(get_me.id)
            if get_me.last_name:
                self.name = f"{get_me.first_name} {get_me.last_name}"
            else:
                self.name = get_me.first_name
            LOGGER(__name__).info(f"Assistant {assistant_number} Started as {self.name}")

    async def join_common_channels(self):
        common_channels = ["TeamYM", "TheYukki", "YukkiSupport"]
        for channel in common_channels:
            try:
                await self.join_chat(channel)
            except Exception as e:
                LOGGER(__name__).error(f"Failed to join channel {channel}: {e}")

userbots = [Userbot(session, i + 1) for i, session in enumerate(config.STRING) if session]

async def start_assistants():
    for i, userbot in enumerate(userbots, start=1):
        await userbot.start(i)
        assistants.append(i)
