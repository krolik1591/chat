from TonTools.Contracts.Wallet import Wallet
from aiogram import F, Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from bot.consts.const import START_POINTS
from bot.db import db
from bot.handlers.context import Context
from bot.handlers.states import Menu, StateKeys
from bot.menus import main_menu
from bot.tokens.token_ton import TonWrapper

flags = {"throttling_key": "default"}
router = Router()


async def send_main_menu(context: Context, msg_id=None):
    balances = await db.get_user_balances(context.user_id)
    text, keyboard = main_menu(balances)

    if msg_id is None:
        msg = await context.fsm_context.bot.send_message(context.user_id, text, reply_markup=keyboard)
        await context.fsm_context.update_data(**{StateKeys.LAST_MSG_ID: msg.message_id})
    else:
        await context.fsm_context.bot.edit_message_text(
            chat_id=context.user_id, message_id=msg_id, text=text, reply_markup=keyboard)

    await context.fsm_context.set_state(Menu.delete_message)


@router.message(F.chat.type == "private", commands="start", flags=flags)
async def cmd_start(message: Message, state: FSMContext):
    try:
        await db.get_user_lang(message.from_user.id)
    except ValueError:
        await db.create_new_user(message.from_user.id, message.from_user.username)
        await db.update_user_balance(message.from_user.id, 'demo', START_POINTS)  # add demo

        new_wallet = Wallet(provider=TonWrapper.INSTANCE)
        mnemonics = ','.join(new_wallet.mnemonics)
        await db.create_user_wallet(message.from_user.id, new_wallet.address, mnemonics)

    context = await Context.from_fsm_context(message.from_user.id, state)
    await send_main_menu(context)


@router.callback_query(text=["main_menu"])
async def back_to_main(call: types.CallbackQuery, state: FSMContext):
    context = await Context.from_fsm_context(call.from_user.id, state)
    await send_main_menu(context, msg_id=call.message.message_id)
