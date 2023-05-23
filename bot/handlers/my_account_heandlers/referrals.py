from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.i18n import gettext as _

from bot.consts.const import USER_REF_LEVEL
from bot.db import db
from bot.menus.account_menus.referrals_menu import referrals_menu

router = Router()


@router.callback_query(Text("referrals_menu"))
async def referrals(call: types.CallbackQuery, state: FSMContext):
    invite_link = await create_start_link(state.bot, str(call.from_user.id))
    referrals_count = await db.get_count_all_user_referrals(call.from_user.id)
    total_ref_withdraw = await db.get_total_ref_withdraw(call.from_user.id)
    referrals_bets = await db.get_referrals_bets(call.from_user.id)
    all_profit = referrals_bets + total_ref_withdraw

    text, keyboard = referrals_menu(invite_link, referrals_count, total_ref_withdraw, referrals_bets, all_profit)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("promo_to_general"))
async def referrals(call: types.CallbackQuery, state: FSMContext):
    total_bonus = await how_many_cash_referrer_can_withdraw(call.from_user.id)




@router.inline_query()
async def inline_send_invite(query: types.InlineQuery, state):
    await query.answer([types.InlineQueryResultArticle(
        title=_('REFERRALS_SEND_INVITATION_TITLE_TEXT'), description=_('REFERRALS_SEND_INVITATION_DESC_TEXT'),
        id='skrrrr', input_message_content=types.InputTextMessageContent(
            message_text=_('REFERRALS_SEND_INVITATION_TEXT')),
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[
            types.InlineKeyboardButton(text=_('REFERRALS_SEND_INVITATION_BTN_TEXT'),
                                       url=await create_start_link(state.bot, str(query.from_user.id)))
        ]]))
    ])


async def how_many_cash_referrer_can_withdraw(user_id):
    referrals_bets = await db.get_referrals_bets(user_id)
    total_ref_withdraw = await db.get_total_ref_withdraw(user_id)
    all_bets = referrals_bets + total_ref_withdraw

    total_bonus = 0
    name_range_bonus = []
    index_range_bonus = []
    bonuses_lvl_reverse = reversed(list(USER_REF_LEVEL.items()))
    bonuses_lvl = list(USER_REF_LEVEL.items())

    for name, (profit, percent) in bonuses_lvl_reverse:
        if len(name_range_bonus) == 0:
            if all_bets >= profit:
                name_range_bonus.append(name)

        if total_ref_withdraw >= profit:
            name_range_bonus.append(name)
            name_range_bonus = list(reversed(name_range_bonus))
            break

    for i in range(len(bonuses_lvl)):
        if bonuses_lvl[i][0] == name_range_bonus[0]:
            index_range_bonus.append(i)
        if bonuses_lvl[i][0] == name_range_bonus[1]:
            index_range_bonus.append(i)

    if index_range_bonus[0] != index_range_bonus[1]:
        for i in range(len(bonuses_lvl)):
            if bonuses_lvl[i][0] == name_range_bonus[0]:
                next_interval = bonuses_lvl[index_range_bonus[0] + 1][1][0]
                percent = bonuses_lvl[i][1][1]
                total_bonus += (next_interval - total_ref_withdraw) * percent / 100
                continue

            if i == 4:
                percent = bonuses_lvl[i][1][1]
                total_bonus += (all_bets - bonuses_lvl[i][1][0]) * percent / 100
                break

            if index_range_bonus[0] < i <= index_range_bonus[1]:
                if all_bets >= bonuses_lvl[i + 1][1][0]:
                    percent = bonuses_lvl[i][1][1]
                    next_interval = bonuses_lvl[i + 1][1][0]
                    pre_interval = bonuses_lvl[i][1][0]
                    total_bonus += (next_interval - pre_interval) * percent / 100
                else:
                    percent = bonuses_lvl[i][1][1]
                    total_bonus += (all_bets - bonuses_lvl[i][1][0]) * percent / 100
                    break
    else:
        percent = bonuses_lvl[index_range_bonus[0]][1][1]
        total_bonus += (all_bets - total_ref_withdraw) * percent / 100

    print(all_bets, total_ref_withdraw)
    print(total_bonus)
    return total_bonus