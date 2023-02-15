import os
import pathlib
import shutil

from ton import TonlibClient


class Wallets:
    def __init__(self, wallet_seed: str):
        self.wallet_seed = wallet_seed
        self.client = TonlibClient()
        TonlibClient.enable_unaudited_binaries()

    async def init(self):
        await self.client.init_tonlib()

    async def get_wallet(self, wallet_id: int):
        return await self.client.import_wallet(self.wallet_seed, wallet_id=wallet_id)

    async def transfer(self, wallet_id: int, to_address: str):
        pass
        # todo


if __name__ == "__main__":
    wallets = Wallets(wallet_seed="water wish artist boss random burst entry assault size "
                                 "february equal inner satoshi wire camp reason throw "
                                 "allow chapter dose gym jungle vibrant truth")


    async def test():
        await wallets.init()
        wallet = await wallets.get_wallet(1)
        print(wallet.address)

    import asyncio
    asyncio.run(test())

    file_to_rem = pathlib.Path("./.keystore")
    shutil.rmtree(file_to_rem)