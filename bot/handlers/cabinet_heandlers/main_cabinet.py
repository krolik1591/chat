from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext

from bot.db import db
from bot.menus.cabinet_menus.cabinet_menu import cabinet_menu

router = Router()


@router.callback_query(text=["cabinet_menu"])
async def main_cabinet(call: types.CallbackQuery, state: FSMContext):

    text, keyboard = cabinet_menu()
    await call.message.edit_text(text, reply_markup=keyboard)
