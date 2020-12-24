import unittest

from source.data.knowledge import Knowledge
from source.data.knowledge_table import KnowledgeTable
from source.data.rumour import Rumour
from source.data.session import Session
from source.logic.solution_finder import SolutionFinder
from test.fixture.context import context_fixture, Cards, tom, menno, michiel


class TestSolutionFinder(unittest.TestCase):
    def setUp(self) -> None:
        context = context_fixture
        self.empty_solution_finder = SolutionFinder(Session(context),
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
        self.half_full_solution_finder = SolutionFinder(Session(context), knowledge_table)

    def test_possible_solution_empty_state(self):
        self.assertFalse(self.empty_solution_finder.find_possible_solution() is None)

    def test_possible_solution_only_rumours(self):
        solution_finder = self.empty_solution_finder
        solution_finder.session.add_rumour(
            Rumour(
                tom,
                [Cards.KANDELAAR, Cards.BUBBELBAD, Cards.DEWIT],
                [
                    (menno, Knowledge.FALSE),
                    (michiel, Knowledge.TRUE)
                ]
            )
        )
        solution_finder.session.add_rumour(
            Rumour(
                menno,
                [Cards.HALTER, Cards.HAL, Cards.PIMPEL],
                [
                    (tom, Knowledge.TRUE),
                    (michiel, Knowledge.FALSE)
                ]
            )
        )
        self.assertFalse(solution_finder.find_possible_solution() is None)

    def test_has_solution_false_negative(self):
        solution_finder = self.half_full_solution_finder
        solution_finder.session.add_rumour(
            Rumour(
                tom,
                [Cards.KNUPPEL, Cards.BUBBELBAD, Cards.BLAAUWVANDRAET],
                [
                    (menno, Knowledge.FALSE),
                    (michiel, Knowledge.TRUE)
                ]
            )
        )
        self.assertEqual(None, solution_finder.find_possible_solution())

    def test_has_solution_false_positive(self):
        solution_finder = self.half_full_solution_finder
        solution_finder.session.add_rumour(
            Rumour(
                tom,
                [Cards.BIJL, Cards.BUBBELBAD, Cards.BLAAUWVANDRAET],
                [
                    (menno, Knowledge.FALSE),
                    (michiel, Knowledge.TRUE)
                ]
            )
        )
        solution_finder.knowledge_table.set(michiel, Cards.BIJL, Knowledge.FALSE)
        solution_finder.knowledge_table.set(michiel, Cards.BUBBELBAD, Knowledge.FALSE)
        solution_finder.knowledge_table.set(michiel, Cards.BLAAUWVANDRAET, Knowledge.FALSE)
        self.assertEqual(None, solution_finder.find_possible_solution())

    def test_has_solution_too_many_cards(self):
        solution_finder = self.half_full_solution_finder
        solution_finder.session.add_rumour(
            Rumour(
                tom,
                [Cards.BLAAUWVANDRAET, Cards.BUBBELBAD, Cards.MES],
                [(menno, Knowledge.TRUE)]
            )
        )
        solution_finder.session.add_rumour(
            Rumour(
                tom,
                [Cards.BLAAUWVANDRAET, Cards.BUBBELBAD, Cards.KANDELAAR],
                [(menno, Knowledge.TRUE)]
            )
        )
        solution_finder.knowledge_table.set(menno, Cards.PISTOOL, Knowledge.TRUE)
        self.assertEqual(None, solution_finder.find_possible_solution())
