import datetime
import json

import aiogram.exceptions
import humanize
from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import I18n, gettext as _

from bot.consts.balance import PROMO_FUNDS_ICON, TON_FUNDS_ICON
from bot.db import db, manager
from bot.handlers.states import StateKeys
from bot.menus.main_menus.wheel_of_fortune_menus import what_balance_withdraw_menu, wheel_of_fortune_doesnt_exist_menu, \
    wheel_of_fortune_menu

router = Router()


@router.callback_query(Text("wheel_of_fortune"))
async def wheel_of_fortune(call: types.CallbackQuery, state: FSMContext, i18n: I18n):
    wof_info = await db.get_active_wheel_info()
    wof_reward_json = await db.get_user_wof_win(call.from_user.id)
    wof_reward = json.loads(wof_reward_json)
    if not wof_info:
        text, keyboard = wheel_of_fortune_doesnt_exist_menu(wof_reward)
        await call.message.edit_text(text, reply_markup=keyboard)
        return True

    active_codes = await db.get_all_active_user_promo_codes(call.from_user.id)
    if active_codes:
        for code in active_codes:
            if code.promocode.type == 'ticket':
                await state.update_data({StateKeys.ACTIVE_PROMO_NAME: code.promo_name_id})
            else:
                await state.update_data({StateKeys.ACTIVE_PROMO_NAME: None})
    else:
        await state.update_data({StateKeys.ACTIVE_PROMO_NAME: None})

    general_user_tickets = await db.get_count_user_tickets(call.from_user.id, 'all')
    time_end_text = await get_time_to_spin_text(wof_info.timestamp_end, i18n.current_locale)

    text, keyboard = wheel_of_fortune_menu(wof_info.ticket_cost, time_end_text, general_user_tickets, wof_reward)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("check_status"))
async def check_status_menu(call: types.CallbackQuery, i18n: I18n):
    wof_info = await db.get_active_wheel_info()

    try:
        await wheel_of_fortune(call, i18n)
    except aiogram.exceptions.TelegramBadRequest as e:
        print('Try send the same msg: ', e)

    if not wof_info:
        await call.answer(_('WOF_CHECK_STATUS_ANSWER'), show_alert=True)
        return

    time_end_text = await get_time_to_spin_text(wof_info.timestamp_end, i18n.current_locale)
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
        f'{place} - {str(winner[0]).zfill(7)}'
        for place, winner in enumerate(winners, start=1)
    ])

    time_end_text = await get_time_to_spin_text(last_wof_info.timestamp_end, i18n.current_locale)
    await call.answer(_('WOF_SPIN_RESULT_ANSWER').format(date_end=time_end_text, text=text), show_alert=True)


@router.callback_query(Text("claim_wof_reward"))
async def claim_reward(call: types.CallbackQuery, i18n: I18n):
    wof_rewards_json = await db.get_user_wof_win(call.from_user.id)
    wof_rewards = json.loads(wof_rewards_json)
    if not wof_rewards['general'] and not wof_rewards['promo']:
        await call.answer(_('WOF_CLAIM_REWARD_ANSWER_ERROR'), show_alert=True)
        return

    if not wof_rewards['promo']:
        await process_update_balance(call, wof_rewards, 'general', TON_FUNDS_ICON)
        await wheel_of_fortune(call, i18n)

    elif not wof_rewards['general']:
        promo_code = await db.get_all_info_user_promo_code(call.from_user.id, 'ticket')
        await db.update_wagers_and_bonus(call.from_user.id, wof_rewards['promo'], promo_code)
        await process_update_balance(call, wof_rewards, 'promo', PROMO_FUNDS_ICON)
        await wheel_of_fortune(call, i18n)

    else:
        text, kb = what_balance_withdraw_menu(wof_rewards)
        await call.message.edit_text(text, reply_markup=kb)


@router.callback_query(Text(startswith="claim_wof_balance_"))
async def wof_balance_withdraw(call: types.CallbackQuery, i18n: I18n):
    balance_type = call.data.removeprefix('claim_wof_balance_')
    wof_rewards_json = await db.get_user_wof_win(call.from_user.id)
    wof_rewards = json.loads(wof_rewards_json)

    if balance_type == 'general':
        await process_update_balance(call, wof_rewards, balance_type, TON_FUNDS_ICON)
    if balance_type == 'promo':
        await process_update_balance(call, wof_rewards, balance_type, PROMO_FUNDS_ICON)

    await wheel_of_fortune(call, i18n)


async def process_update_balance(call, wof_rewards, balance_type, emoji):
    await call.answer(_('WOF_CLAIM_REWARD_ANSWER').format(wof_reward=str(wof_rewards[balance_type]) + emoji), show_alert=True)

    with manager.pw_database.atomic():
        await db.update_user_balance(call.from_user.id, balance_type, wof_rewards[balance_type])
        wof_rewards[balance_type] = 0
        await db.update_user_wof_win(call.from_user.id, json.dumps(wof_rewards))


async def get_time_to_spin_text(timestamp, locale):
    if not timestamp:
        return _('WOF_NO_DATE_END')

    if isinstance(timestamp, int):
        timestamp = datetime.datetime.fromtimestamp(timestamp)

    humanize.i18n.activate(locale)
    return humanize.naturaltime(timestamp)
