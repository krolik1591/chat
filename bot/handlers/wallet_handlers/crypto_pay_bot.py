from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from bot.handlers.states import StateKeys
from bot.menus.wallet_menus.crypto_pay_menus import crypto_pay_menu

router = Router()


@router.callback_query(Text("crypto_pay"))
async def crypro_pay(call: types.CallbackQuery, state: FSMContext):
    text, keyboard = crypto_pay_menu(None)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(Text(startswith="crypto_pay_"))
async def crypro_pay(call: types.CallbackQuery, state: FSMContext):
    payment_coin = call.data.removeprefix('crypto_pay_')
    await state.update_data({StateKeys.PAYMENT_COIN: payment_coin})

    # crypto_pay: AioCryptoPay = state.bot.crypto_pay

    text, keyboard = amount_for_crypto_payment_menu(payment_coin)
    await call.message.edit_text(text, reply_markup=keyboard)
