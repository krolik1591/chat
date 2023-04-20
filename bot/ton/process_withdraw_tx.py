import asyncio

from bot.db import manager
from bot.db.methods import add_new_transaction, get_last_manual_transaction, update_manual_withdraw_state
from bot.handlers.states import StateKeys
from bot.ton.wallets import TonWrapper


async def process_withdraw_tx(state, user_withdraw_address, withdraw_amount_ton, user_id, master_wallet_address):
    await asyncio.sleep(25)

    withdraw_amount_nano = withdraw_amount_ton * 1e9

    ton_client: TonWrapper = state.bot.ton_client
    all_tx = await ton_client.get_transactions(master_wallet_address)
    for tx in all_tx:
        for out_msg in tx.out_msgs:
            if out_msg.destination == user_withdraw_address and out_msg.source == master_wallet_address and int(out_msg.value) == int(withdraw_amount_nano):
                token_id = (await state.get_data()).get(StateKeys.TOKEN_ID)
                last_manual_tx = await get_last_manual_transaction(user_id, token_id)

                with manager.pw_database.atomic():
                    await add_new_transaction(user_id, token_id=2, amount=withdraw_amount_nano, tx_type=3,
                                              tx_address=user_withdraw_address, tx_hash=tx.hash,
                                              logical_time=tx.lt, utime=tx.utime)

                    await update_manual_withdraw_state(last_manual_tx['ManualTXs_id'], 'approved')
                    return True
    return False
