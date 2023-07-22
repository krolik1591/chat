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
    wof_win = CharField(default='{"general": 0, "promo": 0}')

    balance_general = DecimalField(default=0)
    balance_demo = DecimalField(default=0)
    balance_promo = DecimalField(default=0)

    is_blocked = BooleanField(default=0)

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


class Settings(manager.Model):
    key = CharField(primary_key=True)
    value = CharField()     # json format


class PromoCodes(manager.Model):
    name = CharField(primary_key=True)
    type = CharField()
    bonus = BigIntegerField()
    number_of_users = DecimalField()
    max_deposits = BigIntegerField()
    date_start = BigIntegerField()
    date_end = BigIntegerField()
    duration = IntegerField()
    min_wager = DecimalField()
    wager = DecimalField()
    special_users = CharField(null=True)


class UsersPromoCodes(manager.Model):
    userspromocodes_id = BigIntegerField(primary_key=True)
    user = ForeignKeyField(User, backref='userspromocodes')
    promo_name = ForeignKeyField(PromoCodes, backref='userspromocodes')
    deposited_bonus = DecimalField(default=0)
    available_bonus_tickets = BigIntegerField(null=True)
    deposited_min_wager = DecimalField(default=0)
    deposited_wager = DecimalField(default=0)
    date_activated = BigIntegerField(null=True)
    date_end = BigIntegerField()
    is_active = BooleanField()
    won = BooleanField(default=False)


class WoFTickets(manager.Model):
    woftickets_id = BigIntegerField(primary_key=True)
    user = ForeignKeyField(User, backref='wof_tickets')
    promo = ForeignKeyField(PromoCodes, backref='wof_tickets', null=True)
    ticket_num = BigIntegerField()
    ticket_type = CharField()
    buy_timestamp = DateTimeField()

    # is_promo = BooleanField(default=False)


class WoFSettings(manager.Model):
    wofsettings_id = BigIntegerField(primary_key=True)

    ticket_cost = BigIntegerField()
    commission = BigIntegerField()
    rewards = CharField()
    winners = CharField(null=True)   # ticket_num: tg_id:reward
    random_seed = CharField()

    timestamp_start = DateTimeField()
    timestamp_end = DateTimeField(null=True)

    is_active = BooleanField(default=1)