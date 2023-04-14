from TonTools.Contracts.Wallet import Wallet
from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

import bot.db.methods as db
from bot.const import START_POINTS
from bot.handlers.context import Context
from bot.handlers.states import StateKeys
from bot.menus import main_menu
from bot.menus.deposit_menus.deposit_menu import deposit_menu
from bot.titan_tx.process_titan_tx import process_titan_tx

flags = {"throttling_key": "default"}
router = Router()


@router.message(commands="start", flags=flags)
async def cmd_start(message: Message, state: FSMContext):
    try:
        await db.get_user_lang(message.from_user.id)
    except ValueError:
        await db.create_new_user(message.from_user.id, message.from_user.username)
        await db.deposit_token(message.from_user.id, 1, START_POINTS)  # add demo
        await db.deposit_token(message.from_user.id, 2, 0)  # add ton

        new_wallet = Wallet(provider=state.bot.ton_client)
        mnemonics = ','.join(new_wallet.mnemonics)
        await db.create_user_wallet(message.from_user.id, new_wallet.address, mnemonics)

    balances = await db.get_user_balances(message.from_user.id)
    text, keyboard = main_menu(balances)
    msg = await message.answer(text, reply_markup=keyboard)

    await state.update_data(**{StateKeys.LAST_MSG_ID: msg.message_id})


@router.callback_query(text=["main_menu"])
async def back_to_main(call: types.CallbackQuery, state: FSMContext):
    balances = await db.get_user_balances(call.from_user.id)
    text, keyboard = main_menu(balances)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(text=["deposit"])
async def deposit_menus(call: types.CallbackQuery, state: FSMContext):
    balances = await db.get_user_balances(call.from_user.id)

    TOKEN_ID = 2
    token = await db.get_token_by_id(TOKEN_ID)

    text, keyboard = deposit_menu(balances, token.price)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.message(commands="admin", flags=flags)
async def admin_menu(call: types.CallbackQuery, state: FSMContext):
    pass

