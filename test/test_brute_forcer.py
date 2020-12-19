import unittest

from brute_forcer import BruteForcer
from knowledge import Knowledge
from knowledge_table import KnowledgeTable
from rumour import Rumour
from session import Session
from test.fixture.context import Cards, ctx
from test.fixture.session import ExpectedSession


class TestBruteForcer(unittest.TestCase):

    def setUp(self) -> None:
        self.context = ctx
        players = self.context.players
        knowledge_table = KnowledgeTable(self.context.players, self.context.cards)
        knowledge_table.set(players[0], Cards.MES, Knowledge.TRUE)
        knowledge_table.set(players[1], Cards.MES, Knowledge.FALSE)
        knowledge_table.set(players[2], Cards.MES, Knowledge.FALSE)

        knowledge_table.set(players[0], Cards.BUBBELBAD, Knowledge.FALSE)
        knowledge_table.set(players[1], Cards.BUBBELBAD, Knowledge.TRUE)
        knowledge_table.set(players[2], Cards.BUBBELBAD, Knowledge.FALSE)

        knowledge_table.set(players[2], Cards.PIMPEL, Knowledge.FALSE)

        self.small_knowledge_table = knowledge_table

    def test_smart_check_knowledge(self):
        session = Session(self.context, {}, [])
        knowledge_table = KnowledgeTable(self.context.players, self.context.cards)
        brute_forcer = BruteForcer(session, knowledge_table)
        player_hands = {}
        for player in self.context.players:
            player_hands[player] = []
        unknown_cards = self.context.cards
        self.assertTrue(brute_forcer.smart_check_knowledge(player_hands, unknown_cards))

        session = ExpectedSession.session
        players = self.context.players
        brute_forcer.knowledge_table = self.small_knowledge_table
        player_hands = {}
        for player in players:
            player_hands[player] = []
        unknown_cards = self.context.cards

        brute_forcer.session.rumours = [
            Rumour(
                players[0],
                [Cards.MES, Cards.THEATER, Cards.BLAAUWVANDRAET],
                [
                    (players[1], Knowledge.FALSE),
                    (players[2], Knowledge.TRUE),
                ]
            )
        ]
        self.assertTrue(brute_forcer.smart_check_knowledge(player_hands, unknown_cards))

        brute_forcer.session.rumours.append(
            Rumour(
                players[1],
                [Cards.MES, Cards.THEATER, Cards.BLAAUWVANDRAET],
                [
                    (players[0], Knowledge.FALSE),
                ]
            )
        )
        self.assertFalse(brute_forcer.smart_check_knowledge(player_hands, unknown_cards))

