from peewee import *
import peewee_async
from ._async_sqlite import SqliteDatabase as AsyncSqliteDatabase

database = AsyncSqliteDatabase('db.sqlite3')
objects = peewee_async.Manager(database)
database.set_allow_sync(False)


def execute(query):
    return objects.execute(query)


class Token(Model):
    token = CharField(unique=True)
    price = IntegerField()
    icon = CharField()

    class Meta:
        database = database


class User(Model):
    tg_id = BigIntegerField(unique=True)
    lang = CharField(default='en')

    timestamp_registered = DateTimeField()
    timestamp_last_active = DateTimeField()
    timestamp_first_tx = DateTimeField(null=True)
    timestamp_last_tx = DateTimeField(null=True)

    class Meta:
        database = database


class Balances(Model):
    user = ForeignKeyField(User, backref='balances')
    token = ForeignKeyField(Token, backref='balances')
    amount = BigIntegerField(default=0)

    class Meta:
        database = database


class Transactions(Model):
    user = ForeignKeyField(User, backref='transactions')
    token = ForeignKeyField(Token, backref='transactions')
    is_deposit = BooleanField()
    tx_address = CharField()
    tx_hash = CharField()
    logical_time = BigIntegerField()
    amount = BigIntegerField()

    class Meta:
        database = database


class GameLogs(Model):
    user = ForeignKeyField(User, backref='game_logs')
    token = ForeignKeyField(Token, backref='game_logs')
    game = CharField()
    game_info = TextField()
    bet = BigIntegerField()
    result = BigIntegerField()
    timestamp = DateTimeField()

    class Meta:
        database = database
