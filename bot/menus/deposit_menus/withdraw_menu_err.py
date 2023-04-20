from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.const import MAXIMUM_WITHDRAW, MAXIMUM_WITHDRAW_DAILY, MIN_WITHDRAW
from bot.texts import PREVIOUS_MANUAL_TX_IN_PROCESS, WITHDRAW_DAILY_LIMIT, WITHDRAW_ERR1, WITHDRAW_ERR3, WITHDRAW_ERR4, \
    WITHDRAW_ERR5, WITHDRAW_ERR6, WITHDRAW_ERR7, WITHDRAW_TOO_BIG
from bot.utils.rounding import round_down


def manual_tx_in_process():
    return PREVIOUS_MANUAL_TX_IN_PROCESS, _keyboard()


def reached_daily_limit(allowable_amount):
    allowable_amount = round_down(allowable_amount, 2)
    return WITHDRAW_DAILY_LIMIT.format(allowable_amount=allowable_amount), _keyboard()


def withdraw_too_big(token_price):
    maximum_withdraw_daily_token = MAXIMUM_WITHDRAW_DAILY * token_price
    return WITHDRAW_TOO_BIG.format(
        maximum_withdraw_token=maximum_withdraw_daily_token, maximum_withdraw=MAXIMUM_WITHDRAW), _keyboard()


def withdraw_too_small(token_price):
    ton_amount = MIN_WITHDRAW / token_price
    return WITHDRAW_ERR1.format(min_withdraw=MIN_WITHDRAW, ton_amount=ton_amount), _keyboard()


def withdraw_err_rejected_by_admin():
    return WITHDRAW_ERR7, _keyboard()


def withdraw_err_insufficient_funds_master():
    return WITHDRAW_ERR6, _keyboard()


def withdraw_err_insufficient_funds():
    return WITHDRAW_ERR5, _keyboard()


def withdraw_err_incorrect_address():
    return WITHDRAW_ERR4, _keyboard()


def withdraw_err_testnet_address():
    return WITHDRAW_ERR3, _keyboard()


def _keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='OK', callback_data="delete_replenish_message")
    ]])
