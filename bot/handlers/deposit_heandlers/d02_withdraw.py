from TonTools import *
from TonTools.Contracts.Wallet import Wallet
from TonTools.Providers.LsClient import LsClient
from aiogram import Router, types
from aiogram.types import Message
from aiogram.dispatcher.fsm.context import FSMContext

from bot.db.methods import get_last_transaction, \
    get_token_by_id, get_user_wallet
from bot.menus.deposit_menus.replenish_menu import replenish_menu
from bot.menus.deposit_menus.withdraw_menu1 import withdraw_menu
from bot.utils.config_reader import config

flags = {"throttling_key": "default"}
router = Router()


@router.callback_query(text=["withdraw"])
async def withdraw(call: types.CallbackQuery, state: FSMContext):

    text, keyboard = withdraw_menu()
    await call.message.edit_text(text, reply_markup=keyboard)

@router.message()
async def withdraw_user_text(message: Message, state: FSMContext):
    await message.delete()
    try:
        user_withdraw = float(message.text)
    except ValueError:
        return
    round_user_withdraw = round(user_withdraw, 2)
    print(round_user_withdraw)