from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from bot.const import START_POINTS, MIN_BET, MAX_BET
from bot.menus.game_choice_menu import game_choice_menu
from bot.menus.game_menus import get_game_menu
from bot.menus.main_menu import main_menu

flags = {"throttling_key": "default"}
router = Router()


@router.callback_query(text=["casino", "random_cube", "basket", "darts", "football", "cuefa", "bowling", "mine"])
async def choice_game(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_bet = user_data.get('bet', MIN_BET)
    user_balance = user_data.get('balance', START_POINTS)

    text, keyboard = get_game_menu(user_bet, user_balance)
    msg = await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(text=["all_games"])
async def all_games(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_bet = user_data.get('bet', MIN_BET)
    user_balance = user_data.get('balance', START_POINTS)

    text, keyboard = game_choice_menu(user_balance, user_balance)
    msg = await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(text=["bet_minus", "bet_plus", "bet_min", "bet_max", "bet_x2"])
async def bet_change(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_bet = user_data.get('bet', MIN_BET)
    user_balance = user_data.get('balance', START_POINTS)

    if call.data == 'bet_minus':
        new_user_bet = user_bet - MIN_BET
    elif call.data == 'bet_plus':
        new_user_bet = user_bet + MIN_BET
    elif call.data == 'bet_min':
        new_user_bet = MIN_BET
    elif call.data == 'bet_max':
        new_user_bet = MAX_BET
    elif call.data == 'bet_x2':
        new_user_bet = user_bet * 2
    else:
        raise Exception("this should not happen")

    new_user_bet = normalize_bet(new_user_bet, user_balance)

    if new_user_bet == user_bet:
        await call.answer()
        return

    await state.update_data(bet=new_user_bet)

    text, keyboard = get_game_menu(new_user_bet, user_balance)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.message()
async def bet_change_text(message: Message, state: FSMContext):
    await message.delete()
    try:
        new_user_bet = int(message.text)
    except ValueError:
        return

    user_data = await state.get_data()
    last_msg = user_data.get('last_msg_id')
    user_balance = user_data.get('balance', START_POINTS)
    user_bet = user_data.get('bet', MIN_BET)

    if last_msg is None:
        return

    new_user_bet = normalize_bet(new_user_bet, user_balance)
    if new_user_bet == user_bet:
        return

    await state.update_data(bet=new_user_bet)

    text, keyboard = get_game_menu(new_user_bet, user_balance)
    await state.bot.edit_message_text(text, reply_markup=keyboard, chat_id=message.chat.id, message_id=last_msg)


@router.callback_query(text=["end_money"])
async def demo_money(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(balance=START_POINTS)
    await call.answer('Людяність відновлена')

    await cmd_start(call.message, state)
    await call.message.delete()


def normalize_bet(bet, balance):
    bet = max(bet, MIN_BET)
    bet = min(bet, MAX_BET, balance)
    return bet
