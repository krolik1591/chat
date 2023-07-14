from aiogram import Router, exceptions, types
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from bot.db import db, manager
from bot.handlers.states import Menu, StateKeys
from bot.menus.account_menus import promocodes_menu

router = Router()


@router.callback_query(Text("promo_codes"))
async def promo_codes_handler(call: types.CallbackQuery, state: FSMContext):
    promo_code = (await state.get_data()).get(StateKeys.PROMO_CODE_ENTERED)
    if promo_code is None:
        promo_code = ''

    text, keyboard = promocodes_menu.promo_code_menu(promo_code)
    await call.message.edit_text(text, reply_markup=keyboard)

    await state.set_state(Menu.enter_promo_code)


@router.message(StateFilter(Menu.enter_promo_code))
async def enter_promo_code(message: Message, state: FSMContext):
    await message.delete()

    promo_code = message.text
    previous_promo_code = (await state.get_data()).get(StateKeys.PROMO_CODE_ENTERED)
    if previous_promo_code == promo_code:
        return

    await state.update_data({StateKeys.PROMO_CODE_ENTERED: promo_code})
    last_msg = (await state.get_data()).get(StateKeys.LAST_MSG_ID)

    text, keyboard = promocodes_menu.promo_code_menu(promo_code)
    await state.bot.edit_message_text(text, message.from_user.id, last_msg, reply_markup=keyboard)


@router.callback_query(Text("active_promo_code"))
async def active_promo_code(call: types.CallbackQuery, state: FSMContext):
    promo_code = (await state.get_data()).get(StateKeys.PROMO_CODE_ENTERED)
    active_promo = await db.get_active_promo_code_of_user(call.from_user.id, 'balance')
    all_active_promo = await db.get_all_available_promo_code_for_user(call.from_user.id)

    err = check_enter_promo_code(promo_code, active_promo, all_active_promo)
    if err is not None:
        await call.answer(err, show_alert=True)
        return

    await db.user_activated_promo_code(call.from_user.id, promo_code)
    await call.answer(_("PROMO_CODE_IS_ACTIVATED").format(promo_code=promo_code), show_alert=True)


@router.callback_query(Text("my_promo_codes"))
async def my_promo_codes(call: types.CallbackQuery):
    promo_code = await db.get_active_promo_code_of_user(call.from_user.id, 'balance')
    if not promo_code:
        await call.answer(_("MY_PROMO_CODES_ACTIVE_PROMO_NOT_FOUND_ERR"), show_alert=True)
        return

    sum_bets, min_wager, wager = await db.get_sum_bets_from_activated_promo_min_wager_and_wager(call.from_user.id)

    text, keyboard = promocodes_menu.my_promo_code_menu(sum_bets, min_wager, wager, promo_code)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("claim_reward"))
async def promo_code_claim_reward(call: types.CallbackQuery):
    sum_bets, min_wager, wager = await db.get_sum_bets_from_activated_promo_min_wager_and_wager(call.from_user.id)

    err = check_promo_claim_reward_err(sum_bets, min_wager, wager)
    if err is not None:
        await call.answer(err, show_alert=True)
        return

    balances = await db.get_user_balances(call.from_user.id)
    with manager.pw_database.atomic():
        await db.update_user_balance(call.from_user.id, 'general', balances['promo'])
        await db.update_user_balance(call.from_user.id, 'promo', 0)


@router.callback_query(Text("promo_code_available"))
async def active_promo_codes(call: types.CallbackQuery, state: FSMContext):
    promo_codes = await db.get_all_available_promo_code_for_user(call.from_user.id)
    text = get_promo_codes_text(promo_codes)

    text, keyboard = promocodes_menu.active_promo_code_menu(text)
    await call.message.edit_text(text, reply_markup=keyboard)


def check_enter_promo_code(promo_code, active_promo, all_active_promo):
    if not promo_code:
        return _("PROMO_CODE_U_NEED_ENTER_ERR")

    if active_promo:
        return _("PROMO_CODE_IS_ALREADY_ACTIVATED").format(promo_code=active_promo)

    if promo_code not in all_active_promo:
        return _("PROMO_CODE_DOESNT_EXIST_ERR")

    return None


def check_promo_claim_reward_err(sum_bets, min_wager, wager):
    if not min_wager:
        return _('M06_PLAY_DICE_NOT_EXIST_PROMO_BALANCE')

    if not sum_bets:
        return _('M06_PLAY_DICE_NOT_ENOUGH_BETS_TO_PLAY_PROMO')

    if sum_bets < wager:
        return _("PROMO_CODE_CLAIM_REWARD_NOT_ENOUGH_BETS_ERR")

    return None


def get_promo_codes_text(promo_codes):
    text = ''
    for promo_code in promo_codes:
        text += f"<code>{promo_code}</code>" + '\n'

    return text
