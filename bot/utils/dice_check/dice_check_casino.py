from enum import Enum
from typing import List

from bot.games_const import THREE_BAR, THREE_GRAPES, THREE_LEMON, THREE_SEVEN, TWO_BAR, TWO_GRAPES, TWO_LEMON, \
    TWO_NEAR_BAR, \
    TWO_NEAR_GRAPES, \
    TWO_NEAR_LEMON, \
    TWO_NEAR_SEVEN, TWO_SEVEN


class Dice(Enum):
    BAR = "➖"
    GRAPES = "🍇"
    LEMON = "🍋"
    SEVEN = "7️⃣"

    def __str__(self):
        return self.value


dices = [Dice.BAR, Dice.GRAPES, Dice.LEMON, Dice.SEVEN]


def get_coefficient(dice_value: int) -> float:
    result = parse_dice(dice_value)

    for condition, reward in REWARDS.items():
        if condition(result):
            return reward

    return 0


def two_near(x):
    return lambda slot_result: slot_result.count(x) == 2 and slot_result[1] == x


def two(x):
    return lambda slot_result: slot_result.count(x) == 2 and slot_result[1] != x


def three(x):
    return lambda slot_result: slot_result.count(x) == 3


REWARDS = {
    three(Dice.SEVEN): THREE_SEVEN,
    three(Dice.GRAPES): THREE_GRAPES,
    three(Dice.LEMON):THREE_LEMON,
    three(Dice.BAR): THREE_BAR,

    two_near(Dice.SEVEN): TWO_NEAR_SEVEN,
    two_near(Dice.GRAPES): TWO_NEAR_GRAPES,
    two_near(Dice.LEMON): TWO_NEAR_LEMON,
    two_near(Dice.BAR): TWO_NEAR_BAR,

    two(Dice.SEVEN): TWO_SEVEN,
    two(Dice.GRAPES): TWO_GRAPES,
    two(Dice.LEMON): TWO_LEMON,
    two(Dice.BAR): TWO_BAR,
}


def parse_dice(dice_value: int) -> List[Dice]:
    dice_value -= 1
    return [
        dices[dice_value // i % 4]
        for i in (1, 4, 16)
    ]
