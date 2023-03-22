import json
from datetime import datetime
from pprint import pprint

from peewee import fn, JOIN

from bot.db import first_start
from bot.db.db import Balance, User, Token, Transaction, GameLog, Wallets_key
from bot.db.db import manager


async def create_new_user(tg_id, username):
    return await User.create(user_id=tg_id, username=username, timestamp_registered=datetime.utcnow(),
                             timestamp_last_active=datetime.utcnow())


async def create_user_wallet(tg_id, address, mnemonic):
    return await Wallets_key.create(user_id=tg_id, mnemonic=mnemonic, address=address)


async def get_all_users():
    return await Wallets_key.select(Wallets_key.user_id, Wallets_key.address, Wallets_key.mnemonic)


async def update_username(tg_id, username):
    return await User.update({User.username: username}).where(User.user_id == tg_id)


async def get_user_wallet(tg_id):
    return await Wallets_key.select().where(Wallets_key.user_id == tg_id).first()


async def get_user_balances(user_id):
    result = await Token.select(Balance.amount, Token.icon, Token.name) \
        .join(Balance, JOIN.LEFT_OUTER).switch(Balance) \
        .where((Balance.user_id == user_id) | (Balance.user_id.is_null(True))).dicts()

    return {
        i['name']: {**i, 'amount': i['amount'] or 0}  # replace `amount` field, set 0 instead None
        for i in result
    }


async def get_user_balance(user_id, token_id):
    result = await Balance.select(Balance.amount).where(Balance.user_id == user_id, Balance.token_id == token_id)
    if not result:
        return 0
    return result[0].amount


async def update_user_balance(user_id, token_id, new_balance):
    return await Balance.update({Balance.amount: fn.ROUND(Balance.amount + new_balance, 5)}). \
        where(Balance.user_id == user_id, Balance.token_id == token_id)


async def get_tokens():
    return await Token.select()


async def get_token_by_id(token_id):
    return await Token.select().where(Token.token_id == token_id).first()


async def deposit_token(tg_id, token_id, amount):
    return await Balance \
        .insert(user_id=tg_id, token_id=token_id, amount=amount) \
        .on_conflict(
        conflict_target=(Balance.user_id, Balance.token_id),
        preserve=(Balance.user_id, Balance.token_id),
        update=({Balance.amount: fn.ROUND(Balance.amount + amount, 5)})
    )


async def update_withdraw_state(tx_hash):
    return await Transaction.update({Transaction.withdraw_state: True}).where(Transaction.tx_hash == tx_hash)


async def add_new_transaction(user_id, token_id, amount, tx_type, tx_address, tx_hash, logical_time, utime, *, withdraw_state=False):
    return await Transaction.create(user_id=user_id, token_id=token_id, tx_type=tx_type,
                                    logical_time=logical_time, amount=amount,
                                    tx_address=tx_address, tx_hash=tx_hash, utime=utime, withdraw_state=withdraw_state)


async def get_last_transaction(tg_id, token_id):
    result = await Transaction.select(Transaction.tx_hash, fn.Max(Transaction.utime)) \
        .where(Transaction.user_id == tg_id, Transaction.token_id == token_id)
    return result[0]


async def get_user_lang(tg_id):
    user_lang = await User.select(User.lang).where(User.user_id == tg_id)
    if not user_lang:
        raise ValueError
    return user_lang[0].lang


async def set_user_lang(tg_id, new_lang):
    return await User.update({User.lang: new_lang}).where(User.user_id == tg_id)


async def set_user_last_active(tg_id):
    return await User.update({User.timestamp_last_active: datetime.utcnow()}).where(User.user_id == tg_id)


async def insert_game_log(user_id, token_id, game_info, bet, result, game):
    # game = game name, ex: slots or mines or darts
    # game_info = ex:
    # slots/darts/...: {dice_result: 1-64}
    # dice: {dice_result: 1-6, dice_bet: 1-6 or 1-2 / 3-4 / 5/6 or even / odd}
    # mines: {mines_field: [], ...}
    # cuefa: {cuefa_bet: rock or paper or scissors}
    game_info = json.dumps(game_info)

    return await GameLog.create(user_id=user_id, token_id=token_id,
                                game=game, game_info=game_info,
                                bet=bet, result=result, timestamp=datetime.utcnow())


if __name__ == "__main__":
    async def test():
        await first_start()
        # await add_new_transaction(228322, 3, 45641560, 9, 'cfvervrbgrtbr4ergb', 'fwgvrgbvgb43b5rbhr5', 46814651658146, 5651656)
        await update_withdraw_state('fwgvrgbvgb43b5rbhr5')



    import asyncio

    asyncio.run(test())
