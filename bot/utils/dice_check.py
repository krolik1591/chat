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
    three(Dice.SEVEN): 15,
    three(Dice.GRAPES): 10,
    three(Dice.LEMON): 5,
    three(Dice.BAR): 3,

    two_near(Dice.SEVEN): 1,
    two_near(Dice.GRAPES): 0.5,
    two_near(Dice.LEMON): 0.5,
    two_near(Dice.BAR): 0.5,

    two(Dice.SEVEN): 0.5,
    two(Dice.GRAPES): 0.25,
    two(Dice.LEMON): 0.25,
    two(Dice.BAR): 0.25,
}


def parse_dice(dice_value: int) -> List[Dice]:
    dice_value -= 1
    return [
        dices[dice_value // i % 4]
        for i in (1, 4, 16)
    ]


if __name__ == '__main__':
    print('{')
    for dice_val in range(1, 65):
        human_readable = ''.join([str(i) for i in parse_dice(dice_val)])
        coef = get_coefficient(dice_val)
        print(f"    {dice_val}: {coef},  \t# {human_readable}")
    print('}')
