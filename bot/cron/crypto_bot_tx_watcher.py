import asyncio
import logging
from pprint import pprint

from bot.consts.const import DEPOSIT_COMMISSION_CRYPTO_BOT, USDT_TO_GAMETOKENS
from bot.db import db, manager
from bot.tokens.CryptoPay import CryptoPay
from bot.tokens.token_ton.tx_watcher import send_successful_deposit_msg, set_user_locale_to_i18n
from bot.tokens.tokens import TOKENS
from bot.utils.rounding import round_down

MINUTE = 60


async def crypto_bot_tx_watcher(bot, i18n):
    while True:
        logging.info("CRYPTO BOT TX WATCHER STARTED")
        crypto_pay = CryptoPay.INSTANCE
        last_invoice_id = await db.get_last_crypto_pay_id()
        invoices = await crypto_pay.get_invoices(last_invoice_id)
        for invoice in invoices:
            await process_invoice(bot, i18n, invoice)

        await asyncio.sleep(MINUTE/3)


async def process_invoice(bot, i18n, invoice):
    logging.info(f'Process invoice {invoice.invoice_id} in crypto bot tx watcher start')
    payload = invoice.payload.split('|')
    user_id = int(payload[0])
    game_tokens_to_deposit = float(payload[1])
    token_id = invoice.asset.lower()

    if token_id not in TOKENS:
        logging.info(f"Crypto pay token {token_id} not in TOKENS")
        return

    token = TOKENS[token_id]
    promo_code = await db.need_a_bonus(user_id)

    with manager.pw_database.atomic():
        if promo_code:
            promo_bonus = game_tokens_to_deposit * promo_code.promocode.bonus / 100
            await db.update_user_balance(user_id, 'promo', promo_bonus)
            await db.update_wagers_and_bonus(user_id, promo_bonus, promo_code)

        await db.update_user_balance(user_id, 'general', round_down(game_tokens_to_deposit, 5))
        await db.add_new_crypto_pay_tx(user_id, token_id, invoice.amount * 10 ** 9, invoice.invoice_id,
                                       invoice.paid_at.timestamp())

    try:
        await set_user_locale_to_i18n(user_id, i18n)
        await send_successful_deposit_msg(bot, user_id, round(game_tokens_to_deposit, 2))
    except ValueError:
        print('User from crypto bot tx watcher not found in db')


if __name__ == '__main__':

    async def test():
        await crypto_bot_tx_watcher()
        print()


    asyncio.run(test())
