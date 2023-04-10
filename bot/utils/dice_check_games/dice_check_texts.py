from bot.texts import BOWLING_TEXT_4, BOWLING_TEXT_5, BOWLING_TEXT_6, \
    DARTS_OR_BOWLING_TEXT_1, DARTS_OR_BOWLING_TEXT_2, DARTS_OR_BOWLING_TEXT_3, DARTS_TEXT_4, \
    DARTS_TEXT_5, DARTS_TEXT_6


def darts_text(dice_value, score_change, token_icon):
    if dice_value == 1:
        return DARTS_OR_BOWLING_TEXT_1
    if dice_value == 2:
        return DARTS_OR_BOWLING_TEXT_2
    if dice_value == 3:
        return DARTS_OR_BOWLING_TEXT_3
    if dice_value == 4:
        return DARTS_TEXT_4.format(score_change=score_change, token_icon=token_icon)
    if dice_value == 5:
        return DARTS_TEXT_5.format(score_change=score_change, token_icon=token_icon)
    if dice_value == 6:
        return DARTS_TEXT_6.format(score_change=score_change, token_icon=token_icon)
    return 'svinerus gay'


def bowling_text(dice_value, score_change, token_icon):
    if dice_value == 1:
        return DARTS_OR_BOWLING_TEXT_1
    if dice_value == 2:
        return DARTS_OR_BOWLING_TEXT_2
    if dice_value == 3:
        return DARTS_OR_BOWLING_TEXT_3
    if dice_value == 4:
        return BOWLING_TEXT_4
    if dice_value == 5:
        return BOWLING_TEXT_5.format(score_change=score_change, token_icon=token_icon)
    if dice_value == 6:
        return BOWLING_TEXT_6.format(score_change=score_change, token_icon=token_icon)
    return 'svinerus gay'
