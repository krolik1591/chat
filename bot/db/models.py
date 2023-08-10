import pathlib

from peewee import *
from peewee_aio import Manager

# app/db/db.sqlite3
path = pathlib.Path(__file__).parent.parent.parent / 'db' / 'db.sqlite3'
manager = Manager(f'aiosqlite:////{path}')


class User(manager.Model):
    user_id = BigIntegerField(primary_key=True)
    username = CharField(default='', null=True)

    def __str__(self):
        return f'USER: {self.user_id}; {self.lang=}'


class GameLog(manager.Model):
    gamelog_id = BigIntegerField(primary_key=True)
    user = ForeignKeyField(User, backref='game_logs')
    game = CharField()
    result = DecimalField()
    timestamp = DateTimeField()

    def __str__(self):
        return f'GAMELOG: {self.user_id=} {self.token_id=} {self.bet=} {self.result=} {self.timestamp=}'
