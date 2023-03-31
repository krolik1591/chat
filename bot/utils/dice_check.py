from enum import Enum
from typing import List


class Dice(Enum):
    BAR = "➖"
    GRAPES = "🍇"
    LEMON = "🍋"
    SEVEN = "7️⃣"

    def __str__(self):
        return self.value


dices = [Dice.BAR, Dice.GRAPES, Dice.LEMON, Dice.SEVEN]

REWARDS = [
    # DICE | COUNT | REWARD
    (Dice.SEVEN, 3, 15),
    (Dice.GRAPES, 3, 10),
    (Dice.LEMON, 3, 5),
    (Dice.BAR, 3, 3),
    (Dice.SEVEN, 2, 1),
    (Dice.GRAPES, 2, 0.25),
    (Dice.LEMON, 2, 0.25),
    (Dice.BAR, 2, 0.25),
]


def get_coefficient(dice_value: int) -> float:
    result = parse_dice(dice_value)

    def is_two_items(x):
        return result.count(x) == 2  # and result[1] == x

    def is_three_items(x):
        return result.count(x) == 3

    for dice, count, reward in REWARDS:
        if count == 3 and is_three_items(dice):
            return reward
        if count == 2 and is_two_items(dice):
            return reward

    return 0


def parse_dice(dice_value: int) -> List[Dice]:
    dice_value -= 1
    return [
        dices[dice_value // i % 4]
        for i in (1, 4, 16)
    ]


if __name__ == '__main__':
    for dice_val in range(1, 65):
        print(dice_val, ''.join([str(i) for i in parse_dice(dice_val)]), get_coefficient(dice_val), sep='\t')
