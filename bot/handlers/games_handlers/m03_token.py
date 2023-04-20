import time

from aiogram import Router, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

import bot.db.methods as db
from bot.const import START_POINTS
from bot.db.methods import add_new_transaction, update_user_balance
from bot.handlers.context import Context
from bot.handlers.games_handlers.m04_game_settings import settings_menu
from bot.handlers.games_handlers.m05_bets import bet_menu
from bot.handlers.states import Menu, StateKeys
from bot.menus.game_menus.main_or_demo_balance_menu import main_or_demo_balance

router = Router()


async def tokens_menu(context: Context, msg_id=None):
    tokens = await db.get_tokens()
    balances = await db.get_user_balances(context.user_id)
    text, keyboard = main_or_demo_balance(tokens, balances)

    if msg_id is None:
        await context.fsm_context.bot.send_message(
            chat_id=context.user_id, text=text, reply_markup=keyboard)
    else:
        await context.fsm_context.bot.edit_message_text(
            chat_id=context.user_id, message_id=msg_id, text=text, reply_markup=keyboard)


@router.callback_query(text=["tokens"])
async def tokens_show(call: types.CallbackQuery, state: FSMContext):
    context = await Context.from_fsm_context(call.from_user.id, state)
    await tokens_menu(context, msg_id=call.message.message_id)
    await state.set_state(Menu.delete_message)


@router.callback_query(Text(text_startswith='set_token_'))
async def set_token(call: types.CallbackQuery, state: FSMContext):
    token_id = int(call.data.removeprefix('set_token_'))
    try:
        token = await db.get_token_by_id(token_id)
    except:
        # todo. integrity error; move user to start
        return

    await state.update_data(**{StateKeys.TOKEN_ID: token_id, StateKeys.TOKEN_ICON: token.icon})

    context = await Context.from_fsm_context(call.from_user.id, state)
    await settings_menu(context, msg_id=call.message.message_id)


# only for DEMO token
@router.callback_query(text=["end_money"])
async def replenish_demo_balance(call: types.CallbackQuery, state: FSMContext):
    context = await Context.from_fsm_context(call.from_user.id, state)

    DEMO_TOKEN = 1
    assert context.token.id == DEMO_TOKEN, "REPLENISH NOT A DEMO TOKEN"

    await update_user_balance(call.from_user.id, DEMO_TOKEN, START_POINTS)
    await add_new_transaction(call.from_user.id, DEMO_TOKEN, 500, int(time.time()), START_POINTS, 'demo_address',
                              'demo_hash', int(time.time()))

    # context with updated balance
    context = await Context.from_fsm_context(call.from_user.id, state)
    await bet_menu(context, msg_id=call.message.message_id)
