from aiogram import Router, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

import bot.db.methods as db
from bot.handlers.context import Context
from bot.handlers.games_handlers.m03_token import tokens_menu
from bot.handlers.states import StateKeys
from bot.menus.game_menus import select_game_menu

router = Router()


@router.callback_query(text=["all_games"])
async def all_games(call: types.CallbackQuery, state: FSMContext):
    balances = await db.get_user_balances(call.from_user.id)

    text, keyboard = select_game_menu(balances)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text(text_startswith='set_game_'))
async def set_game(call: types.CallbackQuery, state: FSMContext):
    game = call.data.removeprefix('set_game_')
    await state.update_data(**{StateKeys.GAME: game})

    context = await Context.from_fsm_context(call.from_user.id, state)
    await tokens_menu(context, call.message.message_id)
