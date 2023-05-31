import logging

from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.i18n import gettext as _

from bot.consts.const import MIN_REF_WITHDRAW, USER_REF_LEVEL
from bot.db import db, manager
from bot.menus.account_menus.referrals_menu import referrals_menu
from bot.utils.rounding import round_down

router = Router()
flags = {"throttling_key": "default"}


@router.callback_query(Text("referrals_menu"))
async def referrals(call: types.CallbackQuery, state: FSMContext):
    invite_link, referrals_count, total_ref_withdraw, referrals_bets, money_to_withdraw = await referral_info(call,
                                                                                                              state)

    text, keyboard = referrals_menu(invite_link, referrals_count, total_ref_withdraw, referrals_bets, money_to_withdraw)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("promo_to_general"), flags=flags)
async def referrals(call: types.CallbackQuery, state: FSMContext):
    total_bonus = await how_many_cash_referrer_can_withdraw(call.from_user.id)
    if total_bonus < MIN_REF_WITHDRAW:
        await call.answer(_('REFERRALS_PROMO_TO_GENERAL_NO_MORE_MONEY').format(min_ref_withdraw=MIN_REF_WITHDRAW), True)
        return

    with manager.pw_database.atomic():
        await db.update_datetime_and_amount_ref_withdraw(call.from_user.id, total_bonus)
        await db.update_user_balance(call.from_user.id, 'general', total_bonus)

    await call.answer(_('REFERRALS_PROMO_TO_GENERAL_SUCCESS'))

    invite_link, referrals_count, total_ref_withdraw, referrals_bets, money_to_withdraw = await referral_info(call,
                                                                                                              state)

    text, keyboard = referrals_menu(invite_link, referrals_count, total_ref_withdraw, referrals_bets, money_to_withdraw)
    await call.message.edit_text(text, reply_markup=keyboard)


async def referral_info(call, state):
    invite_link = await create_start_link(state.bot, str(call.from_user.id))
    referrals_count = await db.get_count_all_user_referrals(call.from_user.id)
    total_ref_withdraw = await db.get_total_ref_withdraw(call.from_user.id)
    money_to_withdraw = await how_many_cash_referrer_can_withdraw(call.from_user.id)
    referrals_bets = await db.get_all_referrals_bets(call.from_user.id)

    return invite_link, referrals_count, total_ref_withdraw, referrals_bets, money_to_withdraw


@router.inline_query()
async def inline_send_invite(query: types.InlineQuery, state):
    await query.answer([types.InlineQueryResultArticle(
        title=_('REFERRALS_SEND_INVITATION_TITLE_TEXT'), description=_('REFERRALS_SEND_INVITATION_DESC_TEXT'),
        id=query.id, input_message_content=types.InputTextMessageContent(
            message_text=_('REFERRALS_SEND_INVITATION_TEXT')),
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[
            types.InlineKeyboardButton(text=_('REFERRALS_SEND_INVITATION_BTN_TEXT'),
                                       url=await create_start_link(state.bot, str(query.from_user.id)))
        ]]))
    ], cache_time=0, is_personal=True)


async def how_many_cash_referrer_can_withdraw(user_id):
    current_ref_value = await db.get_total_ref_withdraw(user_id)
    addition_ref_value = await db.get_referrals_bets_from_last_withdraw(user_id)

    total_bonus = calc_bonus(addition_ref_value, current_ref_value)

    new_ref_value = current_ref_value + addition_ref_value
    _, new_ref_name = find_ref_lvl(new_ref_value)

    return total_bonus


def calc_bonus(addition_ref_value, current_ref_value):
    total_ref_value = addition_ref_value + current_ref_value

    current_ref_id, _ = find_ref_lvl(current_ref_value)

    total_bonus = 0
    for lvl_ends, percent in list(USER_REF_LEVEL.values())[current_ref_id:]:
        lvl_ends = min(lvl_ends, total_ref_value)
        this_lvl_bonus = (lvl_ends - current_ref_value)
        if this_lvl_bonus <= 0:
            break

        total_bonus += this_lvl_bonus * percent / 100
        current_ref_value = lvl_ends

    return round_down(total_bonus, 2)


def find_ref_lvl(value):
    for i, (lvl_name, (lvl_ends, _)) in enumerate(USER_REF_LEVEL.items()):
        if value < lvl_ends:
            return i, lvl_name


if __name__ == "__main__":
    import asyncio

    asyncio.run(how_many_cash_referrer_can_withdraw(357108179))
