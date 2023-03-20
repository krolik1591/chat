import pathlib
from pprint import pprint

from TonTools import *
from ton.tl.functions import Raw_GetTransactions
from ton.tl.types import Internal_TransactionId

from bot.db import methods as db, first_start

libpath = pathlib.Path(__file__).parent / 'libtonlibjson.so.0.5'


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

        account = await self.find_account(address, preload_state=False)
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


if __name__ == '__main__':
    async def test():
        # як зрозуміти шо в юзера є нова транза

        await first_start()
        ton_wrapper = await TonWrapper.create()

        account = await ton_wrapper.find_account('EQDM703pKa70fP1G9MTNHt40hMekSRuMTmM6pmcizl49xnOr')

        last_tx_from_blockchain = account.state.last_transaction_id

        last_tx_from_db = await db.get_last_transaction(1, 2)  # типу беремо з бд

        # last_tx_from_db.tx_hash зараз None.  спробуй розкоментити шось з цього шоб отримати інший результат

        # last_tx_from_db.tx_hash = 'piMvJgACp7qH6HqWFC3m3Vlv2vuQiMv7q93s4DpFd68='  # нема нових
        # last_tx_from_db.tx_hash = 'Cp1TXEm3Pw05UZJjB5Xk6ZaHIrVn5VUL4CBRdrbuVeE='  # є одна нова


        if last_tx_from_blockchain.hash != last_tx_from_db.tx_hash:
            print("NEW TX!")
            # добуваємо нові транзи

            pprint(await ton_wrapper.get_account_transactions(
                account.address,
                last_tx_lt=last_tx_from_blockchain.lt,
                last_tx_hash=last_tx_from_blockchain.hash,
                first_tx_hash=last_tx_from_db.tx_hash)
                   )
        else:
            print("NO NEW TX :(")
        await ton_wrapper.tonlib_wrapper.close()


    async def test2():
        # як юзати get_account_transactions
        ton_wrapper = await TonWrapper.create()
        print('---------Всі транзи кошелю---------')
        pprint(await ton_wrapper.get_account_transactions('EQDM703pKa70fP1G9MTNHt40hMekSRuMTmM6pmcizl49xnOr'))
        print('---------Транзи починаючі з тої де кошель перевів 100000 на мастер воллет (не включно) ---------')
        pprint(await ton_wrapper.get_account_transactions('EQDM703pKa70fP1G9MTNHt40hMekSRuMTmM6pmcizl49xnOr',
                                                          first_tx_lt=36181412000001))


    asyncio.run(test())
