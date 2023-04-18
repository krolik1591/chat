from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.texts import PREVIOUS_MANUAL_TX_IN_PROCESS, WITHDRAW_DAILY_LIMIT, WITHDRAW_ERR1, WITHDRAW_ERR2, \
    WITHDRAW_ERR3, WITHDRAW_ERR4, WITHDRAW_ERR5, WITHDRAW_ERR6, WITHDRAW_ERR7

WITHDRAW_ERR = {
    1: WITHDRAW_ERR1,   # round_user_withdraw < MIN_WITHDRAW
    2: WITHDRAW_ERR2,   # user balance < MIN_WITHDRAW
    3: WITHDRAW_ERR3,   # test.net address
    4: WITHDRAW_ERR4,   # incorrect address
    5: WITHDRAW_ERR5,   # round_user_withdraw > user_balance
    6: WITHDRAW_ERR6,   # end money on master wallet
    7: WITHDRAW_ERR7,    # rejected by admin
    'withdraw_daily_limit': WITHDRAW_DAILY_LIMIT,
    'previous_manual_tx_in_process': PREVIOUS_MANUAL_TX_IN_PROCESS

}


def withdraw_menu_err(err, amount=0):
    if amount <= 0:
        amount = 0
    text = WITHDRAW_ERR[err].format(amount=amount)
    kb = _keyboard()

    return text, kb


def _keyboard():
    kb = [
        [
            InlineKeyboardButton(text='OK', callback_data="delete_replenish_message")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)