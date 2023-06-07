from aiogram.utils.i18n import gettext as _

from bot.consts.const import MAXIMUM_WITHDRAW_DAILY, MIN_WITHDRAW
from bot.menus.utils import kb_del_msg
from bot.utils.rounding import round_down


def manual_tx_in_process():
    return _('PREVIOUS_WITHDRAW_IN_PROCESS'), kb_del_msg()


def reached_daily_limit(allowable_amount):
    allowable_amount = round_down(allowable_amount, 2)
    return _('REACHED_DAILY_LIMIT').format(allowable_amount=allowable_amount), kb_del_msg()


def withdraw_exceeds_daily_limit(daily_limit_token):
    return _('WITHDRAW_TOO_BIG').format(
        daily_limit_token=daily_limit_token, daily_limit=MAXIMUM_WITHDRAW_DAILY), kb_del_msg()


def withdraw_too_small(token_amount):
    return _('AMOUNT_TOO_SMALL').format(min_withdraw=MIN_WITHDRAW, ton_amount=token_amount), kb_del_msg()


def insufficient_funds_master():
    return _('INSUFFICIENT_FUNDS_MASTER'), kb_del_msg()


def withdraw_err_insufficient_funds():
    return _('INSUFFICIENT_FUNDS'), kb_del_msg()


def withdraw_err_incorrect_address():
    return _('WRONG_ADDRESS'), kb_del_msg()


def withdraw_err_testnet_address():
    return _('TON_TESTNET_ADDRESS'), kb_del_msg()
