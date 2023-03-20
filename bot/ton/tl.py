from ton.tl.base import TLObject


class BlockLookup(TLObject):
    def __init__(self, workchain, shard, seqno=None, lt=None, unixtime=None):
        assert (seqno is not None) or (lt is not None) or (
                unixtime is not None), "Seqno, LT or unixtime should be defined"
        mode = 0
        if seqno is not None:
            mode += 1
        if lt is not None:
            mode += 2
        if unixtime is not None:
            mode += 4

        self.type = 'blocks.lookupBlock'
        self.mode = mode
        self.lt = lt
        self.utime = unixtime
        self.id = BlockId(workchain, shard, seqno)


class BlockId(TLObject):
    def __init__(self, workchain, shard, seqno=None):
        self.type = 'ton.blockId'
        self.workchain = workchain
        self.shard = shard
        self.seqno = seqno


class Blocks_GetTransaction(TLObject):
    def __init__(self, fullblock, count, after_tx):
        self.type = 'blocks.getTransactions'
        self.id = fullblock
        self.mode = 7 if not after_tx else 7 + 128
        self.count = count
        self.after = after_tx


class Blocks_AccountTransactionId(TLObject):
    def __init__(self, after_hash=None,  after_lt=None):
        self.type = 'blocks.accountTransactionId'
        self.account = after_hash if after_hash else 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='
        self.lt = after_lt if after_lt else 0


class Blocks_GetMasterchainInfo(TLObject):
    def __init__(self):
        self.type = 'blocks.getMasterchainInfo'
