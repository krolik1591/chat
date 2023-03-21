from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from bot.class_for_state import Choosen_message
from bot.const import MIN_WITHDRAW
from bot.db.methods import get_user_balance
from bot.menus.deposit_menus.withdraw_menu1 import withdraw_menu_amount
from bot.menus.deposit_menus.withdraw_menu2 import withdraw_menu_address
from bot.menus.deposit_menus.withdraw_menu3 import withdraw_menu_check
from bot.menus.deposit_menus.withdraw_menu_err import withdraw_menu_err
from bot.texts import WITHDRAW_MENU_TEXT1_1, WITHDRAW_MENU_TEXT1_2
from TonTools import Address
import tonsdk.utils

flags = {"throttling_key": "default"}
router = Router()


@router.callback_query(text=["withdraw"])
async def withdraw(call: types.CallbackQuery, state: FSMContext):
    text, keyboard = withdraw_menu_amount()  # enter amount
    await call.message.edit_text(text, reply_markup=keyboard)

    await state.update_data(last_msg_id=call.message.message_id)

    await state.set_state(Choosen_message.choosing_withdraw_amount)


@router.message(state=Choosen_message.choosing_withdraw_amount)
async def withdraw_user_text(message: Message, state: FSMContext):
    await message.delete()
    try:
        user_withdraw = float(message.text)
    except ValueError:
        return
    round_user_withdraw = round(user_withdraw, 2)

    TOKEN_ID = 2
    user_balance = await get_user_balance(message.from_user.id, TOKEN_ID)

    if user_balance < MIN_WITHDRAW or round_user_withdraw < MIN_WITHDRAW:
        err = 2  # user balance < MIN_WITHDRAW
        if round_user_withdraw < MIN_WITHDRAW:
            err = 1  # round_user_withdraw < MIN_WITHDRAW
        text, keyboard = withdraw_menu_err(err)
        await message.answer(text, reply_markup=keyboard)
        return

    user_data = await state.get_data()
    last_msg = user_data.get('last_msg_id')

    await state.update_data(user_withdraw_amount=round_user_withdraw)

    text, keyboard = withdraw_menu_address()  # enter address
    await state.bot.edit_message_text(text, reply_markup=keyboard, chat_id=message.chat.id, message_id=last_msg)
    await state.set_state(Choosen_message.choosing_withdraw_address)


@router.message(state=Choosen_message.choosing_withdraw_address)
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

    user_data = await state.get_data()
    user_withdraw_amount = user_data.get('user_withdraw_amount')
    last_msg = user_data.get('last_msg_id')
    await state.update_data(user_withdraw_address=user_withdraw_address.to_string())

    text, keyboard = withdraw_menu_check(user_withdraw_amount, user_withdraw_address.to_string())
    await state.bot.edit_message_text(text, reply_markup=keyboard, chat_id=message.chat.id, message_id=last_msg)


@router.callback_query(text=["approve"])
async def replenish_to_user(call: types.CallbackQuery, state: FSMContext):
    text, keyboard = withdraw_menu_amount()
    await call.message.edit_text(text, reply_markup=keyboard)

    await state.update_data(last_msg_id=call.message.message_id)

    await state.set_state(Choosen_message.choosing_withdraw_amount)