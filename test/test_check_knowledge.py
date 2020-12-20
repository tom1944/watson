import unittest

from check_knowledge import check_knowledge
from knowledge import Knowledge
from knowledge_table import KnowledgeTable
from rumour import Rumour
from session import Session
from test.fixture.context import context_fixture, Cards, tom, menno, michiel


class TestCheckKnowledge(unittest.TestCase):
    def setUp(self) -> None:
        context = context_fixture
        self.empty_session = Session(context)

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

    def test_empty_session(self):
        session = self.empty_session
        context = session.get_context()
        self.assertTrue(check_knowledge(KnowledgeTable(context.players, context.cards), session))

    def test_small_game(self):
        session = self.empty_session

        session.rumours = [
            Rumour(
                tom,
                [Cards.MES, Cards.THEATER, Cards.BLAAUWVANDRAET],
                [
                    (menno, Knowledge.FALSE),
                    (michiel, Knowledge.TRUE),
                ]
            )
        ]

        self.assertTrue(check_knowledge(self.small_knowledge_table, session))

    def test_false_negative_reply(self):
        # tom lies about not having MES
        session = self.empty_session
        session.rumours.append(
            Rumour(
                menno,
                [Cards.MES, Cards.THEATER, Cards.BLAAUWVANDRAET],
                [
                    (tom, Knowledge.FALSE),
                ]
            )
        )

        self.assertFalse(check_knowledge(self.small_knowledge_table, session))

    def test_false_positive_reply(self):
        # michiel lies about having any of the cards
        session = self.empty_session
        knowledge_table = self.small_knowledge_table

        session.rumours = [
            Rumour(
                tom,
                [Cards.MES, Cards.BUBBELBAD, Cards.PIMPEL],
                [
                    (menno, Knowledge.FALSE),
                    (michiel, Knowledge.TRUE),
                ]
            )
        ]
        self.assertFalse(check_knowledge(knowledge_table, session))

    def test_direct_card_amount_contradiction(self):
        knowledge_table = self.tom_full_knowledge_table
        knowledge_table.set(tom, Cards.HAL, Knowledge.TRUE)
        self.assertFalse(check_knowledge(knowledge_table, self.empty_session))

    def test_indirect_card_amount_contradiction(self):
        knowledge_table = self.tom_full_knowledge_table
        session = self.empty_session

        # Should not yet be contradictory
        self.assertTrue(check_knowledge(knowledge_table, session))

        session.rumours.append(
            Rumour(
                menno,
                [Cards.HALTER, Cards.ZITKAMER, Cards.ROODHART],
                [
                    (tom, Knowledge.TRUE),
                ]
            )
        )

        self.assertFalse(check_knowledge(knowledge_table, session))

    def test_additional_player_hands(self):
        session = self.empty_session
        knowledge_table = self.small_knowledge_table
        session.rumours = [
            Rumour(
                tom,
                [Cards.MES, Cards.THEATER, Cards.BLAAUWVANDRAET],
                [
                    (menno, Knowledge.FALSE),
                    (michiel, Knowledge.TRUE),
                ]
            )
        ]
        player_hands = {p: [] for p in session.context.players}
        # Should not yet be contradictory
        self.assertTrue(check_knowledge(knowledge_table, session, player_hands))

        player_hands[menno].append(Cards.BLAAUWVANDRAET)
        self.assertFalse(check_knowledge(knowledge_table, session, player_hands))
