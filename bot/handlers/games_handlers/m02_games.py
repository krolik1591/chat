from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from bot.db import db
from bot.handlers.context import Context
from bot.handlers.games_handlers.m03_balance import balances_menu
from bot.handlers.states import StateKeys
from bot.menus.game_menus import select_game_menu

router = Router()


@router.callback_query(Text("all_games"))
async def all_games(call: types.CallbackQuery, state: FSMContext):
    balances = await db.get_user_balances(call.from_user.id)

    text, keyboard = select_game_menu(balances)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text(startswith='set_game_'))
async def set_game(call: types.CallbackQuery, state: FSMContext):
    game = call.data.removeprefix('set_game_')
    await state.update_data(**{StateKeys.GAME: game})

    context = await Context.from_fsm_context(call.from_user.id, state)
    await balances_menu(context, msg_id=call.message.message_id)
