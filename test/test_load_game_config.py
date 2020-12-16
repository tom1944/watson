import unittest

from gamestate import GameState
from knowledge import Knowledge
from load_game_config import load_game_config
from player import Player
from rumour import Rumour
from session import Session
from test.fixture.context import Cards
from test.fixture.expected_game_config import ExpectedGameConfig


class TestLoadGameConfig(unittest.TestCase):
    def test_load_game_config(self):
        game_state, session = load_game_config('test/fixture/game_config.json')
        expected_game_state = ExpectedGameConfig.game_state
        expected_session = ExpectedGameConfig.session
        self.assertEqual(game_state, expected_game_state)
        self.assertEqual(session, expected_session)
