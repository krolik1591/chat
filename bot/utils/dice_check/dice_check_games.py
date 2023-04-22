from bot.utils.dice_check import dice_check_casino

from bot.utils.dice_check.rewards import SLOTS_REWARDS, CubeRewards, BASKET_REWARDS, DARTS_REWARDS, FOOTBALL_REWARDS, \
    BOWLING_REWARDS


def slots(dice_value: int, game_settings) -> float:
    return dice_check_casino.get_coefficient(dice_value, SLOTS_REWARDS)


def cube(dice_value: int, user_bets) -> float:
    win = 0
    for user_bet in user_bets:
        if str(dice_value) in user_bet:
            if len(user_bet) == 1:
                win += CubeRewards.EXACT_VALUE_BET
            if len(user_bet) == 2:
                win += CubeRewards.BET_ON_RANGE
            if len(user_bet) == 3:
                win += CubeRewards.BET_ON_PARITY
    return win


def basket(dice_value: int, game_settings) -> float:
    return BASKET_REWARDS.get(dice_value, 0)


def darts(dice_value: int, game_settings) -> float:
    return DARTS_REWARDS.get(dice_value, 0)


def bowling(dice_value: int, game_settings) -> float:
    return BOWLING_REWARDS.get(dice_value, 0)


def football(dice_value: int, game_settings) -> float:
    return FOOTBALL_REWARDS.get(dice_value, 0)
