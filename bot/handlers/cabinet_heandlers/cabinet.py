from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import create_start_link

from bot.consts import const
from bot.db import db
from bot.menus.cabinet_menus.cabinet_menu import cabinet_menu
from bot.menus.cabinet_menus.referrals_menu import referrals_menu

router = Router()


@router.callback_query(Text("cabinet_menu"))
async def cabinet(call: types.CallbackQuery, state: FSMContext):

    text, keyboard = cabinet_menu()
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text("referrals_menu"))
async def referrals(call: types.CallbackQuery, state: FSMContext):
    invite_link = await create_start_link(state.bot, str(call.from_user.id))
    referrals_count = await db.get_count_all_user_referrals(call.from_user.id)
    total_ref_withdraw = await db.get_total_ref_withdraw(call.from_user.id)
    referrals_bets = await db.get_referrals_bets(call.from_user.id)
    all_profit = referrals_bets + total_ref_withdraw

    text, keyboard = referrals_menu(invite_link, referrals_count, total_ref_withdraw, referrals_bets, all_profit)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.inline_query()
async def inline_send_invite(query: types.InlineQuery, state):
    await query.answer([types.InlineQueryResultArticle(
        title='Send invitation', description='huihuihuihjughrtyjgrgri',
        id='wqweqweqwe', input_message_content=types.InputTextMessageContent(message_text='hi noggers'),
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[
            types.InlineKeyboardButton(text='pohui', url=await create_start_link(state.bot, str(query.from_user.id)))
        ]]))
    ])
