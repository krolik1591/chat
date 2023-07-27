MIN_BET = 20
CHANGE_BET = 10
MAX_BET = 5000
START_POINTS = 500

MIN_WITHDRAW = 5  # game tokens
MAXIMUM_WITHDRAW = 30  # game tokens
MAXIMUM_WITHDRAW_DAILY = 110  # game tokens

DEFAULT_TICKET_COUNT = 10
WOF_MIN_NUM = 0
WOF_MAX_NUM = 9_999_999
MAX_BUY_TICKETS_PER_ONE_CLICK = 33_333

TON_INITIALISATION_FEE = 0.015  # ton

INTERVAL_FOR_REJECT_LOST_TX = 5 * 60  # sec

MIN_REF_WITHDRAW = 50  # game tokens

USER_REF_LEVEL = {
    # [where lvl ends | percent]
    'adept': [50_000, 5],
    'experienced': [100_000, 7],
    'connoisseur': [500_000, 10],  # 100_000 - bets, 10 - percent
    'expert': [1_000_000, 12],
    'maestro': [float('inf'), 15]
}

THROTTLE_TIME_SPIN = 2  # время искусственной задержки между броском дайса и ответом, оно же период троттлинга
THROTTLE_TIME_OTHER = 1  # время искусственной задержки между остальными командами, оно же период троттлинга

USDT_TO_GAMETOKENS = 100  # 1 USDT == 100 GENERAL

TTL = 30  # second, the time of relevance of the coin rate
