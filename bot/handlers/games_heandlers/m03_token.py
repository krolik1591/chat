import time
from datetime import datetime

from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext

from bot.const import START_POINTS, MIN_BET
from bot.db.methods import update_user_balance, get_user_balance, add_new_transaction
from bot.menus.game_menus.game_menus import get_game_menu

router = Router()


# only for DEMO token
@router.callback_query(text=["end_money"])
async def replenish_demo_balance(call: types.CallbackQuery, state: FSMContext):
    DEMO_TOKEN = 1
    await update_user_balance(call.from_user.id, DEMO_TOKEN, START_POINTS)
    user_data = await state.get_data()
    user_bet = user_data.get('bet', MIN_BET)
    token_icon = user_data.get('token_icon')
    user_balance = await get_user_balance(call.from_user.id, 1)

    text, keyboard = get_game_menu(user_bet, user_balance, token_icon, DEMO_TOKEN)
    await call.message.edit_text(text, reply_markup=keyboard)

    await add_new_transaction(call.from_user.id, DEMO_TOKEN, 500, int(time.time()), START_POINTS, 'demo_address', 'demo_hash', int(time.time()))

# todo кнопка віддай гроші з'являється на ТОН балансе, а не тільки на демо
