import unittest

from source.logic.brute_forcer import BruteForcer
from source.data.knowledge import Knowledge
from source.data.knowledge_table import KnowledgeTable
from source.data.rumour import Rumour
from source.data.session import Session
from test.fixture.context import context_fixture, Cards, tom, menno, michiel


class TestBruteForcer(unittest.TestCase):
    def setUp(self) -> None:
        context = context_fixture
        self.empty_brute_forcer = BruteForcer(Session(context),
                                              KnowledgeTable(context.players, context.cards))

        knowledge_table = KnowledgeTable(context.players, context.cards)
        tom_cards = [Cards.BLAAUWVANDRAET, Cards.BUBBELBAD, Cards.BIJL, Cards.HALTER]
        menno_cards = [Cards.ROODHART, Cards.ZITKAMER, Cards.KNUPPEL, Cards.GASTENVERBLIJF]
        michiel_cards = [Cards.DEWIT, Cards.THEATER, Cards.TOUW]
        for card in tom_cards:
            knowledge_table.set(tom, card, Knowledge.TRUE)
        for card in menno_cards:
            knowledge_table.set(menno, card, Knowledge.TRUE)
        for card in michiel_cards:
            knowledge_table.set(michiel, card, Knowledge.TRUE)
        self.half_full_brute_forcer = BruteForcer(Session(context), knowledge_table)

    def test_has_solution_empty_state(self):
        self.assertTrue(self.empty_brute_forcer.has_solution())

    def test_has_solution_only_rumours(self):
        brute_forcer = self.empty_brute_forcer
        brute_forcer.session.add_rumour(
            Rumour(
                tom,
                [Cards.KANDELAAR, Cards.BUBBELBAD, Cards.DEWIT],
                [
                    (menno, Knowledge.FALSE),
                    (michiel, Knowledge.TRUE)
                ]
            )
        )
        brute_forcer.session.add_rumour(
            Rumour(
                menno,
                [Cards.HALTER, Cards.HAL, Cards.PIMPEL],
                [
                    (tom, Knowledge.TRUE),
                    (michiel, Knowledge.FALSE)
                ]
            )
        )
        self.assertTrue(brute_forcer.has_solution())

    def test_has_solution_false_negative(self):
        brute_forcer = self.half_full_brute_forcer
        brute_forcer.session.add_rumour(
            Rumour(
                tom,
                [Cards.KNUPPEL, Cards.BUBBELBAD, Cards.BLAAUWVANDRAET],
                [
                    (menno, Knowledge.FALSE),
                    (michiel, Knowledge.TRUE)
                ]
            )
        )
        self.assertFalse(brute_forcer.has_solution())

    def test_has_solution_false_positive(self):
        brute_forcer = self.half_full_brute_forcer
        brute_forcer.session.add_rumour(
            Rumour(
                tom,
                [Cards.BIJL, Cards.BUBBELBAD, Cards.BLAAUWVANDRAET],
                [
                    (menno, Knowledge.FALSE),
                    (michiel, Knowledge.TRUE)
                ]
            )
        )
        brute_forcer.knowledge_table.set(michiel, Cards.BIJL, Knowledge.FALSE)
        brute_forcer.knowledge_table.set(michiel, Cards.BUBBELBAD, Knowledge.FALSE)
        brute_forcer.knowledge_table.set(michiel, Cards.BLAAUWVANDRAET, Knowledge.FALSE)
        self.assertFalse(brute_forcer.has_solution())

    def test_has_solution_too_many_cards(self):
        brute_forcer = self.half_full_brute_forcer
        brute_forcer.session.add_rumour(
            Rumour(
                tom,
                [Cards.BLAAUWVANDRAET, Cards.BUBBELBAD, Cards.MES],
                [(menno, Knowledge.TRUE)]
            )
        )
        brute_forcer.session.add_rumour(
            Rumour(
                tom,
                [Cards.BLAAUWVANDRAET, Cards.BUBBELBAD, Cards.KANDELAAR],
                [(menno, Knowledge.TRUE)]
            )
        )
        brute_forcer.knowledge_table.set(menno, Cards.PISTOOL, Knowledge.TRUE)
        self.assertFalse(brute_forcer.has_solution())

