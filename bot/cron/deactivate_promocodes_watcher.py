import asyncio
import logging
from datetime import datetime, timedelta

from bot.cron.wof_watcher import send_msg
from bot.db import db

import pytz

from bot.tokens.token_ton.tx_watcher import set_user_locale_to_i18n
from aiogram.utils.i18n import gettext as _


HOUR = 3600
TIME_OF_DURATION = HOUR * 5


async def warning_about_expiration_promo_code(bot, i18n):
    while True:
        logging.info("DEACTIVATE PROMO CODE TIMER STARTED")

        users = await db.get_users_whose_promo_code_expire(TIME_OF_DURATION)
        for user_id in users:
            await set_user_locale_to_i18n(user_id, i18n)
            promo_code = await db.get_active_promo_code_of_user(user_id, 'balance')
            if not promo_code.min_wager:
                await send_msg(bot, user_id, _("DEACTIVATE_PROMO_WATCHER_MSG_TEXT_WITHOUT_DEPOSIT").format(
                    promo_code_name=promo_code.name, time_of_duration=TIME_OF_DURATION / 60))
            else:
                await send_msg(bot, user_id, _("DEACTIVATE_PROMO_WATCHER_MSG_TEXT").format(
                    promo_code_name=promo_code.name, time_of_duration=TIME_OF_DURATION / 60,
                    min_wager=promo_code.min_wager))

        await asyncio.sleep(HOUR)


if __name__ == '__main__':

    async def test():
        gmt_timezone = pytz.timezone('Etc/GMT')
        current_datetime = datetime.now(gmt_timezone)
        next_day = current_datetime + timedelta(days=1)
        next_day = next_day.replace(hour=0, minute=0, second=0, microsecond=0)
        unix_timestamp = next_day.timestamp()
        print(unix_timestamp)


    asyncio.run(test())
