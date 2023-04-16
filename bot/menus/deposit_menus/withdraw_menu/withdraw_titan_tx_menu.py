from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.texts import WITHDRAW_TITAN_TX


def process_titan_tx_menu(user_id, username, ton_amount, id_new_tx, token_id, token_price):
    text = WITHDRAW_TITAN_TX.format(user_id=user_id, username=username, ton_amount=ton_amount, token_id=token_id,
                                    token_price=token_price)
    kb = _keyboard(id_new_tx)

    return text, kb


def _keyboard(id_new_tx):
    kb = [
        [
            InlineKeyboardButton(text='✅ Approve', callback_data=f"approve_titan_tx_{id_new_tx}"),
            InlineKeyboardButton(text='❌ Denied', callback_data=f"denied_titan_tx_{id_new_tx}")

        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
