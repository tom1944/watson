import os
import unittest

from load_session import load_session
from serialize import serialize
from test.fixture.session import ExpectedSession


class TestSerialize(unittest.TestCase):
    def test_serialize(self):
        serialize(ExpectedSession.session, "serialize_test.json")
        session = load_session("serialize_test.json")
        if os.path.exists("serialize_test.json"):
            os.remove("serialize_test.json")
        self.assertEqual(ExpectedSession.session, session)




