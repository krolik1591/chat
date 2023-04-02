from asyncio import sleep

from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext

from bot.const import THROTTLE_TIME_SPIN, MIN_BET, START_POINTS
from bot.handlers.states import BET, GAME, LAST_MSG_ID, TOKEN_ICON, TOKEN_ID
from bot.menus.game_menus.game_menus import get_game_menu
from bot.utils.dice_check import get_coefficient
import bot.db.methods as db

flags = {"throttling_key": "spin"}
router = Router()


@router.callback_query(text=["game_play"])
async def casino_play(call: types.CallbackQuery, state: FSMContext):
    await db.set_user_last_active(call.from_user.id)

    user_data = await state.get_data()
    user_bet = float(user_data.get(BET, MIN_BET))
    token_icon = user_data.get(TOKEN_ICON)
    token_id = user_data.get(TOKEN_ID)
    game = user_data[GAME]

    user_balance = await db.get_user_balance(call.from_user.id, token_id)

    if user_bet > user_balance:
        await call.answer("Ставка більше балансу", show_alert=True)
        return

    # Send dice
    msg = await call.message.answer_dice(emoji="🎰")
    await call.message.edit_text(text="Успіхів!")

    # Parse dice result
    score_change = round((get_coefficient(msg.dice.value) * user_bet), 5)
    user_win = round(score_change - user_bet, 5)
    await db.update_user_balance(call.from_user.id, token_id, user_win)
    user_balance = await db.get_user_balance(call.from_user.id, token_id)
    await sleep(THROTTLE_TIME_SPIN)

    # Send result
    win_or_lose_text = "К сожалению, вы не выиграли." if score_change == 0 \
        else f"Вы выиграли {score_change} очков!"
    await call.message.edit_text(text=win_or_lose_text)

    # Send new game menu
    text, keyboard = get_game_menu(user_bet, user_balance, token_icon, token_id)
    msg_ = await call.message.answer(text, reply_markup=keyboard)
    await state.update_data(**{LAST_MSG_ID: msg.message_id})

    game_info = {"dice_result": msg.dice.value}
    await db.insert_game_log(call.from_user.id, token_id, game=game,
                             game_info=game_info, bet=user_bet, result=score_change)
