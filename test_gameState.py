from unittest import TestCase
from gamestate import GameState, Rumour
from gameconfig import load_game_config
from card import allCards, Category
from user_io import match_card
from knowledge import Knowledge


def init_game_state():
    test_game_config = load_game_config()
    used_cards = [c for c in test_game_config.all_cards if c not in test_game_config.open_cards]
    return GameState(test_game_config.players, used_cards)


class TestGameState(TestCase):
    def test_add_card(self):
        game_state = init_game_state()
        test_card = match_card("Knuppel")
        test_player = game_state.players[0]
        game_state.add_card(test_player, test_card, Knowledge.TRUE)
        for player in game_state.players:
            knowledge = game_state.knowledge_tables[Category.WEAPON][player][test_card]
            if player == test_player:
                self.assertEqual(knowledge, Knowledge.TRUE)
            else:
                self.assertEqual(knowledge, Knowledge.FALSE)

    def test_add_rumour(self):
        game_state = init_game_state()
        test_player = game_state.players[1]

        game_state.add_card(game_state.players[2], match_card("Kandelaar"), Knowledge.FALSE)
        game_state.add_card(game_state.players[2], match_card("Hal"), Knowledge.FALSE)

        test_weapon = match_card("Kandelaar")
        test_room = match_card("Hal")
        test_character = match_card("Pimpel")

        test_replies = [(game_state.players[0], Knowledge.FALSE), (game_state.players[2], Knowledge.TRUE)]
        test_rumour = Rumour(test_player, test_weapon, test_room, test_character, test_replies)

        game_state.add_rumour(test_rumour)
