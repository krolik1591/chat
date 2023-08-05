from aiogram import Router, types
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from bot.handlers.states import Menu, StateKeys
from bot.menus.wallet_menus.crypto_pay_menus import crypto_pay_menu, get_link_to_deposit_menu, \
    warning_about_optimized_buy_gametoken
from bot.tokens import tokens
from bot.tokens.CryptoPay import CryptoPay

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

    previous_amount = (await state.get_data()).get(StateKeys.ENTERED_DEPOSIT_AMOUNT)
    if previous_amount == deposit_amount:
        return

    await state.update_data({StateKeys.ENTERED_DEPOSIT_AMOUNT: deposit_amount})

    tokens_ = tokens.TOKENS.values()
    prices = {token.token_id.upper(): await token.from_gametokens_with_fees(deposit_amount) for token in tokens_}

    last_msg_id = (await state.get_data()).get(StateKeys.LAST_MSG_ID)
    text, keyboard = crypto_pay_menu(deposit_amount, prices, deposit_amount)
    await state.bot.edit_message_text(text, message.from_user.id, last_msg_id, reply_markup=keyboard)


@router.callback_query(Text(startswith="crypto_pay_"))
async def get_link_to_dep(call: types.CallbackQuery, state: FSMContext):
    coin_name_and_amount = call.data.removeprefix('crypto_pay_').split('|')
    coin_name = coin_name_and_amount[0]

    desired_gametokens_amount = (await state.get_data()).get(StateKeys.ENTERED_DEPOSIT_AMOUNT)

    token = tokens.TOKENS[coin_name.lower()]
    min_dep_token_amount = await token.token_min_dep()
    gametoken_min_dep = await token.to_gametokens(min_dep_token_amount)
    token_min_dep_with_fees = await token.from_gametokens_with_fees(gametoken_min_dep)

    if desired_gametokens_amount < gametoken_min_dep:
        await call.answer(_("CRYPTO_PAY_BOT_REPLENISH_ERR_MIN_DEPOSIT").format(
            min_dep_token_amount=round(token_min_dep_with_fees, 5), coin=coin_name,
            min_dep_gametoken=round(gametoken_min_dep, 2)), show_alert=True)
        return

    if coin_name in ['TON', 'BTC', 'USDT']:
        await state.update_data({StateKeys.TOKEN_NAME_AND_AMOUNT: coin_name_and_amount})
        text, kb = warning_about_optimized_buy_gametoken()
        await call.message.edit_text(text, reply_markup=kb)
        return

    await create_and_send_link(call, token, desired_gametokens_amount, coin_name_and_amount)


@router.callback_query(Text(startswith="dunky_choice_accept"))
async def are_u_sure(call: types.CallbackQuery, state: FSMContext):
    coin_name_and_amount = (await state.get_data()).get(StateKeys.TOKEN_NAME_AND_AMOUNT)
    desired_gametokens_amount = (await state.get_data()).get(StateKeys.ENTERED_DEPOSIT_AMOUNT)
    token = tokens.TOKENS[coin_name_and_amount[0].lower()]

    await create_and_send_link(call, token, desired_gametokens_amount, coin_name_and_amount)


async def create_and_send_link(call, token, desired_gametokens_amount, coin_name_and_amount):
    coin_name = coin_name_and_amount[0]

    payload = str(call.from_user.id) + '|' + str(desired_gametokens_amount)
    crypto_pay = CryptoPay.INSTANCE.crypto_pay
    amount_to_invoice = await token.from_gametokens_with_fees(desired_gametokens_amount)
    link = (await crypto_pay.create_invoice(asset=coin_name, payload=payload, amount=amount_to_invoice)).pay_url

    text, keyboard = get_link_to_deposit_menu(coin_name, amount_to_invoice, link, desired_gametokens_amount)
    await call.message.edit_text(text, reply_markup=keyboard)
