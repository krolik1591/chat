import asyncio

from bot.db import db, manager
from bot.tokens.token_ton import TonWrapper


async def find_withdraw_tx(user_withdraw_address, withdraw_amount_ton, user_id):
    await asyncio.sleep(25)  # TODO why

    withdraw_amount_nano = withdraw_amount_ton * 1e9
    found_tx = await find_withdraw_tx_(user_withdraw_address, withdraw_amount_nano)
    if found_tx is None:
        return False

    last_manual_tx = await db.get_last_withdraw_transaction(user_id, token_id="ton")

    with manager.pw_database.atomic():
        await db.add_new_transaction(
            user_id=user_id,
            token_id="ton",
            amount=withdraw_amount_nano,
            tx_type=3,  # withdraw
            tx_address=user_withdraw_address,
            tx_hash=found_tx.hash,
            logical_time=found_tx.lt,
            utime=found_tx.utime)
        await db.update_withdraw_tx_state(last_manual_tx.withdrawtx_id, 'success')

    return True


async def find_withdraw_tx_(user_withdraw_address, withdraw_amount_nanoton):
    master_wallet_address = TonWrapper.INSTANCE.master_wallet.address
    all_tx = await TonWrapper.INSTANCE.get_transactions(master_wallet_address)  # todo why not get_account_transactions?

    for tx in all_tx:
        for out_msg in tx.out_msgs:

            is_same_tx = out_msg.destination == user_withdraw_address and \
                         out_msg.source == master_wallet_address and \
                         int(out_msg.value) == int(withdraw_amount_nanoton)

            if is_same_tx:
                return tx
