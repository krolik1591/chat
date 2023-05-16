from bot.consts import texts as t
from aiogram.utils.i18n import gettext as _


def basket_texts(dice):
    BASKET_TEXTS = {
        1: _('DARTS_BOWLING_BASKET_FOOTBALL_TEXT_1'),
        2: _('BASKET_TEXT_2'),
        3: _('BASKET_TEXT_3'),
        4: _('DARTS_TEXT_5_OR_BASKET_4'),
        5: _('BASKET_TEXT_5')
    }
    return BASKET_TEXTS[dice]


def darts_texts(dice):
    DARTS_TEXTS = {
        1: _('DARTS_BOWLING_BASKET_FOOTBALL_TEXT_1'),
        2: _('DARTS_OR_BOWLING_TEXT_2'),
        3: _('DARTS_OR_BOWLING_TEXT_3'),
        4: _('DARTS_TEXT_4'),
        5: _('DARTS_TEXT_5_OR_BASKET_4'),
        6: _('DARTS_TEXT_6')
    }
    return DARTS_TEXTS[dice]


def bowling_texts(dice):
    BOWLING_TEXTS = {
        1: _('DARTS_BOWLING_BASKET_FOOTBALL_TEXT_1'),
        2: _('DARTS_OR_BOWLING_TEXT_2'),
        3: _('DARTS_OR_BOWLING_TEXT_3'),
        4: _('BOWLING_TEXT_4'),
        5: _('BOWLING_TEXT_5'),
        6: _('BOWLING_TEXT_6')
    }
    return BOWLING_TEXTS[dice]


def football_texts(dice):
    FOOTBALL_TEXTS = {
        1: _('DARTS_BOWLING_BASKET_FOOTBALL_TEXT_1'),
        2: _('FOOTBALL_TEXT_LOSE'),
        3: _('FOOTBALL_TEXT_WIN'),
        4: _('FOOTBALL_TEXT_WIN'),
        5: _('FOOTBALL_TEXT_WIN')
    }
    return FOOTBALL_TEXTS[dice]


def cube_texts(lose_streak):
    CUBE_TEXTS = {
        0: _('CUBE_TEXT_0'),
        1: _('CUBE_TEXT_1'),
        2: _('CUBE_TEXT_2'),
        3: _('CUBE_TEXT_3'),
        4: _('CUBE_TEXT_3'),
        5: _('CUBE_TEXT_3'),
        6: _('CUBE_TEXT_3')
    }
    return CUBE_TEXTS[lose_streak]


def numbers_emoji(dice):
    NUMBERS_EMOJI = {
        1: _('DICE_GAMES_NUMBERS_CUBE_EMOJI_1'),
        2: _('DICE_GAMES_NUMBERS_CUBE_EMOJI_2'),
        3: _('DICE_GAMES_NUMBERS_CUBE_EMOJI_3'),
        4: _('DICE_GAMES_NUMBERS_CUBE_EMOJI_4'),
        5: _('DICE_GAMES_NUMBERS_CUBE_EMOJI_5'),
        6: _('DICE_GAMES_NUMBERS_CUBE_EMOJI_6')
    }
    return NUMBERS_EMOJI[dice]
