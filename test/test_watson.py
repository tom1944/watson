from unittest import TestCase, skip

from knowledge import Knowledge
from rumour import Rumour
from session import Session
from test.fixture.context import Cards, context_fixture
from test.fixture.session import ExpectedSession
from watson import Watson


class TestWatson(TestCase):
    def setUp(self) -> None:
        context = context_fixture
        session = Session(context)
        self.empty_watson = Watson(session)

        small_watson = Watson(session)
        players = context.players
        knowledge_table = small_watson.get_knowledge_table()
        knowledge_table.set(players[0], Cards.MES, Knowledge.TRUE)
        knowledge_table.set(players[1], Cards.MES, Knowledge.FALSE)
        knowledge_table.set(players[2], Cards.MES, Knowledge.FALSE)

        knowledge_table.set(players[0], Cards.BUBBELBAD, Knowledge.FALSE)
        knowledge_table.set(players[1], Cards.BUBBELBAD, Knowledge.TRUE)
        knowledge_table.set(players[2], Cards.BUBBELBAD, Knowledge.FALSE)

        knowledge_table.set(players[2], Cards.PIMPEL, Knowledge.FALSE)

        self.small_watson = small_watson

        self.full_watson = self.create_full_watson()

    def create_full_watson(self) -> Watson:
        session = ExpectedSession.session
        context = session.get_context()
        full_watson = Watson(session)

        self.murderer = Cards.GROENEWOUD
        self.murder_weapon = Cards.PISTOOL
        self.murder_location = Cards.KEUKEN
        self.murder_cards = [self.murderer, self.murder_weapon, self.murder_location]

        player_hands = {
            context.players[0]: [Cards.MES, Cards.KANDELAAR, Cards.WERKKAMER, Cards.THEATER, Cards.ZITKAMER,
                                 Cards.DEWIT],
            context.players[1]: [Cards.VERGIF, Cards.TOUW, Cards.KNUPPEL, Cards.BUBBELBAD, Cards.GASTENVERBLIJF,
                                 Cards.PIMPEL],
            context.players[2]: [Cards.BIJL, Cards.HALTER, Cards.EETKAMER, Cards.BLAAUWVANDRAET,
                                 Cards.ROODHART]
        }

        for card in context.cards:
            for player in context.players:
                full_watson.get_knowledge_table().set(player, card, Knowledge.FALSE)

        for player, cards in player_hands.items():
            for card in cards:
                full_watson.get_knowledge_table().set_forcefully(player, card, Knowledge.TRUE)

        return full_watson

    def test_has_solution_trivial(self):
        watson = self.empty_watson
        self.assertTrue(watson.has_solution())   # Trivial

    def test_has_solution_basic(self):
        watson = self.empty_watson
        context = watson.context
        session = watson.session
        rum1 = Rumour(
            context.players[0],
            [Cards.KANDELAAR, Cards.BUBBELBAD, Cards.DEWIT],
            [
                (context.players[1], Knowledge.FALSE),
                (context.players[2], Knowledge.TRUE)
            ]
        )

        rum2 = Rumour(
            context.players[1],
            [Cards.HALTER, Cards.HAL, Cards.PIMPEL],
            [
                (context.players[0], Knowledge.TRUE),
                (context.players[2], Knowledge.FALSE)
            ]
        )

        session.rumours = [rum1, rum2]

        self.assertTrue(watson.has_solution())

    @skip
    def test_has_solution_false_negative(self):
        watson = self.empty_watson
        context = watson.context
        session = watson.session
        knowledge_tables = watson.get_knowledge_table()

        rum1 = Rumour(
            context.players[0],
            [Cards.KANDELAAR, Cards.BUBBELBAD, Cards.DEWIT],
            [
                (context.players[1], Knowledge.FALSE),
                (context.players[2], Knowledge.TRUE)
            ]
        )

        session.rumours = [rum1]
        knowledge_tables.set(context.players[1], Cards.BUBBELBAD, Knowledge.TRUE)
        self.assertFalse(watson.has_solution())

    @skip
    def test_has_solution_false_positive(self):
        watson = self.empty_watson
        context = watson.context
        session = watson.session
        knowledge_tables = watson.get_knowledge_table()

        rum1 = Rumour(
            context.players[0],
            [Cards.KANDELAAR, Cards.BUBBELBAD, Cards.DEWIT],
            [
                (context.players[1], Knowledge.FALSE),
                (context.players[2], Knowledge.TRUE)
            ]
        )

        rum2 = Rumour(
            context.players[1],
            [Cards.HALTER, Cards.HAL, Cards.PIMPEL],
            [
                (context.players[0], Knowledge.TRUE),
                (context.players[2], Knowledge.FALSE)
            ]
        )

        session.rumours = [rum1, rum2]

        knowledge_tables.set(context.players[0], Cards.HALTER, Knowledge.FALSE)
        knowledge_tables.set(context.players[0], Cards.HAL, Knowledge.FALSE)
        knowledge_tables.set(context.players[0], Cards.PIMPEL, Knowledge.FALSE)
        self.assertFalse(watson.has_solution())

    @skip
    def test_has_solution_triplet(self):
        context = self.empty_watson.context
        session = self.empty_watson.session
        knowledge_tables = context.knowledge_tables

        rum1 = Rumour(
            context.players[0],
            [Cards.HALTER, Cards.GASTENVERBLIJF, Cards.DEWIT],
            [
                (context.players[1], Knowledge.TRUE),
                (context.players[2], Knowledge.FALSE)
            ]
        )

        rum2 = Rumour(
            context.players[0],
            [Cards.HALTER, Cards.GASTENVERBLIJF, Cards.ROODHART],
            [
                (context.players[1], Knowledge.TRUE),
                (context.players[2], Knowledge.FALSE)
            ]
        )

        rum3 = Rumour(
            context.players[0],
            [Cards.HALTER, Cards.GASTENVERBLIJF, Cards.BLAAUWVANDRAET],
            [
                (context.players[1], Knowledge.TRUE),
                (context.players[2], Knowledge.FALSE)
            ]
        )
        session.rumours = [rum1, rum2, rum3]
        knowledge_tables.set(context.players[1], Cards.HALTER, Knowledge.FALSE)
        knowledge_tables.set(context.players[1], Cards.GASTENVERBLIJF, Knowledge.FALSE)
        knowledge_tables.set(context.players[1], Cards.VERGIF, Knowledge.TRUE)
        knowledge_tables.set(context.players[1], Cards.TOUW, Knowledge.TRUE)
        knowledge_tables.set(context.players[1], Cards.KNUPPEL, Knowledge.TRUE)
        knowledge_tables.set(context.players[1], Cards.BUBBELBAD, Knowledge.TRUE)
        self.assertFalse(context.has_solution())

    def test_add_card(self):
        watson = self.empty_watson
        game_state = watson.context
        watson.add_knowledge(game_state.players[0], Cards.KNUPPEL, Knowledge.TRUE)

        for player in game_state.players:
            knowledge = watson.get_knowledge_table().get(player, Cards.KNUPPEL)
            if player == game_state.players[0]:
                self.assertEqual(knowledge, Knowledge.TRUE)
            else:
                self.assertEqual(knowledge, Knowledge.FALSE)

    @skip
    def test_add_rumour(self):
        game_state = self.empty_watson.context
        watson = self.empty_watson

        watson.knowledge_table.set(game_state.players[2], Cards.KANDELAAR, Knowledge.FALSE)
        watson.knowledge_table.set(game_state.players[2], Cards.HAL, Knowledge.FALSE)

        test_rumour = Rumour(
            game_state.players[1],
            [Cards.KANDELAAR, Cards.HAL, Cards.ROODHART],
            [
                (game_state.players[0], Knowledge.FALSE),
                (game_state.players[2], Knowledge.TRUE)
            ]
        )

        watson.add_rumour(test_rumour)
        self.assertEqual(
            watson.knowledge_table.get(game_state.players[2], Cards.ROODHART),
            Knowledge.TRUE
        )
