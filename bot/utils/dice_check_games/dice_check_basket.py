def get_coefficient_basket(dice_value: int) -> float:
    print(dice_value)
    # 2 - pokrutilsa i upal, 5 - very very nice, 3 - zastryal, 1 - miss
    if dice_value == 5:
        return 2.5

    if dice_value == 4:
        return 1.5

    return 0
