from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext

from bot.const import START_POINTS, MIN_BET
from bot.db.methods import update_user_balance, get_user_balance
from bot.menus import get_game_menu

router = Router()


# only for DEMO token
@router.callback_query(text=["end_money"])
async def replenish_demo_balance(call: types.CallbackQuery, state: FSMContext):
    await update_user_balance(call.from_user.id, 1, START_POINTS)
    user_data = await state.get_data()
    user_bet = user_data.get('bet', MIN_BET)
    token_icon = user_data.get('token_icon')
    user_balance = await get_user_balance(call.from_user.id, 1)

    text, keyboard = get_game_menu(user_bet, user_balance, token_icon)
    await call.message.edit_text(text, reply_markup=keyboard)

# todo
