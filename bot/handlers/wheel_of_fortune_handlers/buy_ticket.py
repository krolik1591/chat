from aiogram import Router, exceptions, types
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext

from bot.db import db
from bot.handlers.states import Menu, StateKeys
from bot.menus.main_menus.wheel_of_fortune_menus import buy_random_num_menu, buy_selected_num_menu, buy_ticket_menu
from bot.menus.utils import kb_del_msg

router = Router()


@router.callback_query(Text("buy_ticket"))
async def buy_ticket(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Menu.delete_message)

    text, keyboard = buy_ticket_menu()
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("buy_selected_num"))
async def buy_selected_ticket(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Menu.enter_ticket_num)

    text, keyboard = buy_selected_num_menu()
    await call.message.edit_text(text, reply_markup=keyboard)


@router.message(StateFilter(Menu.enter_ticket_num))
async def enter_ticket_num(message: types.Message, state: FSMContext):
    await message.delete()

    ticket_num = message.text
    last_msg_id = (await state.get_data()).get(StateKeys.LAST_MSG_ID)

    if not ticket_num.isnumeric():
        await message.answer('Вводити треба тільки числа!', reply_markup=kb_del_msg())
        return

    if len(ticket_num) != 7:
        await message.answer('Тільки семизначні числа!', reply_markup=kb_del_msg())
        return

    text, keyboard = buy_selected_num_menu(ticket_num)
    try:
        await state.bot.edit_message_text(text, message.from_user.id, last_msg_id, reply_markup=keyboard)
    except exceptions.TelegramBadRequest as e:
        print("User enter the same ticket num")


@router.callback_query(Text("buy_random_num"))
async def buy_selected_ticket(call: types.CallbackQuery, state: FSMContext):

    text, keyboard = buy_random_num_menu()
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("buy_this_ticket"))
async def buy_selected_ticket(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Menu.delete_message)

    user_balance = await db.get_user_balance(call.from_user.id, 'general')
