from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

import bot.db.methods as db
from bot.const import START_POINTS, MIN_BET
from bot.menus import game_choice_menu, get_game_menu

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
    user_data = await state.get_data()
    user_bet = user_data.get('bet', MIN_BET)

    balances = await db.get_user_balances(call.from_user.id)

    text, keyboard = main_or_demo_balance(balances)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(text=["1", "2"])
async def choice_balance(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_bet = user_data.get('bet', MIN_BET)
    await state.update_data(token=call.data)

    # user_balance = user_data.get('balance', START_POINTS)
    balances = await db.get_user_balances(call.from_user.id)
    print(balances)
    text, keyboard = get_game_menu(user_bet, balances)
    await call.message.edit_text(text, reply_markup=keyboard)

