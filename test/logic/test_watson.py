from unittest import TestCase

from source.domain.clues import Clues
from source.domain.knowledge import Knowledge
from source.domain.rumour import Rumour
from source.logic.watson import Watson
from test.fixture.context import Cards, michiel, menno, context_fixture, tom


class TestWatson(TestCase):
    def setUp(self) -> None:
        context = context_fixture
        self.empty_watson = Watson(context)

    def test_add_card(self):
        watson = self.empty_watson
        watson.add_knowledge(tom, Cards.KNUPPEL, Knowledge.TRUE)

        for player in watson.context.players:
            knowledge = watson.get_knowledge_table().get(player, Cards.KNUPPEL)
            if player == tom:
                self.assertEqual(knowledge, Knowledge.TRUE)
            else:
                self.assertEqual(knowledge, Knowledge.FALSE)

    def test_add_rumour(self):
        watson = self.empty_watson

        watson.knowledge_table.set(michiel, Cards.KANDELAAR, Knowledge.FALSE)
        watson.knowledge_table.set(michiel, Cards.HAL, Knowledge.FALSE)

        watson.add_rumour(
            Rumour(
                menno,
                [Cards.KANDELAAR, Cards.HAL, Cards.ROODHART],
                [(michiel, Knowledge.TRUE)]
            )
        )
        self.assertEqual(
            Knowledge.TRUE,
            watson.knowledge_table.get(michiel, Cards.ROODHART)
        )

    def test_add_info_from_clues(self):
        clues = Clues(context_fixture)
        clues.add_card(Cards.BLAAUWVANDRAET, tom)
        clues.add_card(Cards.KANDELAAR, tom)
        rumour_cards = [Cards.BLAAUWVANDRAET, Cards.KANDELAAR, Cards.GASTENVERBLIJF]
        clues.add_rumour(
            Rumour(
                menno,
                rumour_cards,
                [
                    (menno, Knowledge.FALSE), (michiel, Knowledge.TRUE)
                ]
            )
        )
        watson = self.empty_watson
        watson.add_info_from_clues(clues)
        for card in rumour_cards:
            for player in context_fixture.players:
                if (card is Cards.KANDELAAR or card is Cards.BLAAUWVANDRAET) and player is tom:
                    self.assertEqual(Knowledge.TRUE, watson.get_knowledge_table().get(player, card))
                elif card is Cards.GASTENVERBLIJF and player is michiel:
                    self.assertEqual(Knowledge.TRUE, watson.get_knowledge_table().get(player, card))
                else:
                    self.assertEqual(Knowledge.FALSE, watson.get_knowledge_table().get(player, card))
