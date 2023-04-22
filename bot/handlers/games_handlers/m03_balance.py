import time

from aiogram import Router, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

from bot.db import db
from bot.consts.const import START_POINTS
from bot.handlers.context import Context
from bot.handlers.games_handlers.m04_game_settings import settings_menu
from bot.handlers.games_handlers.m05_bets import bet_menu
from bot.handlers.states import Menu, StateKeys
from bot.menus.game_menus import select_balance_menu

router = Router()


async def balances_menu(context: Context, msg_id=None):
    balances = await db.get_user_balances(context.user_id)
    text, keyboard = select_balance_menu(balances)

    if msg_id is None:
        await context.fsm_context.bot.send_message(
            chat_id=context.user_id, text=text, reply_markup=keyboard)
    else:
        await context.fsm_context.bot.edit_message_text(
            chat_id=context.user_id, message_id=msg_id, text=text, reply_markup=keyboard)


@router.callback_query(text=["select_balance_type"])
async def balance_type_show(call: types.CallbackQuery, state: FSMContext):
    context = await Context.from_fsm_context(call.from_user.id, state)
    await balances_menu(context, msg_id=call.message.message_id)
    await state.set_state(Menu.delete_message)


@router.callback_query(Text(text_startswith='set_balance_type_'))
async def set_balance_type(call: types.CallbackQuery, state: FSMContext):
    balance_type = call.data.removeprefix('set_balance_type_')
    await state.update_data(**{StateKeys.BALANCE_TYPE: balance_type})

    context = await Context.from_fsm_context(call.from_user.id, state)
    await settings_menu(context, msg_id=call.message.message_id)


# only for DEMO balance_type
@router.callback_query(text=["end_money"])
async def replenish_demo_balance(call: types.CallbackQuery, state: FSMContext):
    context = await Context.from_fsm_context(call.from_user.id, state)
    DEMO_TYPE = 'demo'
    assert context.balance_type == DEMO_TYPE, "REPLENISH NOT A DEMO TOKEN"

    await db.update_user_balance(call.from_user.id, DEMO_TYPE, START_POINTS)
    await db.add_new_transaction(call.from_user.id, DEMO_TYPE, 500, int(time.time()), START_POINTS, 'demo_address',
                                 'demo_hash', int(time.time()))

    # context with updated balance
    context = await Context.from_fsm_context(call.from_user.id, state)
    await bet_menu(context, msg_id=call.message.message_id)
