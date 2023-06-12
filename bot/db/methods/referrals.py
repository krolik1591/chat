import time

from peewee import fn

from bot.db.models import User, GameLog


# referrals


async def update_datetime_and_amount_ref_withdraw(tg_id, amount):
    return await User.update({User.total_ref_withdraw: fn.Round(User.total_ref_withdraw + amount, 2),
                              User.timestamp_ref_withdraw: time.time()}).where(User.user_id == tg_id)


async def get_date_last_total_ref_withdraw(tg_id):
    result = await User.select().where(User.user_id == tg_id)
    return result[0].timestamp_ref_withdraw


async def get_total_ref_withdraw(tg_id):
    result = await User.select().where(User.user_id == tg_id)
    return result[0].total_ref_withdraw or 0


async def get_user_referrer(tg_id):
    user_ref = await User.select().where(User.user_id == tg_id)
    return user_ref[0].referrer


async def get_count_all_user_referrals(tg_id):
    result = await User.select().where(User.referrer == tg_id)
    return len(result)


async def get_referrals_bets_from_last_withdraw(referrer):
    time_ = await User.select().where(User.user_id == referrer)
    time_ = time_[0].timestamp_ref_withdraw or 0

    result = (await User
              .select(fn.SUM(GameLog.bet).alias('total_bets'))
              .join(GameLog)
              .where(User.referrer == referrer, GameLog.timestamp > time_, GameLog.balance_type == "general").scalar())
    return result or 0


async def get_all_referrals_bets(referrer):
    result = (await User
              .select(fn.SUM(GameLog.bet).alias('total_bets'))
              .join(GameLog)
              .where(User.referrer == referrer, GameLog.balance_type == "general").scalar())
    return result or 0
