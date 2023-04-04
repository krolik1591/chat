from aiogram import Router, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

import bot.db.methods as db
from bot.const import MIN_BET
from bot.handlers.games_handlers.m04_bets import Choosen_message
from bot.handlers.states import BET, GAME, TOKEN_ICON, TOKEN_ID
from bot.menus import game_choice_menu
from bot.menus.game_menus.game_menus import get_game_menu
from bot.menus.game_menus.main_or_demo_balance_menu import main_or_demo_balance

router = Router()


@router.callback_query(text=["all_games"])
async def all_games(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_bet = user_data.get(BET, MIN_BET)

    balances = await db.get_user_balances(call.from_user.id)

    text, keyboard = game_choice_menu(balances)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(text=["casino", "cube_menu", "basket", "darts", "football", "cuefa", "bowling", "mine"])
async def choice_main_or_demo_balance(call: types.CallbackQuery, state: FSMContext):
    tokens = await db.get_tokens()
    balances = await db.get_user_balances(call.from_user.id)

    await state.update_data(**{GAME: call.data})

    text, keyboard = main_or_demo_balance(tokens, balances)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text(text_startswith='token_'))
async def choice_token(call: types.CallbackQuery, state: FSMContext):
    token_id = int(call.data.removeprefix('token_'))
    try:
        token = await db.get_token_by_id(token_id)
    except:
        # todo. integrity error; move user to start
        return

    await state.update_data(**{TOKEN_ID: token_id, TOKEN_ICON: token.icon})

    user_data = await state.get_data()

    user_bet = user_data.get(BET, MIN_BET)
    game = user_data.get(GAME)
    user_balance = await db.get_user_balance(call.from_user.id, token_id)

    text, keyboard = get_game_menu(user_bet, user_balance, token.icon, token.token_id, game)
    await call.message.edit_text(text, reply_markup=keyboard)

    await state.set_state(Choosen_message.bet)


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
