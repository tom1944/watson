from gameconfig import loadGameConfig
from gamestate import GameState
from card import allCards
import io

if __name__ == "__main__":
    players, open_card, your_cards = loadGameConfig()

    # todo: remove open cards from all cards
    game_state = GameState(players, allCards)

    while True:
        rumour = io.get_info()
        game_state.add_rumour(rumour)
        io.print_gamestate(game_state)
