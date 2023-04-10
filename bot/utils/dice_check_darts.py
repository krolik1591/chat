def get_coefficient_darts(dice_value: int) -> float:
    print(dice_value)
    if dice_value == 6:
        return 3

    if dice_value == 5:
        return 1.5

    if dice_value == 4:
        return 1

    return 0
