from TonTools.Contracts.Wallet import Wallet
from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext

from bot.db import db
from bot.menus.wallet_menus.deposit_menu import deposit_menu
from bot.tokens.token_ton import TonWrapper

router = Router()


@router.callback_query(text=["replenish"])
async def replenish(call: types.CallbackQuery, state: FSMContext):
    user_wallet = await db.get_user_wallet(call.from_user.id)

    text, keyboard = deposit_menu(user_wallet.address)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(text=["ton_check"])
async def ton_check(call: types.CallbackQuery, state: FSMContext):
    master_wallet = TonWrapper.INSTANCE.master_wallet

    user_wallet_info = await db.get_user_wallet(call.from_user.id)
    user_mnemonic = user_wallet_info.mnemonic.split(',')
    user_wallet = Wallet(provider=TonWrapper.INSTANCE, mnemonics=user_mnemonic)

    mw_init_condition = await master_wallet.get_state()
    user_init_condition = await user_wallet.get_state()
    print(user_init_condition, mw_init_condition)

    mw_balance = await master_wallet.get_balance()
    uw_balance = await user_wallet.get_balance()
    print('mw balance', mw_balance)
    print('uw balance', uw_balance)
