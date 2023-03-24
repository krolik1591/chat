import asyncio
import logging

import ton
from TonTools.Contracts.Wallet import Wallet

from bot.const import INIT_PAY_TON
from bot.db import methods as db
from bot.db.db import Wallets_key, manager
from bot.db.methods import get_all_users, get_last_transaction, get_token_by_id
from bot.menus.deposit_menus.init_menu import init_menu
from bot.menus.deposit_menus.successful_replenish_menu import successful_replenish_menu
from bot.ton.wallets import TonWrapper

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

    user_mnemonic = user.mnemonic.split(',')
    user_wallet = Wallet(provider=ton_wrapper, mnemonics=user_mnemonic)

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
            await process_tx(tx, token, user.user_id, master_address, user.address, bot, user_wallet)

    else:
        print("NO NEW TX :(")


async def process_tx(tx, token, user_id, master_address, user_address, bot, user_wallet):
    # поповнення рахунку для поповнення
    if tx['destination'] == user_address:

        tx_type = 1
        tx_address = tx['source']
        amount = int(tx['value']) / 1e9 * token.price
        nano_ton_amount = int(tx['value'])

        user_init_condition = await user_wallet.get_state()
        if user_init_condition == 'uninitialized':
            inited = await init_user_wallet(nano_ton_amount, bot, user_id, user_wallet)
            nano_ton_amount -= INIT_PAY_TON * 1e9

        await successful_deposit(bot, amount, user_id)

        with manager.pw_database.atomic():
            await db.deposit_token(user_id, token.token_id, amount)
            await db.add_new_transaction(user_id, token.token_id, tx['value'], tx_type, tx_address, tx['tx_hash'],
                                         logical_time=tx['tx_lt'], utime=tx['utime'])

        # одразу відправляємо отримані гроші на мастер воллет
        print('tut pracue')
        await user_wallet.transfer_ton(master_address, amount=500_000_000, send_mode=128)


    # переказ з юзер воллету на мастер воллет
    elif tx['source'] == user_address and tx['destination'] == master_address:
        tx_type = 2
        tx_address = master_address
        await db.add_new_transaction(user_id, token.token_id, tx['value'], tx_type, tx_address, tx['tx_hash'],
                                     logical_time=tx['tx_lt'], utime=tx['utime'])

    else:
        raise AssertionError('This should not happen')


async def successful_deposit(bot, amount, user_id):
    amount = round(amount, 2)
    text, keyboard = successful_replenish_menu(amount)

    await bot.send_message(user_id, text, reply_markup=keyboard)


async def init_user_wallet(tx_value, bot, user_id, user_wallet):
    if tx_value < INIT_PAY_TON * 1e9:
        text, keyboard = init_menu(False, INIT_PAY_TON)
        await bot.send_message(text, reply_markup=keyboard, chat_id=user_id)
        return False

    else:
        await user_wallet.deploy()
        print('мінус 13 центів сучара')
        text, keyboard = init_menu(True, INIT_PAY_TON)
        await bot.send_message(text, reply_markup=keyboard, chat_id=user_id)
        return True