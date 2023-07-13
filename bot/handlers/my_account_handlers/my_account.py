from aiogram import Router, types
from aiogram.filters import Text

from bot.db import db
from bot.handlers.states import Menu, StateKeys
from bot.menus.account_menus.account_menu import my_account_menu

router = Router()


@router.callback_query(Text("my_account"))
async def settings(call: types.CallbackQuery, state):
    balances = await db.get_user_balances(call.from_user.id)
    await state.update_data({StateKeys.PROMO_CODE_ENTERED: None})

    text, keyboard = my_account_menu(balances)
    await call.message.edit_text(text, reply_markup=keyboard)

    await state.set_state(Menu.delete_message)
