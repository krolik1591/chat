import os
import pathlib
import shutil

from ton import TonlibClient

libpath = pathlib.Path(__file__).parent / 'libtonlibjson.so.0.5'

wallets = None

class Wallets:
    def __init__(self, wallet_seed: str, config, ls_index):
        self.wallet_seed = wallet_seed
        self.client = TonlibClient(config=config, ls_index=ls_index)

    async def init(self):
        await self.client.init_tonlib(cdll_path=libpath)

    async def get_wallet(self, wallet_id: int):
        return await self.client.import_wallet(self.wallet_seed, wallet_id=wallet_id)

    async def transfer(self, wallet_id: int, to_address: str, amount: int):
        sender_wallet = await self.get_wallet(wallet_id)

        return await sender_wallet.transfer(to_address, amount)


async def create_wallets(wallet_seed, config='https://ton.org/testnet-global.config.json'):
    print('HI FROM WALLETS SUKA')
    global wallets
    wallets = Wallets(wallet_seed, config)
    await wallets.init()
    return wallets


if __name__ == "__main__":




    async def test():
        for i in range(32):
            wallets = Wallets(wallet_seed="water wish artist boss random burst entry assault size "
                                          "february equal inner satoshi wire camp reason throw "
                                          "allow chapter dose gym jungle vibrant truth",config='https://ton.org/testnet-global.config.json', ls_index=i)
            await wallets.init()
            wallet = await wallets.get_wallet(357108179)

            try:
                await wallet.get_transactions(1677618345, 'p0V7nfdmNjmhFcd5uxqWwH+pghYdTGQvp2tYVhKTErc=')
            except:
                print(i, 'is not working')
                pass


        print(wallet.address)


    import asyncio

    asyncio.run(test())

    file_to_rem = pathlib.Path("./.keystore")
    shutil.rmtree(file_to_rem)
