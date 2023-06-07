from aiogram.fsm.state import State, StatesGroup


class Menu(StatesGroup):
    bet = State()
    settings = State()
    withdraw_amount = State()
    withdraw_amount_approve = State()
    withdraw_address = State()
    delete_message = State()
    do_nothing = State()
    # admin
    enter_spam_msg = State()
    get_id_spam_receiver = State()
    # WheelOfFortune
    enter_ticket_num = State()


class StateKeys:
    # common
    LAST_MSG_ID = 'last_msg_id'
    # game
    GAME = 'game'
    BALANCE_TYPE = 'balance_type'
    GAME_SETTINGS = 'game_settings'
    BET = 'bet'
    CUBE_LOSE_STREAK = 'cube_lose_streak'
    # withdraw
    TOKEN_ID = 'token_id'
    WITHDRAW_AMOUNT = 'withdraw_amount'
    WITHDRAW_ADDRESS = 'withdraw_address'
    # admin
    SPAM_TYPE = 'spam_type'
    SPAM_LANG = 'spam_lang'
    SPAM_MSG_ID = 'spam_msg_id'
    ID_RECEIVERS = 'id_receiver'


class Games:
    CASINO = 'CASINO'
    CUBE = 'CUBE'
    BASKET = 'BASKET'
    BOWLING = 'BOWLING'
    DARTS = 'DARTS'
    FOOTBALL = 'FOOTBALL'
    CUEFA = 'CUEFA'
    MINES = 'MINES'
