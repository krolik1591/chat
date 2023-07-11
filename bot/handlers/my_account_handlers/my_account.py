from aiogram import Router, types
from aiogram.filters import Text

from bot.db import db
from bot.menus.account_menus.account_menu import active_promo_code_menu, my_account_menu, promo_code_menu

router = Router()


@router.callback_query(Text("my_account"))
async def settings(call: types.CallbackQuery):
    balances = await db.get_user_balances(call.from_user.id)

    text, keyboard = my_account_menu(balances)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("promo_codes"))
async def promo_codes_handler(call: types.CallbackQuery):
    text, keyboard = promo_code_menu()
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("active_promo_codes"))
async def active_promo_codes(call: types.CallbackQuery):
    promo_codes = await db.get_all_active_promo_code()
    text = get_promo_codes_text(promo_codes)

    text, keyboard = active_promo_code_menu(text)
    await call.message.edit_text(text, reply_markup=keyboard)


def get_promo_codes_text(promo_codes):
    text = ''
    for promo_code in promo_codes:
        text += f"<code>{promo_code}</code>" + '\n'

    return text
