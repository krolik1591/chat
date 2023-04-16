from aiogram import Router, types
import re

from aiogram import Router, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext

from bot.db.methods import get_titan_tx_by_id, get_token_by_id, update_user_balance, \
    update_withdraw_state
from bot.menus.deposit_menus.withdraw_menu.withdraw_menu_err import withdraw_menu_err
from bot.ton.withdraw_cash import withdraw_cash_to_user
from bot.utils.config_reader import config

flags = {"throttling_key": "default"}
router = Router()


@router.callback_query(Text(text_startswith='approve_titan_tx_'))
async def approve_titan_tx(call: types.CallbackQuery, state: FSMContext):
    titan_tx_id = call.data.removeprefix('approve_titan_tx_')
    titan_tx = await get_titan_tx_by_id(titan_tx_id)

    await update_withdraw_state(titan_tx_id, 'approved')
    await state.bot.edit_message_text(
        f'{call.message.text} \n\n✅ Approve', chat_id=config.admin_chat_id, message_id=call.message.message_id)

    master_wallet = state.bot.ton_client.master_wallet
    TOKEN_ID = 2
    token = await get_token_by_id(TOKEN_ID)

    await withdraw_cash_to_user(master_wallet, titan_tx.tx_address, titan_tx.amount / 10 ** 9, titan_tx.user_id,
                                token, state)


@router.callback_query(Text(text_startswith='denied_titan_tx_'))
async def decline_titan_tx(call: types.CallbackQuery, state: FSMContext):
    await state.bot.edit_message_text(
        f'{call.message.text} \n\n❌ Denied', chat_id=config.admin_chat_id, message_id=call.message.message_id)

    titan_tx_id = call.data.removeprefix('denied_titan_tx_')
    await update_withdraw_state(titan_tx_id, 'rejected')

    text_ = call.message.text
    user_id, token_id, amount, token_price = get_withdraw_user_info(text_)
    await update_user_balance(user_id, token_id, amount * token_price)

    text, kb = withdraw_menu_err(7)
    await state.bot.send_message(chat_id=user_id, text=text, reply_markup=kb)


def get_withdraw_user_info(text):
    match = re.search(r"\(id:\s*(\d+)\)", text)
    user_id = match.group(1) if match else None

    match = re.search(r"купу грошей:\s*([\d.]+)", text)
    amount = match.group(1) if match else None

    match = re.search(r"Token_id:\s*(\d+)", text)
    token_id = match.group(1) if match else None

    match = re.search(r"Token_price:\s*([\d.]+)", text)
    token_price = match.group(1) if match else None

    return int(user_id), int(token_id), float(amount), int(token_price)
