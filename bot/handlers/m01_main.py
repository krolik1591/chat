from pprint import pprint

from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

import bot.db.methods as db
from bot.const import START_POINTS
from bot.menus import main_menu
from bot.menus.deposit_menu import deposit_menu
from bot.ton.api import Api
from bot.ton.wallets import Wallets

flags = {"throttling_key": "default"}
router = Router()


@router.message(commands="start", flags=flags)
async def cmd_start(message: Message, state: FSMContext):
    try:
        await db.get_user_lang(message.from_user.id)
    except ValueError:
        await db.create_new_user(message.from_user.id)
        await db.update_username(message.from_user.id, message.from_user.username)
        await db.deposit_token(message.from_user.id, 1, START_POINTS)  # add demo

    balances = await db.get_user_balances(message.from_user.id)
    text, keyboard = main_menu(balances)
    msg = await message.answer(text, reply_markup=keyboard)
    await state.update_data(last_msg_id=msg.message_id)


@router.callback_query(text=["main_menu"])
async def back_to_main(call: types.CallbackQuery, state: FSMContext):
    balances = await db.get_user_balances(call.from_user.id)
    text, keyboard = main_menu(balances)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(text=["deposit"])
async def deposit_menus(call: types.CallbackQuery, state: FSMContext):
    balances = await db.get_user_balances(call.from_user.id)
    text, keyboard = deposit_menu(balances)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(text="ton")
async def ton(message: Message, state: FSMContext):
    wallets = Wallets(wallet_seed="water wish artist boss random burst entry assault size "
                                  "february equal inner satoshi wire camp reason throw "
                                  "allow chapter dose gym jungle vibrant truth")
    await wallets.init()
    wallet = await wallets.get_wallet(message.from_user.id)
    wallet.get_balance, wallet.get_transaction
    await message.answer(wallet.address)


@router.message(commands="ton_check", flags=flags)
async def ton_check(message: Message, state: FSMContext):
    #todo 2 arg token to .env, 24 words tuda je, 1 arg toje
    api = Api('https://testnet.toncenter.com/api/v2' ,'621699dde4b908a9d5c98ab16a887e9348ed3a05afe44a32bf8e6244f7a2bde0')
    last_tx = await db.get_last_transaction(message.from_user.id, 2)
    res = await api.get_address_transactions('EQDLmQypksMNktrdskBEiSF_9oxvwxVIS1IO__K4IqTczUco',
                                             last_tx.tx_hash, last_tx.logical_time)

    user_data = await state.get_data()
    token_id = user_data.get('token_id')
    value = res[0]['in_msg']['value']
    print(token_id)
    # await db.update_user_balance(message.from_user.id, token_id, value)

    #todo закинуть на баланс юзеру, сохранить эту транзу. проверить, что пришло с кошелька юзера (destination == 1 arg)
    #+с кошеля юзера закинуть (ВСЕ ДЕНЬГИ) на мастер кошель (wallets.py transfer).
    pprint(res)
