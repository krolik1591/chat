import asyncio
import logging
import time
from datetime import datetime

from bot.db import db
from bot.handlers.wheel_of_fortune_handlers.wof_start_event import start_wheel_of_fortune


async def start_wof_timer():
    while True:
        logging.info("WOF TIMER STARTED")
        wof_info = await db.get_active_wheel_info()

        if not wof_info:
            await asyncio.sleep(3600)
            logging.info("WOF TIMER SLEEP")
            continue

        try:
            date_end = wof_info.timestamp_end
        except AttributeError:
            logging.info("Date end not found")
            await asyncio.sleep(3600)
            continue
        now = time.time()
        time_delta = date_end - now
        logging.info(f"Seconds to WOF: {time_delta}")
        if time_delta < 3600:
            logging.info("Timer to WOF is started")
            await start_wheel_of_fortune()

        await asyncio.sleep(3600)
