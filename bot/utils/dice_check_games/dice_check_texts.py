from bot.handlers.states import Games

from bot.texts import BASKET_TEXT_2, BASKET_TEXT_3, BASKET_TEXT_5, BOWLING_TEXT_4, BOWLING_TEXT_5, BOWLING_TEXT_6, \
    CUBE_TEXT_0, CUBE_TEXT_1, CUBE_TEXT_2, CUBE_TEXT_3, DARTS_BOWLING_BASKET_FOOTBALL_TEXT_1, DARTS_OR_BOWLING_TEXT_2, \
    DARTS_OR_BOWLING_TEXT_3, \
    DARTS_TEXT_4, DARTS_TEXT_5_OR_BASKET_4, DARTS_TEXT_6, FOOTBALL_TEXT_LOSE, FOOTBALL_TEXT_WIN, LOSE_TEXT, WIN_TEXT


def game_text(context, score_change, dice_value, cube_lose_streak):
    if context.game == Games.CASINO:
        return LOSE_TEXT if score_change == 0 \
            else WIN_TEXT.format(score_change=score_change, token_icon=context.token.icon)

    if context.game == Games.CUBE:
        return cube_text(cube_lose_streak, dice_value, score_change=score_change, token_icon=context.token.icon)

    if context.game == Games.BASKET:
        return basket_text(dice_value, score_change=score_change, token_icon=context.token.icon)

    if context.game == Games.DARTS:
        return darts_text(dice_value, score_change=score_change, token_icon=context.token.icon)

    if context.game == Games.BOWLING:
        return bowling_text(dice_value, score_change=score_change, token_icon=context.token.icon)

    if context.game == Games.FOOTBALL:
        return football_text(dice_value, score_change=score_change, token_icon=context.token.icon)


NUMBERS_EMOJI = {
    1: '1️⃣ <b>- непарне</b>',
    2: '2️⃣ <b>- парне</b>',
    3: '3️⃣ <b>- непарне</b>',
    4: '4️⃣ <b>- парне</b>',
    5: '5️⃣ <b>- непарне</b>',
    6: '6️⃣ <b>- парне</b>'
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


def cube_text(cube_lose_streak, dice_value, score_change, token_icon):
    dice_number_emoji = NUMBERS_EMOJI[dice_value]
    return CUBE_TEXTS[cube_lose_streak].format(score_change=score_change, token_icon=token_icon,
                                              cube_lose_streak=cube_lose_streak, dice_number_emoji=dice_number_emoji)


def basket_text(dice_value, score_change, token_icon):
    return BASKET_TEXTS[dice_value].format(score_change=score_change, token_icon=token_icon)


def darts_text(dice_value, score_change, token_icon):
    return DARTS_TEXTS[dice_value].format(score_change=score_change, token_icon=token_icon)


def bowling_text(dice_value, score_change, token_icon):
    return BOWLING_TEXTS[dice_value].format(score_change=score_change, token_icon=token_icon)


def football_text(dice_value, score_change, token_icon):
    return FOOTBALL_TEXTS[dice_value].format(score_change=score_change, token_icon=token_icon)
