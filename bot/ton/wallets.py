import pathlib

from TonTools import *

libpath = pathlib.Path(__file__).parent / 'libtonlibjson.so.0.5'


# async def main():
#     # client = TonApiClient()
#
#     # client = TonCenterClient(base_url='http://127.0.0.1:80/')
#
#     client = LsClient(ls_index=0, default_timeout=20,  config='https://ton.org/global.config.json')
#     await client.init_tonlib(cdll_path=libpath)
#
#     new_wallet = Wallet(provider=client, mnemonics=['online', 'become', 'audit', 'false', 'oil', 'bind', 'spend', 'cargo', 'tube', 'beef', 'report', 'dynamic', 'ugly', 'atom', 'next', 'junk', 'alley', 'able', 'foster', 'already', 'chase', 'crazy', 'quality', 'enact'])
#     print(new_wallet.address)
#
#
#
#     print(await new_wallet.get_balance())
#
#     # await new_wallet.deploy()
#     await new_wallet.transfer_ton(destination_address='EQCRtYOB0RjvWEkfIu1e-dhu2V-ikQlRAqGbpu1bV3GHs283', amount=0.0001)
#
#     print(await new_wallet.get_state())  # active
#     print(await new_wallet.get_balance())


async def create_wallets(config='https://ton.org/global.config.json'):
    print('HI FROM WALLETS SUKA WIP')
    ton_client = LsClient(ls_index=0, default_timeout=20, config=config)
    await ton_client.init_tonlib(cdll_path=libpath)

    return ton_client




# if __name__ == '__main__':
#     asyncio.run(main())
