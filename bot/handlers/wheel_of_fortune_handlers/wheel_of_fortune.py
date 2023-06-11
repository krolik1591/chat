import datetime
import json

import humanize
from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.db import db, manager
from bot.menus.main_menus.wheel_of_fortune_menus import wheel_of_fortune_doesnt_exist_menu, \
    wheel_of_fortune_menu

router = Router()


@router.callback_query(Text("wheel_of_fortune"))
async def wheel_of_fortune(call: types.CallbackQuery, state: FSMContext):
    if not await get_correct_wof_menu(call, state):
        return


async def get_correct_wof_menu(call, state):
    wof_info = await db.get_active_wheel_info()
    wof_reward = await db.get_user_wof_win(call.from_user.id)
    if not wof_info:
        text, keyboard = wheel_of_fortune_doesnt_exist_menu(wof_reward)
        await call.message.edit_text(text, reply_markup=keyboard)
        return True

    user_tickets = await db.get_count_user_tickets(call.from_user.id, 'all')
    time_diff_text = await get_time_diff_text_to_spin(state, wof_info.timestamp_end)

    text, keyboard = wheel_of_fortune_menu(wof_info.ticket_cost, time_diff_text, user_tickets, wof_reward)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("check_status"))
async def check_status_menu(call: types.CallbackQuery, state: FSMContext):
    wof_info = await db.get_active_wheel_info()
    time_diff_text = await get_time_diff_text_to_spin(state, wof_info.timestamp_end)

    if not wof_info:
        await call.answer(_('WOF_CHECK_STATUS_ANSWER'), show_alert=True)
        return

    user_tickets = await db.get_count_user_tickets(call.from_user.id, 'all')
    if user_tickets == 0:
        await call.answer(_('WOF_CHECK_STATUS_NO_TICKETS').format(date_end=time_diff_text), show_alert=True)
    else:
        await call.answer(_('WOF_CHECK_STATUS_TICKETS').format(date_end=time_diff_text, user_tickets=user_tickets),
                          show_alert=True)


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


@router.callback_query(Text("claim_reward"))
async def claim_reward(call: types.CallbackQuery, state: FSMContext):
    wof_reward = await db.get_user_wof_win(call.from_user.id)
    if not wof_reward:
        await call.answer(_('WOF_CLAIM_REWARD_ANSWER_ERROR'), show_alert=True)
        return

    await call.answer(_('WOF_CLAIM_REWARD_ANSWER').format(wof_reward=wof_reward), show_alert=True)

    with manager.pw_database.atomic():
        await db.update_user_balance(call.from_user.id, 'general', wof_reward)
        await db.update_user_wof_win(call.from_user.id, 0)

    await get_correct_wof_menu(call, state)


async def get_time_diff_text_to_spin(state, date):
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
