import unittest

from source.logic.deriver import Deriver
from source.data.knowledge import Knowledge
from source.data.knowledge_table import KnowledgeTable
from source.data.rumour import Rumour
from source.data.session import Session
from test.fixture.context import context_fixture, Cards, tom, menno, michiel


class TestDeriver(unittest.TestCase):
    def setUp(self) -> None:
        session = Session(context_fixture)
        self.context = session.get_context()
        self.empty_knowledge_table = KnowledgeTable(self.context.players, self.context.cards)
        self.empty_deriver = Deriver(session, self.empty_knowledge_table)

    def test_inspect_clauses(self):
        deriver = self.empty_deriver
        knowledge_table = self.empty_knowledge_table
        deriver.derive_from_new_rumour(
            Rumour(
                tom,
                [Cards.KANDELAAR, Cards.BUBBELBAD, Cards.DEWIT],
                [
                    (menno, Knowledge.TRUE),
                ]
            )
        )
        knowledge_table.set(menno, Cards.KANDELAAR, Knowledge.FALSE)
        knowledge_table.set(menno, Cards.BUBBELBAD, Knowledge.FALSE)
        deriver.derive_from_new_knowledge(menno, Cards.KANDELAAR)
        deriver.derive_from_new_knowledge(menno, Cards.BUBBELBAD)
        deriver.inspect_clauses()
        self.assertEqual(Knowledge.TRUE, knowledge_table.get(menno, Cards.DEWIT))

    def test_derive_from_new_rumour_with_positive_reply_with_two_not_owned(self):
        deriver = self.empty_deriver
        knowledge_table = self.empty_knowledge_table
        knowledge_table.set(menno, Cards.KANDELAAR, Knowledge.FALSE)
        knowledge_table.set(menno, Cards.BUBBELBAD, Knowledge.FALSE)
        deriver.derive_from_new_rumour(
            Rumour(
                tom,
                [Cards.KANDELAAR, Cards.BUBBELBAD, Cards.DEWIT],
                [
                    (menno, Knowledge.TRUE),
                ]
            )
        )
        clauses = deriver.get_clauses().get_clauses(menno)
        self.assertEqual(0, len(clauses))
        self.assertEqual(Knowledge.TRUE, knowledge_table.get(menno, Cards.DEWIT))

    def test_derive_from_new_rumour_with_positive_reply_with_card_owned(self):
        deriver = self.empty_deriver
        knowledge_table = self.empty_knowledge_table
        knowledge_table.set(menno, Cards.KANDELAAR, Knowledge.TRUE)
        deriver.derive_from_new_rumour(
            Rumour(
                tom,
                [Cards.KANDELAAR, Cards.BUBBELBAD, Cards.DEWIT],
                [
                    (menno, Knowledge.TRUE),
                ]
            )
        )
        clauses = deriver.get_clauses().get_clauses(menno)
        self.assertEqual(0, len(clauses))

    def test_derive_from_new_rumour_with_positive_reply_empty_knowledge_table(self):
        deriver = self.empty_deriver
        deriver.derive_from_new_rumour(
            Rumour(
                tom,
                [Cards.KANDELAAR, Cards.BUBBELBAD, Cards.DEWIT],
                [
                    (menno, Knowledge.TRUE),
                ]
            )
        )
        clauses = deriver.get_clauses().get_clauses(menno)
        self.assertEqual([Cards.KANDELAAR, Cards.BUBBELBAD, Cards.DEWIT], clauses[0])

    def test_derive_from_new_rumour_with_negative_reply(self):
        deriver = self.empty_deriver
        knowledge_table = self.empty_knowledge_table
        deriver.derive_from_new_rumour(
            Rumour(
                tom,
                [Cards.KANDELAAR, Cards.BUBBELBAD, Cards.DEWIT],
                [
                    (menno, Knowledge.FALSE),
                ]
            )
        )
        self.assertEqual(Knowledge.FALSE, knowledge_table.get(menno, Cards.KANDELAAR))
        self.assertEqual(Knowledge.FALSE, knowledge_table.get(menno, Cards.BUBBELBAD))
        self.assertEqual(Knowledge.FALSE, knowledge_table.get(menno, Cards.DEWIT))

    def test_create_clause_with_one_card_owned(self):
        deriver = self.empty_deriver
        deriver.knowledge_table.set(menno, Cards.KANDELAAR, Knowledge.TRUE)
        self.assertEqual([],
                         deriver.create_clause(menno, [Cards.KANDELAAR, Cards.BUBBELBAD, Cards.DEWIT]))

    def test_create_clause_for_two_new_cards(self):
        deriver = self.empty_deriver
        deriver.knowledge_table.set(menno, Cards.KANDELAAR, Knowledge.FALSE)
        self.assertEqual([Cards.BUBBELBAD, Cards.DEWIT],
                         deriver.create_clause(menno, [Cards.KANDELAAR, Cards.BUBBELBAD, Cards.DEWIT]))

    def test_create_clause_for_three_new_cards(self):
        deriver = self.empty_deriver
        self.assertEqual([Cards.KANDELAAR, Cards.BUBBELBAD, Cards.DEWIT],
                         deriver.create_clause(menno, [Cards.KANDELAAR, Cards.BUBBELBAD, Cards.DEWIT]))

    def test_derive_new_true_knowledge_max_cards(self):
        deriver = self.empty_deriver
        knowledge_table = self.empty_knowledge_table
        knowledge_table.set(michiel, Cards.MES, Knowledge.TRUE)
        knowledge_table.set(michiel, Cards.BIJL, Knowledge.TRUE)
        knowledge_table.set(michiel, Cards.KEUKEN, Knowledge.TRUE)
        knowledge_table.set(michiel, Cards.GASTENVERBLIJF, Knowledge.TRUE)
        knowledge_table.set(michiel, Cards.PISTOOL, Knowledge.TRUE)
        knowledge_table.set(michiel, Cards.KANDELAAR, Knowledge.TRUE)
        deriver.derive_new_true_knowledge(michiel, Cards.MES)
        deriver.derive_new_true_knowledge(michiel, Cards.BIJL)
        deriver.derive_new_true_knowledge(michiel, Cards.KEUKEN)
        deriver.derive_new_true_knowledge(michiel, Cards.GASTENVERBLIJF)
        deriver.derive_new_true_knowledge(michiel, Cards.PISTOOL)
        deriver.derive_new_true_knowledge(michiel, Cards.KANDELAAR)

        for player in deriver.context.players:
            for card in deriver.context.cards:
                if card in [Cards.MES, Cards.BIJL, Cards.KEUKEN, Cards.GASTENVERBLIJF, Cards.PISTOOL, Cards.KANDELAAR]:
                    if player == michiel:
                        self.assertEqual(Knowledge.TRUE, knowledge_table.get(player, card))
                    else:
                        self.assertEqual(Knowledge.FALSE, knowledge_table.get(player, card))
                elif player == michiel:
                    self.assertEqual(Knowledge.FALSE, knowledge_table.get(player, card))
                else:
                    self.assertEqual(Knowledge.MAYBE, knowledge_table.get(player, card))

    def test_derive_new_true_knowledge_exclusion(self):
        deriver = self.empty_deriver
        knowledge_table = self.empty_knowledge_table
        knowledge_table.set(menno, Cards.KEUKEN, Knowledge.TRUE)
        deriver.derive_new_true_knowledge(menno, Cards.KEUKEN)
        for player in deriver.context.players:
            for card in deriver.context.cards:
                if card == Cards.KEUKEN:
                    if player == menno:
                        self.assertEqual(Knowledge.TRUE, knowledge_table.get(player, card))
                    else:
                        self.assertEqual(Knowledge.FALSE, knowledge_table.get(player, card))
                else:
                    self.assertEqual(Knowledge.MAYBE, knowledge_table.get(player, card))

    def test_nr_of_known_cards_without_cards(self):
        for player in self.context.players:
            self.assertEqual(0, self.empty_deriver.nr_known_cards(player))

    def test_nr_of_known_cards_with_cards(self):
        knowledge_table = self.empty_knowledge_table
        knowledge_table.set(tom, Cards.MES, Knowledge.TRUE)
        knowledge_table.set(tom, Cards.BIJL, Knowledge.TRUE)
        knowledge_table.set(tom, Cards.GASTENVERBLIJF, Knowledge.FALSE)
        self.assertEqual(2, self.empty_deriver.nr_known_cards(tom))

    def test_set_other_cards_to_false_with_only_maybe(self):
        self.empty_deriver.set_other_cards_to_false(menno)
        for card in self.empty_deriver.context.cards:
            self.assertEqual(Knowledge.FALSE, self.empty_deriver.knowledge_table.get(menno, card))

    def test_set_other_cards_to_false_with_some_true(self):
        deriver = self.empty_deriver
        knowledge_table = self.empty_knowledge_table
        knowledge_table.set(michiel, Cards.MES, Knowledge.TRUE)
        knowledge_table.set(michiel, Cards.BIJL, Knowledge.TRUE)
        deriver.set_other_cards_to_false(michiel)
        for card in deriver.context.cards:
            if card == Cards.BIJL or card == Cards.MES:
                self.assertEqual(Knowledge.TRUE, deriver.knowledge_table.get(michiel, card))
            else:
                self.assertEqual(Knowledge.FALSE, deriver.knowledge_table.get(michiel, card))
