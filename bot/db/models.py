import pathlib

from peewee import *
from peewee_aio import Manager

# app/db/db.sqlite3
path = pathlib.Path(__file__).parent.parent.parent / 'db' / 'db.sqlite3'
manager = Manager(f'aiosqlite:////{path}')


class User(manager.Model):
    user_id = BigIntegerField(primary_key=True)
    username = CharField(default='', null=True)


class GameLog(manager.Model):
    gamelog_id = BigIntegerField(primary_key=True)
    user = ForeignKeyField(User, backref='game_logs')
    game = CharField()
    result = IntegerField()
    timestamp = DateTimeField()
