import unittest

from gamestate import GameState
from knowledge import Knowledge
from load_game_config import load_game_config
from player import Player
from rumour import Rumour
from session import Session
from test.fixture.context import Cards


class TestLoadGameConfig(unittest.TestCase):
    def test_load_game_config(self):
        game_state, session = load_game_config('test/fixture/game_config.json')

        player1 = Player("Tom", "Roodhart", 6)
        player2 = Player("Menno", "Blaauw van Draet", 6)
        player3 = Player("Michiel", "De Wit", 6)
        cards = [Cards.MES, Cards.KANDELAAR, Cards. PISTOOL, Cards.VERGIF, Cards.TOUW,
                 Cards.KNUPPEL, Cards.BIJL, Cards.HALTER, Cards.HAL, Cards.EETKAMER,
                 Cards.KEUKEN, Cards.WERKKAMER, Cards.THEATER, Cards.ZITKAMER,
                 Cards.BUBBELBAD, Cards.GASTENVERBLIJF, Cards.PIMPEL, Cards.GROENEWOUD,
                 Cards.BLAAUWVANDRAET, Cards.ROODHART, Cards.DEWIT]

        expected_game_state = GameState([player1, player2, player3], cards)

        self.assertEqual(game_state, expected_game_state)
        cards_seen = {player1: [Cards.ROODHART, Cards.GROENEWOUD, Cards.KEUKEN, Cards.THEATER, Cards.KNUPPEL],
                      player2: [],
                      player3: []}
        rumours = [Rumour(player2, [Cards.MES, Cards.HAL, Cards.PIMPEL],[(player1, Knowledge.TRUE),(player3, Knowledge.FALSE)])]
        expected_session = Session(cards_seen, rumours)
        self.assertEqual(session, expected_session)

