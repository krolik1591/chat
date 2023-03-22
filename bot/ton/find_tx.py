import asyncio
import logging

import ton

from bot.db.db import Wallets_key
from bot.db.methods import get_all_users, get_last_transaction, get_token_by_id
from bot.handlers.deposit_heandlers.d01_replenish import prepare_wallets_to_work
from bot.menus.deposit_menus.successful_replenish_menu import successful_replenish_menu
from bot.ton.wallets import TonWrapper
from bot.db.db import manager
from bot.db import methods as db
from aiogram.dispatcher.fsm.context import FSMContext


import time
from time import monotonic as timer

import requests


TOKEN_ID = 2


# оптимизация: сортировать пользователей по последней активности
async def watch_txs(ton_wrapper: TonWrapper, bot):
    async def find_new_user_tx_(user_):
        try:
            await find_new_user_tx(ton_wrapper, user_, bot)

        except ton.tonlibjson.TonlibError as ex:
            logging.exception('TonLib error')

    while True:
        all_users_wallet = await get_all_users()
        coros = [find_new_user_tx_(user) for user in all_users_wallet]
        await asyncio.gather(*coros)

        await asyncio.sleep(10)


async def find_new_user_tx(ton_wrapper: TonWrapper, user: Wallets_key, bot):
    master_address = ton_wrapper.master_wallet.address
    account = await ton_wrapper.find_account(user.address)

    last_tx_from_blockchain = account.state.last_transaction_id

    last_tx_from_db = await get_last_transaction(user.user_id, TOKEN_ID)  # типу беремо з бд

    if last_tx_from_blockchain.hash != last_tx_from_db.tx_hash:
        print("NEW TX!")
        # добуваємо нові транзи

        new_tx = await ton_wrapper.get_account_transactions(
            account.address,
            last_tx_lt=last_tx_from_blockchain.lt,
            last_tx_hash=last_tx_from_blockchain.hash,
            first_tx_hash=last_tx_from_db.tx_hash)

        token = await get_token_by_id(TOKEN_ID)

        for tx in new_tx:
            await process_tx(tx, token, user.user_id, master_address, user.address, bot, account)

    else:
        print("NO NEW TX :(")


async def process_tx(tx, token, user_id, master_address, user_address, bot, user_account):
    # поповнення рахунку для поповнення
    if tx['destination'] == user_address:

        tx_type = 1
        tx_address = tx['source']
        amount = int(tx['value']) / 1e9 * token.price

        await successful_replenish(bot, amount, user_id)

        with manager.pw_database.atomic():
            await db.deposit_token(user_id, token.token_id, amount)
            await db.add_new_transaction(user_id, token.token_id, tx['value'], tx_type, tx_address, tx['tx_hash'],
                                         logical_time=tx['tx_lt'], utime=tx['utime'])

        # одразу відправляємо отримані гроші на мастер воллет
        # await user_wallet.transfer_ton(master_wallet.address, 0, send_mode=128) # так надо  # todo
        # await user_account.transfer(master_address, 0, send_mode=128)

    # переказ з юзер воллету на мастер воллет
    elif tx['source'] == user_address and tx['destination'] == master_address:
        tx_type = 2
        tx_address = master_address
        await db.add_new_transaction(user_id, token.token_id, tx['value'], tx_type, tx_address, tx['tx_hash'],
                                     logical_time=tx['tx_lt'], utime=tx['utime'])


    # переказ з мастер воллету на юзер воллет
    elif tx['source'] == master_address and tx['destination'] == user_address:
        tx_type = 3
        tx_address = user_address
        await db.add_new_transaction(user_id, token.token_id, tx['value'], tx_type, tx_address, tx['tx_hash'],
                                     logical_time=tx['tx_lt'], utime=tx['utime'])


    else:
        raise AssertionError('This should not happen')


async def successful_replenish(bot, amount, user_id):
    amount = round(amount, 2)
    text, keyboard = successful_replenish_menu(amount)

    await bot.send_message(user_id, text, reply_markup=keyboard)

