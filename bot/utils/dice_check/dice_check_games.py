from bot.games_const import BET_ON_PARITY, BET_ON_RANGE, CLEAR_HIT, DIRTY_HIT, EXACT_VALUE_BET, GOAL, HIT_1_CIRCLE, \
    HIT_2_CIRCLE, HIT_CENTER, ONE_PIN_LEFT, STRIKE
from bot.utils.dice_check import dice_check_casino


def slots(dice_value: int, game_settings) -> float:
    return dice_check_casino.get_coefficient(dice_value)


def cube(dice_value: int, user_bets) -> float:
    win = 0
    for user_bet in user_bets:
        if len(user_bet) == 1 and str(dice_value) in user_bet:
            win += EXACT_VALUE_BET
        if len(user_bet) == 2 and str(dice_value) in user_bet:
            win += BET_ON_RANGE
        if len(user_bet) == 3 and str(dice_value) in user_bet:
            win += BET_ON_PARITY
    return win


def basket(dice_value: int, game_settings) -> float:
    if dice_value == 5:
        return CLEAR_HIT
    if dice_value == 4:
        return DIRTY_HIT
    return 0


def darts(dice_value: int, game_settings) -> float:
    if dice_value == 6:
        return HIT_CENTER
    if dice_value == 5:
        return HIT_1_CIRCLE
    if dice_value == 4:
        return HIT_2_CIRCLE
    return 0


def bowling(dice_value: int, game_settings) -> float:
    if dice_value == 6:
        return STRIKE
    if dice_value == 5:
        return ONE_PIN_LEFT
    return 0


def football(dice_value: int, game_settings) -> float:
    ez_win = [3, 4, 5]
    if dice_value in ez_win:
        return GOAL
    return 0
