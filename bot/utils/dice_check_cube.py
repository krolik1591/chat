def get_coefficient_cube(dice_value: int, user_bet_on) -> float:

    if len(user_bet_on) == 1 and str(dice_value) in user_bet_on:
        return 5

    if len(user_bet_on) == 2 and str(dice_value) in user_bet_on:
        return 2.7

    if len(user_bet_on) == 3 and str(dice_value) in user_bet_on:
        return 1.8

    return 0
