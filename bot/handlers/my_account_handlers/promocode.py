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
    active_promo = await db.get_all_active_user_promo_codes(call.from_user.id)
    all_available_promo = await db.get_all_available_promo_code_for_user(call.from_user.id)
    active_promo_info = [await db.get_promo_code_info(code) for code in active_promo]
    new_promo_info = await db.get_promo_code_info(promo_code)

    err = check_enter_promo_code(new_promo_info, active_promo, all_available_promo, active_promo_info)
    if err is not None:
        await call.answer(err, show_alert=True)
        return

    await db.user_activated_promo_code(call.from_user.id, promo_code)
    await call.answer(_("PROMO_CODE_IS_ACTIVATED").format(promo_code=promo_code), show_alert=True)


@router.callback_query(Text("my_promo_codes"))
async def my_promo_codes(call: types.CallbackQuery):
    try:
        sum_bets, balance_promo, ticket_promo = await db.get_sum_bets_and_promo_info(call.from_user.id)
    except TypeError as e:
        await call.answer(_("MY_PROMO_CODES_ACTIVE_PROMO_NOT_FOUND_ERR"), show_alert=True)
        return

    if not balance_promo and not ticket_promo:
        await call.answer(_("MY_PROMO_CODES_ACTIVE_PROMO_NOT_FOUND_ERR"), show_alert=True)
        return

    if balance_promo and sum_bets:
        if sum_bets > balance_promo.promocode.min_wager:
            await db.min_wager_condition_accepted(call.from_user.id, balance_promo.promo_name)

    text, keyboard = promocodes_menu.my_promo_code_menu(sum_bets, balance_promo, ticket_promo)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("claim_reward"))
async def promo_code_claim_reward(call: types.CallbackQuery):
    bets_sum, balance_promo_code, ticket_promo_code = await db.get_sum_bets_and_promo_info(call.from_user.id)

    err = check_promo_claim_reward_err(bets_sum, balance_promo_code.promocode.min_wager,
                                       balance_promo_code.promocode.wager)
    if err is not None:
        await call.answer(err, show_alert=True)
        return

    if bets_sum > balance_promo_code.promocode.min_wager:
        await db.min_wager_condition_accepted(call.from_user.id, balance_promo_code.promo_name)

    balances = await db.get_user_balances(call.from_user.id)
    with manager.pw_database.atomic():
        await db.update_user_balance(call.from_user.id, 'general', balances['promo'])
        await db.update_user_balance(call.from_user.id, 'promo', -balances['promo'])
        await db.deactivate_user_promo_code(call.from_user.id)


@router.callback_query(Text("decline_promo_code"))
async def decline_promo_code(call: types.CallbackQuery, state):
    promo_code = await db.get_all_info_user_promo_code(call.from_user.id, 'balance')
    await db.deactivate_user_promo_code(call.from_user.id)

    balances = await db.get_user_balances(call.from_user.id)
    promo_balance = balances['promo']
    if promo_balance > 0:
        await db.update_user_balance(call.from_user.id, 'promo', -promo_balance)

    await call.answer(_("PROMO_CODE_DECLINE_TEXT").format(promo_code=promo_code.promo_name), show_alert=True)
    await promo_codes_handler(call, state)


@router.callback_query(Text("promo_code_available"))
async def active_promo_codes(call: types.CallbackQuery, state: FSMContext):
    promo_codes = await db.get_all_available_promo_code_for_user(call.from_user.id)
    text = get_promo_codes_text(promo_codes)

    text, keyboard = promocodes_menu.active_promo_code_menu(text)
    await call.message.edit_text(text, reply_markup=keyboard)


def check_enter_promo_code(new_promo_info, active_promo, all_available_promo, promo_codes_info):
    if not new_promo_info:
        return _("PROMO_CODE_U_NEED_ENTER_ERR")

    if new_promo_info.name in active_promo:
        return _("PROMO_CODE_IS_ALREADY_ACTIVATED").format(promo_code=new_promo_info.name)

    if new_promo_info.name not in all_available_promo:
        return _("PROMO_CODE_DOESNT_EXIST_ERR")

    for code in promo_codes_info:
        if code.type == new_promo_info.type:
            return _("PROMO_CODE_CANT_BE_TWO_PROMOCODES_SAME_TYPE")

    return None


def check_promo_claim_reward_err(sum_bets, min_wager, wager):
    if not min_wager:
        return _('M06_PLAY_DICE_NOT_EXIST_PROMO_BALANCE')

    if not sum_bets:
        return _('M06_PLAY_DICE_NOT_ENOUGH_BETS_TO_PLAY_PROMO').format(missing_bets=wager)

    if sum_bets < wager:
        return _("PROMO_CODE_CLAIM_REWARD_NOT_ENOUGH_BETS_ERR").format(missing_bets=wager - sum_bets)

    return None


def get_promo_codes_text(promo_codes):
    text = ''
    for promo_code in promo_codes:
        text += f"<code>{promo_code}</code>" + '\n'

    return text
