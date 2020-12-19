import unittest

from load_game_config import load_session
from test.fixture.expected_game_config import ExpectedGameConfig


class TestLoadSession(unittest.TestCase):
    def test_load_session(self):
        session = load_session('test/fixture/game_config.json')
        expected_session = ExpectedGameConfig.session
        self.assertEqual(session, expected_session)
