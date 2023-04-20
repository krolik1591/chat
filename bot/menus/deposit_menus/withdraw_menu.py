from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.const import MIN_WITHDRAW
from bot.texts import WITHDRAW_APPROVE, WITHDRAW_MENU_TEXT3, WITHDRAW_MENU_TEXT2, WITHDRAW_MENU_TEXT1, \
    WITHDRAW_MANUAL_TX, PAYMENT_CONFIRMED, PAYMENT_DENIED


def input_amount(token_price):
    ton_amount = MIN_WITHDRAW / token_price
    text = WITHDRAW_MENU_TEXT1.format(min_withdraw=MIN_WITHDRAW, ton_amount=ton_amount)
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Мій гаманець', callback_data="deposit")
    ]])

    return text, kb


def input_address():
    text = WITHDRAW_MENU_TEXT2.format()
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Назад', callback_data="withdraw")
    ]])

    return text, kb


def input_validation(user_withdraw_amount, user_withdraw_address, token_price):
    user_withdraw_amount_ton = round(user_withdraw_amount / token_price, 4)
    text = WITHDRAW_MENU_TEXT3.format(user_withdraw_amount=user_withdraw_amount,
                                      user_withdraw_address=user_withdraw_address,
                                      user_withdraw_amount_ton=user_withdraw_amount_ton)
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


def admin_manual_tx(user_id, username, ton_amount, id_new_tx):
    text = WITHDRAW_MANUAL_TX.format(user_id=user_id, username=username, ton_amount=ton_amount)
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='✅ Approve', callback_data=f"approve_manual_tx_{id_new_tx}"),
        InlineKeyboardButton(text='❌ Denied', callback_data=f"denied_manual_tx_{id_new_tx}")
    ]])

    return text, kb


def withdraw_result(is_ok):
    if is_ok:
        text = PAYMENT_CONFIRMED.format()  # round_user_withdraw < MIN_WITHDRAW
    else:
        text = PAYMENT_DENIED.format()  # user balance < MIN_WITHDRAW

    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='OK', callback_data="delete_replenish_message")
    ]])

    return text, kb
