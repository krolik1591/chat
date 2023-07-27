import datetime
import time

from peewee import fn

from bot.db.models import WithdrawTx, Transactions


# transactions


async def get_user_daily_total_amount(user_id):
    today_midnight = datetime.datetime.combine(datetime.datetime.today().date(), datetime.time())
    next_day_midnight = today_midnight + datetime.timedelta(days=1)

    result = await Transactions.select(fn.SUM(Transactions.amount)).where(
        Transactions.user_id == user_id,
        Transactions.tx_type == 3,
        Transactions.utime.between(today_midnight.timestamp(), next_day_midnight.timestamp())
    )

    return result[0].amount or 0


async def add_new_transaction(user_id, token_id, amount, tx_type, tx_address, tx_hash, logical_time, utime,
                              comment=''):
    """
    :param user_id:
    :param token_id:
    :param amount: amount in wei / nano ton
    :param tx_type: 1 - deposit, 2 - deposit moved to master, 3 - withdraw
    :param tx_address:
    :param tx_hash:
    :param logical_time:
    :param utime:
    :param comment: only for withdraw tx
    :return:
    """
    return await Transactions.create(user_id=user_id, token_id=token_id, tx_type=tx_type,
                                     logical_time=logical_time, amount=amount,
                                     tx_address=tx_address, tx_hash=tx_hash, utime=utime, comment=comment)


async def add_new_crypto_pay_tx(user_id, token_id, amount, crypto_pay_id, utime, tx_type=1):
    return await Transactions.create(user_id=user_id, token_id=token_id, tx_type=tx_type, amount=amount,
                                     utime=utime, crypto_pay_id=crypto_pay_id)


async def get_last_transaction(tg_id, token_id):
    result = await Transactions.select(Transactions.tx_hash, fn.Max(Transactions.utime)) \
        .where(Transactions.user_id == tg_id, Transactions.token_id == token_id, Transactions.tx_type != 3)
    return result[0]


async def get_last_tx_by_tx_type(tx_type):
    result = await Transactions.select(Transactions.tx_hash, fn.Max(Transactions.utime)) \
        .where(Transactions.tx_type == tx_type)
    return result[0]


async def get_all_pending_tx(utime):
    result = await WithdrawTx.select().where(WithdrawTx.withdraw_state == 'pending',
                                             WithdrawTx.utime < utime)
    return result


# manual transactions


async def add_new_withdraw_tx(user_id, token_id, amount, tx_address, utime, withdraw_state='pending', is_manual=True):
    return await WithdrawTx.create(
        user_id=user_id,
        token_id=token_id,
        amount=amount,
        tx_address=tx_address,
        utime=utime,
        withdraw_state=withdraw_state,
        is_manual=is_manual
    )


async def update_withdraw_tx_state(tx_id, new_state):
    return await WithdrawTx.update({WithdrawTx.withdraw_state: new_state}).where(WithdrawTx.withdrawtx_id == tx_id)


async def get_withdraw_tx_by_id(tx_id):
    result = await WithdrawTx.select().where(WithdrawTx.withdrawtx_id == tx_id)
    return result[0]


async def get_last_withdraw_transaction(user_id, token_id):
    result = await WithdrawTx.select(WithdrawTx.withdrawtx_id, WithdrawTx.withdraw_state,
                                     fn.Max(WithdrawTx.utime)).where(
        WithdrawTx.user_id == user_id,
        WithdrawTx.token_id == token_id,
        (WithdrawTx.withdraw_state == 'moderating') | (WithdrawTx.withdraw_state == 'pending')
    )
    return result[0]


async def get_last_crypto_pay_id():
    result = await Transactions.select().where(Transactions.crypto_pay_id != None).order_by(Transactions.utime.desc()).first()
    if not result:
        return None
    return result.crypto_pay_id


if __name__=='__main__':
    import asyncio

    async def test():
        x = await get_last_crypto_pay_id()
        print(x)

    asyncio.run(test())
