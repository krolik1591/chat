from asyncio import sleep

from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext

import bot.db.methods as db
from bot.const import THROTTLE_TIME_SPIN
from bot.handlers.context import Context
from bot.handlers.games_handlers.m04_game_settings import settings_menu
from bot.handlers.states import Games
from bot.texts import DICE_ROLL_TEXT, LOSE_TEXT, \
    WIN_TEXT
from bot.utils.dice_check_games.dice_check_basket import get_coefficient_basket
from bot.utils.dice_check_games.dice_check_bowling import get_coefficient_bowling
from bot.utils.dice_check_games.dice_check_casino import get_coefficient
from bot.utils.dice_check_games.dice_check_cube import get_coefficient_cube
from bot.utils.dice_check_games.dice_check_darts import get_coefficient_darts
from bot.utils.dice_check_games.dice_check_football import get_coefficient_football
from bot.utils.dice_check_games.dice_check_texts import basket_text, bowling_text, darts_text, football_text
from bot.utils.rounding import round_down

flags = {"throttling_key": "spin"}
router = Router()


@router.callback_query(text=["game_play"])
async def games_play(call: types.CallbackQuery, state: FSMContext):
    await db.set_user_last_active(call.from_user.id)
    context = await Context.from_fsm_context(call.from_user.id, state)

    if context.bet > context.balance:
        await call.answer("Ставка більше балансу", show_alert=True)
        return

    if context.game == Games.CASINO:
        # Send dice
        dice_msg = await call.message.answer_dice(emoji="🎰")
        await call.message.edit_text(text=DICE_ROLL_TEXT)

        # Parse dice result
        coef = get_coefficient(dice_msg.dice.value)
        await process_dice(call, context, coef, dice_msg, state)

    if context.game == Games.CUBE:
        if context.game_settings is None:
            await call.answer("❌ You have not chosen an outcome for a bet")
            # text, keyboard = game_menu_err(1)  # user doesnt choice bet
            # await call.message.answer(text, reply_markup=keyboard)
            return

        dice_msg = await call.message.answer_dice(emoji="🎲")
        await call.message.edit_text(text=DICE_ROLL_TEXT)

        coef = get_coefficient_cube(dice_msg.dice.value, context.game_settings)
        await process_dice(call, context, coef, dice_msg, state)

    if context.game == Games.BASKET:
        dice_msg = await call.message.answer_dice(emoji="🏀")
        await call.message.edit_text(text=DICE_ROLL_TEXT)

        coef = get_coefficient_basket(dice_msg.dice.value)
        await process_dice(call, context, coef, dice_msg, state)

    if context.game == Games.DARTS:
        dice_msg = await call.message.answer_dice(emoji="🎯")
        await call.message.edit_text(text=DICE_ROLL_TEXT)

        coef = get_coefficient_darts(dice_msg.dice.value)
        await process_dice(call, context, coef, dice_msg, state)

    if context.game == Games.BOWLING:
        dice_msg = await call.message.answer_dice(emoji="🎳")
        await call.message.edit_text(text=DICE_ROLL_TEXT)

        coef = get_coefficient_bowling(dice_msg.dice.value)
        await process_dice(call, context, coef, dice_msg, state)

    if context.game == Games.FOOTBALL:
        dice_msg = await call.message.answer_dice(emoji="⚽️")
        await call.message.edit_text(text=DICE_ROLL_TEXT)

        coef = get_coefficient_football(dice_msg.dice.value)
        await process_dice(call, context, coef, dice_msg, state)


async def process_dice(call: types.CallbackQuery, context: Context, coef, dice_msg: types.Message, state):
    token_id = context.token.id

    score_change = round_down((coef * context.bet), 5)
    user_win = round_down(score_change - context.bet, 5)

    # todo atomic db

    await db.update_user_balance(call.from_user.id, token_id, user_win)
    user_balance = await db.get_user_balance(call.from_user.id, token_id)

    game_info = {"dice_result": dice_msg.dice.value}
    await db.insert_game_log(call.from_user.id, token_id, game=context.game,
                             game_info=game_info, bet=context.bet, result=score_change)

    await sleep(THROTTLE_TIME_SPIN)

    # Send result
    win_or_lose_text = ''
    if context.game == Games.CASINO and Games.CUBE:
        win_or_lose_text = LOSE_TEXT if score_change == 0 \
            else WIN_TEXT.format(score_change=round_down(score_change, 2), token_icon=context.token.icon)

    if context.game == Games.BASKET:
        win_or_lose_text = basket_text(dice_msg.dice.value,
                                      score_change=round_down(score_change, 2), token_icon=context.token.icon)

    if context.game == Games.DARTS:
        win_or_lose_text = darts_text(dice_msg.dice.value,
                                      score_change=round_down(score_change, 2), token_icon=context.token.icon)

    if context.game == Games.BOWLING:
        win_or_lose_text = bowling_text(dice_msg.dice.value,
                                      score_change=round_down(score_change, 2), token_icon=context.token.icon)

    if context.game == Games.FOOTBALL:
        win_or_lose_text = football_text(dice_msg.dice.value,
                                        score_change=round_down(score_change, 2), token_icon=context.token.icon)

    await call.message.edit_text(text=win_or_lose_text)

    # Send settings menu
    context = await Context.from_fsm_context(call.from_user.id, state)
    await settings_menu(context, msg_id=None)
