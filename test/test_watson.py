from unittest import TestCase, skip

from load_game_config import load_game_config
from session import Session
from watson import Watson
from rumour import Rumour
from test.fixture.context import Cards
from knowledge import Knowledge


class TestWatson(TestCase):
    def setUp(self) -> None:
        context, session = load_game_config('test/fixture/game_config.json')
        session = Session({}, [])
        self.empty_watson = Watson(context, session)

        small_watson = Watson(context, session)
        players = small_watson.context.players
        small_watson.knowledge_tables.set(players[0], Cards.MES, Knowledge.TRUE)
        small_watson.knowledge_tables.set(players[1], Cards.MES, Knowledge.FALSE)
        small_watson.knowledge_tables.set(players[2], Cards.MES, Knowledge.FALSE)

        small_watson.knowledge_tables.set(players[0], Cards.BUBBELBAD, Knowledge.FALSE)
        small_watson.knowledge_tables.set(players[1], Cards.BUBBELBAD, Knowledge.TRUE)
        small_watson.knowledge_tables.set(players[2], Cards.BUBBELBAD, Knowledge.FALSE)

        small_watson.knowledge_tables.set(players[2], Cards.PIMPEL, Knowledge.FALSE)

        self.small_watson = small_watson

        self.full_watson = self.create_full_watson()

    def create_full_watson(self) -> Watson:
        context, session = load_game_config('test/fixture/game_config.json')
        full_watson = Watson(context, session)

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
                full_watson.knowledge_tables.set(player, card, Knowledge.FALSE)

        for player, cards in player_hands.items():
            for card in cards:
                full_watson.knowledge_tables.set_forcefully(player, card, Knowledge.TRUE)

        return full_watson

    def test_check_knowledge(self):
        watson = self.small_watson
        context = watson.context
        session = watson.session
        players = context.players

        session.rumours = [
            Rumour(
                players[0],
                [Cards.MES, Cards.THEATER, Cards.BLAAUWVANDRAET],
                [
                    (players[1], Knowledge.FALSE),
                    (players[2], Knowledge.TRUE),
                ]
            )
        ]

        self.assertTrue(watson.check_knowledge())

        session.rumours.append(
            Rumour(
                players[1],
                [Cards.MES, Cards.THEATER, Cards.BLAAUWVANDRAET],
                [
                    (players[0], Knowledge.FALSE),
                ]
            )
        )

        self.assertFalse(watson.check_knowledge())

        session.rumours[1] = Rumour(
            players[0],
            [Cards.MES, Cards.BUBBELBAD, Cards.PIMPEL],
            [
                (players[2], Knowledge.TRUE),
            ]
        )

        self.assertFalse(watson.check_knowledge())

    def test_check_knowledge_card_amount(self):
        watson = self.full_watson
        game_state = watson.context
        watson.knowledge_tables.set_forcefully(game_state.players[0], Cards.PIMPEL, Knowledge.TRUE)
        watson.knowledge_tables.set_forcefully(game_state.players[1], Cards.PIMPEL, Knowledge.FALSE)
        self.assertFalse(watson.check_knowledge())

    def test_smart_check_knowledge(self):
        watson = self.empty_watson
        context = watson.context
        player_hands = {}
        for player in context.players:
            player_hands[player] = []
        unknown_cards = context.cards
        self.assertTrue(watson.smart_check_knowledge(player_hands, unknown_cards))

        watson = self.small_watson
        context = watson.context
        session = watson.session
        players = context.players
        player_hands = {}
        for player in players:
            player_hands[player] = []
        unknown_cards = context.cards

        session.rumours = [
            Rumour(
                players[0],
                [Cards.MES, Cards.THEATER, Cards.BLAAUWVANDRAET],
                [
                    (players[1], Knowledge.FALSE),
                    (players[2], Knowledge.TRUE),
                ]
            )
        ]
        self.assertTrue(watson.smart_check_knowledge(player_hands, unknown_cards))

        session.rumours.append(
            Rumour(
                players[1],
                [Cards.MES, Cards.THEATER, Cards.BLAAUWVANDRAET],
                [
                    (players[0], Knowledge.FALSE),
                ]
            )
        )
        self.assertFalse(watson.smart_check_knowledge(player_hands, unknown_cards))

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
        knowledge_tables = watson.knowledge_tables

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
        knowledge_tables = watson.knowledge_tables

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
            knowledge = watson.knowledge_tables.get(player, Cards.KNUPPEL)
            if player == game_state.players[0]:
                self.assertEqual(knowledge, Knowledge.TRUE)
            else:
                self.assertEqual(knowledge, Knowledge.FALSE)

    @skip
    def test_add_rumour(self):
        game_state = self.empty_watson.context
        watson = self.empty_watson

        watson.knowledge_tables.set(game_state.players[2], Cards.KANDELAAR, Knowledge.FALSE)
        watson.knowledge_tables.set(game_state.players[2], Cards.HAL, Knowledge.FALSE)

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
            watson.knowledge_tables.get(game_state.players[2], Cards.ROODHART),
            Knowledge.TRUE
        )
