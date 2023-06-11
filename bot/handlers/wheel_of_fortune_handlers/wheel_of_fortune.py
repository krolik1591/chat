import datetime
import json

import humanize
from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

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
    time_diff_text = await get_time_diff_text(state, wof_info.timestamp_end)

    text, keyboard = wheel_of_fortune_menu(wof_info.ticket_cost, time_diff_text, user_tickets, user_wof_win)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("check_status"))
async def check_status_menu(call: types.CallbackQuery, state: FSMContext):
    wof_info = await db.get_active_wheel_info()
    time_diff_text = await get_time_diff_text(state, wof_info.timestamp_end)
    await call.answer(_('WOF_CHECK_STATUS_ANSWER').format(date_end=time_diff_text), show_alert=True)


@router.callback_query(Text("spin_result"))
async def spin_result_answer(call: types.CallbackQuery, state: FSMContext):
    last_wof_info = await db.get_last_deactivate_wheel_info()
    if not last_wof_info:
        await call.answer(_('WOF_SPIN_RESULT_ANSWER_ERROR'), show_alert=True)
        return

    winners = json.loads(last_wof_info.winners)
    text = ''
    for place, winner in enumerate(winners, start=1):
        text += f'{place} - {winner}\n'

    time_diff = await get_time_difference_to_spin(state, last_wof_info.timestamp_end)
    await call.answer(_('WOF_SPIN_RESULT_ANSWER').format(date_end=time_diff, text=text), show_alert=True)


async def get_time_diff_text(state, date):
    if date:
        time_diff = await get_time_difference_to_spin(state, date)
    else:
        time_diff = _('WOF_NO_DATE_END')
    return time_diff


async def get_time_difference_to_spin(state, date_end):
    if isinstance(date_end, int):
        timestamp = date_end / 1000  # Ділимо на 1000, оскільки ми працюємо з мілісекундами
        date_end = datetime.datetime.fromtimestamp(timestamp)

    locale = (await state.get_data()).get('locale')

    humanize.i18n.activate(locale)
    return humanize.naturaltime(date_end)
