from aiogram import types, Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from bot import tokens
from bot.consts.const import USDT_TO_GAMETOKENS
from bot.db import db
from bot.menus import wallet_menus

router = Router()


@router.callback_query(Text("wallet_menu"))
async def wallet_menu_handler(call: types.CallbackQuery, state: FSMContext):
    balances = await db.get_user_balances(call.from_user.id)

    text, keyboard = wallet_menus.wallet_menu(balances, USDT_TO_GAMETOKENS)
    await call.message.edit_text(text, reply_markup=keyboard)
