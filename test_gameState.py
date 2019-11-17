from unittest import TestCase
from gamestate import GameState, Rumour
from gameconfig import loadGameConfig
from card import allCards, Category
from user_io import match_card
from knowledge import Knowledge


def init_test():
    players, open_cards, your_cards = loadGameConfig()
    used_cards = [c for c in allCards if c not in open_cards]
    return GameState(players, used_cards)


class TestGameState(TestCase):
    def test_add_card(self):
        game_state = init_test()
        test_card = match_card("knuppel")
        test_player = game_state.players[0]
        game_state.add_card(test_player, test_card, Knowledge.TRUE)
        for player in game_state.players:
            knowledge = game_state.knowledge_tables[Category.WEAPON][player][test_card]
            if player == test_player:
                self.assertEqual(knowledge, Knowledge.TRUE)
            else:
                self.assertEqual(knowledge, Knowledge.FALSE)

    def test_add_rumour(self):
        game_state = init_test()
        test_player = game_state.players[1]
        test_weapon = match_card("kandelaar")
        test_room = match_card("hal")
        test_character = match_card("Pimpel")
        test_replies = [(game_state.players[0], Knowledge.FALSE), (game_state.players[2], Knowledge.FALSE)]
        test_rumour = Rumour(test_player, test_weapon, test_room, test_character, test_replies)
        game_state.add_rumour(test_rumour)
        test_line = 1

    def test_deduce(self):
        self.fail()