from watson import Watson
from gameconfig import load_game_config


def load_test_watson():
    test_game_config = load_game_config('test/game_config.json')
    return Watson(test_game_config.players, test_game_config.used_cards)
