from bot import texts
from bot.menus.base_game_menu import base_game_menu


def get_game_menu(bet, balance, game_mode=None, is_demo=True):
    funds_icon = texts.DEMO_FUNDS_ICON if is_demo else texts.TON_FUNDS_ICON

    if game_mode == "SLOTS":
        return base_game_menu(balance, bet, funds_icon=funds_icon,
                              play_text=texts.SLOTS_PLAY_TEXT)
    if game_mode == "FOOTBALL":
        return base_game_menu(balance, bet, funds_icon=funds_icon,
                              play_text=texts.FOOTBALL_PLAY_TEXT)
    if game_mode == "DARTS":
        return base_game_menu(balance, bet, funds_icon=funds_icon,
                              play_text=texts.DARTS_PLAY_TEXT)

    return base_game_menu(balance, bet)
