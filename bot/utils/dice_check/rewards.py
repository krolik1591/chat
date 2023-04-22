from bot.utils.dice_check.dice_check_casino import three, Slot, two_near, two

# CASINO (16 WINNING COMBOS), CASINO_PROFIT = 40.625 %
SLOTS_REWARDS = {
    three(Slot.SEVEN): 17,
    three(Slot.LEMON): 7,
    three(Slot.GRAPES): 5,
    three(Slot.BAR): 3,

    two_near(Slot.SEVEN): 1,
    two_near(Slot.GRAPES): 0.5,
    two_near(Slot.LEMON): 0.5,
    two_near(Slot.BAR): 0.5,

    two(Slot.SEVEN): 0.25,
    two(Slot.GRAPES): 0.25,
    two(Slot.LEMON): 0.25,
    two(Slot.BAR): 0.25,
}


# CUBE, CASINO_PROFIT = (16.7, 16.7, 15) %
class CubeRewards:
    EXACT_VALUE_BET = 5  # (1), (2), (3), (4), (5), (6) COMBINATIONS
    BET_ON_RANGE = 2.5  # (1-2), (3-4), (5-6) COMBINATIONS
    BET_ON_PARITY = 1.7  # (EVEN), (ODD) COMBINATIONS


BASKET_REWARDS = {
    5: 2.5,  # clear hit
    4: 1.5,  # dirty hit
    3: 0,  # dirty miss
    2: 0,  # rebound miss
    1: 0,  # stuck miss
}


DARTS_REWARDS = {
    6: 3,  # hit center
    5: 1.5,  # hit 1 circle
    4: 0.25,  # hit 2 circle
    3: 0,  # hit 3 circle
    2: 0,  # hit 4 circle
    1: 0,  # dartboard missed
}


BOWLING_REWARDS = {
    6: 5,  # strike
    5: 0,  # one pin left
    4: 0,  # two pin left
    3: 0,  # three pin left
    2: 0,  # five pin left
    1: 0,  # all(6) pin left
}


FOOTBALL_REWARDS = {
    1: 1.3,  # central goal,
    2: 1.3,  # right goal
    3: 1.3,  # left goal
    4: 0,  # rebound miss
    5: 0,  # miss
}
