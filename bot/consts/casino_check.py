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


def get_casino_result(dice_value):
    result = parse_dice(dice_value)

    for condition, reward in SLOTS_TEXT.items():
        if condition(result):
            return reward

    return 'Не пощастило :(', 0


def three(x):
    return lambda slot_result: slot_result.count(x) == 3


def parse_dice(dice_value: int) -> List[Slot]:
    dice_value -= 1
    return [
        dices[dice_value // i % 4]
        for i in (1, 4, 16)
    ]


SLOTS_TEXT = {
    three(Slot.SEVEN): ('🤑 <b>Джекпот!</b> 🤑', 10),
    three(Slot.LEMON): ('Три в ряд 🍋', 3),
    three(Slot.GRAPES): ('Три в ряд 🍇', 3),
    three(Slot.BAR): ('Три в ряд ➖', 5),
}
