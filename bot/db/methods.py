import json
from datetime import datetime, time, timedelta

from peewee import fn

from bot.db.models import GameLog, ManualTXs, Transactions, User, Wallets_key


# users


async def create_new_user(tg_id, username):
    return await User.create(user_id=tg_id, username=username, timestamp_registered=datetime.utcnow(),
                             timestamp_last_active=datetime.utcnow())


async def update_username(tg_id, username):
    return await User.update({User.username: username}).where(User.user_id == tg_id)


async def get_user_lang(tg_id):
    user_lang = await User.select(User.lang).where(User.user_id == tg_id)
    if not user_lang:
        raise ValueError
    return user_lang[0].lang


async def set_user_lang(tg_id, new_lang):
    return await User.update({User.lang: new_lang}).where(User.user_id == tg_id)


async def set_user_last_active(tg_id):
    return await User.update({User.timestamp_last_active: datetime.utcnow()}).where(User.user_id == tg_id)


# balances


async def get_user_balances(user_id):
    result = await User.select(User.balance_demo, User.balance_promo, User.balance_general) \
        .where(User.user_id == user_id)
    if not result:
        raise ValueError
    return {
        'demo': result[0].balance_demo,
        'promo': result[0].balance_promo,
        'general': result[0].balance_general
    }


async def get_user_balance(user_id, balance_type):
    return (await get_user_balances(user_id))[balance_type]


async def update_user_balance(user_id, balance_type, balance_to_add):
    field = {
        'demo': User.balance_demo,
        'promo': User.balance_promo,
        'general': User.balance_general
    }[balance_type]

    return await User.update({field: fn.ROUND(field + balance_to_add, 5)}).where(User.user_id == user_id)


# transactions


async def get_user_daily_total_amount(user_id):
    today_midnight = datetime.combine(datetime.today().date(), time())
    next_day_midnight = today_midnight + timedelta(days=1)

    result = await Transactions.select(fn.SUM(Transactions.amount)).where(
        Transactions.user_id == user_id,
        Transactions.tx_type == 3,
        Transactions.utime.between(today_midnight.timestamp(), next_day_midnight.timestamp())
    )

    return result[0].amount or 0


async def add_new_transaction(user_id, token_id, amount, tx_type, tx_address, tx_hash, logical_time, utime):
    """
    :param user_id:
    :param token_id:
    :param amount: amount in wei / nano ton
    :param tx_type: 1 - deposit, 2 - deposit moved to master, 3 - withdraw
    :param tx_address:
    :param tx_hash:
    :param logical_time:
    :param utime:
    :return:
    """
    return await Transactions.create(user_id=user_id, token_id=token_id, tx_type=tx_type,
                                     logical_time=logical_time, amount=amount,
                                     tx_address=tx_address, tx_hash=tx_hash, utime=utime)


async def get_last_transaction(tg_id, token_id):
    result = await Transactions.select(Transactions.tx_hash, fn.Max(Transactions.utime)) \
        .where(Transactions.user_id == tg_id, Transactions.token_id == token_id, Transactions.tx_type != 3)
    return result[0]


# manual transactions


async def add_new_manual_tx(user_id, nano_ton_amount, token_id, price, tx_address, utime,
                            withdraw_state='pending', is_manual=True):
    return await ManualTXs.create(user_id=user_id, token_id=token_id, amount=nano_ton_amount, price=price,
                                  tx_address=tx_address, utime=utime,
                                  withdraw_state=withdraw_state, is_manual=is_manual)


async def update_manual_withdraw_state(tx_id, new_state):
    return await ManualTXs.update({ManualTXs.withdraw_state: new_state}).where(ManualTXs.ManualTXs_id == tx_id)


async def get_manual_tx_by_id(tx_id):
    result = await ManualTXs.select().where(ManualTXs.ManualTXs_id == tx_id)
    return result[0]


async def get_last_manual_transaction(tg_id, token_id):
    result = await ManualTXs.select(ManualTXs.ManualTXs_id, ManualTXs.withdraw_state, fn.Max(ManualTXs.utime)).where(
        ManualTXs.user_id == tg_id, ManualTXs.token_id == token_id, ManualTXs.withdraw_state == 'pending').dicts()
    return result[0]


# wallets


async def create_user_wallet(tg_id, address, mnemonic):
    return await Wallets_key.create(user_id=tg_id, mnemonic=mnemonic, address=address)


async def get_all_user_wallets():
    return await Wallets_key.select(Wallets_key.user_id, Wallets_key.address, Wallets_key.mnemonic)


async def get_user_wallet(tg_id):
    return await Wallets_key.select().where(Wallets_key.user_id == tg_id).first()


# game logs


async def insert_game_log(user_id, balance_type, game_info, bet, result, game):
    # game = game name, ex: slots or mines or darts
    # game_info = ex:
    # slots/darts/...: {dice_result: 1-64}
    # dice: {dice_result: 1-6, dice_bet: 1-6 or 1-2 / 3-4 / 5/6 or even / odd}
    # mines: {mines_field: [], ...}
    # cuefa: {cuefa_bet: rock or paper or scissors}
    game_info = json.dumps(game_info)

    return await GameLog.create(user_id=user_id, balance_type=balance_type,
                                game=game, game_info=game_info,
                                bet=bet, result=result, timestamp=datetime.utcnow())


if __name__ == "__main__":
    async def test():
        pass


    import asyncio

    asyncio.run(test())
