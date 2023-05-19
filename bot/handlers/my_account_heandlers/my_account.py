from aiogram import Router, types
from aiogram.filters import Text

from bot.db import db
from bot.menus.my_account_menus.my_account_menu import my_account_menu

router = Router()


@router.callback_query(Text("my_account"))
async def settings(call: types.CallbackQuery):
    balances = await db.get_user_balances(call.from_user.id)

    text, keyboard = my_account_menu(balances)
    await call.message.edit_text(text, reply_markup=keyboard)


