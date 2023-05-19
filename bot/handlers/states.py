from aiogram.fsm.state import State, StatesGroup


class Menu(StatesGroup):
    bet = State()
    settings = State()
    withdraw_amount = State()
    withdraw_amount_approve = State()
    withdraw_address = State()
    delete_message = State()
    do_nothing = State()


class StateKeys:
    # common
    LAST_MSG_ID = 'last_msg_id'
    LOCALE = 'locale'
    # game
    GAME = 'game'
    BALANCE_TYPE = 'balance_type'
    GAME_SETTINGS = 'game_settings'
    BET = 'bet'
    CUBE_LOSE_STREAK = 'cube_lose_streak'
    AT_LEAST_ONE_BET = 'at_least_one_bet'
    CUBE_COEF = 'cube_coef'
    # withdraw
    TOKEN_ID = 'token_id'
    WITHDRAW_AMOUNT = 'withdraw_amount'
    WITHDRAW_ADDRESS = 'withdraw_address'


class Games:
    CASINO = 'CASINO'
    CUBE = 'CUBE'
    BASKET = 'BASKET'
    BOWLING = 'BOWLING'
    DARTS = 'DARTS'
    FOOTBALL = 'FOOTBALL'
    CUEFA = 'CUEFA'
    MINES = 'MINES'
