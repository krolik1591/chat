from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from bot.db import db
from bot.menus.main_menus.wheel_of_fortune_menus import wheel_of_fortune_doesnt_exist_menu, \
    wheel_of_fortune_menu

router = Router()


@router.callback_query(Text("wheel_of_fortune"))
async def wheel_of_fortune(call: types.CallbackQuery, state: FSMContext):
    wof_info = await db.get_wheel_info()
    user_wof_win = await db.get_user_wof_win(call.from_user.id)

    if not wof_info:
        text, keyboard = wheel_of_fortune_doesnt_exist_menu(user_wof_win)
        await call.message.edit_text(text, reply_markup=keyboard)
        return

    user_tickets = await db.get_count_user_tickets(call.from_user.id, 'all')

    text, keyboard = wheel_of_fortune_menu(wof_info.ticket_cost, wof_info.timestamp_end, user_tickets, user_wof_win)
    await call.message.edit_text(text, reply_markup=keyboard)
