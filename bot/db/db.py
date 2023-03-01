import pathlib

from peewee import *
from peewee_aio import Manager

# app/db/db.sqlite3
path = pathlib.Path(__file__).parent.parent.parent / 'db' / 'db.sqlite3'
print(path)
manager = Manager(f'aiosqlite:////{path}')


class Token(manager.Model):
    name = CharField()
    price = IntegerField()
    icon = CharField()

    def __str__(self):
        return f'TOKEN: {self.icon} {self.name}; {self.price=}, {self.id=}'


class User(manager.Model):
    tg_id = BigIntegerField(primary_key=True)
    username = CharField(default='')
    lang = CharField(default='en')

    timestamp_registered = DateTimeField()
    timestamp_last_active = DateTimeField()

    def __str__(self):
        return f'USER: {self.tg_id}; {self.lang=}'


class Balances(manager.Model):
    user = ForeignKeyField(User, backref='balances')
    token = ForeignKeyField(Token, backref='balances')
    amount = BigIntegerField(default=0)

    class Meta:
        indexes = (
            (("user_id", "token_id"), True),
        )

    def __str__(self):
        return f'BALANCES: {self.user_id} {self.token_id}; price:{self.amount} id:{self.id}'


class Transactions(manager.Model):
    user = ForeignKeyField(User, backref='transactions')
    token = ForeignKeyField(Token, backref='transactions')
    tx_type = SmallIntegerField()
    # 1) tx_address = адреса з якої поповнюють; tx_type = 1
    # 2) tx_address = похуй ; tx_type = 2
    # 3) tx_address = адреса на яку виводимо гроши; tx_type = 3
    tx_address = CharField()
    tx_hash = CharField()
    logical_time = BigIntegerField()
    amount = BigIntegerField()

    def __str__(self):
        return f'TRANSACTION: {self.user_id=}, {self.token_id=}, {self.tx_hash=}, {self.amount=}'


class GameLogs(manager.Model):
    user = ForeignKeyField(User, backref='game_logs')
    token = ForeignKeyField(Token, backref='game_logs')
    game = CharField()
    game_info = TextField()
    bet = BigIntegerField()
    result = BigIntegerField()
    timestamp = DateTimeField()

    def __str__(self):
        return f'GAMELOG: {self.user_id=} {self.token_id=} {self.bet=} {self.result=} {self.timestamp=}'
