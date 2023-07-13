from aiogram import Router, types
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from bot.db import db, manager
from bot.handlers.states import Menu
from bot.menus.account_menus import promocodes_menu
from bot.menus.utils import kb_del_msg

router = Router()


@router.callback_query(Text("promo_codes"))
async def promo_codes_handler(call: types.CallbackQuery, state):
    text, keyboard = promocodes_menu.promo_code_menu()
    await call.message.edit_text(text, reply_markup=keyboard)

    await state.set_state(Menu.delete_message)


@router.callback_query(Text("my_promo_codes"))
async def promo_codes_handler(call: types.CallbackQuery):
    is_active = await db.get_active_promo_code(call.from_user.id, 'balance')
    if not is_active:
        await call.answer(_("MY_PROMO_CODES_ACTIVE_PROMO_NOT_FOUND_ERR"))
        return

    text, keyboard = promocodes_menu.my_promo_code_menu()
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("claim_reward"))
async def promo_code_claim_reward(call: types.CallbackQuery):
    try:
        sum_bets, min_wager, wager = await db.get_sum_bets_from_activated_promo_min_wager_and_wager(call.from_user.id)
    except TypeError:
        await call.answer('poshel nahui', show_alert=True)
        return

    if sum_bets < wager:
        await call.answer(_("PROMO_CODE_CLAIM_REWARD_NOT_ENOUGH_BETS_ERR"), show_alert=True)
        return

    balances = await db.get_user_balances(call.from_user.id)
    with manager.pw_database.atomic():
        await db.update_user_balance(call.from_user.id, 'general', balances['promo'])
        await db.update_user_balance(call.from_user.id, 'promo', 0)


@router.callback_query(Text("promo_code_available"))
async def active_promo_codes(call: types.CallbackQuery, state: FSMContext):
    promo_codes = await db.get_all_active_promo_code(call.from_user.id)
    text = get_promo_codes_text(promo_codes)

    text, keyboard = promocodes_menu.active_promo_code_menu(text)
    await call.message.edit_text(text, reply_markup=keyboard)

    await state.set_state(Menu.enter_promo_code)


def get_promo_codes_text(promo_codes):
    text = ''
    for promo_code in promo_codes:
        text += f"<code>{promo_code}</code>" + '\n'

    return text


@router.message(StateFilter(Menu.enter_promo_code))
async def enter_promo_code(message: Message):
    await message.delete()
    promo_code = message.text
    all_active_promo = await db.get_all_active_promo_code(message.from_user.id)

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
