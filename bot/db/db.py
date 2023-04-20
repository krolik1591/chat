import pathlib

from peewee import *
from peewee_aio import Manager

# app/db/db.sqlite3
path = pathlib.Path(__file__).parent.parent.parent / 'db' / 'db.sqlite3'
print(path)
manager = Manager(f'aiosqlite:////{path}')

class Wallets_key(manager.Model):
    wallets_key_id = BigIntegerField(primary_key=True)
    user_id = IntegerField()
    address = CharField()
    mnemonic = CharField()


    def __str__(self):
        return f'Wallets_: {self.user_id} {self.mnemonic} {self.address}'



class Token(manager.Model):
    token_id = BigIntegerField(primary_key=True)
    name = CharField()
    price = IntegerField()
    icon = CharField()

    def __str__(self):
        return f'TOKEN: {self.icon} {self.name}; {self.price=}, {self.token_id=}'


class User(manager.Model):
    user_id = BigIntegerField(primary_key=True)
    username = CharField(default='')
    lang = CharField(default='en')

    timestamp_registered = DateTimeField()
    timestamp_last_active = DateTimeField()

    def __str__(self):
        return f'USER: {self.user_id}; {self.lang=}'


class Balance(manager.Model):
    balance_id = BigIntegerField(primary_key=True)
    user = ForeignKeyField(User, backref='balances')
    token = ForeignKeyField(Token, backref='balances')
    amount = DecimalField(default=0)

    class Meta:
        indexes = (
            (("user_id", "token_id"), True),
        )

    def __str__(self):
        return f'BALANCES: {self.user_id} {self.token_id}; price:{self.amount} id:{self.balance_id}'


class ManualTXs(manager.Model):
    ManualTXs_id = BigIntegerField(primary_key=True)
    user = ForeignKeyField(User, backref='manualTXs')
    amount = BigIntegerField()
    token = ForeignKeyField(Token, backref='manualTXs')
    price = IntegerField()
    tx_address = CharField()
    utime = BigIntegerField()
    withdraw_state = CharField()
    is_manual = BooleanField()


class Transactions(manager.Model):
    transaction_id = BigIntegerField(primary_key=True)
    user = ForeignKeyField(User, backref='transactions')
    token = ForeignKeyField(Token, backref='transactions')
    tx_type = SmallIntegerField()
    # 1) tx_address = адреса з якої поповнюють; tx_type = 1
    # 2) tx_address = похуй ; tx_type = 2
    # 3) tx_address = адреса на яку виводимо гроши; tx_type = 3
    tx_address = CharField()
    tx_hash = CharField()
    logical_time = BigIntegerField()
    utime = BigIntegerField()
    amount = BigIntegerField()

    def __str__(self):
        return f'TRANSACTION: {self.user_id=}, {self.token_id=}, {self.tx_hash=}, {self.amount=}'


class GameLog(manager.Model):
    gamelog_id = BigIntegerField(primary_key=True)
    user = ForeignKeyField(User, backref='game_logs')
    token = ForeignKeyField(Token, backref='game_logs')
    game = CharField()
    game_info = TextField()
    bet = BigIntegerField()
    result = BigIntegerField()
    timestamp = DateTimeField()

    def __str__(self):
        return f'GAMELOG: {self.user_id=} {self.token_id=} {self.bet=} {self.result=} {self.timestamp=}'
