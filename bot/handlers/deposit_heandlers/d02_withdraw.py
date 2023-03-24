import tonsdk.utils
from TonTools import Address
from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from bot.const import MIN_WITHDRAW
from bot.db.methods import get_token_by_id, get_user_balance
from bot.handlers.states import Choosen_message
from bot.menus.deposit_menus.withdraw_approve_menu import withdraw_approve_menu
from bot.menus.deposit_menus.withdraw_menu1 import withdraw_menu_amount
from bot.menus.deposit_menus.withdraw_menu2 import withdraw_menu_address
from bot.menus.deposit_menus.withdraw_menu3 import withdraw_menu_check
from bot.menus.deposit_menus.withdraw_menu_err import withdraw_menu_err
from bot.ton.withdraw_cash import withdraw_cash_to_user

flags = {"throttling_key": "default"}
router = Router()


@router.callback_query(text=["withdraw"])
async def withdraw(call: types.CallbackQuery, state: FSMContext):
    text, keyboard = withdraw_menu_amount()  # enter amount
    await call.message.edit_text(text, reply_markup=keyboard)

    await state.update_data(last_msg_id=call.message.message_id)

    await state.set_state(Choosen_message.withdraw_amount)


@router.message(state=Choosen_message.withdraw_amount)
async def withdraw_user_text(message: Message, state: FSMContext):
    await message.delete()
    try:
        user_withdraw = float(message.text)
    except ValueError:
        return
    round_user_withdraw = round(user_withdraw, 2)

    TOKEN_ID = 2
    user_balance = await get_user_balance(message.from_user.id, TOKEN_ID)

    if user_balance < MIN_WITHDRAW or round_user_withdraw < MIN_WITHDRAW or round_user_withdraw > user_balance:
        err = await check_user_withdraw_amount_err(user_balance, round_user_withdraw)
        text, keyboard = withdraw_menu_err(err)
        await message.answer(text, reply_markup=keyboard)
        return

    user_data = await state.get_data()
    last_msg = user_data.get('last_msg_id')

    await state.update_data(user_withdraw_amount=round_user_withdraw)

    text, keyboard = withdraw_menu_address()  # enter address
    await state.bot.edit_message_text(text, reply_markup=keyboard, chat_id=message.chat.id, message_id=last_msg)
    await state.set_state(Choosen_message.withdraw_address)


@router.message(state=Choosen_message.withdraw_address)
async def withdraw_user_address(message: Message, state: FSMContext):
    await message.delete()
    try:
        user_withdraw_address = Address(message.text)
    except tonsdk.utils.InvalidAddressError:
        err = 4  # incorrect address
        text, keyboard = withdraw_menu_err(err)
        await message.answer(text, reply_markup=keyboard)
        return

    if user_withdraw_address.is_test_only:
        err = 3  # test.net address
        text, keyboard = withdraw_menu_err(err)
        await message.answer(text, reply_markup=keyboard)
        return

    TOKEN_ID = 2
    token = await get_token_by_id(TOKEN_ID)

    user_withdraw_amount = (await state.get_data()).get('user_withdraw_amount')
    last_msg = (await state.get_data()).get('last_msg_id')
    await state.update_data(user_withdraw_address=user_withdraw_address.to_string())

    text, keyboard = withdraw_menu_check(user_withdraw_amount, user_withdraw_address.to_string(), token.price)
    await state.bot.edit_message_text(text, reply_markup=keyboard, chat_id=message.chat.id, message_id=last_msg)
    await state.set_state(Choosen_message.withdraw_amount_approve)


@router.message(state=Choosen_message.withdraw_amount_approve)
async def withdraw_user_amount_approve(message: Message, state: FSMContext):
    await message.delete()
    try:
        user_withdraw = float(message.text)
    except ValueError:
        return
    round_user_withdraw = round(user_withdraw, 2)

    TOKEN_ID = 2
    token = await get_token_by_id(TOKEN_ID)
    user_balance = await get_user_balance(message.from_user.id, TOKEN_ID)

    if user_balance < MIN_WITHDRAW or round_user_withdraw < MIN_WITHDRAW or round_user_withdraw > user_balance:
        err = await check_user_withdraw_amount_err(user_balance, round_user_withdraw)
        text, keyboard = withdraw_menu_err(err)
        await message.answer(text, reply_markup=keyboard)
        return

    await state.update_data(user_withdraw_amount=round_user_withdraw)
    last_msg = (await state.get_data()).get('last_msg_id')
    user_withdraw_address = (await state.get_data()).get('user_withdraw_address')

    text, keyboard = withdraw_menu_check(round_user_withdraw, user_withdraw_address, token.price)
    await state.bot.edit_message_text(text, reply_markup=keyboard, chat_id=message.chat.id, message_id=last_msg)


@router.callback_query(text=["approve"])
async def replenish_to_user(call: types.CallbackQuery, state: FSMContext):
    user_withdraw_amount = (await state.get_data()).get('user_withdraw_amount')
    user_withdraw_address = (await state.get_data()).get('user_withdraw_address')

    TOKEN_ID = 2
    token = await get_token_by_id(TOKEN_ID)
    ton_amount = user_withdraw_amount / token.price

    master_wallet = state.bot.ton_client.master_wallet

    text, keyboard = withdraw_approve_menu(user_withdraw_amount)
    await call.message.edit_text(text, reply_markup=keyboard)

    await withdraw_cash_to_user(master_wallet, user_withdraw_address, ton_amount, call.from_user.id, token, state)


async def check_user_withdraw_amount_err(user_balance, round_user_withdraw):
    err = 0
    if user_balance < MIN_WITHDRAW:
        err = 2
    if round_user_withdraw < MIN_WITHDRAW:
        err = 1
    if round_user_withdraw > user_balance:
        err = 5
    return err