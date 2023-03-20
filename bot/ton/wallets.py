import pathlib
from collections import defaultdict
from pprint import pprint

from TonTools import *
from ton.tl.functions import Raw_GetTransactions
from ton.tl.types import Internal_TransactionId
from tonsdk.utils import b64str_to_hex

from bot.ton.tl import BlockLookup, Blocks_GetTransaction, Blocks_AccountTransactionId, Blocks_GetMasterchainInfo

libpath = pathlib.Path(__file__).parent / 'libtonlibjson.so.0.5'

# master workchain; master shard
workchain, shard = -1, -9223372036854775808


class TonWrapper(LsClient):

    @classmethod
    async def create(cls, config='https://ton.org/global.config.json', **kwargs):
        ton_wrapper = cls(config=config, default_timeout=10, **kwargs)
        await ton_wrapper.init_tonlib(cdll_path=libpath)
        return ton_wrapper

    # account tx

    async def get_account_transactions(self, address,
                                       last_tx_lt=None, last_tx_hash=None,
                                       first_tx_lt=0, first_tx_hash=None, include_first_tx=False,
                                       limit=float('Infinity')):

        account = await self.find_account(address)
        # all_txs = await account.get_transactions()
        all_txs = await self._get_account_transactions(account, last_tx_lt, last_tx_hash,
                                                       first_tx_lt, first_tx_hash, include_first_tx, limit)

        results = []

        for outer_tx in all_txs:
            inners_txs = outer_tx.out_msgs + ([outer_tx.in_msg] if hasattr(outer_tx, 'in_msg') else [])

            for tx in inners_txs:
                res = {
                    "destination": tx.destination.account_address,
                    "source": tx.source.account_address,
                    "tx_hash": outer_tx.transaction_id.hash,
                    "tx_lt": outer_tx.transaction_id.lt,
                    "utime": outer_tx.utime,
                    "value": tx.value,
                }
                if res['source'] == '':
                    continue
                results.append(res)

        return results

    async def _get_account_transactions(self, account: Account,
                                        last_tx_lt=None, last_tx_hash=None,
                                        first_tx_lt=0, first_tx_hash=None, include_first_tx=False,
                                        limit=float('Infinity')):
        """
        Return account transactions from newest to oldest
         If `last_tx_lt` AND `last_tx_hash` provided - it will be newest tx in returned list (included)
         If `first_tx_lt` OR `first_tx_hash` provided - it will be oldest tx in returned list (included if `include_first_tx` is True)
        """
        if last_tx_lt is None or last_tx_hash is None:
            state = await account.get_state(force=True)
            tx_id = Internal_TransactionId(state.last_transaction_id.lt, state.last_transaction_id.hash)
        else:
            tx_id = Internal_TransactionId(last_tx_lt, last_tx_hash)

        results = []

        while True:
            request = Raw_GetTransactions(account.account_address, tx_id)
            raw_transactions = await self.tonlib_wrapper.execute(request)

            for tx in raw_transactions.transactions:
                if int(tx.transaction_id.lt) <= first_tx_lt or tx.transaction_id.hash == first_tx_hash:
                    # reached oldest tx, break loop
                    if include_first_tx:
                        results.append(tx)
                    return results

                results.append(tx)

                if len(results) >= limit:
                    return results

            if not hasattr(raw_transactions, "previous_transaction_id"):
                break
            tx_id = raw_transactions.previous_transaction_id
            if int(tx_id.lt) == 0:
                break

        return results

    # block tx

    async def get_block_transactions(self, block):
        return await self._get_block_transactions(workchain, shard, block)

    async def _get_block_transactions(self, workchain, shard, seqno):

        fullblock = await self._lookup_block(workchain, shard, seqno)
        after_tx = Blocks_AccountTransactionId()
        total_result = []

        while True:
            result = await self._raw_get_block_transactions(fullblock, 256, after_tx)
            total_result += result.transactions

            if not result.incomplete:
                break

            after_tx = Blocks_AccountTransactionId(result.transactions[-1].account, result.transactions[-1].lt)

        for tx in total_result:
            tx.account = f"{workchain:d}:{b64str_to_hex(tx.account)}"

        return total_result

    async def _raw_get_block_transactions(self, fullblock, count, after_tx):
        request = Blocks_GetTransaction(fullblock, count, after_tx)
        return await self.tonlib_wrapper.execute(request, timeout=self.default_timeout)

    async def _lookup_block(self, workchain, shard, seqno=None, lt=None, unixtime=None):
        request = BlockLookup(workchain, shard, seqno, lt, unixtime)
        return await self.tonlib_wrapper.execute(request, timeout=self.default_timeout)

    # utils

    async def get_masterchain_info(self):
        return await self.tonlib_wrapper.execute(Blocks_GetMasterchainInfo(), timeout=self.default_timeout)


if __name__ == '__main__':

    async def test():
        ton_wrapper = await TonWrapper.create()

        account = await ton_wrapper.find_account('EQDM703pKa70fP1G9MTNHt40hMekSRuMTmM6pmcizl49xnOr')
        print(await ton_wrapper._get_account_transactions(account))

        await ton_wrapper.tonlib_wrapper.close()


    async def main():
        BLOCK_TIME = 5  # seconds
        MAX_BLOCKS_AT_TIME = 100

        ton_wrapper = await TonWrapper.create()
        last_processed_block = 100

        while True:
            last_block_number = (await ton_wrapper.get_masterchain_info()).last.seqno

            block_from = last_processed_block
            block_to = min(block_from+MAX_BLOCKS_AT_TIME, last_block_number)

            print(f'processing block {block_from=} {block_to=}')
            blocks_txs = await get_txs_from_blocks(ton_wrapper, block_from, block_to)
            print('find', len(blocks_txs), 'txs')
            addresses = await get_addresses_in_txs(ton_wrapper, blocks_txs)
            print(addresses)

            last_processed_block = block_to

            await asyncio.sleep(BLOCK_TIME)

        await ton_wrapper.tonlib_wrapper.close()


    async def get_txs_from_blocks(ton_wrapper, block_from, block_to):
        blocks_txs = []
        for block_num in range(block_from, block_to):
            block_txs = await ton_wrapper.get_block_transactions(block_num)
            blocks_txs.extend(block_txs)
        return blocks_txs

    async def get_addresses_in_txs(ton_wrapper, block_txs):
        results = set()  # hashset (unique values)

        addresses = defaultdict(dict)
        for tx in block_txs:
            addr = addresses[tx.account]
            if 'newest_lt' not in addr or int(tx.lt) > addr['newest_lt']:
                addr['newest_lt'] = int(tx.lt)
                addr['newest_hash'] = tx.hash
            if 'oldest_lt' not in addr or int(tx.lt) < addr['oldest_lt']:
                addr['oldest_lt'] = int(tx.lt)

        print(len(addresses), 'uniq callers in txs')

        for addr, options in addresses.items():
            norm_addr = Address(addr).to_string(True, False, True, False)
            txs = await ton_wrapper.get_account_transactions(
                norm_addr,
                last_tx_hash=options['newest_hash'], last_tx_lt=options['newest_lt'],
                first_tx_lt=options['oldest_lt'], include_first_tx=True
            )
            for tx in txs:
                results.add(tx['source'])
                results.add(tx['destination'])

        return results


    asyncio.run(main())
