import unittest

from source.logic.check_knowledge import check_knowledge
from source.domain.knowledge import Knowledge
from source.domain.knowledge_table import KnowledgeTable
from source.domain.rumour import Rumour
from source.domain.clues import Clues
from test.fixture.context import context_fixture, Cards, tom, menno, michiel


class TestCheckKnowledge(unittest.TestCase):
    def setUp(self) -> None:
        context = context_fixture
        self.empty_clues = Clues(context)

        knowledge_table = KnowledgeTable(context.players, context.cards)
        knowledge_table.set(tom, Cards.MES, Knowledge.TRUE)
        knowledge_table.set(menno, Cards.MES, Knowledge.FALSE)
        knowledge_table.set(michiel, Cards.MES, Knowledge.FALSE)

        knowledge_table.set(tom, Cards.BUBBELBAD, Knowledge.FALSE)
        knowledge_table.set(menno, Cards.BUBBELBAD, Knowledge.TRUE)
        knowledge_table.set(michiel, Cards.BUBBELBAD, Knowledge.FALSE)

        knowledge_table.set(michiel, Cards.PIMPEL, Knowledge.FALSE)
        self.small_knowledge_table = knowledge_table

        knowledge_table.set(tom, Cards.THEATER, Knowledge.TRUE)
        knowledge_table.set(tom, Cards.BIJL, Knowledge.TRUE)
        knowledge_table.set(tom, Cards.DEWIT, Knowledge.TRUE)
        knowledge_table.set(tom, Cards.EETKAMER, Knowledge.TRUE)
        knowledge_table.set(tom, Cards.GASTENVERBLIJF, Knowledge.TRUE)
        self.tom_full_knowledge_table = knowledge_table

    def test_empty_clues(self):
        clues = self.empty_clues
        context = clues.get_context()
        self.assertTrue(check_knowledge(KnowledgeTable(context.players, context.cards), clues))

    def test_small_game(self):
        clues = self.empty_clues

        clues.rumours = [
            Rumour(
                tom,
                [Cards.MES, Cards.THEATER, Cards.BLAAUWVANDRAET],
                [
                    (menno, Knowledge.FALSE),
                    (michiel, Knowledge.TRUE),
                ]
            )
        ]

        self.assertTrue(check_knowledge(self.small_knowledge_table, clues))

    def test_false_negative_reply(self):
        # tom lies about not having MES
        clues = self.empty_clues
        clues.rumours.append(
            Rumour(
                menno,
                [Cards.MES, Cards.THEATER, Cards.BLAAUWVANDRAET],
                [
                    (tom, Knowledge.FALSE),
                ]
            )
        )

        self.assertFalse(check_knowledge(self.small_knowledge_table, clues))

    def test_false_positive_reply(self):
        # michiel lies about having any of the cards
        clues = self.empty_clues
        knowledge_table = self.small_knowledge_table

        clues.rumours = [
            Rumour(
                tom,
                [Cards.MES, Cards.BUBBELBAD, Cards.PIMPEL],
                [
                    (menno, Knowledge.FALSE),
                    (michiel, Knowledge.TRUE),
                ]
            )
        ]
        self.assertFalse(check_knowledge(knowledge_table, clues))

    def test_direct_card_amount_contradiction(self):
        knowledge_table = self.tom_full_knowledge_table
        knowledge_table.set(tom, Cards.HAL, Knowledge.TRUE)
        self.assertFalse(check_knowledge(knowledge_table, self.empty_clues))

    def test_indirect_card_amount_contradiction(self):
        knowledge_table = self.tom_full_knowledge_table
        clues = self.empty_clues

        # Should not yet be contradictory
        self.assertTrue(check_knowledge(knowledge_table, clues))

        clues.rumours.append(
            Rumour(
                menno,
                [Cards.HALTER, Cards.ZITKAMER, Cards.ROODHART],
                [
                    (tom, Knowledge.TRUE),
                ]
            )
        )

        self.assertFalse(check_knowledge(knowledge_table, clues))

    def test_additional_player_hands(self):
        clues = self.empty_clues
        knowledge_table = self.small_knowledge_table
        clues.rumours = [
            Rumour(
                tom,
                [Cards.MES, Cards.THEATER, Cards.BLAAUWVANDRAET],
                [
                    (menno, Knowledge.FALSE),
                    (michiel, Knowledge.TRUE),
                ]
            )
        ]
        player_hands = {p: [] for p in clues.context.players}
        # Should not yet be contradictory
        self.assertTrue(check_knowledge(knowledge_table, clues, player_hands))

        player_hands[menno].append(Cards.BLAAUWVANDRAET)
        self.assertFalse(check_knowledge(knowledge_table, clues, player_hands))

    def test_one_murder_card_per_category(self):
        clues = self.empty_clues
        knowledge_table = KnowledgeTable(clues.get_context().players, clues.get_context().cards)
        for player in clues.get_context().players:
            knowledge_table.set(player, Cards.MES, Knowledge.FALSE)
        self.assertTrue(check_knowledge(knowledge_table, clues))
        for player in clues.get_context().players:
            knowledge_table.set(player, Cards.BIJL, Knowledge.FALSE)
        self.assertFalse(check_knowledge(knowledge_table, clues))
