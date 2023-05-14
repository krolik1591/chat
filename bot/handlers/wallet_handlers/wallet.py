from aiogram import types, Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from bot import tokens
from bot.db import db
from bot.menus import wallet_menus

router = Router()


@router.callback_query(Text("wallet_menu"))
async def wallet_menu_handler(call: types.CallbackQuery, state: FSMContext):
    balances = await db.get_user_balances(call.from_user.id)

    token = await tokens.get_token_by_id("ton")

    text, keyboard = wallet_menus.wallet_menu(balances, await token.get_price())
    await call.message.edit_text(text, reply_markup=keyboard)
