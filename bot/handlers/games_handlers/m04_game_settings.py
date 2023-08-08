import json

from aiogram import Router, types
from aiogram.filters import Text, StateFilter
from aiogram.fsm.context import FSMContext

from bot.handlers.context import Context
from bot.handlers.games_handlers.m05_bets import bet_change_state, bet_menu
from bot.handlers.states import Games, Menu, StateKeys
from bot.menus.game_menus.cube_settings import cube_settings

router = Router()


async def settings_menu(context: Context, msg_id=None, chat_id=None):
    if context.game == Games.CUBE:
        await context.fsm_context.set_state(Menu.settings)

        text, keyboard = cube_settings(context.game_settings or [], context.balance, context.bet, context.balance_type)

        await context.fsm_context.bot.edit_message_text(
            chat_id=chat_id, message_id=msg_id, text=text, reply_markup=keyboard)

    else:
        return await bet_menu(context, msg_id=msg_id, chat_id=chat_id)


@router.callback_query(Text(startswith='game_settings'))
async def show_settings(call: types.CallbackQuery, state: FSMContext):
    context = await Context.from_fsm_context(call.from_user.id, state)
    await settings_menu(context, msg_id=call.message.message_id, chat_id=call.message.chat.id)


@router.callback_query(Text(startswith='cube_game_settings_'))
async def set_cube_settings(call: types.CallbackQuery, state: FSMContext):
    setting_to_toggle = call.data.removeprefix('cube_game_settings_')

    context = await Context.from_fsm_context(call.from_user.id, state)
    game_settings: [str] = context.game_settings or []

    if setting_to_toggle == "RESET":
        game_settings = []
    else:
        if setting_to_toggle in game_settings:
            game_settings.remove(setting_to_toggle)
        else:
            game_settings.append(setting_to_toggle)

    await state.update_data(**{StateKeys.GAME_SETTINGS: json.dumps(game_settings)})
    context = await Context.from_fsm_context(call.from_user.id, state)

    await settings_menu(context, msg_id=call.message.message_id, chat_id=call.message.chat.id)


@router.message(StateFilter(Menu.settings))
async def bet_change_text_cube(message, state):
    await bet_change_state(message, state)

    context = await Context.from_fsm_context(message.from_user.id, state)
    await settings_menu(context, msg_id=context.last_msg_id, chat_id=message.chat.id)

