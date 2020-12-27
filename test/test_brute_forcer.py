import unittest

from source.data.knowledge import Knowledge
from source.data.knowledge_table import KnowledgeTable
from source.data.rumour import Rumour
from source.data.clues import Clues
from source.logic.brute_forcer import BruteForcer
from test.fixture.context import context_fixture, tom, Cards, menno, michiel


class TestBruteForcer(unittest.TestCase):
    def setUp(self) -> None:
        self.knowledge_table = KnowledgeTable(context_fixture.players, context_fixture.cards)
        self.clues = Clues(context_fixture)
        self.empty_brute_forcer = BruteForcer(self.clues, self.knowledge_table)

    def test_brute_force_on_card_empty_state(self):
        self.assertEqual(Knowledge.MAYBE, self.empty_brute_forcer.brute_force_on_card(tom, Cards.MES))

    def test_brute_force_on_card_with_true_result(self):
        brute_forcer = self.empty_brute_forcer
        knowledge_table = self.knowledge_table
        clues = self.clues

        clues.add_rumour(
            Rumour(
                tom,
                [Cards.ROODHART, Cards.MES, Cards.EETKAMER],
                [
                    (menno, Knowledge.TRUE)
                ]
            )
        )
        knowledge_table.set(menno, Cards.ROODHART, Knowledge.FALSE)
        knowledge_table.set(menno, Cards.MES, Knowledge.FALSE)

        # For speed:
        tom_cards = [Cards.DEWIT, Cards.BUBBELBAD, Cards.BIJL, Cards.KEUKEN]
        menno_cards = [Cards.BLAAUWVANDRAET, Cards.HAL, Cards.HALTER, Cards.KANDELAAR]
        michiel_cards = [Cards.PISTOOL, Cards.GASTENVERBLIJF, Cards.KNUPPEL, Cards.THEATER]
        player_cards = {tom: tom_cards, menno: menno_cards, michiel: michiel_cards}
        for player in [tom, menno, michiel]:
            for card in player_cards[player]:
                knowledge_table.set(player, card, Knowledge.TRUE)
        self.assertEqual(Knowledge.TRUE, brute_forcer.brute_force_on_card(menno, Cards.EETKAMER))

    def test_brute_force_on_card_with_false_result(self):
        brute_forcer = self.empty_brute_forcer
        clues = self.clues

        clues.add_rumour(
            Rumour(
                tom,
                [Cards.ROODHART, Cards.MES, Cards.EETKAMER],
                [
                    (menno, Knowledge.FALSE)
                ]
            )
        )
        self.assertEqual(Knowledge.FALSE, brute_forcer.brute_force_on_card(menno, Cards.EETKAMER))
