from aiocryptopay import AioCryptoPay
from aiogram import Router, exceptions, types
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.consts.const import DEPOSIT_COMMISSION_CRYPTO_BOT
from bot.handlers.states import Menu, StateKeys
from bot.menus.wallet_menus.crypto_pay_menus import crypto_pay_menu, get_link_to_deposit_menu
from bot.tokens import tokens
from bot.tokens.CryptoPay import CryptoPay
from bot.tokens.token_ton import ton_token

router = Router()


@router.callback_query(Text("crypto_pay"))
async def crypto_pay_enter_amount(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Menu.enter_deposit_amount)

    text, keyboard = crypto_pay_menu()
    await call.message.edit_text(text, reply_markup=keyboard)


@router.message(StateFilter(Menu.enter_deposit_amount))
async def enter_deposit_amount(message: Message, state: FSMContext):
    await message.delete()
    deposit_amount = message.text
    if not deposit_amount.isdigit():
        return
    deposit_amount = float(deposit_amount)
    await state.update_data({StateKeys.ENTERED_DEPOSIT_AMOUNT: deposit_amount})

    tokens_ = tokens.TOKENS.values()
    prices = {}
    for token in tokens_:
        if token.token_id == 'btc':
            prices['mBTC'] = await ton_token.from_gametokens(deposit_amount) * 10**6    # convert BTC to mBTC
        else:
            prices[token.token_id.upper()] = await token.from_gametokens(deposit_amount)

    last_msg_id = (await state.get_data()).get(StateKeys.LAST_MSG_ID)
    text, keyboard = crypto_pay_menu(deposit_amount, prices)
    try:
        await state.bot.edit_message_text(text, message.from_user.id, last_msg_id, reply_markup=keyboard)
    except exceptions.TelegramBadRequest as e:
        print("User enter the same deposit amount", e)


@router.callback_query(Text(startswith="crypto_pay_"))
async def get_link_to_dep(call: types.CallbackQuery, state: FSMContext):
    coin_price = call.data.removeprefix('crypto_pay_').split('|')
    coin = coin_price[0]
    if coin == 'mBTC':
        coin = 'BTC'
        price = float(coin_price[1]) / 10**6
    else:
        price = float(coin_price[1])
    deposit_amount = (await state.get_data()).get(StateKeys.ENTERED_DEPOSIT_AMOUNT)

    crypto_pay = CryptoPay.INSTANCE.crypto_pay
    link = (await crypto_pay.create_invoice(asset=coin, payload=call.from_user.id,
                                            amount=price + price / 100 * DEPOSIT_COMMISSION_CRYPTO_BOT)).pay_url

    text, keyboard = get_link_to_deposit_menu(coin, price, link, deposit_amount)
    await call.message.edit_text(text, reply_markup=keyboard)
