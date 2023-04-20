import re

from aiogram import Router, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from bot.db import manager, db
from bot.handlers.states import StateKeys
from bot.menus.wallet_menus import withdraw_menu
from bot.middlewares.filters import FilterChatId
from bot.tokens.token_ton import withdraw_cash_to_user
from bot.utils.config_reader import config

router = Router()


@router.callback_query(Text(text_startswith='approve_manual_tx_'))
async def approve_titan_tx(call: types.CallbackQuery, state: FSMContext):
    titan_tx_id = call.data.removeprefix('approve_manual_tx_')
    titan_tx = await db.get_manual_tx_by_id(titan_tx_id)

    await state.bot.edit_message_text(
        f'{call.message.text} \n\n✅ Approve', chat_id=config.admin_chat_id, message_id=call.message.message_id)

    text, kb = withdraw_menu.withdraw_manual_approved(titan_tx.amount / 10 ** 9 * titan_tx.price)
    await state.bot.send_message(chat_id=titan_tx.user_id, text=text, reply_markup=kb)

    token_id = titan_tx.token_id
    await state.update_data(**{StateKeys.TOKEN_ID: token_id})
    token = await db.get_token_by_id(token_id)

    await withdraw_cash_to_user(state, titan_tx.tx_address, titan_tx.amount / 10 ** 9, titan_tx.user_id,
                                token, manual_tx=True)


@router.callback_query(Text(text_startswith='denied_manual_tx_'))
async def decline_titan_tx(call: types.CallbackQuery, state: FSMContext):
    await state.bot.edit_message_text(
        f'{call.message.text} \n\n❌ Denied', chat_id=config.admin_chat_id, message_id=call.message.message_id)

    manual_tx_id = call.data.removeprefix('denied_manual_tx_')
    manual_tx = await db.get_manual_tx_by_id(manual_tx_id)

    with manager.pw_database.atomic():
        await db.update_manual_withdraw_state(manual_tx_id, 'rejected')
        await db.update_user_balance(manual_tx.user_id, manual_tx.token_id, manual_tx.amount / 10**9 * manual_tx.price)

    text, kb = withdraw_menu.withdraw_manual_rejected()
    await state.bot.send_message(chat_id=manual_tx.user_id, text=text, reply_markup=kb)


@router.message(lambda message: message.reply_to_message is not None, FilterChatId(), state='*',)
async def send_msg_from_admin_to_user(message: Message, state: FSMContext):
    match = re.search(r"\(id:\s*(\d+)\)", message.reply_to_message.text)
    user_id = match.group(1) if match else None

    await state.bot.send_message(chat_id=user_id, text=message.text)
