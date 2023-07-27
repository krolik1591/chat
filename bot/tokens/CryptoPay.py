import time

from aiocryptopay import AioCryptoPay, Networks

from bot.consts.const import TTL


class CryptoPay:
    INSTANCE: 'CryptoPay' = None

    def __init__(self, token):
        self.crypto_pay = AioCryptoPay(token=token, network=Networks.MAIN_NET)
        self.prices = {}
        self.last_prices_update_time = 0

    async def get_invoices(self, last_invoice_id):
        all_invoices = []
        while True:
            invoices = await self.crypto_pay.get_invoices(count=1000, offset=len(all_invoices), status='paid') or []
            invoices = list(reversed(invoices))
            if not invoices:
                break
            index = index_of_first(invoices, lambda x: x.invoice_id == last_invoice_id)
            if index is not None:
                if index == len(invoices) - 1:
                    return []
                invoices = invoices[index + 1:]
                all_invoices.extend(invoices)
                break
            all_invoices.extend(invoices)
        return all_invoices

    async def get_price(self, coin):
        if time.time() > self.last_prices_update_time + TTL:
            self.last_prices_update_time = time.time()
            self.prices = await self._get_prices()
        return self.prices[coin]

    async def _get_prices(self):
        prices = await self.crypto_pay.get_exchange_rates()
        return {price.source: price.rate for price in prices if price.target == "USD"}


def index_of_first(lst, pred):
    for i, v in enumerate(lst):
        if pred(v):
            return i
    return None


if __name__ == '__main__':
    import asyncio

    async def hui():
        crypto_pay = CryptoPay('110852:AAdW7LmeecnXfR5vJNlhkSf0ph3fHLBz8dq')

        x = await crypto_pay.get_price('TON')
        print(x)
    asyncio.run(hui())
