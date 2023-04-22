from bot.texts import BASKET_TEXT_2, BASKET_TEXT_3, BASKET_TEXT_5, BOWLING_TEXT_4, BOWLING_TEXT_5, BOWLING_TEXT_6, \
    CUBE_TEXT_0, CUBE_TEXT_1, CUBE_TEXT_2, CUBE_TEXT_3, DARTS_BOWLING_BASKET_FOOTBALL_TEXT_1, DARTS_OR_BOWLING_TEXT_2, \
    DARTS_OR_BOWLING_TEXT_3, \
    DARTS_TEXT_4, DARTS_TEXT_5_OR_BASKET_4, DARTS_TEXT_6, FOOTBALL_TEXT_LOSE, FOOTBALL_TEXT_WIN, LOSE_TEXT, WIN_TEXT


BASKET_TEXTS = {
    1: DARTS_BOWLING_BASKET_FOOTBALL_TEXT_1,
    2: BASKET_TEXT_2,
    3: BASKET_TEXT_3,
    4: DARTS_TEXT_5_OR_BASKET_4,
    5: BASKET_TEXT_5
}

DARTS_TEXTS = {
    1: DARTS_BOWLING_BASKET_FOOTBALL_TEXT_1,
    2: DARTS_OR_BOWLING_TEXT_2,
    3: DARTS_OR_BOWLING_TEXT_3,
    4: DARTS_TEXT_4,
    5: DARTS_TEXT_5_OR_BASKET_4,
    6: DARTS_TEXT_6
}

BOWLING_TEXTS = {
    1: DARTS_BOWLING_BASKET_FOOTBALL_TEXT_1,
    2: DARTS_OR_BOWLING_TEXT_2,
    3: DARTS_OR_BOWLING_TEXT_3,
    4: BOWLING_TEXT_4,
    5: BOWLING_TEXT_5,
    6: BOWLING_TEXT_6
}

FOOTBALL_TEXTS = {
    1: DARTS_BOWLING_BASKET_FOOTBALL_TEXT_1,
    2: FOOTBALL_TEXT_LOSE,
    3: FOOTBALL_TEXT_WIN,
    4: FOOTBALL_TEXT_WIN,
    5: FOOTBALL_TEXT_WIN
}

CUBE_TEXTS = {
    0: CUBE_TEXT_0,
    1: CUBE_TEXT_1,
    2: CUBE_TEXT_2,
    3: CUBE_TEXT_3,
    4: CUBE_TEXT_3,
    5: CUBE_TEXT_3,
    6: CUBE_TEXT_3
}

NUMBERS_EMOJI = {
    1: '1️⃣ <b>- непарне</b>',
    2: '2️⃣ <b>- парне</b>',
    3: '3️⃣ <b>- непарне</b>',
    4: '4️⃣ <b>- парне</b>',
    5: '5️⃣ <b>- непарне</b>',
    6: '6️⃣ <b>- парне</b>'
}


def casino(dice_value, score_change, token_icon):
    if score_change == 0:
        return LOSE_TEXT
    return WIN_TEXT.format(score_change=score_change, token_icon=token_icon)


def cube(dice_value, score_change, token_icon, cube_lose_streak):
    dice_number_emoji = NUMBERS_EMOJI[dice_value]
    return CUBE_TEXTS[cube_lose_streak].format(score_change=score_change, token_icon=token_icon,
                                               cube_lose_streak=cube_lose_streak, dice_number_emoji=dice_number_emoji)


def basket(dice_value, score_change, token_icon):
    return BASKET_TEXTS[dice_value].format(score_change=score_change, token_icon=token_icon)


def darts(dice_value, score_change, token_icon):
    return DARTS_TEXTS[dice_value].format(score_change=score_change, token_icon=token_icon)


def bowling(dice_value, score_change, token_icon):
    return BOWLING_TEXTS[dice_value].format(score_change=score_change, token_icon=token_icon)


def football(dice_value, score_change, token_icon):
    return FOOTBALL_TEXTS[dice_value].format(score_change=score_change, token_icon=token_icon)
