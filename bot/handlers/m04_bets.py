from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from bot.const import START_POINTS, MIN_BET, MAX_BET
from bot.menus import get_game_menu

router = Router()


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


def normalize_bet(bet, balance):
    bet = max(bet, MIN_BET)
    bet = min(bet, MAX_BET, balance)
    return bet