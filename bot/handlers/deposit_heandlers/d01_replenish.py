import time
from datetime import datetime
from pprint import pprint

from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

import bot.db.methods as db
from bot.menus.deposit_menus.replenish_menu import replenish_menu
from bot.texts import PRICE
from bot.ton.api import Api
from bot.ton.wallets import Wallets

flags = {"throttling_key": "default"}
router = Router()

@router.callback_query(text=["replenish"])
async def replenish(call: types.CallbackQuery, state: FSMContext):
    wallets = Wallets(wallet_seed="water wish artist boss random burst entry assault size "
                                  "february equal inner satoshi wire camp reason throw "
                                  "allow chapter dose gym jungle vibrant truth")

    await wallets.init()
    wallet = await wallets.get_wallet(call.from_user.id)
    #wallet.get_balance, wallet.get_transaction
    text, keyboard = replenish_menu(wallet.address)
    await call.message.edit_text(text, reply_markup=keyboard)




@router.callback_query(text=["ton_check"])
async def ton_check(call: types.CallbackQuery, state: FSMContext):
    #todo 2 arg token to .env, 24 words tuda je, 1 arg toje
    api = Api('https://testnet.toncenter.com/api/v2' ,'621699dde4b908a9d5c98ab16a887e9348ed3a05afe44a32bf8e6244f7a2bde0')
    last_tx = await db.get_last_transaction(call.from_user.id, 2)
    res = await api.get_address_transactions('EQDLmQypksMNktrdskBEiSF_9oxvwxVIS1IO__K4IqTczUco',
                                             last_tx.tx_hash, last_tx.logical_time)
    pprint(res[-1])

    amount = res[-1]['in_msg']['value'] / 1e9 * PRICE
    token_id = 2
    tx_type = 1
    tx_address = res[-1]['in_msg']['source']
    tx_hash = res[-1]['transaction_id']['hash']
    await db.update_user_balance(call.from_user.id, token_id, amount)
    await db.add_new_transaction(call.from_user.id, token_id, amount, tx_type, tx_address, tx_hash, int(time.time()))

    #todo закинуть на баланс юзеру, сохранить эту транзу. проверить, что пришло с кошелька юзера (destination == 1 arg)
    #+с кошеля юзера закинуть (ВСЕ ДЕНЬГИ) на мастер кошель (wallets.py transfer).
