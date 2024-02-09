#
# Copyright (C) 2021-present by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio
import speedtest
from pyrogram import filters
from strings import get_command
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS

# Commands
SPEEDTEST_COMMAND = get_command("SPEEDTEST_COMMAND")


def testspeed():
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        download_speed = test.download()
        upload_speed = test.upload()
        result = test.results.dict()
        result['download_speed'] = download_speed
        result['upload_speed'] = upload_speed
    except Exception as e:
        raise e
    return result


async def run_testspeed(m):
    result = await asyncio.to_thread(testspeed)
    return result


async def main():
    m = await app.send_message("Running Speed test")
    try:
        result = await run_testspeed(m)
        output = f"""**Speedtest Results**
        
    <u>**Client:**</u>
    **__ISP:__** {result['client']['isp']}
    **__Country:__** {result['client']['country']}
    
    <u>**Server:**</u>
    **__Name:__** {result['server']['name']}
    **__Country:__** {result['server']['country']}, {result['server']['cc']}
    **__Sponsor:__** {result['server']['sponsor']}
    **__Latency:__** {result['server']['latency']}  
    **__Ping:__** {result['ping']}"""
        await app.send_photo(
            chat_id=m.chat.id, 
            photo=result["share"], 
            caption=output
        )
        await m.delete()
    except Exception as e:
        await m.edit(f"Error: {str(e)}")


@app.on_message(filters.command(SPEEDTEST_COMMAND) & SUDOERS)
def speedtest_command(client, message):
    asyncio.run(main())
