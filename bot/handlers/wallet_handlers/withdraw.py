import logging
import time

import tonsdk.utils
from TonTools import Address
from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramMigrateToChat

from bot.const import MAXIMUM_WITHDRAW, MAXIMUM_WITHDRAW_DAILY, MIN_WITHDRAW
from bot.db import manager, db
from bot.handlers.context import Context
from bot.handlers.states import Menu, StateKeys
from bot.handlers.wallet_handlers.withdraw_cash import withdraw_cash_to_user
from bot.menus.wallet_menus import withdraw_menu, withdraw_menu_err
from bot.utils.config_reader import config

router = Router()

TOKEN_ID = 2


@router.callback_query(text=["withdraw"])
async def withdraw_input_amount_menu(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(**{StateKeys.TOKEN_ID: TOKEN_ID})
    token = await db.get_token_by_id(TOKEN_ID)

    text, keyboard = withdraw_menu.input_amount(token.price)
    await call.message.edit_text(text, reply_markup=keyboard)
    await state.update_data(**{StateKeys.LAST_MSG_ID: call.message.message_id})
    await state.set_state(Menu.withdraw_amount)


@router.message(state=Menu.withdraw_amount)
async def withdraw_input_amount_handler(message: types.Message, state: FSMContext):
    await message.delete()

    amount = await validate_amount(message, token_id=2)
    if amount is None:
        return  # error msg already sent by validate_amount

    await state.update_data(user_withdraw_amount=amount)

    if await is_user_has_unresolved_tx(message.from_user.id):
        text, keyboard = withdraw_menu_err.manual_tx_in_process()
        await message.answer(text, reply_markup=keyboard)
        return

    context = await Context.from_fsm_context(message.from_user.id, state)
    await withdraw_input_address_menu(context)


async def withdraw_input_address_menu(context: Context):
    text, keyboard = withdraw_menu.input_address()  # input address
    await context.fsm_context.bot.edit_message_text(text, reply_markup=keyboard, chat_id=context.user_id,
                                                    message_id=context.last_msg_id)
    await context.fsm_context.set_state(Menu.withdraw_address)


@router.message(state=Menu.withdraw_address)
async def withdraw_input_address_handler(message: types.Message, state: FSMContext):
    await message.delete()
    try:
        user_withdraw_address = Address(message.text)
    except tonsdk.utils.InvalidAddressError:
        text, keyboard = withdraw_menu_err.withdraw_err_incorrect_address()
        await message.answer(text, reply_markup=keyboard)
        return

    if user_withdraw_address.is_test_only:
        text, keyboard = withdraw_menu_err.withdraw_err_testnet_address()
        await message.answer(text, reply_markup=keyboard)
        return

    await state.update_data(user_withdraw_address=user_withdraw_address.to_string())

    context = await Context.from_fsm_context(message.from_user.id, state)
    await withdraw_approve_menu(context)


async def withdraw_approve_menu(context: Context):
    withdraw_amount = context.state['user_withdraw_amount']
    withdraw_address = context.state['user_withdraw_address']
    token_price = (await db.get_token_by_id(token_id=2)).price

    text, keyboard = withdraw_menu.input_validation(withdraw_amount, withdraw_address, token_price)
    await context.fsm_context.bot.edit_message_text(text, reply_markup=keyboard, chat_id=context.user_id,
                                                    message_id=context.last_msg_id)
    await context.fsm_context.set_state(Menu.withdraw_amount_approve)


@router.message(state=Menu.withdraw_amount_approve)
async def withdraw_input_amount_handler_at_approve(message: types.Message, state: FSMContext):
    await message.delete()
    amount = await validate_amount(message, token_id=2)
    if amount is None:
        return  # error msg already sent by validate_amount

    await state.update_data(user_withdraw_amount=amount)

    context = await Context.from_fsm_context(message.from_user.id, state)
    await withdraw_approve_menu(context)


@router.callback_query(text=["withdraw_queued"])
async def withdraw_complete(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Menu.delete_message)

    state_data = await state.get_data()

    withdraw_amount = state_data['user_withdraw_amount']
    withdraw_address = state_data['user_withdraw_address']
    token_id = state_data[StateKeys.TOKEN_ID]

    token = await db.get_token_by_id(token_id)
    ton_amount = withdraw_amount / token.price

    #  Заявка на виплату {user_withdraw_amount_ton} TON • {user_withdraw_amount} 💎 прийнята!
    text, keyboard = withdraw_menu.withdraw_queued(withdraw_amount)
    await call.message.edit_text(text, reply_markup=keyboard)

    can_withdraw_today = how_much_can_withdraw_today(call.from_user.id, token_price=token.price)
    if withdraw_amount > can_withdraw_today:
        text, keyboard = withdraw_menu_err.reached_daily_limit(can_withdraw_today)
        await state.bot.send_message(call.from_user.id, text, reply_markup=keyboard)
        return

    if ton_amount > MAXIMUM_WITHDRAW:
        await create_manual_tx(call.from_user.id, call.from_user.username, ton_amount, state.bot, token,
                               withdraw_address)
        return

    await db.update_user_balance(call.from_user.id, token.token_id, -withdraw_amount)

    await withdraw_cash_to_user(state.bot, withdraw_address, ton_amount, call.from_user.id, token, manual_tx=False)


async def validate_amount(message, token_id):
    try:
        user_withdraw = float(message.text)
    except ValueError:
        return
    amount = round(user_withdraw, 2)

    token = await db.get_token_by_id(token_id)
    user_balance = await db.get_user_balance(message.from_user.id, 'general')

    if amount < MIN_WITHDRAW:
        text, keyboard = withdraw_menu_err.withdraw_too_small(token_price=token.price)
        await message.answer(text, reply_markup=keyboard)
        return

    if amount > user_balance:
        text, keyboard = withdraw_menu_err.withdraw_err_insufficient_funds()
        await message.answer(text, reply_markup=keyboard)
        return

    if amount > MAXIMUM_WITHDRAW_DAILY * token.price:
        text, keyboard = withdraw_menu_err.withdraw_too_big(token.price)
        await message.answer(text, reply_markup=keyboard)
        return

    return amount


async def create_manual_tx(user_id, username, ton_amount, bot, token, withdraw_address):
    with manager.pw_database.atomic():
        new_tx = await db.add_new_manual_tx(user_id=user_id, nano_ton_amount=ton_amount * 1e9,
                                            token_id=token.token_id, price=token.price,
                                            tx_address=withdraw_address, utime=int(time.time()))

        if not await send_manual_tx_to_admin_chat(bot, user_id, username, ton_amount, new_tx.ManualTXs_id):
            return  # failed to send msg

        await db.update_user_balance(user_id, token.token_id, -ton_amount * token.price)


async def send_manual_tx_to_admin_chat(bot, user_id, username, ton_amount, id_new_tx):
    text, keyboard = withdraw_menu.admin_manual_tx(user_id, username, ton_amount, id_new_tx)
    try:
        await bot.send_message(chat_id=config.admin_chat_id, text=text, reply_markup=keyboard)
    except TelegramMigrateToChat as ex:
        logging.exception('User trying withdraw cash')
        return False
    return True


async def is_user_has_unresolved_tx(user_id):
    last_manual_tx = await db.get_last_manual_transaction(user_id, token_id=2)
    return last_manual_tx['withdraw_state'] is not None


async def how_much_can_withdraw_today(user_id, token_price):
    # how much user already withdraw today
    already_withdraw_today_nanoton = await db.get_user_daily_total_amount(user_id)
    already_withdraw_today_tokens = already_withdraw_today_nanoton / 1e9 * token_price

    allowable_amount = MAXIMUM_WITHDRAW_DAILY * token_price - already_withdraw_today_tokens
    return allowable_amount
