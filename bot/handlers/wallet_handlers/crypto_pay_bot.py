from aiocryptopay import AioCryptoPay
from aiogram import Router, exceptions, types
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.states import Menu, StateKeys
from bot.menus.wallet_menus.crypto_pay_menus import crypto_pay_menu
from bot.tokens import tokens
from bot.tokens.token_ton import ton_token

router = Router()


@router.callback_query(Text("crypto_pay"))
async def crypro_pay(call: types.CallbackQuery, state: FSMContext, replenish_tokens=None):
    await state.set_state(Menu.deposit_amount)

    text, keyboard = crypto_pay_menu(replenish_tokens)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.message(StateFilter(Menu.deposit_amount))
async def enter_replenishment_tokens(message: Message, state: FSMContext):
    await message.delete()
    deposit_amount = message.text
    if not deposit_amount.isdigit():
        return

    crypto_pay: AioCryptoPay = state.bot.crypto_pay
    exchange_rate = await crypto_pay.get_exchange_rates()
    amount_gametokens = await ton_token.to_gametokens(deposit_amount)
    token = await tokens.get_token_by_id("ton")

    await token.get_price()


    last_msg_id = (await state.get_data()).get(StateKeys.LAST_MSG_ID)
    text, keyboard = crypto_pay_menu(deposit_amount)
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
