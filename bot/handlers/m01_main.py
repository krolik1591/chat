from TonTools.Contracts.Wallet import Wallet
from aiogram import F, Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from bot.const import START_POINTS
from bot.db import db
from bot.handlers.states import Menu, StateKeys
from bot.menus import main_menu, wallet_menus
from bot.tokens.token_ton import TonWrapper
from bot.utils.config_reader import config

flags = {"throttling_key": "default"}
router = Router()


@router.message(F.chat.type == "private", commands="start", flags=flags)
async def cmd_start(message: Message, state: FSMContext):
    try:
        await db.get_user_lang(message.from_user.id)
    except ValueError:
        await db.create_new_user(message.from_user.id, message.from_user.username)
        await db.deposit_token(message.from_user.id, 1, START_POINTS)  # add demo
        await db.deposit_token(message.from_user.id, 2, 0)  # add token_ton

        new_wallet = Wallet(provider=TonWrapper.INSTANCE)
        mnemonics = ','.join(new_wallet.mnemonics)
        await db.create_user_wallet(message.from_user.id, new_wallet.address, mnemonics)

    balances = await db.get_user_balances(message.from_user.id)
    text, keyboard = main_menu(balances)
    msg = await message.answer(text, reply_markup=keyboard)

    await state.update_data(**{StateKeys.LAST_MSG_ID: msg.message_id})
    await state.set_state(Menu.delete_message)


@router.callback_query(text=["main_menu"])
async def back_to_main(call: types.CallbackQuery, state: FSMContext):
    balances = await db.get_user_balances(call.from_user.id)
    text, keyboard = main_menu(balances)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(text=["wallet_menu"])
async def wallet_menu_handler(call: types.CallbackQuery, state: FSMContext):
    balances = await db.get_user_balances(call.from_user.id)

    TOKEN_ID = 2
    token = await db.get_token_by_id(TOKEN_ID)

    text, keyboard = wallet_menus.wallet_menu(balances, token.price)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.message(commands="admin", flags=flags)
async def admin_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    is_admin = str(user_id) in config.admin_ids


@router.message(state=Menu.delete_message)
async def delete_message(message: Message, state: FSMContext):
    await message.delete()
    return
