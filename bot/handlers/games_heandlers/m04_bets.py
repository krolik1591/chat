from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from bot.const import MAX_BET, MIN_BET
from bot.db.methods import get_token_by_id, get_user_balance
from bot.handlers.states import Choosen_message
from bot.menus.game_menus.game_menus import get_game_menu

router = Router()


@router.callback_query(text=["bet_minus", "bet_plus", "bet_min", "bet_max", "bet_x2"])
async def bet_change(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_bet = float(user_data.get('bet', MIN_BET))
    token_id = user_data.get('token_id')
    user_balance = float(await get_user_balance(call.from_user.id, token_id))
    token_icon = user_data.get('token_icon')

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

    text, keyboard = get_game_menu(new_user_bet, user_balance, token_icon, token_id)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.message(state=Choosen_message.bet)
async def bet_change_text(message: Message, state: FSMContext):
    await message.delete()
    try:
        new_user_bet = float(message.text)
    except ValueError:
        return
    new_user_bet = round(new_user_bet, 5)

    user_data = await state.get_data()
    last_msg = user_data.get('last_msg_id')
    user_bet = user_data.get('bet', MIN_BET)
    token_id = user_data.get('token_id')
    user_balance = await get_user_balance(message.from_user.id, token_id)
    token = await get_token_by_id(token_id)

    if last_msg is None:
        return

    new_user_bet = normalize_bet(new_user_bet, user_balance)
    if new_user_bet == user_bet:
        return

    await state.update_data(bet=new_user_bet)

    text, keyboard = get_game_menu(new_user_bet, user_balance, token.icon)
    await state.bot.edit_message_text(text, reply_markup=keyboard, chat_id=message.chat.id, message_id=last_msg)


def normalize_bet(bet, balance):
    bet = min(bet, MAX_BET, balance)
    bet = max(bet, MIN_BET)
    return float(round(bet, 2))
