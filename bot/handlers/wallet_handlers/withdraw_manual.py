import re

from aiogram import Router, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

from bot import tokens
from bot.db import manager, db
from bot.handlers.wallet_handlers.withdraw_cash import withdraw_cash_to_user
from bot.menus.wallet_menus import withdraw_menu
from bot.middlewares.filters import FilterChatId

router = Router()


@router.callback_query(Text(text_startswith='approve_manual_tx_'))
async def approve_manual_tx(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(f'{call.message.text} \n\n✅ Approve')

    tx_id = call.data.removeprefix('approve_manual_tx_')
    tx = await db.get_withdraw_tx_by_id(tx_id)

    await db.update_withdraw_tx_state(tx_id, 'pending')

    text, kb = withdraw_menu.withdraw_manual_approved(tx.amount)
    await state.bot.send_message(chat_id=tx.user_id, text=text, reply_markup=kb)

    token = await tokens.get_token_by_id(tx.token_id)
    await withdraw_cash_to_user(state.bot, tx.tx_address, float(tx.amount), tx.user_id, token, tx)


@router.callback_query(Text(text_startswith='denied_manual_tx_'))
async def decline_manual_tx(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(f'{call.message.text} \n\n❌ Denied')

    tx_id = call.data.removeprefix('denied_manual_tx_')
    tx = await db.get_withdraw_tx_by_id(tx_id)

    with manager.pw_database.atomic():
        await db.update_withdraw_tx_state(tx_id, 'rejected')
        await db.update_user_balance(tx.user_id, 'general', tx.amount)

    text, kb = withdraw_menu.withdraw_manual_rejected()
    await state.bot.send_message(chat_id=tx.user_id, text=text, reply_markup=kb)


@router.message(lambda message: message.reply_to_message is not None, FilterChatId(), state='*', )
async def send_msg_from_admin_to_user(message: types.Message, state: FSMContext):
    match = re.search(r"\(id:\s*(\d+)\)", message.reply_to_message.text)
    user_id = match.group(1) if match else None

    await state.bot.send_message(chat_id=user_id, text=message.text)
