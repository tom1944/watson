from gameconfig import loadGameConfig
from gamestate import GameState
from card import allCards
import user_io

if __name__ == "__main__":
    players, open_cards, your_cards = loadGameConfig()

    used_cards = [c for c in allCards if c not in open_cards]
    game_state = GameState(players, used_cards)
    # todo: add cards of current player

    while True:
        rumour = user_io.get_info()
        game_state.add_rumour(rumour)
        user_io.print_game_state(game_state)
