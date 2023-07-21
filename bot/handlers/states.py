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
    enter_tickets_count = State()
    enter_pages = State()
    # promo-codes
    enter_promo_code = State()


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
    # WheelOfFortune
    TICKET_NUM = 'ticket_num'
    RANDOM_TICKETS_COUNT = 'random_tickets_count'
    ACTIVE_PROMO_NAME = 'active_promo_name'
    AVAILABLE_TICKETS_COUNT = 'available_tickets_count'
    # WheelOfFortune display my tickets
    TICKET_TYPE = 'ticket_type'
    CURRENT_PAGE = 'current_page'
    TOTAL_PAGES = 'tickets_to_display'
    # promo codes
    PROMO_CODE_ENTERED = 'promo_code_entered'


class Games:
    CASINO = 'CASINO'
    CUBE = 'CUBE'
    BASKET = 'BASKET'
    BOWLING = 'BOWLING'
    DARTS = 'DARTS'
    FOOTBALL = 'FOOTBALL'
    CUEFA = 'CUEFA'
    MINES = 'MINES'
