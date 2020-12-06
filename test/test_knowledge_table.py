from unittest import TestCase

from card import Cards
from knowledge import Knowledge
from knowledge_table import KnowledgeTable
from load_game_state import load_game_state


class TestKnowledgeTable(TestCase):
    def setUp(self):
        self.game_state = load_game_state('test/game_config.json')
        self.some_player = self.game_state.players[0]
        self.knowledge_table = KnowledgeTable(self.game_state.players, self.game_state.cards)

    def test_new_knowledge_table(self):
        for player in self.game_state.players:
            for card in self.game_state.cards:
                self.assertEqual(self.knowledge_table[player, card], Knowledge.MAYBE)
                self.assertEqual(self.knowledge_table.get_knowledge(player, card), Knowledge.MAYBE)

    def test_set(self):
        self.knowledge_table[self.some_player, Cards.KNUPPEL] = Knowledge.TRUE
        self.assertEqual(
            self.knowledge_table[self.some_player, Cards.KNUPPEL],
            Knowledge.TRUE
        )

    def test_invalid_overwrite_table(self):
        self.knowledge_table[self.some_player, Cards.KNUPPEL] = Knowledge.TRUE
        with self.assertRaises(ValueError):
            self.knowledge_table[self.some_player, Cards.KNUPPEL] = Knowledge.FALSE

    def test_set_without_check(self):
        self.knowledge_table[self.some_player, Cards.KNUPPEL] = Knowledge.TRUE
        self.knowledge_table.set_item_without_check(self.some_player, Cards.KNUPPEL, Knowledge.FALSE)

    def test_invalid_get(self):
        player = self.game_state.players[0]
        card = self.game_state.cards[0]

        with self.assertRaises(TypeError):
            self.knowledge_table[card, player] = Knowledge.TRUE

    def test_get_current_player_hands(self):
        knowledge_table = self.knowledge_table

        for player in self.game_state.players:
            knowledge_table[player, Cards.KNUPPEL] = Knowledge.FALSE

        knowledge_table[self.some_player, Cards.TOUW] = Knowledge.TRUE

        player_hands, murderer_cards, free_cards = knowledge_table.get_current_player_hands()

        self.assertIn(Cards.KNUPPEL, murderer_cards)
        self.assertIn(Cards.TOUW, player_hands[self.some_player])
        self.assertIn(Cards.PIMPEL, free_cards)


