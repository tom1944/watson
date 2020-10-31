from unittest import TestCase
from gamestate import GameState, Rumour
from gameconfig import load_game_config
from card import usedCards, Category
from user_io import match_card
from knowledge import Knowledge
import random


def init_game_state():
    test_game_config = load_game_config()
    used_cards = [c for c in test_game_config.all_cards if c not in test_game_config.open_cards]
    return GameState(test_game_config.players, used_cards)


def seeded_rand_card(category: str, seed: int):
    random.seed(seed)
    rand_card = usedCards[random.randint(1, len(usedCards)-1)]
    if category in set(c.value for c in Category):
        while rand_card.category.value != category:
            rand_card = usedCards[random.randint(0, len(usedCards)-1)]
        return rand_card
    elif category == "any":
        return rand_card
    else:
        raise Exception(f"{category} is not a valid category")


def seeded_rand_rumour(seed: int):
    random.seed(seed)
    weapon = seeded_rand_card("Weapon", seed)
    room = seeded_rand_card("Room", seed)
    character = seeded_rand_card("Character", seed)


class TestGameState(TestCase):
    def setUp(self) -> None:
        self.empty_game_state = init_game_state()

        small_game_state = init_game_state()
        players = small_game_state.players
        small_game_state.knowledge_tables[Category.WEAPON][players[0]][match_card("Mes")] = Knowledge.TRUE
        small_game_state.knowledge_tables[Category.WEAPON][players[1]][match_card("Mes")] = Knowledge.FALSE
        small_game_state.knowledge_tables[Category.WEAPON][players[2]][match_card("Mes")] = Knowledge.FALSE

        small_game_state.knowledge_tables[Category.ROOM][players[0]][match_card("Bubbelbad")] = Knowledge.FALSE
        small_game_state.knowledge_tables[Category.ROOM][players[1]][match_card("Bubbelbad")] = Knowledge.TRUE
        small_game_state.knowledge_tables[Category.ROOM][players[2]][match_card("Bubbelbad")] = Knowledge.FALSE

        small_game_state.knowledge_tables[Category.CHARACTER][players[2]][match_card("Pimpel")] = Knowledge.FALSE

        self.small_game_state = small_game_state

        self.full_game_state = self.create_full_game_state()

    def create_full_game_state(self) -> GameState:
        full_game_state = init_game_state()

        self.murderer = match_card("Groenewoud")
        self.murder_weapon = match_card("Pistool")
        self.murder_location = match_card("Keuken")
        self.murder_cards = [self.murderer, self.murder_weapon, self.murder_location]

        player_hands = {
            full_game_state.players[0]: ["Mes", "Kandelaar", "Werkkamer", "Theater", "Zitkamer", "De Wit"],
            full_game_state.players[1]: ["Vergif", "Touw", "Knuppel", "Bubbelbad", "Gastenverblijf", "Pimpel"],
            full_game_state.players[2]: ["Bijl", "Halter", "Hal", "Eetkamer", "Blaauw van Draet", "Roodhart"],
        }

        for card in usedCards:
            for player in full_game_state.players:
                full_game_state.knowledge_tables[card.category][player][card] = Knowledge.FALSE

        for player, card_names in player_hands.items():
            for card_name in card_names:
                card = match_card(card_name)
                full_game_state.knowledge_tables[card.category][player][card] = Knowledge.TRUE

        return full_game_state

    def test_check_knowledge(self):
        game_state = self.small_game_state
        players = game_state.players

        game_state.rumours = [
            Rumour(
                players[0],
                match_card("Mes"),
                match_card("Theater"),
                match_card("Blaauw van Draet"),
                [
                    (players[1], Knowledge.FALSE),
                    (players[2], Knowledge.TRUE),
                ]
            )
        ]

        assert game_state.check_knowledge(game_state.knowledge_tables)

        game_state.rumours.append(
            Rumour(
                players[1],
                match_card("Mes"),
                match_card("Theater"),
                match_card("Blaauw van Draet"),
                [
                    (players[0], Knowledge.FALSE),
                ]
            )
        )

        assert not game_state.check_knowledge(game_state.knowledge_tables)

        game_state.rumours[1] = Rumour(
            players[0],
            match_card("Mes"),
            match_card("Bubbelbad"),
            match_card("Pimpel"),
            [
                (players[2], Knowledge.TRUE),
            ]
        )

        assert not game_state.check_knowledge(game_state.knowledge_tables)

    def test_check_knowledge_card_amount(self):
        game_state = self.full_game_state
        game_state.knowledge_tables[Category.CHARACTER][game_state.players[0]][match_card("Pimpel")] = Knowledge.TRUE
        game_state.knowledge_tables[Category.CHARACTER][game_state.players[1]][match_card("Pimpel")] = Knowledge.FALSE
        assert not game_state.check_knowledge(game_state.knowledge_tables)

    def test_has_solution_trivial(self):
        game_state = self.empty_game_state
        knowledge_tables = game_state.knowledge_tables
        assert game_state.has_solution(knowledge_tables) is True   # Trivial

    def test_has_solution_basic(self):
        game_state = self.empty_game_state
        knowledge_tables = game_state.knowledge_tables
        rum1 = Rumour(
            game_state.players[0],
            match_card("Kandelaar"),
            match_card("Bubbelbad"),
            match_card("De Wit"),
            [
                (game_state.players[1], Knowledge.FALSE),
                (game_state.players[2], Knowledge.TRUE)
            ]
        )

        rum2 = Rumour(
            game_state.players[1],
            match_card("Halter"),
            match_card("Hal"),
            match_card("Pimpel"),
            [
                (game_state.players[0], Knowledge.TRUE),
                (game_state.players[2], Knowledge.FALSE)
            ]
        )

        game_state.rumours = [rum1, rum2]

        assert game_state.has_solution(knowledge_tables) is True

    def test_has_solution_false_negative(self):
        game_state = self.empty_game_state
        knowledge_tables = game_state.knowledge_tables

        rum1 = Rumour(
            game_state.players[0],
            match_card("Kandelaar"),
            match_card("Bubbelbad"),
            match_card("De Wit"),
            [
                (game_state.players[1], Knowledge.FALSE),
                (game_state.players[2], Knowledge.TRUE)
            ]
        )

        game_state.rumours = [rum1]
        knowledge_tables[Category.ROOM][game_state.players[1]][match_card("Bubbelbad")] = Knowledge.TRUE
        assert game_state.has_solution(knowledge_tables) is False

    def test_has_solution_false_positive(self):
        game_state = self.empty_game_state
        knowledge_tables = game_state.knowledge_tables

        rum1 = Rumour(
            game_state.players[0],
            match_card("Kandelaar"),
            match_card("Bubbelbad"),
            match_card("De Wit"),
            [
                (game_state.players[1], Knowledge.FALSE),
                (game_state.players[2], Knowledge.TRUE)
            ]
        )

        rum2 = Rumour(
            game_state.players[1],
            match_card("Halter"),
            match_card("Hal"),
            match_card("Pimpel"),
            [
                (game_state.players[0], Knowledge.TRUE),
                (game_state.players[2], Knowledge.FALSE)
            ]
        )

        game_state.rumours = [rum1, rum2]

        knowledge_tables[Category.WEAPON][game_state.players[0]][match_card("Halter")] = Knowledge.FALSE
        knowledge_tables[Category.ROOM][game_state.players[0]][match_card("Hal")] = Knowledge.FALSE
        knowledge_tables[Category.CHARACTER][game_state.players[0]][match_card("Pimpel")] = Knowledge.FALSE
        assert game_state.has_solution(knowledge_tables) is False

    def test_has_solution_triplet(self):
        self.fail()
        game_state = self.empty_game_state
        knowledge_tables = game_state.knowledge_tables

        rum1 = Rumour(
            game_state.players[0],
            match_card("Halter"),
            match_card("Gastenverblijf"),
            match_card("De Wit"),
            [
                (game_state.players[1], Knowledge.TRUE),
                (game_state.players[2], Knowledge.FALSE)
            ]
        )

        rum2 = Rumour(
            game_state.players[0],
            match_card("Halter"),
            match_card("Gastenverblijf"),
            match_card("Roodhart"),
            [
                (game_state.players[1], Knowledge.TRUE),
                (game_state.players[2], Knowledge.FALSE)
            ]
        )

        rum3 = Rumour(
            game_state.players[0],
            match_card("Halter"),
            match_card("Gastenverblijf"),
            match_card("Blaauw van Draet"),
            [
                (game_state.players[1], Knowledge.TRUE),
                (game_state.players[2], Knowledge.FALSE)
            ]
        )
        game_state.rumours = [rum1, rum2, rum3]
        knowledge_tables[Category.WEAPON][game_state.players[1]][match_card("Halter")] = Knowledge.FALSE
        knowledge_tables[Category.ROOM][game_state.players[1]][match_card("Gastenverblijf")] = Knowledge.FALSE
        knowledge_tables[Category.WEAPON][game_state.players[1]][match_card("Vergif")] = Knowledge.TRUE
        knowledge_tables[Category.WEAPON][game_state.players[1]][match_card("Touw")] = Knowledge.TRUE
        knowledge_tables[Category.WEAPON][game_state.players[1]][match_card("Knuppel")] = Knowledge.TRUE
        knowledge_tables[Category.ROOM][game_state.players[1]][match_card("Bubbelbad")] = Knowledge.TRUE
        assert not game_state.has_solution(knowledge_tables)

    def test_add_card(self):
        game_state = init_game_state()
        test_card = match_card("Knuppel")
        test_player = game_state.players[0]
        game_state.add_card(test_player, test_card, Knowledge.TRUE)
        for player in game_state.players:
            knowledge = game_state.knowledge_tables[Category.WEAPON][player][test_card]
            if player == test_player:
                self.assertEqual(knowledge, Knowledge.TRUE)
            else:
                self.assertEqual(knowledge, Knowledge.FALSE)

    def test_add_rumour(self):
        game_state = init_game_state()
        test_player = game_state.players[1]

        game_state.add_card(game_state.players[2], match_card("Kandelaar"), Knowledge.FALSE)
        game_state.add_card(game_state.players[2], match_card("Hal"), Knowledge.FALSE)

        test_weapon = match_card("Kandelaar")
        test_room = match_card("Hal")
        test_character = match_card("Pimpel")

        test_replies = [(game_state.players[0], Knowledge.FALSE), (game_state.players[2], Knowledge.TRUE)]
        test_rumour = Rumour(test_player, test_weapon, test_room, test_character, test_replies)

        game_state.add_rumour(test_rumour)
