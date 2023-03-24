from bot import texts
from bot.menus.game_menus.game_menu_base import game_menu_base


def get_game_menu(bet, balances, token_icon, token_id, game_mode=None):
    balances = round(balances, 2)

    if game_mode == "SLOTS":
        return game_menu_base(balances, bet, token_icon=token_icon, token_id=token_id,
                              play_text=texts.SLOTS_PLAY_TEXT)
    if game_mode == "FOOTBALL":
        return game_menu_base(balances, bet, token_icon=token_icon, token_id=token_id,
                              play_text=texts.FOOTBALL_PLAY_TEXT)
    if game_mode == "DARTS":
        return game_menu_base(balances, bet, token_icon=token_icon, token_id=token_id,
                              play_text=texts.DARTS_PLAY_TEXT)

    return game_menu_base(balances, bet, token_icon=token_icon, token_id=token_id)
