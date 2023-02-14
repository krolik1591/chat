from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from bot.const import START_POINTS
from bot.menus.main_menu import main_menu

flags = {"throttling_key": "default"}
router = Router()


@router.message(commands="start", flags=flags)
async def cmd_start(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_balance = user_data.get("balance", START_POINTS)

    text, keyboard = main_menu(user_balance, user_balance)
    msg = await message.answer(text, reply_markup=keyboard)
    await state.update_data(last_msg_id=msg.message_id)


@router.callback_query(text=["main_menu"])
async def back_to_main(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_balance = user_data.get('balance', START_POINTS)

    text, keyboard = main_menu(user_balance, user_balance)
    await call.message.edit_text(text, reply_markup=keyboard)

