import asyncio
import time

from bot.db import db, manager
from bot.consts.const import INTERVAL_FOR_REJECT_LOST_TX
from bot.menus.wallet_menus.withdraw_menu import withdraw_lost_by_blockchain, withdraw_result
from bot.tokens.token_ton import ton_token
from bot.tokens.token_ton.tx_watcher import set_user_locale_to_i18n


async def find_and_reject_lost_tx(bot):
    while True:
        txs = await db.get_all_pending_tx(time.time() - INTERVAL_FOR_REJECT_LOST_TX)
        for tx in txs:
            with manager.pw_database.atomic():
                await db.update_withdraw_tx_state(tx.withdrawtx_id, 'rejected')
                await db.update_user_balance(tx.user_id, 'general', tx.amount)

            i18n = await set_user_locale_to_i18n(tx.user_id)
            with i18n():
                text, kb = withdraw_lost_by_blockchain(await ton_token.from_gametokens(tx.amount))

            await bot.send_message(tx.user_id, text, reply_markup=kb)

        await asyncio.sleep(350)
