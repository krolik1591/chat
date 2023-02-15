from peewee import *
from peewee_aio import Manager

manager = Manager('aiosqlite:///db.sqlite3')


class Token(manager.Model):
    token_id = CharField(primary_key=True)
    price = IntegerField()
    icon = CharField()


class User(manager.Model):
    tg_id = BigIntegerField(primary_key=True)
    lang = CharField(default='en')

    timestamp_registered = DateTimeField()
    timestamp_last_active = DateTimeField()
    timestamp_first_tx = DateTimeField(null=True)
    timestamp_last_tx = DateTimeField(null=True)


class Balances(manager.Model):
    user = ForeignKeyField(User, backref='balances')
    token = ForeignKeyField(Token, backref='balances')
    amount = BigIntegerField(default=0)


class Transactions(manager.Model):
    user = ForeignKeyField(User, backref='transactions')
    token = ForeignKeyField(Token, backref='transactions')
    is_deposit = BooleanField()
    tx_address = CharField()
    tx_hash = CharField()
    logical_time = BigIntegerField()
    amount = BigIntegerField()


class GameLogs(manager.Model):
    user = ForeignKeyField(User, backref='game_logs')
    token = ForeignKeyField(Token, backref='game_logs')
    game = CharField()
    game_info = TextField()
    bet = BigIntegerField()
    result = BigIntegerField()
    timestamp = DateTimeField()
