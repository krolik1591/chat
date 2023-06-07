from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from bot.consts.const import MIN_WITHDRAW
from bot.menus.utils import kb_del_msg
from bot.utils.rounding import round_down


def input_amount(token_price, general_balance):
    ton_amount = MIN_WITHDRAW / token_price
    text = _('WITHDRAW_MENU_TEXT1').format(min_withdraw=MIN_WITHDRAW, ton_amount=ton_amount,
                                           general_balance=general_balance)
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=_('BTN_BACK'), callback_data="wallet_menu")
    ]])

    return text, kb


def input_address():
    text = _('WITHDRAW_MENU_TEXT2').format()
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=_('BTN_BACK'), callback_data="withdraw")
    ]])

    return text, kb


def input_validation(withdraw_amount, withdraw_address, withdraw_amount_token, general_balance):
    text = _('WITHDRAW_MENU_TEXT3').format(user_withdraw_amount=withdraw_amount,
                                           user_withdraw_address=withdraw_address,
                                           user_withdraw_amount_ton=withdraw_amount_token,
                                           general_balance=general_balance)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_('WITHDRAW_MENU_BTN_STEP_3_APPROVE'), callback_data="withdraw_queued")],
        [InlineKeyboardButton(text=_('BTN_BACK'), callback_data="withdraw")]
    ])

    return text, kb


def withdraw_queued(user_withdraw_amount):
    user_withdraw_amount_ton = user_withdraw_amount / 100  # TODO ????
    text = _('WITHDRAW_APPROVE').format(user_withdraw_amount=user_withdraw_amount,
                                        user_withdraw_amount_ton=user_withdraw_amount_ton)
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=_('WITHDRAW_MENU_BTN_STEP_4_TO_MENU'), callback_data="main_menu")
    ]])

    return text, kb


def admin_manual_tx(user_id, username, token_id, withdraw_amount, id_new_tx):
    text = '@{username} (id: {user_id}) хоче вивести купу грошей: {withdraw_amount}.'\
        .format(user_id=user_id, username=username, withdraw_amount=withdraw_amount)

    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='✅ Approve', callback_data=f"approve_manual_tx_{id_new_tx}"),
        InlineKeyboardButton(text='❌ Denied', callback_data=f"denied_manual_tx_{id_new_tx}")
    ]])

    return text, kb


def withdraw_manual_approved(amount):
    amount = round_down(amount, 2)
    text = _('ADMIN_APPROVE_TX').format(amount=amount)
    return text, kb_del_msg()


def withdraw_manual_rejected():
    text = _('ADMIN_REJECT_TX')
    return text, kb_del_msg()


def withdraw_result(is_ok, ton_amount):
    ton_amount = round_down(ton_amount, 2)
    if is_ok:
        text = _('PAYMENT_CONFIRMED').format(ton_amount=ton_amount)  # round_user_withdraw < MIN_WITHDRAW
    else:
        text = _('PAYMENT_DENIED').format(ton_amount=ton_amount)  # user balance < MIN_WITHDRAW

    return text, kb_del_msg()


def withdraw_lost_by_blockchain(ton_amount):
    ton_amount = round_down(ton_amount, 2)

    text = _('PAYMENT_LOST').format(ton_amount=ton_amount)
    return text, kb_del_msg()
