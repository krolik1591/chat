from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from bot.menus.main_menus.wheel_of_fortune_menus import wheel_of_fortune_menu

router = Router()


@router.callback_query(Text("wheel_of_fortune"))
async def wheel_of_fortune(call: types.CallbackQuery, state: FSMContext):

    text, keyboard = wheel_of_fortune_menu()
    await call.message.edit_text(text, reply_markup=keyboard)
