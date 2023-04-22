from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.const import MIN_WITHDRAW
from bot.menus.utils import kb_del_msg
from bot.texts import WITHDRAW_APPROVE, WITHDRAW_MENU_TEXT3, WITHDRAW_MENU_TEXT2, WITHDRAW_MENU_TEXT1, \
    WITHDRAW_MANUAL_TX, PAYMENT_CONFIRMED, PAYMENT_DENIED, ADMIN_APPROVE_TX, WITHDRAW_ERR7
from bot.utils.rounding import round_down


def input_amount(token_price):
    ton_amount = MIN_WITHDRAW / token_price
    text = WITHDRAW_MENU_TEXT1.format(min_withdraw=MIN_WITHDRAW, ton_amount=ton_amount)
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Мій гаманець', callback_data="wallet_menu")
    ]])

    return text, kb


def input_address():
    text = WITHDRAW_MENU_TEXT2.format()
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Назад', callback_data="withdraw")
    ]])

    return text, kb


def input_validation(withdraw_amount, withdraw_address, withdraw_amount_token):
    text = WITHDRAW_MENU_TEXT3.format(user_withdraw_amount=withdraw_amount,
                                      user_withdraw_address=withdraw_address,
                                      user_withdraw_amount_ton=withdraw_amount_token)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✅ Підтвердити', callback_data="withdraw_queued")],
        [InlineKeyboardButton(text='Назад', callback_data="withdraw")]
    ])

    return text, kb


def withdraw_queued(user_withdraw_amount):
    user_withdraw_amount_ton = user_withdraw_amount / 100  # TODO ????
    text = WITHDRAW_APPROVE.format(user_withdraw_amount=user_withdraw_amount,
                                   user_withdraw_amount_ton=user_withdraw_amount_ton)
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='В меню', callback_data="main_menu")
    ]])

    return text, kb


def admin_manual_tx(user_id, username, token_id, withdraw_amount, id_new_tx):
    text = WITHDRAW_MANUAL_TX.format(user_id=user_id, username=username, withdraw_amount=withdraw_amount)

    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='✅ Approve', callback_data=f"approve_manual_tx_{id_new_tx}"),
        InlineKeyboardButton(text='❌ Denied', callback_data=f"denied_manual_tx_{id_new_tx}")
    ]])

    return text, kb


def withdraw_manual_approved(amount):
    amount = round_down(amount, 2)
    text = ADMIN_APPROVE_TX.format(amount=amount)
    return text, kb_del_msg()


def withdraw_manual_rejected():
    text = WITHDRAW_ERR7
    return text, kb_del_msg()


def withdraw_result(is_ok):
    if is_ok:
        text = PAYMENT_CONFIRMED.format()  # round_user_withdraw < MIN_WITHDRAW
    else:
        text = PAYMENT_DENIED.format()  # user balance < MIN_WITHDRAW

    return text, kb_del_msg()

