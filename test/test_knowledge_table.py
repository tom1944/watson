from unittest import TestCase

from load_game_config import load_game_config
from test.fixture.context import Cards
from knowledge import Knowledge
from knowledge_table import KnowledgeTable


class TestKnowledgeTable(TestCase):
    def setUp(self):
        context, session = load_game_config('test/fixture/game_config.json')
        self.context = context
        self.some_player = self.context.players[0]
        self.knowledge_table = KnowledgeTable(self.context.players, self.context.cards)

    def test_new_knowledge_table(self):
        for player in self.context.players:
            for card in self.context.cards:
                self.assertEqual(self.knowledge_table.get(player, card), Knowledge.MAYBE)

    def test_set(self):
        self.knowledge_table.set(self.some_player, Cards.KNUPPEL, Knowledge.TRUE)
        self.assertEqual(
            self.knowledge_table.get(self.some_player, Cards.KNUPPEL),
            Knowledge.TRUE
        )

    def test_invalid_set(self):
        self.knowledge_table.set(self.some_player, Cards.KNUPPEL, Knowledge.TRUE)
        with self.assertRaises(ValueError):
            self.knowledge_table.set(self.some_player, Cards.KNUPPEL, Knowledge.FALSE)

    def test_set_forcefully(self):
        self.knowledge_table.set(self.some_player, Cards.KNUPPEL, Knowledge.TRUE)
        self.knowledge_table.set_forcefully(self.some_player, Cards.KNUPPEL, Knowledge.FALSE)

    def test_current_player_hands(self):
        knowledge_table = self.knowledge_table

        for player in self.context.players:
            knowledge_table.set(player, Cards.KNUPPEL, Knowledge.FALSE)

        knowledge_table.set(self.some_player, Cards.TOUW, Knowledge.TRUE)

        player_hands, murderer_cards, free_cards = knowledge_table.current_player_hands()

        self.assertIn(Cards.KNUPPEL, murderer_cards)
        self.assertIn(Cards.TOUW, player_hands[self.some_player])
        self.assertIn(Cards.PIMPEL, free_cards)


