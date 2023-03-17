from pprint import pprint

from TonTools import *
from TonTools.Contracts.Wallet import Wallet
from TonTools.Providers.LsClient import LsClient
from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext

from bot.db.methods import create_user_wallet, get_user_wallet
from bot.menus.deposit_menus.replenish_menu import replenish_menu

from bot.utils.config_reader import config

flags = {"throttling_key": "default"}
router = Router()


@router.callback_query(text=["replenish"])
async def replenish(call: types.CallbackQuery, state: FSMContext):
    user_wallet = await get_user_wallet(call.from_user.id)

    text, keyboard = replenish_menu(user_wallet.address)
    await call.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(text=["ton_check"])
async def ton_check(call: types.CallbackQuery, state: FSMContext):
    # todo 2 arg token to .env, 24 words tuda je, 1 arg toje
    master_wallet_seed = config.wallet_seed.split(' ')
    master_wallet = Wallet(provider=state.bot.ton_client, mnemonics=master_wallet_seed)

    user_wallet_info = await get_user_wallet(call.from_user.id)
    user_mnemonic = user_wallet_info.mnemonic.split(',')
    print(user_mnemonic)

    my_wallet = Wallet(provider=state.bot.ton_client, mnemonics=user_mnemonic)
    user_init_condition = await my_wallet.get_state()
    if user_init_condition == 'uninitialized':
        print('мінус 13 центів сучара')
        await my_wallet.deploy()

    mw_init_condition = await master_wallet.get_state()
    if mw_init_condition == 'uninitialized':
        print('mw not inited')
        non_bounceable_master_wallet_address = Address(master_wallet.address).to_string(True, True, False)
        await my_wallet.transfer_ton(destination_address=non_bounceable_master_wallet_address, amount=0.02)
        await master_wallet.deploy()

    x = await my_wallet.get_transactions()
    pprint(x[0])
    # print(new_wallet.address)

    # wallets = state.bot.wallets
    # wallet = await wallets.get_wallet(call.from_user.id)
    # MASTER_WALLET = await wallets.get_wallet(0)
    # await wallets.transfer(357108179, 'EQAwmioWn9M2qqbtUPjPFY50-0NENZFL2D5Kr_xu8nG5Qswm', 1000000000)
    # # print(wallet, MASTER_WALLET)
    #
    # last_tx = await db.get_last_transaction(call.from_user.id, 2)
    #
    # res = await wallet.get_transactions(last_tx.logical_time, last_tx.tx_hash)
    # pprint(res)
    # print(MASTER_WALLET.address)
    # token = await db.get_token_by_id(2)
    # token_id = 2
    #
    # for item in res:
    #     amount = int(item.in_msg.value) / 1e9 * token.price
    #     value_nano_ton = item.in_msg.value
    #
    #     tx_hash = item.transaction_id.hash
    #     tx_time = item.transaction_id.lt
    #
    #     if str(item.in_msg.destination.account_address) == wallet.address:
    #         # todo с кошеля юзера закинуть (ВСЕ ДЕНЬГИ) на мастер кошель (wallets.py transfer).
    #         tx_type = 1
    #         tx_address = item.in_msg.source.account_address
    #
    #         await wallets.transfer(call.from_user.id, str(MASTER_WALLET.address), int(amount))
    #
    #     elif str(item.in_msg.source) == wallet.address:
    #         tx_address = item.in_msg.destination.account_address
    #         tx_type = 2 if str(item.in_msg.destination) == MASTER_WALLET else 3
    #
    #     else:
    #         raise AssertionError('This should not happen')
    #
    #     with manager.pw_database.atomic():
    #         await db.deposit_token(call.from_user.id, token_id, amount)
    #         await db.add_new_transaction(call.from_user.id, token_id, value_nano_ton, tx_type, tx_address, tx_hash,
    #                                      tx_time)
