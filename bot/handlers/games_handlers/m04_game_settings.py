import json

from aiogram import Router, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

from bot.const import MIN_BET
from bot.handlers.context import Context
from bot.handlers.games_handlers.m05_bets import bet_change_state, bet_menu
from bot.handlers.states import Games, Menu, StateKeys
from bot.menus.game_menus.cube_settings import cube_settings

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

    await settings_menu(context, msg_id=call.message.message_id, general_bet=general_bet)


@router.message(state=Menu.settings)
async def bet_change_text_cube(message, state):
    await bet_change_state(message, state)

    context = await Context.from_fsm_context(message.from_user.id, state)
    await settings_menu(context, msg_id=context.last_msg_id)
