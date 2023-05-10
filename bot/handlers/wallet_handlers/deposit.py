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
