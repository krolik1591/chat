from aiogram import Router, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

import bot.db.methods as db
from bot.const import MIN_BET
from bot.menus import game_choice_menu, get_game_menu
from bot.menus.game_menus.main_or_demo_balance_menu import main_or_demo_balance

router = Router()


@router.callback_query(text=["all_games"])
async def all_games(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_bet = user_data.get('bet', MIN_BET)

    balances = await db.get_user_balances(call.from_user.id)

    text, keyboard = game_choice_menu(balances)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(text=["casino", "random_cube", "basket", "darts", "football", "cuefa", "bowling", "mine"])
async def choice_main_or_demo_balance(call: types.CallbackQuery, state: FSMContext):
    tokens = await db.get_tokens()
    balances = await db.get_user_balances(call.from_user.id)

    await state.update_data(game=call.data)

    text, keyboard = main_or_demo_balance(tokens, balances)
    await call.message.edit_text(text, reply_markup=keyboard)



@router.callback_query(Text(text_startswith='token_'))
async def choice_token(call: types.CallbackQuery, state: FSMContext):
    token_id = int(call.data.removeprefix('token_'))
    try:
        token = await db.get_token_by_id(token_id)
    except:
        return
        # todo. integrity error; move user to start
    await state.update_data(token_id=token_id, token_icon=token.icon)

    user_data = await state.get_data()
    user_bet = user_data.get('bet', MIN_BET)

    user_balance = await db.get_user_balance(call.from_user.id, token_id)

    text, keyboard = get_game_menu(user_bet, user_balance, token.icon)
    await call.message.edit_text(text, reply_markup=keyboard)
