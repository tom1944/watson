import os
import unittest

from load_game_config import load_game_config
from serialize import serialize
from test.fixture.expected_game_config import ExpectedGameConfig


class TestSerialize(unittest.TestCase):
    def test_serialize(self):
        serialize(ExpectedGameConfig.context, ExpectedGameConfig.session, "serialize_test.json")
        game_state, session = load_game_config("serialize_test.json")
        if os.path.exists("serialize_test.json"):
            os.remove("serialize_test.json")
        self.assertEqual(load_game_config('test/fixture/game_config.json'), (game_state, session))




