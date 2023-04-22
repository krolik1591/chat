from asyncio import sleep

from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext

from bot.const import THROTTLE_TIME_SPIN
from bot.db import db, manager
from bot.handlers.context import Context
from bot.utils.dice_check.dice_games import DICE_GAMES, Dice
from bot.handlers.games_handlers.m04_game_settings import settings_menu
from bot.texts import DICE_ROLL_TEXT

flags = {"throttling_key": "spin"}
router = Router()


@router.callback_query(text=["game_play"], flags=flags)
async def games_play(call: types.CallbackQuery, state: FSMContext):
    await db.set_user_last_active(call.from_user.id)
    context = await Context.from_fsm_context(call.from_user.id, state)

    dice_game: Dice = DICE_GAMES[context.game]

    error = dice_game.pre_check(context)
    if error is not None:
        await call.answer(error, show_alert=True)
        return

    dice_msg = await call.message.answer_dice(emoji=dice_game.dice_emoji)
    await call.message.edit_text(text=DICE_ROLL_TEXT)

    result = await dice_game.get_result(dice_msg.dice.value, context)

    score_change = result['score_change']
    user_win = result['user_win']
    game_info = result['game_info']
    text = result['text']

    balance_type = context.balance_type

    with manager.pw_database.atomic():
        await db.update_user_balance(call.from_user.id, balance_type, user_win)
        await db.insert_game_log(call.from_user.id, balance_type, game=context.game,
                                 game_info=game_info, bet=context.bet, result=score_change)

    # Change first msg to game result
    await sleep(THROTTLE_TIME_SPIN)
    await call.message.edit_text(text=text)

    # Send settings menu
    context = await Context.from_fsm_context(call.from_user.id, state)
    await settings_menu(context, msg_id=None)

