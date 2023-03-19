import pathlib
from pprint import pprint

from TonTools import *

libpath = pathlib.Path(__file__).parent / 'libtonlibjson.so.0.5'

# master workchain; master shard
workchain, shard = -1, -9223372036854775808


class TonWrapper (LsClient):

    @classmethod
    async def create(cls, config='https://ton.org/global.config.json', **kwargs):
        ton_wrapper = cls(config=config, **kwargs)
        await ton_wrapper.init_tonlib(cdll_path=libpath)
        return ton_wrapper

    async def get_block_transactions(self, block):
        return await self._get_block_transactions(workchain, shard, block)

    async def _get_block_transactions(self, workchain, shard, seqno):

        fullblock = (await self.lookup_block(workchain, shard, seqno)).to_json()
        after_tx = {
            '@type': 'blocks.accountTransactionId',
            'account': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=',  # after_hash is None
            'lt': 0
        }
        total_result = []

        while True:
            result = await self._raw_get_block_transactions(fullblock, 256, after_tx)
            total_result += result.transactions

            if not result.incomplete:
                break

            after_tx['account'] = result.transactions[-1].account
            after_tx['lt'] = result.transactions[-1].lt

        return total_result

    async def _raw_get_block_transactions(self, fullblock, count, after_tx):
        request = {
            '@type': 'blocks.getTransactions',
            'id': fullblock,
            'mode': 7 if not after_tx else 7+128,
            'count': count,
            'after': after_tx
        }
        return await self.tonlib_wrapper.execute(request, timeout=self.default_timeout)

    async def lookup_block(self, workchain, shard, seqno=None, lt=None, unixtime=None):
        assert (seqno is not None) or (lt is not None) or (unixtime is not None), "Seqno, LT or unixtime should be defined"
        mode = 0
        if seqno is not None:
            mode += 1
        if lt is not None:
            mode += 2
        if unixtime is not None:
            mode += 4

        request = {
            '@type': 'blocks.lookupBlock',
            'mode': mode,
            'id': {
                '@type': 'ton.blockId',
                'workchain': workchain,
                'shard': shard,
                'seqno': seqno
            },
            'lt': lt,
            'utime': unixtime
        }
        return await self.tonlib_wrapper.execute(request, timeout=self.default_timeout)



if __name__ == '__main__':
    async def test():
        ton_wrapper = await TonWrapper.create()
        pprint(await ton_wrapper.get_block_transactions(28192395))
        await ton_wrapper.tonlib_wrapper.close()



    asyncio.run(test())