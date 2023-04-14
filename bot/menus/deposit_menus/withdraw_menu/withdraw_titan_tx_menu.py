from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.texts import WITHDRAW_TITAN_TX


def process_titan_tx_menu(user_id, username, ton_amount):
    text = WITHDRAW_TITAN_TX.format(user_id=user_id, username=username, ton_amount=ton_amount)
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='✅ Approve', callback_data="approve_titan_tx"),
            InlineKeyboardButton(text='❌ Decline', callback_data="decline_titan_tx")

        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
