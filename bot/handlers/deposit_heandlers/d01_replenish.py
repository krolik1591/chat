from pprint import pprint

from TonTools import *
from TonTools.Contracts.Wallet import Wallet
from TonTools.Providers.LsClient import LsClient
from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext

from bot.db.methods import add_new_transaction, create_user_wallet, deposit_token, get_all_users, get_last_transaction, \
    get_token_by_id, get_user_wallet
from bot.menus.deposit_menus.replenish_menu import replenish_menu
from bot.ton.find_tx import find_new_user_tx
from bot.ton.wallets import TonWrapper

from bot.utils.config_reader import config
from bot.db.db import manager

import time
from time import monotonic as timer

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
    # await user_wallet.transfer_ton(master_wallet.address, 0.004)
    # await user_wallet.transfer_ton(master_wallet.address, 0.0001)
    TOKEN_ID = 2
    token = await get_token_by_id(TOKEN_ID)

    last_tx_from_db = await get_last_transaction(call.from_user.id, TOKEN_ID)
    print(last_tx_from_db.logical_time)

    # todo replace with ton_client.get_account_transactions
    # account = await ton_client.find_account(user_wallet.address)
    # all_tx = await account.get_transactions(last_tx_from_db.logical_time, last_tx_from_db.tx_hash)


    # wallets_key = await get_all_users()
    #
    # for user in wallets_key:
    #     await find_new_user_tx(ton_wrapper, user, master_wallet.address)