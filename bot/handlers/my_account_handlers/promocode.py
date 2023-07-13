from aiogram import Router, types
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from bot.db import db, manager
from bot.handlers.states import Menu, StateKeys
from bot.menus.account_menus import promocodes_menu
from bot.menus.utils import kb_del_msg

router = Router()


@router.callback_query(Text("promo_codes"))
async def promo_codes_handler(call: types.CallbackQuery, state):
    text, keyboard = promocodes_menu.promo_code_menu()
    await call.message.edit_text(text, reply_markup=keyboard)

    await state.set_state(Menu.enter_promo_code)


@router.callback_query(Text("active_promo_code"))
async def active_promo_code(call: types.CallbackQuery):
    all_active_promo = await db.get_all_active_promo_code(call.from_user.id)

    if promo_code not in all_active_promo:
        await call.answer(_("PROMO_CODE_DOESNT_EXIST_ERR"), reply_markup=kb_del_msg())
        return

    active_promo = await db.get_active_promo_code(call.from_user.id, 'balance')
    if active_promo:
        await call.answer(_("PROMO_CODE_IS_ALREADY_ACTIVATED").format(promo_code=active_promo),
                             reply_markup=kb_del_msg())
        return

    await db.user_activated_promo_code(357108179, promo_code)
    await call.answer(_("PROMO_CODE_IS_ACTIVATED").format(promo_code=promo_code), reply_markup=kb_del_msg())


@router.callback_query(Text("my_promo_codes"))
async def my_promo_codes(call: types.CallbackQuery):
    is_active = await db.get_active_promo_code(call.from_user.id, 'balance')
    if not is_active:
        await call.answer(_("MY_PROMO_CODES_ACTIVE_PROMO_NOT_FOUND_ERR"), show_alert=True)
        return

    sum_bets, min_wager, wager = await db.get_sum_bets_from_activated_promo_min_wager_and_wager(call.from_user.id)

    text, keyboard = promocodes_menu.my_promo_code_menu(sum_bets, min_wager, wager, is_active)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("claim_reward"))
async def promo_code_claim_reward(call: types.CallbackQuery):
    try:
        sum_bets, min_wager, wager = await db.get_sum_bets_from_activated_promo_min_wager_and_wager(call.from_user.id)
    except TypeError:
        await call.answer('This not should be happen', show_alert=True)
        return

    if not min_wager:
        await call.answer(_('M06_PLAY_DICE_NOT_EXIST_PROMO_BALANCE'), show_alert=True)
        return False

    if not sum_bets:
        await call.answer(_('M06_PLAY_DICE_NOT_ENOUGH_BETS_TO_PLAY_PROMO')
                          .format(missing_bets=wager), show_alert=True)
        return False

    if sum_bets < wager:
        await call.answer(_("PROMO_CODE_CLAIM_REWARD_NOT_ENOUGH_BETS_ERR").format(missing_bets=wager-sum_bets),
                          show_alert=True)
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


def get_promo_codes_text(promo_codes):
    text = ''
    for promo_code in promo_codes:
        text += f"<code>{promo_code}</code>" + '\n'

    return text


@router.message(StateFilter(Menu.enter_promo_code))
async def enter_promo_code(message: Message, state: FSMContext):
    await message.delete()
    promo_code = message.text
    await state.update_data({StateKeys.PROMO_CODE_ENTERED: promo_code})
