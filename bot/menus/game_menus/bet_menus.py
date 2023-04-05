from bot import texts
from bot.menus.game_menus.bet_menu import game_menu_base
from bot.utils.rounding import round_down


def bet_menu(bet, balances, token_icon, token_id, game_mode=None):
    balances = round_down(balances, 2)

    if game_mode == "casino":
        return game_menu_base(balances, bet, token_icon=token_icon, token_id=token_id,
                              play_text=texts.SLOTS_PLAY_TEXT)
    if game_mode == "FOOTBALL":
        return game_menu_base(balances, bet, token_icon=token_icon, token_id=token_id,
                              play_text=texts.FOOTBALL_PLAY_TEXT)
    if game_mode == "DARTS":
        return game_menu_base(balances, bet, token_icon=token_icon, token_id=token_id,
                              play_text=texts.DARTS_PLAY_TEXT)

    if game_mode == "CUBE":
        return game_menu_base(balances, bet, token_icon=token_icon, token_id=token_id,
                              play_text=texts.CUBE_PLAY_TEXT, back_to='game_settings')

    return game_menu_base(balances, bet, token_icon=token_icon, token_id=token_id)
