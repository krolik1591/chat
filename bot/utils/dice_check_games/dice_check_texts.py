from bot.handlers.states import Games, StateKeys
from bot.handlers.context import Context

from bot.texts import BASKET_TEXT_2, BASKET_TEXT_3, BASKET_TEXT_5, BOWLING_TEXT_4, BOWLING_TEXT_5, BOWLING_TEXT_6, \
    DARTS_BOWLING_BASKET_FOOTBALL_TEXT_1, DARTS_OR_BOWLING_TEXT_2, DARTS_OR_BOWLING_TEXT_3, \
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
    1: '1️⃣  <b>- непарне</b>',
    2: '2️⃣  <b>- парне</b>',
    3: '3️⃣  <b>- непарне</b>',
    4: '4️⃣ <b>- парне</b>',
    5: '5️⃣ <b>- непарне</b>',
    6: '6️⃣ <b>- парне</b>'
}


def cube_text(cube_lose_streak, dice_value, score_change, token_icon):

    if cube_lose_streak == 0:
        return f'{NUMBERS_EMOJI[dice_value]}\n\n✅ Ви виграли {score_change} {token_icon}'
    if cube_lose_streak == 1:
        return f'{NUMBERS_EMOJI[dice_value]}\n\n🙄 На жаль, вам не пощастило'
    if cube_lose_streak == 2:
        return f'{NUMBERS_EMOJI[dice_value]}\n\n🤐 Дідько, знов не пощастило'
    else:
        return f'{NUMBERS_EMOJI[dice_value]}\n\n🔥 Вже {cube_lose_streak} раз не щастить'



def basket_text(dice_value, score_change, token_icon):
    if dice_value == 1:
        return DARTS_BOWLING_BASKET_FOOTBALL_TEXT_1
    if dice_value == 2:
        return BASKET_TEXT_2
    if dice_value == 3:
        return BASKET_TEXT_3
    if dice_value == 4:
        return DARTS_TEXT_5_OR_BASKET_4.format(score_change=score_change, token_icon=token_icon)
    if dice_value == 5:
        return BASKET_TEXT_5.format(score_change=score_change, token_icon=token_icon)

    return 'svinerus is gay'


def darts_text(dice_value, score_change, token_icon):
    if dice_value == 1:
        return DARTS_BOWLING_BASKET_FOOTBALL_TEXT_1
    if dice_value == 2:
        return DARTS_OR_BOWLING_TEXT_2
    if dice_value == 3:
        return DARTS_OR_BOWLING_TEXT_3
    if dice_value == 4:
        return DARTS_TEXT_4.format(score_change=score_change, token_icon=token_icon)
    if dice_value == 5:
        return DARTS_TEXT_5_OR_BASKET_4.format(score_change=score_change, token_icon=token_icon)
    if dice_value == 6:
        return DARTS_TEXT_6.format(score_change=score_change, token_icon=token_icon)
    return 'svinerus is gay'


def bowling_text(dice_value, score_change, token_icon):
    if dice_value == 1:
        return DARTS_BOWLING_BASKET_FOOTBALL_TEXT_1
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
    return 'svinerus is gay'


def football_text(dice_value, score_change, token_icon):
    if dice_value == 1:
        return DARTS_BOWLING_BASKET_FOOTBALL_TEXT_1
    if dice_value == 2:
        return FOOTBALL_TEXT_LOSE
    if dice_value == 3 or dice_value == 4 or dice_value == 5:
        return FOOTBALL_TEXT_WIN.format(score_change=score_change, token_icon=token_icon)
    return 'svinerus is gay'