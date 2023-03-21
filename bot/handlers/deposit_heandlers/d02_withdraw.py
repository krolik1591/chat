from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from bot.class_for_state import Choosen_message
from bot.menus.deposit_menus.withdraw_menu1 import withdraw_menu

flags = {"throttling_key": "default"}
router = Router()


@router.callback_query(text=["withdraw"])
async def withdraw(call: types.CallbackQuery, state: FSMContext):

    text, keyboard = withdraw_menu()
    await call.message.edit_text(text, reply_markup=keyboard)

    await state.set_state(Choosen_message.choosing_withdraw_amount)

@router.message(state=Choosen_message.choosing_withdraw_amount)
async def withdraw_user_text(message: Message, state: FSMContext):
    await message.delete()
    try:
        user_withdraw = float(message.text)
    except ValueError:
        return
    round_user_withdraw = round(user_withdraw, 2)
    print(round_user_withdraw)