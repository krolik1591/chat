import asyncio
from datetime import datetime

from bot.db import db
from bot.handlers.wheel_of_fortune_handlers.wof_start_event import start_wheel_of_fortune


async def start_wof_timer():
    while True:
        wof_info = await db.get_active_wheel_info()

        if not wof_info:
            await asyncio.sleep(3600)
            continue

        try:
            date_end = wof_info.date_end
        except AttributeError:
            await asyncio.sleep(3600)
            continue
        now = datetime.utcnow()
        time_delta = date_end - now
        seconds = time_delta.total_seconds()

        if seconds < 3600:
            await start_wheel_of_fortune()

        await asyncio.sleep(3600)
