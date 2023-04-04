from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext

import bot.db.methods as db
from bot.const import MIN_BET
from bot.handlers.states import BET, CUBE_BET, GAME, TOKEN_ICON, TOKEN_ID
from bot.menus.game_menus.game_menus import get_game_menu
from aiogram.dispatcher.filters import Text


router = Router()


@router.callback_query(text=["game_cube_change_bet", "cube_menu_return"])
async def game_cube_change_bet(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(game="game_cube_change_bet")

    user_data = await state.get_data()
    user_bet = float(user_data.get(BET, MIN_BET))
    token_id = user_data.get(TOKEN_ID)
    user_balance = await db.get_user_balance(call.from_user.id, token_id)
    token_icon = user_data.get(TOKEN_ICON)
    game = user_data.get(GAME)

    if call.data == "cube_menu_return":
        game = 'cube_menu'
        text, keyboard = get_game_menu(user_bet, user_balance, token_icon, token_id, game)
        await call.message.edit_text(text, reply_markup=keyboard)
        return

    text, keyboard = get_game_menu(user_bet, user_balance, token_icon, token_id, game)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text(text_startswith='cube_'))
async def cube_bet(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(**{CUBE_BET: call.data.removeprefix('cube_')})
    await call.answer()
