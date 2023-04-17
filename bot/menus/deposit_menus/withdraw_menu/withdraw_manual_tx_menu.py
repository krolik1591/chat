from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.texts import WITHDRAW_MANUAL_TX


def process_manual_tx_menu(user_id, username, ton_amount, id_new_tx):
    text = WITHDRAW_MANUAL_TX.format(user_id=user_id, username=username, ton_amount=ton_amount)
    kb = _keyboard(id_new_tx)

    return text, kb


def _keyboard(id_new_tx):
    kb = [
        [
            InlineKeyboardButton(text='✅ Approve', callback_data=f"approve_manual_tx_{id_new_tx}"),
            InlineKeyboardButton(text='❌ Denied', callback_data=f"denied_manual_tx_{id_new_tx}")

        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
