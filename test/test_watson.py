from unittest import TestCase, skip

from load_game_state import load_game_state
from watson import Watson
from rumour import Rumour
from card import Category, Cards
from knowledge import Knowledge


class TestGameState(TestCase):
    def setUp(self) -> None:
        self.empty_watson = Watson(load_game_state('test/game_config.json'))

        small_watson = Watson(load_game_state('test/game_config.json'))
        players = small_watson.game_state.players
        small_watson.knowledge_tables[Category.WEAPON][players[0]][Cards.MES] = Knowledge.TRUE
        small_watson.knowledge_tables[Category.WEAPON][players[1]][Cards.MES] = Knowledge.FALSE
        small_watson.knowledge_tables[Category.WEAPON][players[2]][Cards.MES] = Knowledge.FALSE

        small_watson.knowledge_tables[Category.ROOM][players[0]][Cards.BUBBELBAD] = Knowledge.FALSE
        small_watson.knowledge_tables[Category.ROOM][players[1]][Cards.BUBBELBAD] = Knowledge.TRUE
        small_watson.knowledge_tables[Category.ROOM][players[2]][Cards.BUBBELBAD] = Knowledge.FALSE

        small_watson.knowledge_tables[Category.CHARACTER][players[2]][Cards.PIMPEL] = Knowledge.FALSE

        self.small_watson = small_watson

        self.full_watson = self.create_full_watson()

    def create_full_watson(self) -> Watson:
        full_game_state = load_game_state('test/game_config.json')
        full_watson = Watson(full_game_state)

        self.murderer = Cards.GROENEWOUD
        self.murder_weapon = Cards.PISTOOL
        self.murder_location = Cards.KEUKEN
        self.murder_cards = [self.murderer, self.murder_weapon, self.murder_location]

        player_hands = {
            full_game_state.players[0]: [Cards.MES, Cards.KANDELAAR, Cards.WERKKAMER, Cards.THEATER, Cards.ZITKAMER,
                                         Cards.DEWIT],
            full_game_state.players[1]: [Cards.VERGIF, Cards.TOUW, Cards.KNUPPEL, Cards.BUBBELBAD, Cards.GASTENVERBLIJF,
                                         Cards.PIMPEL],
            full_game_state.players[2]: [Cards.BIJL, Cards.HALTER, Cards.EETKAMER, Cards.BLAAUWVANDRAET,
                                         Cards.ROODHART],
        }

        for card in full_game_state.used_cards:
            for player in full_game_state.players:
                full_watson.knowledge_tables[card.category][player][card] = Knowledge.FALSE

        for player, cards in player_hands.items():
            for card in cards:
                full_watson.knowledge_tables[card.category][player][card] = Knowledge.TRUE

        return full_watson

    def test_check_knowledge(self):
        watson = self.small_watson
        game_state = watson.game_state
        players = game_state.players

        game_state.rumours = [
            Rumour(
                players[0],
                Cards.MES,
                Cards.THEATER,
                Cards.BLAAUWVANDRAET,
                [
                    (players[1], Knowledge.FALSE),
                    (players[2], Knowledge.TRUE),
                ]
            )
        ]

        self.assertTrue(watson.check_knowledge())

        game_state.rumours.append(
            Rumour(
                players[1],
                Cards.MES,
                Cards.THEATER,
                Cards.BLAAUWVANDRAET,
                [
                    (players[0], Knowledge.FALSE),
                ]
            )
        )

        self.assertFalse(watson.check_knowledge())

        game_state.rumours[1] = Rumour(
            players[0],
            Cards.MES,
            Cards.BUBBELBAD,
            Cards.PIMPEL,
            [
                (players[2], Knowledge.TRUE),
            ]
        )

        self.assertFalse(watson.check_knowledge())

    def test_check_knowledge_card_amount(self):
        watson = self.full_watson
        game_state = watson.game_state
        watson.knowledge_tables[Category.CHARACTER][game_state.players[0]][Cards.PIMPEL] = Knowledge.TRUE
        watson.knowledge_tables[Category.CHARACTER][game_state.players[1]][Cards.PIMPEL] = Knowledge.FALSE
        self.assertFalse(watson.check_knowledge())

    def test_has_solution_trivial(self):
        watson = self.empty_watson
        self.assertTrue(watson.has_solution())   # Trivial

    def test_has_solution_basic(self):
        watson = self.empty_watson
        game_state = watson.game_state
        rum1 = Rumour(
            game_state.players[0],
            Cards.KANDELAAR,
            Cards.BUBBELBAD,
            Cards.DEWIT,
            [
                (game_state.players[1], Knowledge.FALSE),
                (game_state.players[2], Knowledge.TRUE)
            ]
        )

        rum2 = Rumour(
            game_state.players[1],
            Cards.HALTER,
            Cards.HAL,
            Cards.PIMPEL,
            [
                (game_state.players[0], Knowledge.TRUE),
                (game_state.players[2], Knowledge.FALSE)
            ]
        )

        game_state.rumours = [rum1, rum2]

        self.assertTrue(watson.has_solution())

    def test_has_solution_false_negative(self):
        watson = self.empty_watson
        game_state = watson.game_state
        knowledge_tables = watson.knowledge_tables

        rum1 = Rumour(
            game_state.players[0],
            Cards.KANDELAAR,
            Cards.BUBBELBAD,
            Cards.DEWIT,
            [
                (game_state.players[1], Knowledge.FALSE),
                (game_state.players[2], Knowledge.TRUE)
            ]
        )

        game_state.rumours = [rum1]
        knowledge_tables[Category.ROOM][game_state.players[1]][Cards.BUBBELBAD] = Knowledge.TRUE
        self.assertFalse(watson.has_solution())

    def test_has_solution_false_positive(self):
        watson = self.empty_watson
        game_state = watson.game_state
        knowledge_tables = watson.knowledge_tables

        rum1 = Rumour(
            game_state.players[0],
            Cards.KANDELAAR,
            Cards.BUBBELBAD,
            Cards.DEWIT,
            [
                (game_state.players[1], Knowledge.FALSE),
                (game_state.players[2], Knowledge.TRUE)
            ]
        )

        rum2 = Rumour(
            game_state.players[1],
            Cards.HALTER,
            Cards.HAL,
            Cards.PIMPEL,
            [
                (game_state.players[0], Knowledge.TRUE),
                (game_state.players[2], Knowledge.FALSE)
            ]
        )

        game_state.rumours = [rum1, rum2]

        knowledge_tables[Category.WEAPON][game_state.players[0]][Cards.HALTER] = Knowledge.FALSE
        knowledge_tables[Category.ROOM][game_state.players[0]][Cards.HAL] = Knowledge.FALSE
        knowledge_tables[Category.CHARACTER][game_state.players[0]][Cards.PIMPEL] = Knowledge.FALSE
        self.assertFalse(watson.has_solution())

    @skip
    def test_has_solution_triplet(self):
        game_state = self.empty_watson.game_state
        knowledge_tables = game_state.knowledge_tables

        rum1 = Rumour(
            game_state.players[0],
            Cards.HALTER,
            Cards.GASTENVERBLIJF,
            Cards.DEWIT,
            [
                (game_state.players[1], Knowledge.TRUE),
                (game_state.players[2], Knowledge.FALSE)
            ]
        )

        rum2 = Rumour(
            game_state.players[0],
            Cards.HALTER,
            Cards.GASTENVERBLIJF,
            Cards.ROODHART,
            [
                (game_state.players[1], Knowledge.TRUE),
                (game_state.players[2], Knowledge.FALSE)
            ]
        )

        rum3 = Rumour(
            game_state.players[0],
            Cards.HALTER,
            Cards.GASTENVERBLIJF,
            Cards.BLAAUWVANDRAET,
            [
                (game_state.players[1], Knowledge.TRUE),
                (game_state.players[2], Knowledge.FALSE)
            ]
        )
        game_state.rumours = [rum1, rum2, rum3]
        knowledge_tables[Category.WEAPON][game_state.players[1]][Cards.HALTER] = Knowledge.FALSE
        knowledge_tables[Category.ROOM][game_state.players[1]][Cards.GASTENVERBLIJF] = Knowledge.FALSE
        knowledge_tables[Category.WEAPON][game_state.players[1]][Cards.VERGIF] = Knowledge.TRUE
        knowledge_tables[Category.WEAPON][game_state.players[1]][Cards.TOUW] = Knowledge.TRUE
        knowledge_tables[Category.WEAPON][game_state.players[1]][Cards.KNUPPEL] = Knowledge.TRUE
        knowledge_tables[Category.ROOM][game_state.players[1]][Cards.BUBBELBAD] = Knowledge.TRUE
        self.assertFalse(game_state.has_solution())

    def test_add_card(self):
        watson = self.empty_watson
        game_state = watson.game_state
        watson.add_knowledge(game_state.players[0], Cards.KNUPPEL, Knowledge.TRUE)

        for player in game_state.players:
            knowledge = watson.knowledge_tables[Category.WEAPON][player][Cards.KNUPPEL]
            if player == game_state.players[0]:
                self.assertEqual(knowledge, Knowledge.TRUE)
            else:
                self.assertEqual(knowledge, Knowledge.FALSE)

    def test_add_rumour(self):
        game_state = self.empty_watson.game_state
        watson = self.empty_watson

        watson.add_knowledge(game_state.players[2], Cards.KANDELAAR, Knowledge.FALSE)
        watson.add_knowledge(game_state.players[2], Cards.HAL, Knowledge.FALSE)

        test_rumour = Rumour(
            game_state.players[1],
            Cards.KANDELAAR,
            Cards.HAL,
            Cards.PIMPEL,
            [
                (game_state.players[0], Knowledge.FALSE),
                (game_state.players[2], Knowledge.TRUE)
            ]
        )

        watson.add_rumour(test_rumour)
        self.assertEqual(
            watson.knowledge_tables[Category.CHARACTER][game_state.players[2]][Cards.PIMPEL],
            Knowledge.TRUE
        )