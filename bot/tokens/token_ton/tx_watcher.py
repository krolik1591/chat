import asyncio
import logging

import ton.tonlibjson
from TonTools.Contracts import Wallet

from bot.consts.const import TON_INITIALISATION_FEE
from bot.db import db, manager, models
from bot.menus.wallet_menus import deposit_menu
from bot.tokens.token_ton import TonWrapper, ton_token


# todo оптимизация: сортировать пользователей по последней активности
async def watch_txs(ton_wrapper: TonWrapper, bot):
    async def find_new_user_tx_(user_):
        try:
            new_txs = await find_new_txs(ton_wrapper, user_)
            user_wallet = ton_wrapper.get_wallet(user_.mnemonic)
            for tx in new_txs:
                await process_user_tx(tx, user_.user_id, user_wallet, bot)

        except ton.tonlibjson.TonlibError as ex:
            logging.exception('TonLib error')

    while True:
        all_users_wallets = await db.get_all_user_wallets()
        coros = [find_new_user_tx_(user) for user in all_users_wallets]
        await asyncio.gather(*coros)

        await asyncio.sleep(10)


async def find_new_txs(ton_wrapper: TonWrapper, user: models.Wallets_key):
    user_account = await ton_wrapper.find_account(user.address)

    last_tx_from_blockchain = user_account.state.last_transaction_id
    last_tx_from_db = await db.get_last_transaction(user.user_id, ton_token.id)

    if last_tx_from_blockchain.hash == last_tx_from_db.tx_hash:
        # no new txs
        return

    return await ton_wrapper.get_account_transactions(
        user_account.address,
        last_tx_lt=last_tx_from_blockchain.lt,
        last_tx_hash=last_tx_from_blockchain.hash,
        first_tx_hash=last_tx_from_db.tx_hash)


async def process_user_tx(tx, user_id, user_wallet: Wallet, bot):
    # поповнення рахунку для поповнення
    if tx['destination'] == user_wallet.address:
        await user_deposited(tx, bot, user_id, user_wallet)
    # переказ з юзер воллету на мастер воллет
    elif tx['source'] == user_wallet.address and tx['destination'] == TonWrapper.INSTANCE.master_wallet.address:
        await user_deposit_moved_to_master(tx, user_id)
    else:
        raise AssertionError('This should not happen')


async def user_deposited(tx, bot, user_id, user_wallet: Wallet):
    amount_ton = int(tx['value']) / 1e9

    user_init_state = await user_wallet.get_state()
    if user_init_state == 'uninitialized':

        inited = await init_user_wallet(bot, user_id, user_wallet)
        if inited:
            amount_ton -= TON_INITIALISATION_FEE
            await asyncio.sleep(30)  # todo why?

    amount_gametokens = await ton_token.to_gametokens(amount_ton)

    await send_successful_deposit_msg(bot, user_id, amount_gametokens)

    with manager.pw_database.atomic():
        await db.update_user_balance(user_id, 'general', amount_gametokens)
        await db.add_new_transaction(
            user_id=user_id,
            token_id=ton_token.id,
            amount=tx['value'],
            tx_type=1,  # deposit
            tx_address=tx['source'],
            tx_hash=tx['tx_hash'],
            logical_time=tx['tx_lt'],
            utime=tx['utime']
        )

    # одразу відправляємо отримані гроші на мастер воллет
    await transfer_to_master(user_wallet)


async def user_deposit_moved_to_master(tx, user_id):
    await db.add_new_transaction(
        user_id=user_id,
        token_id=ton_token.id,
        amount=tx['value'],
        tx_type=2,  # deposit moved to master
        tx_address=TonWrapper.INSTANCE.master_wallet.address,  # todo ?
        tx_hash=tx['tx_hash'],
        logical_time=tx['tx_lt'],
        utime=tx['utime']
    )


async def transfer_to_master(user_wallet: Wallet):
    try:
        await user_wallet.transfer_ton(TonWrapper.INSTANCE.master_wallet.address, amount=500_000_000, send_mode=128)
    except:
        logging.exception('cant transfer cause wallet not inited '
                          f'(юзер: {user_wallet.address} бомж лох дєб нема 0.014 на рахунку)')


async def init_user_wallet(bot, user_id, user_wallet):
    user_balance = await user_wallet.get_balance()  # nano ton
    if user_balance <= TON_INITIALISATION_FEE * 1e9:
        await send_failed_initiation_msg(bot, user_id)
        return False

    print('deploying account', user_wallet.address)
    await user_wallet.deploy()
    await send_successful_initiation_msg(bot, user_id)
    return True


async def send_successful_deposit_msg(bot, user_id, amount):
    text, keyboard = deposit_menu.successful_deposit_menu(amount=round(amount, 2))
    await bot.send_message(user_id, text, reply_markup=keyboard)


async def send_successful_initiation_msg(bot, user_id):
    text, keyboard = deposit_menu.deposit_account_initiation(is_successful_inited=True)
    await bot.send_message(user_id, text, reply_markup=keyboard)


async def send_failed_initiation_msg(bot, user_id):
    text, keyboard = deposit_menu.deposit_account_initiation(is_successful_inited=False)
    await bot.send_message(user_id, text, reply_markup=keyboard)
