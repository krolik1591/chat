import pathlib

from TonTools import *
from ton.tl.functions import Raw_GetTransactions
from ton.tl.types import Internal_TransactionId


libpath = pathlib.Path(__file__).parent / 'libtonlibjson.so.0.5'
keystorepath = str(pathlib.Path(__file__).parent / '.keystore')


class TonWrapper(LsClient):
    INSTANCE: 'TonWrapper' = None

    def __init__(self, ls_index=0, config='https://ton.org/global-config.json', keystore=keystorepath, workchain_id=0,
                 verbosity_level=0, default_timeout=10, addresses_form='user_friendly', master_wallet_mnemon=None):
        super().__init__(ls_index, config, keystore, workchain_id, verbosity_level, default_timeout, addresses_form)
        master_wallet_seed = master_wallet_mnemon.split(' ')
        self.master_wallet = Wallet(provider=self, mnemonics=master_wallet_seed)

    @classmethod
    async def create(cls, config='https://ton.org/global.config.json', master_wallet_mnemon=None, **kwargs):
        if cls.INSTANCE is not None:
            return TonWrapper.INSTANCE

        ton_wrapper = TonWrapper(config=config, default_timeout=10, master_wallet_mnemon=master_wallet_mnemon, **kwargs)
        await ton_wrapper.init_tonlib(cdll_path=libpath)

        cls.INSTANCE = ton_wrapper
        return ton_wrapper

    def get_wallet(self, mnemonics):
        return Wallet(provider=self, mnemonics=mnemonics.split(','))

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

    async def _get_account_transactions(self, account,
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
