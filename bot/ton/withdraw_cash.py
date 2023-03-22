from TonTools import *
from TonTools.Contracts.Wallet import Wallet
from TonTools.Providers.LsClient import LsClient
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext

from bot.db.methods import get_token_by_id, get_user_wallet
from bot.handlers.deposit_heandlers.d01_replenish import prepare_wallets_to_work
from bot.utils.config_reader import config


async def withdraw_cash_to_user(state: FSMContext, user_id, user_withdraw_address):
    master_wallet, _ = await prepare_wallets_to_work(state, user_id)
    print('mw', master_wallet.address, await master_wallet.get_balance())

    TOKEN_ID = 2
    token = await get_token_by_id(TOKEN_ID)
    amount = (await state.get_data()).get('user_withdraw_amount')
    withdraw_value = amount * 1e9 / token.price

    await master_wallet.transfer_ton(user_withdraw_address, withdraw_value)