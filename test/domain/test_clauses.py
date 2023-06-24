import unittest

from source.domain.clauses import Clauses
from test.fixture.context import context_fixture, michiel, Cards, menno


class TestClauses(unittest.TestCase):
    def setUp(self) -> None:
        self.clauses = Clauses(context_fixture)

    def test_add_knowledge_with_true_knowledge(self):
        clauses = self.clauses
        clauses.add_clause(michiel, [Cards.BLAAUWVANDRAET, Cards.BIJL])
        clauses.add_clause(michiel, [Cards.BLAAUWVANDRAET, Cards.ROODHART])
        clauses.add_clause(michiel, [Cards.HALTER, Cards.KEUKEN])
        clauses.add_clause(menno, [Cards.BLAAUWVANDRAET, Cards.HAL])

        clauses.add_true_knowledge(michiel, Cards.BLAAUWVANDRAET)

        self.assertEqual([Cards.HALTER, Cards.KEUKEN], clauses.get_clauses(michiel)[0])
        self.assertEqual([Cards.HAL], clauses.get_clauses(menno)[0])

    def test_add_knowledge_with_false_knowledge(self):
        clauses = self.clauses
        clauses.add_clause(michiel, [Cards.BLAAUWVANDRAET, Cards.BIJL])
        clauses.add_clause(michiel, [Cards.BLAAUWVANDRAET, Cards.ROODHART])
        clauses.add_clause(michiel, [Cards.HALTER, Cards.KEUKEN])
        clauses.add_clause(menno, [Cards.BLAAUWVANDRAET, Cards.HAL])

        clauses.add_false_knowledge(michiel, Cards.BLAAUWVANDRAET)

        self.assertEqual([Cards.BIJL], clauses.get_clauses(michiel)[0])
        self.assertEqual([Cards.ROODHART], clauses.get_clauses(michiel)[1])
        self.assertEqual([Cards.HALTER, Cards.KEUKEN], clauses.get_clauses(michiel)[2])
        self.assertEqual([Cards.BLAAUWVANDRAET, Cards.HAL], clauses.get_clauses(menno)[0])

    def test_remove_empty_clauses(self):
        clauses = self.clauses
        clauses.add_clause(michiel, [Cards.BLAAUWVANDRAET, Cards.BIJL])
        clauses.add_clause(michiel, [])
        clauses.add_clause(menno, [])
        clauses.add_clause(menno, [])
        clauses.remove_empty_clauses()
        self.assertEqual(0, len(clauses.get_clauses(menno)))
        self.assertEqual([Cards.BLAAUWVANDRAET, Cards.BIJL], clauses.get_clauses(michiel)[0])

    def test_empty_clause_that_has_card(self):
        clauses = self.clauses
        clauses.add_clause(michiel, [Cards.BLAAUWVANDRAET, Cards.BIJL])
        clauses.add_clause(michiel, [Cards.BLAAUWVANDRAET, Cards.ROODHART])
        clauses.add_clause(michiel, [Cards.HALTER, Cards.KEUKEN])
        clauses.empty_clause_that_has_card(michiel, Cards.BLAAUWVANDRAET)
        self.assertEqual([], clauses.get_clauses(michiel)[0])
        self.assertEqual([], clauses.get_clauses(michiel)[1])
        self.assertEqual([Cards.HALTER, Cards.KEUKEN], clauses.get_clauses(michiel)[2])

    def test_remove_card_from_clauses(self):
        clauses = self.clauses
        clauses.add_clause(michiel, [Cards.BLAAUWVANDRAET, Cards.BIJL])
        clauses.add_clause(michiel, [Cards.BLAAUWVANDRAET, Cards.ROODHART])
        clauses.add_clause(michiel, [Cards.HALTER, Cards.KEUKEN])
        clauses.remove_card_from_clauses(michiel, Cards.BLAAUWVANDRAET)
        self.assertEqual([Cards.BIJL], clauses.get_clauses(michiel)[0])
        self.assertEqual([Cards.ROODHART], clauses.get_clauses(michiel)[1])
        self.assertEqual([Cards.HALTER, Cards.KEUKEN], clauses.get_clauses(michiel)[2])
