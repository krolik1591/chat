import pydantic.error_wrappers
from aiogram import Router, types
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from bot.db import db
from bot.handlers.states import Menu
from bot.menus.account_menus.account_menu import active_promo_code_menu, promo_code_menu
from bot.menus.utils import kb_del_msg

router = Router()


@router.callback_query(Text("promo_codes"))
async def promo_codes_handler(call: types.CallbackQuery, state):
    text, keyboard = promo_code_menu()
    await call.message.edit_text(text, reply_markup=keyboard)

    await state.set_state(Menu.delete_message)


@router.callback_query(Text("active_promo_codes"))
async def active_promo_codes(call: types.CallbackQuery, state: FSMContext):
    promo_codes = await db.get_all_active_promo_code()
    text = get_promo_codes_text(promo_codes)

    text, keyboard = active_promo_code_menu(text)
    await call.message.edit_text(text, reply_markup=keyboard)

    await state.set_state(Menu.enter_promo_code)


def get_promo_codes_text(promo_codes):
    text = ''
    for promo_code in promo_codes:
        text += f"<code>{promo_code}</code>" + '\n'

    return text


@router.message(StateFilter(Menu.enter_promo_code))
async def enter_promo_code(message: Message, state):
    await message.delete()
    promo_code = message.text
    all_active_promo = await db.get_all_active_promo_code()

    if promo_code not in all_active_promo:
        await message.answer(_("PROMO_CODE_DOESNT_EXIST_ERR"), reply_markup=kb_del_msg())
        return

    active_promo = await db.get_active_promo_code(message.from_user.id, 'balance')
    if active_promo:
        await message.answer(_("PROMO_CODE_IS_ALREADY_ACTIVATED").format(promo_code=active_promo),
                             reply_markup=kb_del_msg())
        return

    await db.user_activated_promo_code(357108179, promo_code)

    await message.answer(_("PROMO_CODE_IS_ACTIVATED").format(promo_code=promo_code), reply_markup=kb_del_msg())
