from ton import TonlibClient


class Wallets:
    def __init__(self, wallet_seed: str):
        self.wallet_seed = wallet_seed
        self.client = TonlibClient()
        TonlibClient.enable_unaudited_binaries()
        await self.client.init_tonlib()

    async def get_wallet(self, wallet_id: int):
        return await self.client.import_wallet(self.wallet_seed, wallet_id=wallet_id)

    async def transfer(self, wallet_id: int, to_address: str):
        pass
        # todo
