import logging
from datetime import datetime, timedelta
from bot.db import db

import pytz

HOUR = 3600


async def start_wof_timer(bot, i18n):
    while True:
        logging.info("DEACTIVATE PROMO CODE TIMER STARTED")

        await db.get_all_available_promo_code_for_user()

        await asyncio.sleep(HOUR)


if __name__ == '__main__':
    import asyncio

    async def test():
        gmt_timezone = pytz.timezone('Etc/GMT')
        current_datetime = datetime.now(gmt_timezone)
        next_day = current_datetime + timedelta(days=1)
        next_day = next_day.replace(hour=0, minute=0, second=0, microsecond=0)
        unix_timestamp = next_day.timestamp()
        print(unix_timestamp)


    asyncio.run(test())
