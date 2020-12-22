from unittest import TestCase, skip

from source.data.knowledge import Knowledge
from source.data.rumour import Rumour
from source.data.session import Session
from test.fixture.context import Cards, michiel, menno, context_fixture, tom
from source.logic.watson import Watson


class TestWatson(TestCase):
    def setUp(self) -> None:
        context = context_fixture
        session = Session(context)
        self.empty_watson = Watson(session)

    def test_add_card(self):
        watson = self.empty_watson
        watson.add_knowledge(tom, Cards.KNUPPEL, Knowledge.TRUE)

        for player in watson.context.players:
            knowledge = watson.get_knowledge_table().get(player, Cards.KNUPPEL)
            if player == tom:
                self.assertEqual(knowledge, Knowledge.TRUE)
            else:
                self.assertEqual(knowledge, Knowledge.FALSE)

    @skip
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
