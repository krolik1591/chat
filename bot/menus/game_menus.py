from bot import texts
from .game_menu_base import game_menu_base


def get_game_menu(bet, balances, token_icon, game_mode=None):

    if game_mode == "SLOTS":
        return game_menu_base(balances, bet, token_icon=token_icon,
                              play_text=texts.SLOTS_PLAY_TEXT)
    if game_mode == "FOOTBALL":
        return game_menu_base(balances, bet, token_icon=token_icon,
                              play_text=texts.FOOTBALL_PLAY_TEXT)
    if game_mode == "DARTS":
        return game_menu_base(balances, bet, token_icon=token_icon,
                              play_text=texts.DARTS_PLAY_TEXT)

    return game_menu_base(balances, bet)
