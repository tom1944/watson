import os
import unittest

from load_game_config import load_session
from serialize import serialize
from test.fixture.expected_game_config import ExpectedGameConfig


class TestSerialize(unittest.TestCase):
    def test_serialize(self):
        serialize(ExpectedGameConfig.session, "serialize_test.json")
        session = load_session("serialize_test.json")
        if os.path.exists("serialize_test.json"):
            os.remove("serialize_test.json")
        self.assertEqual(load_session('test/fixture/game_config.json'), session)




