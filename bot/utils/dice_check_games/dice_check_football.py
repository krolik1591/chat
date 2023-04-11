def get_coefficient_football(dice_value: int) -> float:
    ez_win = [3, 4, 5]
    if dice_value in ez_win:
        return 1.5

    return 0
