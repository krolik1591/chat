import time

from aiocryptopay import AioCryptoPay, Networks

TTL = 30    # sec


class CryptoPay:
    INSTANCE: 'CryptoPay' = None

    def __init__(self, token):
        self.crypto_pay = AioCryptoPay(token=token, network=Networks.MAIN_NET)
        self.prices = {}
        self.last_prices_update_time = 0

    async def get_price(self, coin):
        if time.time() > self.last_prices_update_time + TTL:
            self.last_prices_update_time = time.time()
            self.prices = await self._get_prices()
        return self.prices[coin]

    async def _get_prices(self):
        prices = await self.crypto_pay.get_exchange_rates()
        return {price.source: price.rate for price in prices if price.target == "USD"}


if __name__ == '__main__':
    import asyncio

    async def hui():
        crypto_pay = CryptoPay('110852:AAdW7LmeecnXfR5vJNlhkSf0ph3fHLBz8dq')

        result = {}

        for pisya in await crypto_pay.get_price():
            if pisya.target == 'USD':
                result[pisya.source] = pisya.rate

        print(result)
    asyncio.run(hui())
