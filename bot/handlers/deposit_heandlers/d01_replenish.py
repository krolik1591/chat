from pprint import pprint

from TonTools import *
from TonTools.Contracts.Wallet import Wallet
from TonTools.Providers.LsClient import LsClient
from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext

from bot.db.methods import add_new_transaction, create_user_wallet, deposit_token, get_last_transaction, \
    get_token_by_id, get_user_wallet
from bot.menus.deposit_menus.replenish_menu import replenish_menu

from bot.utils.config_reader import config
from bot.db.db import manager

flags = {"throttling_key": "default"}
router = Router()


@router.callback_query(text=["replenish"])
async def replenish(call: types.CallbackQuery, state: FSMContext):
    user_wallet = await get_user_wallet(call.from_user.id)

    text, keyboard = replenish_menu(user_wallet.address)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(text=["ton_check"])
async def ton_check(call: types.CallbackQuery, state: FSMContext):
    ton_client: LsClient = state.bot.ton_client

    master_wallet_seed = config.wallet_seed.split(' ')
    master_wallet = Wallet(provider=ton_client, mnemonics=master_wallet_seed)

    user_wallet_info = await get_user_wallet(call.from_user.id)
    user_mnemonic = user_wallet_info.mnemonic.split(',')

    user_wallet = Wallet(provider=ton_client, mnemonics=user_mnemonic)
    user_init_condition = await user_wallet.get_state()

    if user_init_condition == 'uninitialized':
        # todo if balance < 13 centiv:  fuck off
        print('мінус 13 центів сучара')
        await user_wallet.deploy()

    mw_init_condition = await master_wallet.get_state()
    if mw_init_condition == 'uninitialized':
        print('mw not inited')
        non_bounceable_master_wallet_address = Address(master_wallet.address).to_string(True, True, False)
        await user_wallet.transfer_ton(destination_address=non_bounceable_master_wallet_address, amount=0.02)
        await master_wallet.deploy()
    print(await master_wallet.get_balance())
    # await user_wallet.transfer_ton(master_wallet.address, 0.004)
    # await user_wallet.transfer_ton(master_wallet.address, 0.0001)

    TOKEN_ID = 2
    token = await get_token_by_id(TOKEN_ID)

    last_tx_from_db = await get_last_transaction(call.from_user.id, TOKEN_ID)
    print(last_tx_from_db.logical_time)

    account = await ton_client.find_account(user_wallet.address)
    all_tx = await account.get_transactions(last_tx_from_db.logical_time, last_tx_from_db.tx_hash)

    for item in all_tx:
        await process_tx(item, token, call.from_user.id, master_wallet.address, user_wallet.address)


async def process_tx(outer_tx, token, user_id, master_wallet, user_wallet):
    tx_hash = outer_tx.transaction_id.hash
    tx_lt = outer_tx.transaction_id.lt

    inners_txs = [outer_tx.in_msg, *outer_tx.out_msgs]

    for tx in inners_txs:
        source, destination = tx.source.account_address, tx.destination.account_address

        # поповнення рахунку для поповнення
        if destination == user_wallet:
            if source == '':  # ignore empty source coz it means nothing (input msg that trigger some output msg)
                continue

            tx_type = 1
            tx_address = source

            # одразу відправляємо отримані гроші на мастер воллет
            # await user_wallet.transfer_ton(master_wallet.address, 0, send_mode=128) # так надо

        # переказ з юзер воллету на мастер воллет
        elif source == user_wallet and destination == master_wallet:
            tx_type = 2
            tx_address = master_wallet


        # переказ з мастер воллету на юзер воллет
        elif source == master_wallet and destination == user_wallet:
            tx_type = 3
            tx_address = user_wallet


        else:
            raise AssertionError('This should not happen')

        amount = int(tx.value) / 1e9 * token.price
        value_nano_ton = tx.value

        print(f"SAVE TX {tx_type=} {tx_lt=}")
        with manager.pw_database.atomic():
            await deposit_token(user_id, token.token_id, amount)
            await add_new_transaction(
                user_id, token.token_id, value_nano_ton,
                tx_type, tx_address, tx_hash, logical_time=tx_lt, utime=outer_tx.utime)
