from aiogram import Router, exceptions, types
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from bot.db import db, manager
from bot.handlers.states import Menu, StateKeys
from bot.handlers.wheel_of_fortune_handlers.buy_ticket import create_random_tickets
from bot.menus.account_menus import promocodes_menu
from bot.menus.account_menus.promocodes_menu import approve_activation_balance_promo, approve_decline_promo_code_menu

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
    promo_code_entered = (await state.get_data()).get(StateKeys.PROMO_CODE_ENTERED)
    active_promos = await db.get_all_active_user_promo_codes(call.from_user.id)
    all_available_promo = await db.get_all_available_promo_code_for_user(call.from_user.id)
    new_promo_info = await db.get_promo_code_info(promo_code_entered)

    err = check_enter_promo_code(new_promo_info, active_promos, all_available_promo)
    if err is not None:
        await call.answer(err, show_alert=True)
        return

    if len(active_promos) == 1 and active_promos[0].promocode.type == 'ticket' and new_promo_info.type == 'balance':
        text, kb = approve_activation_balance_promo(active_promos[0].promo_name_id, new_promo_info.name)
        await call.message.edit_text(text, reply_markup=kb)
        return

    await db.user_activated_promo_code(call.from_user.id, promo_code_entered)
    await call.answer(_("PROMO_CODE_IS_ACTIVATED").format(promo_code=promo_code_entered), show_alert=True)


@router.callback_query(Text("activate_promo_balance"))
async def approve_activate_promo_balance(call: types.CallbackQuery, state: FSMContext):
    promo_code_entered = (await state.get_data()).get(StateKeys.PROMO_CODE_ENTERED)

    await db.user_activated_promo_code(call.from_user.id, promo_code_entered)
    await call.answer(_("PROMO_CODE_IS_ACTIVATED").format(promo_code=promo_code_entered), show_alert=True)

    await promo_codes_handler(call, state)


@router.callback_query(Text("my_promo_codes"))
async def my_promo_codes(call: types.CallbackQuery):
    try:
        balance_promo, ticket_promo, sum_bets_min_wager, sum_bets_wager = \
            await db.get_sum_bets_and_promo_info(call.from_user.id)
    except TypeError as e:
        await call.answer(_("MY_PROMO_CODES_ACTIVE_PROMO_NOT_FOUND_ERR"), show_alert=True)
        return

    if not balance_promo and not ticket_promo:
        await call.answer(_("MY_PROMO_CODES_ACTIVE_PROMO_NOT_FOUND_ERR"), show_alert=True)
        return

    if balance_promo and sum_bets_min_wager:
        if sum_bets_min_wager > balance_promo.promocode.min_wager:
            await db.min_wager_condition_accepted(call.from_user.id, balance_promo.promo_name_id)

    text, keyboard = promocodes_menu.my_promo_code_menu(sum_bets_min_wager, balance_promo, ticket_promo, sum_bets_wager)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("claim_reward"))
async def promo_code_claim_reward(call: types.CallbackQuery):
    balance_promo_code, ticket_promo_code, bets_sum_min_wager, bets_sum_wager = \
        await db.get_sum_bets_and_promo_info(call.from_user.id)

    err = check_promo_claim_reward_err(balance_promo_code, ticket_promo_code, bets_sum_min_wager, bets_sum_wager)
    if err is not None:
        await call.answer(err, show_alert=True)
        return

    if bets_sum_min_wager > balance_promo_code.promocode.min_wager:
        await db.min_wager_condition_accepted(call.from_user.id, balance_promo_code.promo_name_id)

    balances = await db.get_user_balances(call.from_user.id)
    with manager.pw_database.atomic():
        await db.update_user_balance(call.from_user.id, 'general', balances['promo'])
        await db.update_user_balance(call.from_user.id, 'promo', -balances['promo'])
        await db.deactivate_user_promo_code(call.from_user.id)


@router.callback_query(Text("approve_decline_promo_code"))
async def approve_decline_promo_code(call: types.CallbackQuery, state):
    text, kb = approve_decline_promo_code_menu()
    await call.message.edit_text(text, reply_markup=kb)


@router.callback_query(Text("decline_promo_code"))
async def decline_promo_code(call: types.CallbackQuery, state):
    await db.deactivate_user_promo_code(call.from_user.id)

    balances = await db.get_user_balances(call.from_user.id)
    promo_balance = balances['promo']
    if promo_balance > 0:
        await db.update_user_balance(call.from_user.id, 'promo', -promo_balance)

    await call.answer(_("PROMO_CODE_DECLINE_TEXT"), show_alert=True)
    await promo_codes_handler(call, state)


@router.callback_query(Text("promo_code_available"))
async def get_active_promo_codes(call: types.CallbackQuery, state: FSMContext):
    promo_codes = await db.get_all_available_promo_code_for_user(call.from_user.id)
    text = get_promo_codes_text(promo_codes)

    text, keyboard = promocodes_menu.active_promo_code_menu(text)
    await call.message.edit_text(text, reply_markup=keyboard)


def check_enter_promo_code(new_promo_info, active_promos, all_available_promo):
    active_promo_name = [code.promo_name_id for code in active_promos]

    if not new_promo_info:
        return _("PROMO_CODE_U_NEED_ENTER_ERR")

    if new_promo_info.name in active_promo_name:
        return _("PROMO_CODE_IS_ALREADY_ACTIVATED").format(promo_code=new_promo_info.name)

    if new_promo_info.name not in all_available_promo:
        return _("PROMO_CODE_DOESNT_EXIST_ERR")

    for code in active_promos:
        if code.promocode.type == new_promo_info.type:
            return _("PROMO_CODE_CANT_BE_TWO_PROMOCODES_SAME_TYPE")

    return None


def check_promo_claim_reward_err(balance_promo, ticket_promo, bets_sum_min_wager, bets_sum_wager):
    if balance_promo and ticket_promo:
        if balance_promo.deposited_bonus != 0:
            if balance_promo.deposited_min_wager > bets_sum_min_wager:
                return _("PROMOCODE_CLAIM_ERR_NOT_ENOUGH_MIN_WAGER_BETS").format(min_wager_remainder=balance_promo.deposited_min_wager - bets_sum_min_wager)

        if bets_sum_wager < balance_promo.deposited_wager + ticket_promo.deposited_wager:
            return _("PROMOCODE_CLAIM_ERR_NOT_ENOUGH_WAGER_BETS").format(
                wager_remainder=balance_promo.deposited_wager + ticket_promo.deposited_wager - bets_sum_wager)

    if ticket_promo:
        if ticket_promo.deposited_wager < bets_sum_wager:
            return _("PROMOCODE_CLAIM_ERR_NOT_ENOUGH_WAGER_BETS").format(wager_remainder=ticket_promo.deposited_wager - bets_sum_wager)

    if balance_promo:
        if balance_promo.deposited_min_wager > bets_sum_min_wager:
            return _("PROMOCODE_CLAIM_ERR_NOT_ENOUGH_MIN_WAGER_BETS").format(
                min_wager_remainder=balance_promo.deposited_min_wager - bets_sum_min_wager)

        if balance_promo.deposited_wager > bets_sum_wager:
            return _("PROMOCODE_CLAIM_ERR_NOT_ENOUGH_WAGER BETS").format(wager=balance_promo.deposited_wager - bets_sum_wager)

    return None


def get_promo_codes_text(promo_codes):
    text = ''
    for promo_code in promo_codes:
        text += f"<code>{promo_code}</code>" + '\n'

    return text
