import unittest

from load_game_config import load_game_config
from test.fixture.expected_game_config import ExpectedGameConfig


class TestLoadGameConfig(unittest.TestCase):
    def test_load_game_config(self):
        game_state, session = load_game_config('test/fixture/game_config.json')
        expected_game_state = ExpectedGameConfig.context
        expected_session = ExpectedGameConfig.session
        self.assertEqual(game_state, expected_game_state)
        self.assertEqual(session, expected_session)
