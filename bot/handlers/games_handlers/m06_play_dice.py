from asyncio import sleep

from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from bot.consts.const import THROTTLE_TIME_SPIN
from bot.db import db, manager
from bot.handlers.context import Context
from bot.menus.utils import get_balance_icon
from bot.handlers.games_handlers.dice_games import DICE_GAMES, Dice
from bot.handlers.games_handlers.m04_game_settings import settings_menu
from bot.consts.texts import DICE_ROLL_TEXT

flags = {"throttling_key": "spin"}
router = Router()


@router.callback_query(Text("game_play"), flags=flags)
async def games_play(call: types.CallbackQuery, state: FSMContext):
    await db.set_user_last_active(call.from_user.id)
    context = await Context.from_fsm_context(call.from_user.id, state)

    dice_game: Dice = DICE_GAMES[context.game]

    error = dice_game.pre_check(context)
    if error is not None:
        await call.answer(error, show_alert=True)
        return

    dice_msg = await call.message.answer_dice(emoji=dice_game.EMOJI)
    await call.message.edit_text(text=DICE_ROLL_TEXT)

    result = await dice_game.get_result(context, dice_msg.dice.value)

    with manager.pw_database.atomic():
        await db.update_user_balance(call.from_user.id, context.balance_type, result['score_change'])
        await db.insert_game_log(user_id=call.from_user.id,
                                 balance_type=context.balance_type,
                                 game=context.game,
                                 game_info=result['game_info'],
                                 bet=context.bet,
                                 result=result['score_change'])

    # Change first msg to game result
    await sleep(THROTTLE_TIME_SPIN)
    text = dice_game.get_text(context, dice_msg.dice.value, result['score_change'] + context.bet,
                              get_balance_icon(context.balance_type))
    await call.message.edit_text(text=text)

    # Send settings menu
    context = await Context.from_fsm_context(call.from_user.id, state)
    await settings_menu(context, msg_id=None)
