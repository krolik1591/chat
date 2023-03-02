import time
from datetime import datetime
from pprint import pprint

from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

import bot.db.methods as db
from bot.db.db import manager
from bot.menus.deposit_menus.replenish_menu import replenish_menu
from bot.ton.api import Api

flags = {"throttling_key": "default"}
router = Router()


@router.callback_query(text=["replenish"])
async def replenish(call: types.CallbackQuery, state: FSMContext):
    wallets = state.bot.wallets
    wallet = await wallets.get_wallet(call.from_user.id)
    # wallet.get_balance, wallet.get_transaction
    text, keyboard = replenish_menu(wallet.address)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(text=["ton_check"])
async def ton_check(call: types.CallbackQuery, state: FSMContext):
    # todo 2 arg token to .env, 24 words tuda je, 1 arg toje
    api = Api('https://testnet.toncenter.com/api/v2',
              '621699dde4b908a9d5c98ab16a887e9348ed3a05afe44a32bf8e6244f7a2bde0')

    wallets = state.bot.wallets
    wallet = await wallets.get_wallet(call.from_user.id)
    MASTER_WALLET = await wallets.get_wallet(0)

    last_tx = await db.get_last_transaction(call.from_user.id, 2)
    res = await api.get_address_transactions(wallet.address, last_tx.tx_hash, last_tx.logical_time)

    token = await db.get_token_by_id(2)
    pprint(res)
    token_id = 2
    for item in res:
        amount = int(item['in_msg']['value']) / 1e9 * token.price
        tx_hash = item['transaction_id']['hash']
        tx_time = item['utime']

        if item['in_msg']['destination'] == wallet.address:
            # todo с кошеля юзера закинуть (ВСЕ ДЕНЬГИ) на мастер кошель (wallets.py transfer).
            tx_type = 1
            tx_address = item['in_msg']['source']

        elif item['in_msg']['source'] == wallet.address:
            tx_address = item['in_msg']['destination']
            tx_type = 2 if item['in_msg']['destination'] == MASTER_WALLET else 3

        else:
            raise AssertionError('This should not happen')

        with manager.pw_database.atomic():
            await db.update_user_balance(call.from_user.id, token_id, amount)
            await db.add_new_transaction(call.from_user.id, token_id, amount, tx_type, tx_address, tx_hash,
                                         tx_time)
