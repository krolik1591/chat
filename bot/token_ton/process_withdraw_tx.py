import asyncio

from bot.db import db, manager
from bot.token_ton import TonWrapper


async def process_withdraw_tx(user_withdraw_address, withdraw_amount_ton, user_id, master_wallet_address):
    await asyncio.sleep(25)  # TODO why

    withdraw_amount_nano = withdraw_amount_ton * 1e9

    all_tx = await TonWrapper.INSTANCE.get_transactions(master_wallet_address)
    for tx in all_tx:
        for out_msg in tx.out_msgs:

            is_same_tx = out_msg.destination == user_withdraw_address and \
                         out_msg.source == master_wallet_address and \
                         int(out_msg.value) == int(withdraw_amount_nano)

            if is_same_tx:
                last_manual_tx = await db.get_last_manual_transaction(user_id, token_id=2)

                with manager.pw_database.atomic():
                    await db.add_new_transaction(user_id, token_id=2, amount=withdraw_amount_nano, tx_type=3,
                                                 tx_address=user_withdraw_address, tx_hash=tx.hash,
                                                 logical_time=tx.lt, utime=tx.utime)
                    await db.update_manual_withdraw_state(last_manual_tx['ManualTXs_id'], 'approved')

                return True

    return False
