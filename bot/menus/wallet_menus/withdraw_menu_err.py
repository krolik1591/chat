from bot.consts.const import MAXIMUM_WITHDRAW_DAILY, MIN_WITHDRAW
from bot.menus.utils import kb_del_msg
from bot.consts.texts import PREVIOUS_MANUAL_TX_IN_PROCESS, WITHDRAW_DAILY_LIMIT, WITHDRAW_ERR_AMOUNT_TOO_SMALL, WITHDRAW_ERR_TON_TESTNET_ADDRESS, WITHDRAW_ERR_WRONG_ADDRESS, \
    WITHDRAW_ERR_INSUFFICIENT_FUNDS, WITHDRAW_ERR_INSUFFICIENT_FUNDS_MASTER, ADMIN_REJECT_TX, WITHDRAW_TOO_BIG
from bot.utils.rounding import round_down


def manual_tx_in_process():
    return PREVIOUS_MANUAL_TX_IN_PROCESS, kb_del_msg()


def reached_daily_limit(allowable_amount):
    allowable_amount = round_down(allowable_amount, 2)
    return WITHDRAW_DAILY_LIMIT.format(allowable_amount=allowable_amount), kb_del_msg()


def withdraw_exceeds_daily_limit(daily_limit_token):
    return WITHDRAW_TOO_BIG.format(
        daily_limit_token=daily_limit_token, daily_limit=MAXIMUM_WITHDRAW_DAILY), kb_del_msg()


def withdraw_too_small(token_amount):
    return WITHDRAW_ERR_AMOUNT_TOO_SMALL.format(min_withdraw=MIN_WITHDRAW, ton_amount=token_amount), kb_del_msg()


def insufficient_funds_master():
    return WITHDRAW_ERR_INSUFFICIENT_FUNDS_MASTER, kb_del_msg()


def withdraw_err_insufficient_funds():
    return WITHDRAW_ERR_INSUFFICIENT_FUNDS, kb_del_msg()


def withdraw_err_incorrect_address():
    return WITHDRAW_ERR_WRONG_ADDRESS, kb_del_msg()


def withdraw_err_testnet_address():
    return WITHDRAW_ERR_TON_TESTNET_ADDRESS, kb_del_msg()
