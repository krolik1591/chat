from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from bot.menus.main_menus.wheel_of_fortune_menus import buy_random_num_menu, buy_selected_num_menu, buy_ticket_menu, \
    wheel_of_fortune_menu

router = Router()


@router.callback_query(Text("wheel_of_fortune"))
async def wheel_of_fortune(call: types.CallbackQuery, state: FSMContext):

    text, keyboard = wheel_of_fortune_menu()
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("buy_ticket"))
async def buy_ticket(call: types.CallbackQuery, state: FSMContext):

    text, keyboard = buy_ticket_menu()
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("buy_selected_num"))
async def buy_selected_ticket(call: types.CallbackQuery, state: FSMContext):

    text, keyboard = buy_selected_num_menu()
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("buy_random_num"))
async def buy_selected_ticket(call: types.CallbackQuery, state: FSMContext):

    text, keyboard = buy_random_num_menu()
    await call.message.edit_text(text, reply_markup=keyboard)
