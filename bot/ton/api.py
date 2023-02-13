import aiohttp


class Api:
    def __init__(self, api_base, token):
        self.api_base = api_base
        self.token = token

    async def get_address_transactions(self, address):
        # todo
        return await self._api("getTransactions", {
            "address": address,
            "limit": 30,
            "archival": True
        })

    async def _api(self, method, params):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_base}/{method}", params={**params, "api_key": self.token}) as r:
                r.raise_for_status()
                response = await r.json()
                return response['result']
