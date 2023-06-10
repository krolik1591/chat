import datetime

from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from babel.dates import format_datetime

from bot.db import db
from bot.menus.main_menus.wheel_of_fortune_menus import wheel_of_fortune_doesnt_exist_menu, \
    wheel_of_fortune_menu

router = Router()


@router.callback_query(Text("wheel_of_fortune"))
async def wheel_of_fortune(call: types.CallbackQuery, state: FSMContext):
    wof_info = await db.get_active_wheel_info()
    user_wof_win = await db.get_user_wof_win(call.from_user.id)

    if not wof_info:
        text, keyboard = wheel_of_fortune_doesnt_exist_menu(user_wof_win)
        await call.message.edit_text(text, reply_markup=keyboard)
        return

    user_tickets = await db.get_count_user_tickets(call.from_user.id, 'all')
    locale_datetime = await get_locale_datetime(state, wof_info.timestamp_end)

    text, keyboard = wheel_of_fortune_menu(wof_info.ticket_cost, locale_datetime, user_tickets, user_wof_win)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("check_status"))
async def check_status_menu(call: types.CallbackQuery, state: FSMContext):
    wof_info = await db.get_active_wheel_info()
    locale_datetime = await get_locale_datetime(state, wof_info.timestamp_end)
    await call.answer(_('WOF_CHECK_STATUS_ANSWER').format(date_end=locale_datetime), show_alert=True)


async def get_locale_datetime(state, date_end):
    locale = (await state.get_data()).get('locale')
    date_end = date_end
    if isinstance(date_end, int):
        timestamp = 1686411432000 / 1000  # Ділимо на 1000, оскільки ми працюємо з мілісекундами
        date_end = datetime.datetime.fromtimestamp(timestamp)
    return format_datetime(date_end, format='medium', locale=locale)
