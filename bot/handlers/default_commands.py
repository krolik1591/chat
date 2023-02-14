from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext

from bot.const import START_POINTS, MIN_BET
from bot.handlers.main import cmd_start
from bot.menus.game_choice_menu import game_choice_menu
from bot.menus.game_menus import get_game_menu

router = Router()


@router.callback_query(text=["all_games"])
async def all_games(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_bet = user_data.get('bet', MIN_BET)
    user_balance = user_data.get('balance', START_POINTS)

    text, keyboard = game_choice_menu(user_balance, user_balance)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(text=["casino", "random_cube", "basket", "darts", "football", "cuefa", "bowling", "mine"])
async def choice_game(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_bet = user_data.get('bet', MIN_BET)
    user_balance = user_data.get('balance', START_POINTS)

    text, keyboard = get_game_menu(user_bet, user_balance)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(text=["end_money"])
async def demo_money(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(balance=START_POINTS)
    await call.answer('Людяність відновлена')

    await cmd_start(call.message, state)
    await call.message.delete()
