import datetime
import json

import humanize
from aiogram import Router, types
from aiogram.filters import Text
from aiogram.utils.i18n import I18n, gettext as _

from bot.db import db, manager
from bot.menus.main_menus.wheel_of_fortune_menus import wheel_of_fortune_doesnt_exist_menu, \
    wheel_of_fortune_menu

router = Router()


@router.callback_query(Text("wheel_of_fortune"))
async def wheel_of_fortune(call: types.CallbackQuery, i18n: I18n):
    wof_info = await db.get_active_wheel_info()
    wof_reward = await db.get_user_wof_win(call.from_user.id)
    if not wof_info:
        text, keyboard = wheel_of_fortune_doesnt_exist_menu(wof_reward)
        await call.message.edit_text(text, reply_markup=keyboard)
        return True

    user_tickets = await db.get_count_user_tickets(call.from_user.id, 'all')
    time_end_text = await get_time_to_spin_text(wof_info.timestamp_end, i18n.current_locale)

    text, keyboard = wheel_of_fortune_menu(wof_info.ticket_cost, time_end_text, user_tickets, wof_reward)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("check_status"))
async def check_status_menu(call: types.CallbackQuery, i18n: I18n):
    wof_info = await db.get_active_wheel_info()
    time_end_text = await get_time_to_spin_text(wof_info.timestamp_end, i18n.current_locale)

    if not wof_info:
        await call.answer(_('WOF_CHECK_STATUS_ANSWER'), show_alert=True)
        return

    user_tickets = await db.get_count_user_tickets(call.from_user.id, 'all')
    if user_tickets == 0:
        await call.answer(_('WOF_CHECK_STATUS_NO_TICKETS').format(date_end=time_end_text), show_alert=True)
    else:
        await call.answer(_('WOF_CHECK_STATUS_TICKETS').format(date_end=time_end_text, user_tickets=user_tickets),
                          show_alert=True)


@router.callback_query(Text("spin_result"))
async def spin_result_answer(call: types.CallbackQuery, i18n: I18n):
    last_wof_info = await db.get_last_deactivate_wheel_info()
    if not last_wof_info:
        await call.answer(_('WOF_SPIN_RESULT_ANSWER_ERROR'), show_alert=True)
        return

    winners = json.loads(last_wof_info.winners)
    text = '\n'.join([
        f'{place} - {winner[0]}'
        for place, winner in enumerate(winners, start=1)
    ])

    time_end_text = await get_time_to_spin_text(last_wof_info.timestamp_end, i18n.current_locale)
    await call.answer(_('WOF_SPIN_RESULT_ANSWER').format(date_end=time_end_text, text=text), show_alert=True)


@router.callback_query(Text("claim_reward"))
async def claim_reward(call: types.CallbackQuery, i18n: I18n):
    wof_reward = await db.get_user_wof_win(call.from_user.id)
    if not wof_reward:
        await call.answer(_('WOF_CLAIM_REWARD_ANSWER_ERROR'), show_alert=True)
        return

    await call.answer(_('WOF_CLAIM_REWARD_ANSWER').format(wof_reward=wof_reward), show_alert=True)

    with manager.pw_database.atomic():
        await db.update_user_balance(call.from_user.id, 'general', wof_reward)
        await db.update_user_wof_win(call.from_user.id, 0)

    await wheel_of_fortune(call, i18n)


async def get_time_to_spin_text(timestamp, locale):
    if not timestamp:
        return _('WOF_NO_DATE_END')

    if isinstance(timestamp, int):
        timestamp = datetime.datetime.fromtimestamp(timestamp)

    humanize.i18n.activate(locale)
    return humanize.naturaltime(timestamp)
