from asyncio import sleep

from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext

import bot.db.methods as db
from bot.const import THROTTLE_TIME_SPIN
from bot.db.db import manager
from bot.handlers.context import Context
from bot.handlers.games_handlers.m04_game_settings import settings_menu
from bot.handlers.states import Games, StateKeys
from bot.menus.game_menus.game_menu_err import game_menu_err
from bot.texts import DICE_ROLL_TEXT
from bot.utils.dice_check.dice_check_casino import get_coefficient
from bot.utils.dice_check.dice_check_games import get_coefficient_basket, get_coefficient_bowling, \
    get_coefficient_cube, \
    get_coefficient_darts, get_coefficient_football
from bot.utils.dice_check.dice_check_texts import game_text
from bot.utils.rounding import round_down

flags = {"throttling_key": "spin"}
router = Router()


@router.callback_query(text=["game_play"])
async def games_play(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

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
        coefficient = get_coefficient(dice_msg.dice.value)
        await process_dice(call, context, coefficient, dice_msg, state)

    if context.game == Games.CUBE:
        if await cube_check_bet(call, state):
            return

        if context.game_settings is None or len(context.game_settings) == 0:
            text, keyboard = game_menu_err(1)  # user doesnt choice bet
            await call.message.answer(text, reply_markup=keyboard)
            return

        dice_msg = await call.message.answer_dice(emoji="🎲")
        await call.message.edit_text(text=DICE_ROLL_TEXT)

        coefficient = get_coefficient_cube(dice_msg.dice.value, context.game_settings)

        current_streak = (await state.get_data()).get(StateKeys.CUBE_LOSE_STREAK, 0)
        if coefficient == 0:
            await state.update_data(**{StateKeys.CUBE_LOSE_STREAK: current_streak + 1})
        else:
            await state.update_data(**{StateKeys.CUBE_LOSE_STREAK: 0})

        await process_dice(call, context, coefficient, dice_msg, state)

    if context.game == Games.BASKET:
        dice_msg = await call.message.answer_dice(emoji="🏀")
        await call.message.edit_text(text=DICE_ROLL_TEXT)

        coefficient = get_coefficient_basket(dice_msg.dice.value)
        await process_dice(call, context, coefficient, dice_msg, state)

    if context.game == Games.DARTS:
        dice_msg = await call.message.answer_dice(emoji="🎯")
        await call.message.edit_text(text=DICE_ROLL_TEXT)

        coefficient = get_coefficient_darts(dice_msg.dice.value)
        await process_dice(call, context, coefficient, dice_msg, state)

    if context.game == Games.BOWLING:
        dice_msg = await call.message.answer_dice(emoji="🎳")
        await call.message.edit_text(text=DICE_ROLL_TEXT)

        coefficient = get_coefficient_bowling(dice_msg.dice.value)
        await process_dice(call, context, coefficient, dice_msg, state)

    if context.game == Games.FOOTBALL:
        dice_msg = await call.message.answer_dice(emoji="⚽️")
        await call.message.edit_text(text=DICE_ROLL_TEXT)

        coefficient = get_coefficient_football(dice_msg.dice.value)
        await process_dice(call, context, coefficient, dice_msg, state)


async def process_dice(call: types.CallbackQuery, context: Context, coefficient, dice_msg: types.Message, state):
    token_id = context.token.id

    score_change = round_down((coefficient * context.bet), 5)

    if context.game == Games.CUBE:
        bets = len(context.game_settings)
        user_win = round_down(score_change - context.bet * bets, 5)
    else:
        user_win = round_down(score_change - context.bet, 5)

    game_info = {"dice_result": dice_msg.dice.value}

    with manager.pw_database.atomic():
        await db.update_user_balance(call.from_user.id, token_id, user_win)
        await db.insert_game_log(call.from_user.id, token_id, game=context.game,
                                 game_info=game_info, bet=context.bet, result=score_change)

    await sleep(THROTTLE_TIME_SPIN)

    # Send result
    cube_lose_streak = (await state.get_data()).get(StateKeys.CUBE_LOSE_STREAK)

    win_or_lose_text = game_text(context, round_down(score_change, 2), dice_msg.dice.value, cube_lose_streak)
    await call.message.edit_text(text=win_or_lose_text)

    # Send settings menu
    context = await Context.from_fsm_context(call.from_user.id, state)
    await settings_menu(context, msg_id=None)


async def cube_check_bet(call, state):
    general_bet = (await state.get_data()).get(StateKeys.GENERAL_BET)
    token_id = (await state.get_data()).get(StateKeys.TOKEN_ID)
    user_balance = await db.get_user_balance(call.from_user.id, token_id)

    if user_balance < general_bet:
        text, kb = game_menu_err('low_balance_big_wish')
        await state.bot.send_message(call.from_user.id, text, reply_markup=kb)

    return user_balance < general_bet
