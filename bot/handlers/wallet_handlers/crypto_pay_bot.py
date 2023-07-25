from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from bot.db import db
from bot.menus.wallet_menus.crypto_pay_menus import crypto_pay_menu

router = Router()


@router.callback_query(Text("crypto_pay"))
async def crypro_pay(call: types.CallbackQuery, state: FSMContext):

    text, keyboard = crypto_pay_menu()
    await call.message.edit_text(text, reply_markup=keyboard)
