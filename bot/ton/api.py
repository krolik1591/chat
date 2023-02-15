from pprint import pprint

import aiohttp


class Api:
    def __init__(self, api_base, token):
        self.api_base = api_base
        self.token = token


    async def get_address_transactions(self, address, hash_=None, lt=None):
        params = {
            "address": address,
            "limit": 30,
            "archival": 'true',
        }
        if hash_ is not None:
            params['hash'] = hash_
        if lt is not None:
            params['lt'] = lt
        return await self._api("getTransactions", params)

    async def _api(self, method, params):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_base}/{method}", params={**params, "api_key": self.token}) as r:
                r.raise_for_status()
                response = await r.json()
                return response['result']

if __name__ == "__main__":
    api = Api('https://testnet.toncenter.com/api/v2' ,'621699dde4b908a9d5c98ab16a887e9348ed3a05afe44a32bf8e6244f7a2bde0')


    async def test():
        pprint(await api.get_address_transactions('EQDnV_p8jmDZgj7lFetCctUrEAss8Xdv3x-MZwiZqJHNFnQw'))


    import asyncio
    asyncio.run(test())
