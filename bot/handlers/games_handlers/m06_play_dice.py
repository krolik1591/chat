from asyncio import sleep

from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.consts.const import THROTTLE_TIME_SPIN
from bot.db import db, manager
from bot.handlers.context import Context
from bot.handlers.games_handlers.dice_games import DICE_GAMES, Dice
from bot.handlers.games_handlers.m04_game_settings import settings_menu
from bot.menus.utils import get_balance_icon
from bot.utils.rounding import round_down

flags = {"throttling_key": "spin"}
router = Router()


@router.callback_query(Text("game_play"), flags=flags)
async def games_play(call: types.CallbackQuery, state: FSMContext):
    await db.set_user_last_active(call.from_user.id)
    context = await Context.from_fsm_context(call.from_user.id, state)

    if context.balance_type == 'promo':
        if not await can_play_on_promo_balance(call):
            return

    dice_game: Dice = DICE_GAMES[context.game]

    error = dice_game.pre_check(context)
    if error is not None:
        await call.answer(error, show_alert=True)
        return

    dice_msg = await call.message.answer_dice(emoji=dice_game.EMOJI)
    await call.message.edit_text(text=_('DICE_ROLL_TEXT'))

    result = await dice_game.get_result(context, dice_msg.dice.value)

    with manager.pw_database.atomic():
        await db.update_user_balance(call.from_user.id, context.balance_type, result['score_change'])
        await db.insert_game_log(user_id=call.from_user.id,
                                 balance_type=context.balance_type,
                                 game=context.game,
                                 game_info=result['game_info'],
                                 bet=context.bet,
                                 result=round_down(result['score_change'], 5))

    # Change first msg to game result
    await sleep(THROTTLE_TIME_SPIN)
    text = dice_game.get_text(context, dice_msg.dice.value, round(result['score_change'] + context.bet, 2),
                              get_balance_icon(context.balance_type))
    await call.message.edit_text(text=text)

    # Send settings menu
    context = await Context.from_fsm_context(call.from_user.id, state)
    await settings_menu(context, msg_id=None)


async def can_play_on_promo_balance(call):
    try:
        sum_bets, min_wager, wager = await db.get_sum_bets_from_activated_promo_min_wager_and_wager(call.from_user.id)
    except AttributeError:
        await call.answer(_('M06_PLAY_DICE_NOT_EXIST_PROMO_BALANCE'), show_alert=True)
        return False

    if not min_wager:
        await call.answer(_('M06_PLAY_DICE_NOT_EXIST_PROMO_BALANCE'), show_alert=True)
        return False

    if not sum_bets:
        await call.answer(_('M06_PLAY_DICE_NOT_ENOUGH_BETS_TO_PLAY_PROMO')
                          .format(missing_bets=min_wager), show_alert=True)
        return False

    if sum_bets < min_wager:
        missing_bets = min_wager - sum_bets
        await call.answer(_('M06_PLAY_DICE_NOT_ENOUGH_BETS_TO_PLAY_PROMO')
                          .format(missing_bets=round_down(missing_bets, 2)), show_alert=True)
        return False
    return True
