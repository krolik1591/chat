import pathlib

from peewee import *
from peewee_aio import Manager

# app/db/db.sqlite3
path = pathlib.Path(__file__).parent.parent.parent / 'db' / 'db.sqlite3'
manager = Manager(f'aiosqlite:////{path}')


class Wallets_key(manager.Model):
    wallets_key_id = BigIntegerField(primary_key=True)
    user_id = IntegerField()
    address = CharField()
    mnemonic = CharField()

    def __str__(self):
        return f'Wallets_: {self.user_id} {self.mnemonic} {self.address}'


class User(manager.Model):
    user_id = BigIntegerField(primary_key=True)
    username = CharField(default='', null=True)
    lang = CharField(default='en')
    referrer = BigIntegerField(null=True)
    total_ref_withdraw = DecimalField(default=0)

    balance_general = DecimalField(default=0)
    balance_demo = DecimalField(default=0)
    balance_promo = DecimalField(default=0)

    timestamp_registered = DateTimeField()
    timestamp_last_active = DateTimeField()
    timestamp_ref_withdraw = DateTimeField(null=True)

    def __str__(self):
        return f'USER: {self.user_id}; {self.lang=}'


class WithdrawTx(manager.Model):
    withdrawtx_id = BigIntegerField(primary_key=True)
    user = ForeignKeyField(User, backref='WithdrawTx')
    amount = DecimalField()
    token_id = CharField()
    tx_address = CharField()
    utime = BigIntegerField()
    withdraw_state = CharField()
    is_manual = BooleanField()


class Transactions(manager.Model):
    transaction_id = BigIntegerField(primary_key=True)
    user = ForeignKeyField(User, backref='transactions')
    token_id = CharField()
    tx_type = SmallIntegerField()
    tx_address = CharField()
    tx_hash = CharField()
    logical_time = BigIntegerField()
    utime = BigIntegerField()
    amount = BigIntegerField()
    comment = CharField()

    def __str__(self):
        return f'TRANSACTION: {self.user_id=}, {self.token_id=}, {self.tx_hash=}, {self.amount=}'


class GameLog(manager.Model):
    gamelog_id = BigIntegerField(primary_key=True)
    user = ForeignKeyField(User, backref='game_logs')
    balance_type = CharField()
    game = CharField()
    game_info = TextField()
    bet = DecimalField()
    result = DecimalField()
    timestamp = DateTimeField()

    def __str__(self):
        return f'GAMELOG: {self.user_id=} {self.token_id=} {self.bet=} {self.result=} {self.timestamp=}'
