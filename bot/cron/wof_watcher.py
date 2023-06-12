import asyncio
import logging
import time

from bot.db import db
from bot.handlers.wheel_of_fortune_handlers.wof_start_event import start_wheel_of_fortune

HOUR = 3600


async def start_wof_timer():
    while True:
        logging.info("WOF TIMER STARTED")
        wof_info = await db.get_active_wheel_info()

        if not wof_info:
            await asyncio.sleep(HOUR)
            logging.info("WOF TIMER SLEEP")
            continue

        time_before_wof_finish = wof_info.timestamp_end - time.time()
        logging.info(f"Seconds to WOF: {time_before_wof_finish}")
        if time_before_wof_finish < HOUR:
            logging.info("Timer to WOF is started")
            await start_wheel_of_fortune()

        await asyncio.sleep(HOUR)
