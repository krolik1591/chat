from aiocryptopay import AioCryptoPay
from aiogram import Router, exceptions, types
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.states import Menu, StateKeys
from bot.menus.wallet_menus.crypto_pay_menus import crypto_pay_menu
from bot.tokens import tokens
from bot.tokens.CryptoPay import CryptoPay
from bot.tokens.token_ton import ton_token

router = Router()


@router.callback_query(Text("crypto_pay"))
async def crypro_pay(call: types.CallbackQuery, state: FSMContext):
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

    tokens_ = tokens.TOKENS.values()
    prices = {token.token_id: round(await token.from_gametokens(deposit_amount), 5) for token in tokens_}

    # for token in tokens_:
    #     print(token.token_id)
    #     print(await token.from_gametokens(deposit_amount))

    last_msg_id = (await state.get_data()).get(StateKeys.LAST_MSG_ID)
    text, keyboard = crypto_pay_menu(deposit_amount, prices)
    try:
        await state.bot.edit_message_text(text, message.from_user.id, last_msg_id, reply_markup=keyboard)
    except exceptions.TelegramBadRequest as e:
        print("User enter the same deposit amount", e)





@router.callback_query(Text(startswith="crypto_pay_"))
async def crypro_pay(call: types.CallbackQuery, state: FSMContext):
    payment_coin = call.data.removeprefix('crypto_pay_')
    await state.update_data({StateKeys.PAYMENT_COIN: payment_coin})

    # crypto_pay: AioCryptoPay = state.bot.crypto_pay

    text, keyboard = amount_for_crypto_payment_menu(payment_coin)
    await call.message.edit_text(text, reply_markup=keyboard)
