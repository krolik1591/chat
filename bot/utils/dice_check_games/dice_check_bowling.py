def get_coefficient_bowling(dice_value: int) -> float:
    print(dice_value)
    # 5: 1, 1: miss, 3: 3, 6: 0,  2: -1, 4:2
    if dice_value == 6:
        return 5

    if dice_value == 5:
        return 0.5
    
    return 0
