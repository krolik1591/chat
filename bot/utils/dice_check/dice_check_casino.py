from enum import Enum
from typing import List


class Slot(Enum):
    BAR = "➖"
    GRAPES = "🍇"
    LEMON = "🍋"
    SEVEN = "7️⃣"

    def __str__(self):
        return self.value


dices = [Slot.BAR, Slot.GRAPES, Slot.LEMON, Slot.SEVEN]


def get_coefficient(dice_value: int, rewards_table) -> float:
    result = parse_dice(dice_value)

    for condition, reward in rewards_table.items():
        if condition(result):
            return reward

    return 0


def two_near(x):
    return lambda slot_result: slot_result.count(x) == 2 and slot_result[1] == x


def two(x):
    return lambda slot_result: slot_result.count(x) == 2 and slot_result[1] != x


def three(x):
    return lambda slot_result: slot_result.count(x) == 3


def parse_dice(dice_value: int) -> List[Slot]:
    dice_value -= 1
    return [
        dices[dice_value // i % 4]
        for i in (1, 4, 16)
    ]
