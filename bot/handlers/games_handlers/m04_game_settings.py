import json

from aiogram import Router, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

from bot.const import MIN_BET
from bot.db.methods import get_user_balance
from bot.handlers.context import Context
from bot.handlers.games_handlers.m05_bets import bet_change_state, bet_menu, normalize_bet
from bot.handlers.states import Games, Menu, StateKeys
from bot.menus.game_menus.cube_settings import cube_settings
from bot.menus.game_menus.game_menu_err import game_menu_err

router = Router()


async def settings_menu(context: Context, msg_id=None, general_bet=0):
    if context.game == Games.CUBE:
        await context.fsm_context.set_state(Menu.settings)

        text, keyboard = cube_settings(context.game_settings or [], context.balance, context.bet, context.token.icon,
                                       general_bet)

        if msg_id is None:
            settings_msg = await context.fsm_context.bot.send_message(
                chat_id=context.user_id, text=text, reply_markup=keyboard)
            await context.fsm_context.update_data(**{StateKeys.LAST_MSG_ID: settings_msg.message_id})
        else:
            await context.fsm_context.bot.edit_message_text(
                chat_id=context.user_id, message_id=msg_id, text=text, reply_markup=keyboard)

    else:
        return await bet_menu(context, msg_id=msg_id)


@router.callback_query(Text(text_startswith='game_settings'))
async def show_settings(call: types.CallbackQuery, state: FSMContext):
    context = await Context.from_fsm_context(call.from_user.id, state)
    await settings_menu(context, msg_id=call.message.message_id)


@router.callback_query(Text(text_startswith='cube_game_settings_'))
async def set_settings(call: types.CallbackQuery, state: FSMContext):
    new_settings = call.data.removeprefix('cube_game_settings_')
    context = await Context.from_fsm_context(call.from_user.id, state)
    old_game_settings: [str] = context.game_settings or []

    if new_settings in old_game_settings:
        old_game_settings.remove(new_settings)
    else:
        old_game_settings.append(new_settings)

    await state.update_data(**{StateKeys.GAME_SETTINGS: json.dumps(old_game_settings)})

    context = await Context.from_fsm_context(call.from_user.id, state)
    user_bet = MIN_BET
    state_bet = (await state.get_data()).get(StateKeys.BET)

    if state_bet is not None:
        user_bet = state_bet

    general_bet = user_bet * len(context.game_settings)

    token_id = (await state.get_data()).get(StateKeys.TOKEN_ID)
    user_balance = await get_user_balance(call.from_user.id, token_id)
    if general_bet > user_balance:
        text, kb = game_menu_err('low_balance_big_wish')
        await call.message.answer(text, reply_markup=kb)
        old_game_settings = []
        general_bet = 0
        await state.update_data(**{StateKeys.GAME_SETTINGS: json.dumps(old_game_settings)})
        context = await Context.from_fsm_context(call.from_user.id, state)

    await state.update_data(**{StateKeys.GENERAL_BET: general_bet})
    await settings_menu(context, msg_id=call.message.message_id, general_bet=general_bet)


@router.message(state=Menu.settings)
async def bet_change_text_cube(message, state):
    await bet_change_state(message, state)

    context = await Context.from_fsm_context(message.from_user.id, state)
    await settings_menu(context, msg_id=context.last_msg_id)


@router.callback_query(text=['reset_bet'])
async def cube_reset_bet(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    null_game_settings = json.dumps([])
    await state.update_data(**{StateKeys.GAME_SETTINGS: null_game_settings})

    context = await Context.from_fsm_context(call.from_user.id, state)
    await settings_menu(context, msg_id=call.message.message_id)
