from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from bot.const import CHANGE_BET, MAX_BET, MIN_BET
from bot.handlers.context import Context
from bot.handlers.states import Games, Menu, StateKeys
from bot.menus.game_menus import bet_menus
from bot.menus.game_menus.cube_settings import cube_settings
from bot.utils.rounding import round_down

router = Router()


async def bet_menu(context: Context, msg_id=None):
    text, keyboard = bet_menus.bet_menu(context.bet, context.balance, context.token.icon, context.token.id,
                                        context.game)

    if msg_id is None:
        bet_msg = await context.fsm_context.bot.send_message(
            chat_id=context.user_id, text=text, reply_markup=keyboard)
        await context.fsm_context.update_data(**{StateKeys.LAST_MSG_ID: bet_msg.message_id})
    else:
        await context.fsm_context.bot.edit_message_text(
            chat_id=context.user_id, message_id=msg_id, text=text, reply_markup=keyboard)

    await context.fsm_context.set_state(Menu.bet)


@router.callback_query(text=["bet"])
async def bet_show(call: types.CallbackQuery, state: FSMContext):
    context = await Context.from_fsm_context(call.from_user.id, state)
    await bet_menu(context, msg_id=call.message.message_id)


@router.callback_query(text=["bet_minus", "bet_plus", "bet_min", "bet_max", "bet_x2"])
async def bet_change(call: types.CallbackQuery, state: FSMContext):
    context = await Context.from_fsm_context(call.from_user.id, state)
    user_bet = context.bet
    user_balance = context.balance

    if call.data == 'bet_minus':
        new_user_bet = user_bet - CHANGE_BET
    elif call.data == 'bet_plus':
        new_user_bet = user_bet + CHANGE_BET
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

    await state.update_data(**{StateKeys.BET: new_user_bet})

    context = await Context.from_fsm_context(call.from_user.id, state)
    await bet_menu(context, msg_id=call.message.message_id)


@router.message(state=Menu.bet)
async def bet_change_text(message: Message, state: FSMContext):
    await bet_change_state(message, state)

    context = await Context.from_fsm_context(message.from_user.id, state)
    await bet_menu(context, msg_id=context.last_msg_id)


async def bet_change_state(message: Message, state: FSMContext):
    await message.delete()
    try:
        new_user_bet = float(message.text)
    except ValueError:
        return
    new_user_bet = round(new_user_bet, 5)

    context = await Context.from_fsm_context(message.from_user.id, state)
    user_bet = context.bet
    user_balance = context.balance

    if context.last_msg_id is None:
        return

    new_user_bet = normalize_bet(new_user_bet, user_balance)
    if new_user_bet == user_bet:
        return

    await state.update_data(**{StateKeys.BET: new_user_bet})

    # context = await Context.from_fsm_context(message.from_user.id, state)
    # await bet_menu(context, msg_id=context.last_msg_id)


def normalize_bet(bet, balance):
    bet = min(bet, MAX_BET, balance)
    bet = max(bet, MIN_BET)
    return float(round_down(bet, 2))
