import asyncio
import logging
from pprint import pprint

from bot.tokens.CryptoPay import CryptoPay

MINUTE = 3600


async def crypto_bot_tx_watcher():
    while True:
        logging.info("CRYPTO BOT TX WATCHER STARTED")

        crypto_pay = CryptoPay.INSTANCE.crypto_pay
        invoices = await crypto_pay.get_invoices(count=1000, offset=0, status='paid')
        pprint(invoices)
        invoices = await crypto_pay.get_invoices(count=1000, offset=1, status='paid')
        pprint(invoices)

        await asyncio.sleep(MINUTE)



if __name__ == '__main__':

    async def test():
        await crypto_bot_tx_watcher()
        print()


    asyncio.run(test())
